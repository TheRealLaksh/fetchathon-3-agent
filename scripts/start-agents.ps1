# Starts the three Mandi Net-Price Desk agents, each in its own PowerShell window.
# Run from anywhere:  powershell -ExecutionPolicy Bypass -File scripts\start-agents.ps1
# If the agents are already running, stop them first with scripts\stop-agents.ps1 (the ports would clash).
$root = Split-Path -Parent $PSScriptRoot
$py = Join-Path $root ".venv\Scripts\python.exe"

$running = Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Where-Object { $_.CommandLine -match 'mandi\.(price|logistics|front)_agent' }
if ($running) {
    Write-Host "Mandi agents are already running (PIDs: $($running.ProcessId -join ', ')). Run scripts\stop-agents.ps1 first to restart."
    exit 1
}

foreach ($m in @("mandi.price_agent", "mandi.logistics_agent")) {
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root'; & '$py' -u -m $m"
}
Start-Sleep -Seconds 8   # let the helper agents register before the front agent starts
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root'; `$env:USE_MAILBOX='1'; & '$py' -u -m mandi.front_agent"
Write-Host "Started price agent, logistics agent and front agent (mailbox) in three windows. Keep them open."
