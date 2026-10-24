# Usage: tts.ps1 -Voice "Microsoft Zira Desktop" -Rate -1 -In scene01.txt -Out scene01.wav
param([string]$Voice="Microsoft Zira Desktop",[int]$Rate=-1,[Parameter(Mandatory)][string]$In,[Parameter(Mandatory)][string]$Out)
Add-Type -AssemblyName System.Speech
$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
$s.SelectVoice($Voice); $s.Rate = $Rate
$fmt = New-Object System.Speech.AudioFormat.SpeechAudioFormatInfo(44100, [System.Speech.AudioFormat.AudioBitsPerSample]::Sixteen, [System.Speech.AudioFormat.AudioChannel]::Mono)
$s.SetOutputToWaveFile((Resolve-Path -LiteralPath (Split-Path $Out -Parent)).Path + "\" + (Split-Path $Out -Leaf), $fmt)
$s.Speak((Get-Content -LiteralPath $In -Raw)); $s.Dispose()
