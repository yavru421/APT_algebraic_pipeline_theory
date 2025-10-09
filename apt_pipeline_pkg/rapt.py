from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


# Registry mapping DSL identifiers to module and function
MODULE_REGISTRY: Dict[str, Tuple[str, str]] = {
    "m0": ("APT_MODULES.m0_openapi_resolve", "run"),
    "m1": ("APT_MODULES.m1_base64_encode", "run"),
    "m2": ("APT_MODULES.m2_build_payload", "run"),
    "m3": ("APT_MODULES.m3_parse_response", "run"),
    "m4": ("APT_MODULES.m4_call_proxy", "run"),
    "m5": ("APT_MODULES.m5_parse_chat_completions", "run"),
}


Token = Tuple[str, str]


def _tokenize(s: str) -> List[Token]:
    # Simple tokenizer for identifiers, strings, numbers, punctuation, booleans
    token_spec = [
        ("SKIP", r"[ \t]+"),
        ("STRING", r'"[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\''),
        ("NUMBER", r"\d+(?:\.\d+)?"),
        ("IDENT", r"[A-Za-z_][A-Za-z0-9_]*"),
        ("LPAREN", r"\("),
        ("RPAREN", r"\)"),
        ("COMMA", r","),
        ("EQUAL", r"="),
        ("AT", r"@"),
    ]
    master = re.compile("|".join(f"(?P<{n}>{p})" for n, p in token_spec))
    pos = 0
    tokens: List[Token] = []
    while pos < len(s):
        m = master.match(s, pos)
        if not m:
            raise SyntaxError(f"Unexpected character at {pos}: {s[pos:pos+10]}")
        kind = m.lastgroup or ""
        text = m.group(0)
        pos = m.end()
        if kind == "SKIP":
            continue
        tokens.append((kind, text))
    return tokens


@dataclass
class Call:
    name: str
    args: Dict[str, Any]
    env: Optional[str] = None


def _parse_value(tokens: List[Token], i: int) -> Tuple[Any, int]:
    kind, text = tokens[i]
    if kind == "STRING":
        if text[0] == text[-1] and text[0] in ('"', "'"):
            return text[1:-1], i + 1
    if kind == "NUMBER":
        return (float(text) if "." in text else int(text)), i + 1
    if kind == "IDENT":
        # true/false/null
        low = text.lower()
        if low == "true":
            return True, i + 1
        if low == "false":
            return False, i + 1
        if low == "null":
            return None, i + 1
        # identifier may be a nested call; lookahead for LPAREN
        if i + 1 < len(tokens) and tokens[i + 1][0] == "LPAREN":
            node, j = _parse_call(tokens, i)
            return node, j
        # bare identifier (x1, m2, etc.)
        return text, i + 1
    raise SyntaxError(f"Unexpected token {tokens[i]}")


def _parse_call(tokens: List[Token], i: int) -> Tuple[Call, int]:
    name = tokens[i][1]  # IDENT
    i += 1  # consume ident
    assert tokens[i][0] == "LPAREN"
    i += 1  # consume '('
    args: Dict[str, Any] = {}
    # parse zero or more named args
    while i < len(tokens) and tokens[i][0] != "RPAREN":
        # name = value
        if tokens[i][0] != "IDENT" or tokens[i + 1][0] != "EQUAL":
            raise SyntaxError("Expected named argument 'name=value'")
        arg_name = tokens[i][1]
        i += 2  # skip IDENT and '='
        val, i = _parse_value(tokens, i)
        args[arg_name] = val
        if i < len(tokens) and tokens[i][0] == "COMMA":
            i += 1  # skip comma
    assert tokens[i][0] == "RPAREN"
    i += 1  # consume ')'

    env: Optional[str] = None
    if i < len(tokens) and tokens[i][0] == "AT":
        # '@' envName
        i += 1
        if i >= len(tokens) or tokens[i][0] != "IDENT":
            raise SyntaxError("Expected env name after '@'")
        env = tokens[i][1]
        i += 1
    return Call(name=name, args=args, env=env), i


def _walk(node: Any, vars_map: Dict[str, Any], steps: List[Dict[str, Any]], counts: Dict[str, int]) -> str:
    """Return the step name producing this node's output, appending steps as needed."""
    # plain identifier
    if isinstance(node, str):
        # reference to prior step (mX) or to variable (xX)
        return node
    if isinstance(node, Call):
        ident = node.name
        base_name = ident
        # ensure unique step name if repeated
        counts[base_name] = counts.get(base_name, 0) + 1
        step_name = base_name if counts[base_name] == 1 else f"{base_name}_{counts[base_name]}"
        # resolve args: nested calls become $stepname, identifiers stay identifiers so executor resolves $mX
        resolved_args: Dict[str, Any] = {}
        for k, v in node.args.items():
            if isinstance(v, Call):
                dep = _walk(v, vars_map, steps, counts)
                resolved_args[k] = f"${dep}"
            elif isinstance(v, str) and v.startswith("m"):
                # reference to an existing module output
                resolved_args[k] = f"${v}"
            elif isinstance(v, str) and v in vars_map:
                resolved_args[k] = vars_map[v]
            else:
                resolved_args[k] = v

        mod, fn = MODULE_REGISTRY.get(ident, ("apt_pipeline_pkg.pipeline", ident))
        step: Dict[str, Any] = {"name": step_name, "module": mod, "fn": fn, "args": dict(resolved_args)}
        if node.env:
            step["env"] = node.env
        steps.append(step)
        return step_name
    # literal or dict/list used as value is not allowed directly as a node result
    raise TypeError("Unsupported node type in equation")


def parse_rapt(text: str) -> Dict[str, Any]:
    # Split into assignment lines and the equation line (starts with 'Y' or 'y')
    lines = [l.strip() for l in text.splitlines() if l.strip() and not l.strip().startswith("#")]
    vars_map: Dict[str, Any] = {}
    equation = None
    for line in lines:
        if re.match(r"^[Yy]\s*=", line) or line.startswith("Y "):
            equation = line.split("=", 1)[1].strip()
            break
        if "=" in line:
            k, v = line.split("=", 1)
            key = k.strip()
            val = v.strip()
            # naive parse of literals
            if (val.startswith("\"") and val.endswith("\"")) or (val.startswith("'") and val.endswith("'")):
                vars_map[key] = val[1:-1]
            elif val.lower() in ("true", "false"):
                vars_map[key] = val.lower() == "true"
            elif val.lower() == "null":
                vars_map[key] = None
            else:
                # try number
                try:
                    vars_map[key] = int(val) if val.isdigit() else float(val)
                except Exception:
                    vars_map[key] = val

    if not equation:
        raise ValueError("No equation line found (expected 'Y = ...')")

    tokens = _tokenize(equation)
    node, i = _parse_call(tokens, 0)
    if i != len(tokens):
        raise SyntaxError("Unexpected tokens after equation")

    steps: List[Dict[str, Any]] = []
    _ = _walk(node, vars_map, steps, {})
    return {"steps": steps}
