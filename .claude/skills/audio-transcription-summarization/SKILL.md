---
name: audio-transcription-summarization
description: Transcribe audio with Whisper/ffmpeg and produce structured, timestamped summaries and action items.
model: sonnet
allowed-tools: Read, Write, Edit, Bash
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill audio-transcription-summarization started '{"stage": "utility"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill audio-transcription-summarization ended '{"stage": "utility"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill audio-transcription-summarization instruction_start '{"stage": "utility", "method": "instruction-based"}'
```

---

# Audio Transcription & Summarization Skill

## What This Skill Enables

Claude can transcribe audio files (MP3, WAV, M4A, etc.) and generate structured summaries with timestamps, action items, and speaker identification. This skill leverages Whisper AI and ffmpeg through Claude's Code Interpreter to process audio locally.

## Prerequisites

**Required:**
- Claude Pro subscription
- Code Interpreter feature enabled in Claude Desktop settings
- Audio file uploaded to conversation (drag and drop)

**What Claude handles automatically:**
- Installing and running Whisper AI models
- Audio format conversion with ffmpeg
- Timestamp extraction and alignment
- Summary generation and structuring

## How to Use This Skill

### Basic Transcription

**Prompt:** "Transcribe this audio file and give me a clean text transcript."

Claude will:
1. Detect the audio format
2. Convert to optimal format for transcription
3. Run Whisper AI transcription
4. Return formatted text

### Timestamped Summary

**Prompt:** "Transcribe this meeting recording and create a timestamped summary with key discussion points every 5 minutes."

Claude will:
1. Transcribe the full audio
2. Chunk by time intervals
3. Summarize each segment
4. Present with timestamps

### Action Items Extraction

**Prompt:** "Transcribe this audio and extract all action items, decisions, and to-dos mentioned."

Claude will:
1. Transcribe the audio
2. Analyze for actionable items
3. List action items with timestamps
4. Identify who was assigned what (if mentioned)

### Speaker Diarization

**Prompt:** "Transcribe this conversation and identify different speakers. Label them as Speaker 1, Speaker 2, etc."

Claude will:
1. Detect speaker changes in the audio
2. Segment by speaker
3. Label each segment
4. Present as a conversation transcript

## Tips for Best Results

1. **Audio Quality Matters**: Clear audio with minimal background noise produces better transcriptions
2. **File Size**: For files over 25MB, mention if you want a specific time range transcribed first
3. **Language**: Specify the language if it's not English (e.g., "Transcribe this Spanish audio...")
4. **Model Selection**: For better accuracy on difficult audio, ask Claude to use the "medium" or "large" Whisper model
5. **Post-Processing**: Ask Claude to clean up transcription artifacts like repeated words or filler sounds

## Common Workflows

### Meeting Minutes Generation
```
"Transcribe this meeting and create:
1. Attendee list (if mentioned)
2. Key discussion topics with timestamps
3. Decisions made
4. Action items with owners
5. Next steps"
```

### Podcast Summary
```
"Transcribe this podcast episode and create:
1. Episode summary (2-3 sentences)
2. Main topics discussed with timestamps
3. Key quotes
4. Chapters (every 10 minutes)"
```

### Interview Transcription
```
"Transcribe this interview with speaker labels.
Format as Q&A with:
- Interviewer questions highlighted
- Interviewee responses
- Notable quotes pulled out"
```

## Troubleshooting

**Issue:** Transcription is inaccurate
**Solution:** Ask Claude to use a larger Whisper model or pre-process the audio for noise reduction

**Issue:** Wrong language detected
**Solution:** Explicitly specify the language in your prompt ("Transcribe this French audio...")

**Issue:** Timestamps are off
**Solution:** Ask Claude to re-align timestamps or specify the desired timestamp interval

**Issue:** Speaker diarization missing
**Solution:** Request it explicitly: "Please identify different speakers and label them"

## Learn More

- [Whisper AI by OpenAI](https://github.com/openai/whisper) - The underlying transcription model
- [ffmpeg Audio Processing](https://ffmpeg.org/ffmpeg-filters.html#Audio-Filters) - Audio format conversion details
- [Claude Code Interpreter](https://www.anthropic.com/news/code-interpreter) - How Claude executes code
- [Simon Willison's Analysis](https://simonwillison.net/2025/Oct/10/claude-skills/) - Deep dive into Claude's skills


## Key Features

- Local processing via Whisper
- Format conversion with ffmpeg
- Timestamped notes and action items
- Optional speaker labels

## Use Cases

- Summarize meetings and podcasts
- Generate action items
- Create searchable transcripts

## Examples

### Example 1: Transcribe with Whisper CLI

```bash
# Convert to mono 16kHz WAV
ffmpeg -i input.mp3 -ar 16000 -ac 1 input.wav

# Python whisper (pip install -U openai-whisper)
whisper input.wav --model small --language en --output_format txt
```

### Example 2: Summarize timestamps (Python)

```python
from pathlib import Path

text = Path('input.wav.txt').read_text(encoding='utf-8')
# Split by timestamps like [00:12:34]
# ... produce bullet summaries per 5-minute window ...
print(text[:500])
```

## Troubleshooting

### ffmpeg not found

Install ffmpeg via your package manager and ensure it is on PATH.

### High WER for noisy audio

Downmix to mono, apply noise reduction, and use a larger model.

### Whisper model download fails with SSL certificate verification error

Set SSL_CERT_FILE environment variable to system certificate bundle. Alternative: use --model-dir to specify pre-downloaded model location.

### Code Interpreter not enabled, skill activation fails silently

Open Claude Desktop Settings, enable Code Interpreter under Features tab. Restart Claude Desktop application to activate skill execution environment.

### Transcription timestamps drift out of sync with actual audio timing

Use --language flag to specify correct language explicitly. Re-encode audio at constant frame rate with: ffmpeg -i input.mp3 -ar 16000 -ac 1 output.wav

## Learn More

For additional documentation and resources, visit:

https://github.com/openai/whisper
