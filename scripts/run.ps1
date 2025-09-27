# Simple runner for APT scripts (PowerShell)
param(
    [string]$ApiKey = $env:LLAMA_API_KEY,
    [string]$Script = "apt_curl_3.py"
)

if (-not $ApiKey) {
    Write-Error "LLAMA_API_KEY not set. Set it with: $env:LLAMA_API_KEY = 'your_key' or pass -ApiKey param"
    exit 1
}

$env:LLAMA_API_KEY = $ApiKey
python $Script
