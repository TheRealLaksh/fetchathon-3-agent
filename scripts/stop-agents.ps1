# Stops the three Mandi Net-Price Desk agents.
$procs = Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Where-Object { $_.CommandLine -match 'mandi\.(price|logistics|front)_agent' }
if (-not $procs) { Write-Host "No Mandi agents are running."; exit 0 }
$procs | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
Write-Host "Stopped $($procs.Count) process(es)."
