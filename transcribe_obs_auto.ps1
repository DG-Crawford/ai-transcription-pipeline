# ===============================================
# AI Transcription Script - OBS + WhisperX Edition
# Author: David Crawford
# Description:
#   - Converts latest OBS recording to WAV
#   - Runs WhisperX transcription + diarization
# ===============================================

# ----------------------
# CONFIGURATION
# ----------------------

# Use the system's default Videos folder
$defaultVideos = [Environment]::GetFolderPath("MyVideos")
$obsFolder = Read-Host "Enter path to your OBS recordings folder (Press Enter for default: $defaultVideos)"
if ([string]::IsNullOrWhiteSpace($obsFolder)) {
    $obsFolder = $defaultVideos
}

$wavFolder = "$obsFolder\wav"
$transcriptionFolder = "$obsFolder\transcription"

# Ensure output directories exist
New-Item -ItemType Directory -Path $wavFolder -Force | Out-Null
New-Item -ItemType Directory -Path $transcriptionFolder -Force | Out-Null

# ----------------------
# MAIN PROCESS
# ----------------------

# Get the latest .mkv file
$latestFile = Get-ChildItem -Path $obsFolder -Filter "*.mkv" | Sort-Object LastWriteTime -Descending | Select-Object -First 1

if ($latestFile) {
    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($latestFile.Name)
    $wavFile = "$wavFolder\$baseName.wav"

    Write-Host "🎧 Converting $($latestFile.Name) to WAV..."
    ffmpeg -i "$($latestFile.FullName)" -vn -acodec pcm_s16le -ar 16000 -ac 1 "$wavFile" -y

    Write-Host "🧠 Transcribing with WhisperX (diarization enabled)..."
    whisperx "$wavFile" `
        --model medium `
        --diarize `
        --hf_token $env:HF_TOKEN `
        --compute_type float32 `
        --output_dir "$transcriptionFolder"

    Write-Host "✅ Transcription complete. Output saved to $transcriptionFolder"
} else {
    Write-Host "❌ No OBS recordings found in: $obsFolder" -ForegroundColor Red
}
