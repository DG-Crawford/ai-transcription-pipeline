# AI Transcription Pipeline

This project provides a lightweight, local-first pipeline for transcribing recorded meetings or voice notes using OBS, WhisperX, and optional text cleanup tools.

Built for transparency, speed, and security—no cloud services required.

## Features

- Uses `.mkv` recordings from OBS Studio
- Transcribes audio using WhisperX with diarization support
- Optional keyword and pattern cleanup (redaction)
- Designed for modular integration into larger AI workflows

## Workflow Overview

1. Record using OBS
2. Run `transcribe_obs_auto.ps1` to:
   - Convert `.mkv` to `.wav`
   - Transcribe using WhisperX
   - Output transcript into a subfolder
3. (Optional) Run `redactor.py` to clean names, IPs, versions, etc.

## Repository Contents

| File                     | Purpose                                          |
|--------------------------|--------------------------------------------------|
| `transcribe_obs_auto.ps1` | PowerShell automation for WhisperX transcription |
| `redactor.py`            | Optional keyword and pattern redactor           |
| `.gitignore`             | Cleanup and privacy exclusions                  |
| `LICENSE`                | MIT license                                     |
| `README.md`              | This file                                       |

## Usage

### 1. Transcription

Run from PowerShell:

```powershell
.	ranscribe_obs_auto.ps1
```

- Prompts for OBS recording folder
- Automatically processes the latest `.mkv`
- Uses WhisperX with Hugging Face diarization support

Dependencies:

- `ffmpeg` (in PATH)
- `whisperx` installed
- Hugging Face token available via `$env:HF_TOKEN`

### 2. Optional Cleanup

Run from Python:

```bash
python redactor.py transcript.txt [keywords.txt]
```

- Replaces names, domains, IPs, and version strings with `[REDACTED]`
- If provided, loads custom redaction terms from `keywords.txt` (one per line)
- Outputs: `transcript.redacted.txt`

## Summarizer Module (Prototype)

This optional script (included separately) attempts to summarize transcripts using a local LLM (e.g., Mistral 7B).

Current/planned features:

- Transcript chunking for token window management
- Debugging support and structured output (WIP)
- Summary generation via local models

Limitations:

- Early-stage prototype
- Local-only; no API integration
- Not yet production-ready

This module is included to demonstrate forward-looking architecture and AI integration potential.

## Roadmap

- [ ] Summarizer: bullet summaries with context window management
- [ ] Web-based transcript viewer
- [ ] Diarization parser and speaker tag refinements
- [ ] Optional pre-trimming based on silence or voice activity

## Privacy Note

No data is uploaded or stored externally. All processing happens locally on your machine. Redaction and summarization are optional modules and can be excluded from the workflow entirely.

## License

MIT © 2025 David Crawford
