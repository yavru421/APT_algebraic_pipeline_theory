param(
  [Parameter(Mandatory=$true)] [string] $EnvName,
  [Parameter(Mandatory=$true)] [string] $Module,
  [Parameter(Mandatory=$true)] [string] $Function,
  [Parameter(Mandatory=$true)] [string] $ArgsJson
)

$ErrorActionPreference = 'Stop'

# Resolve repo root and env python
$repoRoot = Split-Path -Parent $PSScriptRoot
$venvPython = Join-Path $repoRoot "APT_ENV/venvs/$EnvName/.venv/Scripts/python.exe"
if (-not (Test-Path $venvPython)) {
  throw "Env python not found: $venvPython"
}

# Inline python to import and invoke
$code = @'
import json, importlib, sys
m = sys.argv[1]
f = sys.argv[2]
args = json.loads(sys.argv[3])
fn = getattr(importlib.import_module(m), f)
out = fn(**args)
print(json.dumps(out, default=str))
'@

$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = $venvPython
$psi.ArgumentList.Add('-c')
$psi.ArgumentList.Add($code)
$psi.ArgumentList.Add($Module)
$psi.ArgumentList.Add($Function)
$psi.ArgumentList.Add($ArgsJson)
$psi.WorkingDirectory = $repoRoot
$psi.UseShellExecute = $false
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $true

$p = [System.Diagnostics.Process]::Start($psi)
$stdout = $p.StandardOutput.ReadToEnd()
$stderr = $p.StandardError.ReadToEnd()
$p.WaitForExit()
if ($p.ExitCode -ne 0) {
  throw "Step failed: $stderr"
}
Write-Output $stdout