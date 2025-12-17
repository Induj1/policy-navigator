# Start Backend Script
cd backend
$env:PYTHONPATH = $PWD.Path
Write-Host "Starting Policy Navigator Backend..." -ForegroundColor Green
Write-Host "PYTHONPATH set to: $env:PYTHONPATH" -ForegroundColor Yellow
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
