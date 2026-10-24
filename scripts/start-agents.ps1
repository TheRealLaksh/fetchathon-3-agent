# Starts the three Mandi Net-Price Desk agents, each in its own PowerShell window (output also goes to logs\<agent>.log).
# Run from anywhere:  powershell -ExecutionPolicy Bypass -File scripts\start-agents.ps1
# If the agents are already running, stop them first with scripts\stop-agents.ps1 (the ports would clash).
$root = Split-Path -Parent $PSScriptRoot
$py = Join-Path $root ".venv\Scripts\python.exe"

$running = Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Where-Object { $_.CommandLine -match 'mandi\.(price|logistics|front)_agent' }
if ($running) {
    Write-Host "Mandi agents are already running (PIDs: $($running.ProcessId -join ', ')). Run scripts\stop-agents.ps1 first to restart."
    exit 1
}

New-Item -ItemType Directory -Force (Join-Path $root "logs") | Out-Null
# UTF-8 so Hindi and Hinglish messages are handled and logged correctly on Windows.
$prefix = "cd '$root'; `$env:PYTHONIOENCODING='utf-8'; `$env:PYTHONUTF8='1'; "

foreach ($m in @("mandi.price_agent", "mandi.logistics_agent")) {
    $log = Join-Path $root ("logs\" + ($m -replace 'mandi\.', '') + ".log")
    Start-Process powershell -ArgumentList "-NoExit", "-Command", ($prefix + "& '$py' -u -m $m 2>&1 | Tee-Object -FilePath '$log'")
}
Start-Sleep -Seconds 8   # let the helper agents register before the front agent starts
$flog = Join-Path $root "logs\front_agent.log"
Start-Process powershell -ArgumentList "-NoExit", "-Command", ($prefix + "`$env:USE_MAILBOX='1'; & '$py' -u -m mandi.front_agent 2>&1 | Tee-Object -FilePath '$flog'")
Write-Host "Started price agent, logistics agent and front agent (mailbox) in three windows. Keep them open. Logs: $root\logs"
