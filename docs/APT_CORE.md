# APT_CORE.md — Algebraic Pipeline Theory (APT) Minimal Core

## 1. What is APT?
APT (Algebraic Pipeline Theory) is a formal methodology for specifying, composing, and reasoning about computational pipelines using algebraic notation. It is not an app, not a product, not a demo—it's a way to make pipelines explicit, modular, auditable, and reproducible.

## 2. Core Principles
- **Modularity:** Every pipeline is a composition of modules $m_i$, each with explicit input/output variables.
- **Algebraic Notation:** Pipelines are described as equations: $y = m_n( ... m_2(m_1(x_1, x_2, ...)) ... )$
- **Explicit Variables:** All variables (inputs, outputs, intermediates) are defined before use.
- **Traceability:** Every step and variable can be logged, snapshotted, or audited.
- **Reproducibility:** The pipeline equation, variable definitions, and environment together fully determine the output.

## 3. Minimal APT Pipeline Example
Let $x_1$ = image, $x_2$ = prompt.

Define modules:
- $m_1$: base64_encode_image($x_1$) → $y_1$
- $m_2$: build_payload($y_1$, $x_2$) → $y_2$
- $m_3$: call_api($y_2$) → $y_3$
- $m_4$: parse_response($y_3$) → $y_4$

Pipeline equation:
$$
y_4 = m_4(m_3(m_2(m_1(x_1), x_2)))
$$

## 4. APT DSL (Minimal)
A pipeline is a list of modules with explicit variable bindings:

```yaml
pipeline:
  - name: m1
    fn: base64_encode_image
    inputs: { image: x1 }
    output: y1
  - name: m2
    fn: build_payload
    inputs: { image_b64: y1, prompt: x2 }
    output: y2
  - name: m3
    fn: call_api
    inputs: { payload: y2 }
    output: y3
  - name: m4
    fn: parse_response
    inputs: { response: y3 }
    output: y4
```

## 5. APT Execution Contract
- **Inputs:** $x_1$, $x_2$ (must be defined)
- **Modules:** $m_1, m_2, m_3, m_4$ (must be defined)
- **Equation:** $y_4 = m_4(m_3(m_2(m_1(x_1), x_2)))$
- **Trace:** For each step $i$, record $(m_i, inputs, output)$

## 6. Minimal Reference Implementation (optional)
- APT executor: a function that takes a pipeline spec (as above), a variable context, and a module registry, and produces the output and a trace.
- No production code, no telemetry, no demos—just a reference.

## 7. How to Use This Repo
- Read this doc and `README_APT.md`.
- Use `/docs` for theory, `/apt_core` for minimal reference code, `/specs` for pipeline examples.
- All other code is experimental and not part of the APT core.

## 8. Next Steps
- Refactor repo to keep only `/docs`, `/apt_core`, `/specs` in main; move all else to `/experimental`.
- Expand this doc with more algebraic examples, proofs, and formal properties as needed.
