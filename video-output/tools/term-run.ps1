# Usage: term-run.ps1 -Name 05 -Cmd '.venv\Scripts\python.exe -u -m mandi.chat_test "..."' -Match 'mandi\.chat_test'
# Records the dedicated "mandi-demo-term" Windows Terminal window (handle in .termhandle, placed top-left, 2560x1440 capture),
# types the command like a person, waits for the process to exit, then stops. Output: clips\rawTNAME.mkv + timing JSON.
param([Parameter(Mandatory)][string]$Name, [Parameter(Mandatory)][string]$Cmd, [string]$Match = "", [int]$MaxWait = 200, [int]$TailSec = 14)
$root = Split-Path -Parent $PSScriptRoot
Add-Type -TypeDefinition 'using System; using System.Runtime.InteropServices; public class TR { [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h); [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int c); [DllImport("user32.dll")] public static extern void keybd_event(byte k, byte s, uint f, UIntPtr e); }'
$h = [IntPtr][int64](Get-Content (Join-Path $PSScriptRoot ".termhandle"))
[TR]::ShowWindow($h, 9) | Out-Null
[TR]::keybd_event(0x12,0,0,[UIntPtr]::Zero); [TR]::keybd_event(0x12,0,2,[UIntPtr]::Zero)
[TR]::SetForegroundWindow($h) | Out-Null
Start-Sleep -Milliseconds 600
$ws = New-Object -ComObject WScript.Shell
$ws.SendKeys("cls{ENTER}"); Start-Sleep -Milliseconds 800
$out = Join-Path $root "clips\rawT$Name.mkv"
$ff = (Get-Command ffmpeg).Source
$ffStart = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
$p = Start-Process -FilePath $ff -ArgumentList "-hide_banner -loglevel error -y -f gdigrab -framerate 30 -draw_mouse 0 -video_size 2560x1440 -offset_x 0 -offset_y 0 -i desktop -c:v libx264 -preset veryfast -crf 20 -g 15 -flush_packets 1 -pix_fmt yuv420p `"$out`"" -WindowStyle Hidden -PassThru
Start-Sleep -Seconds 3
$typeStart = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
$oldClip = $null; try { $oldClip = Get-Clipboard -Raw } catch {}
Set-Clipboard -Value $Cmd
Start-Sleep -Milliseconds 400
$ws.SendKeys("^v")
Start-Sleep -Milliseconds 700
$ws.SendKeys("{ENTER}")
$enter = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
if ($null -ne $oldClip) { try { Set-Clipboard -Value $oldClip } catch {} }
$exit = $null
if ($Match) {
  $t0 = Get-Date; $seen = $false
  while (((Get-Date) - $t0).TotalSeconds -lt $MaxWait) {
    $run = Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Where-Object { $_.CommandLine -match $Match }
    if ($run) { $seen = $true } elseif ($seen) { break } elseif (((Get-Date) - $t0).TotalSeconds -gt 25) { break }
    Start-Sleep -Milliseconds 500
  }
  $exit = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
} else { Start-Sleep -Seconds 8; $exit = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds() }
Start-Sleep -Seconds $TailSec
Stop-Process -Id $p.Id -Force
Start-Sleep -Seconds 1
"{`"name`":`"$Name`",`"ffStart`":$ffStart,`"typeStart`":$typeStart,`"enter`":$enter,`"exit`":$exit,`"typeAt`":$(($typeStart-$ffStart)/1000.0),`"enterAt`":$(($enter-$ffStart)/1000.0),`"exitAt`":$(($exit-$ffStart)/1000.0)}"
