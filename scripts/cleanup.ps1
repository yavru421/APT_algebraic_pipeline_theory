# Remove outputs, cache, venv, logs, archive, and results
Remove-Item -Recurse -Force __pycache__ -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force archive -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force results -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force APT_OUTPUTS -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force APT_PIPELINE_RUNS -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force APT_LOGS -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force APT_INPUTS -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force APT_ENV/venvs -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force venv -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force .env -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force .venv -ErrorAction SilentlyContinue
