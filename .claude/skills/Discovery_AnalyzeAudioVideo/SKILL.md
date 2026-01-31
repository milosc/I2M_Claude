---
name: analyzing-audio-video-transcripts
description: Transcribe audio/video files and analyze transcripts for discovery insights.
model: sonnet
allowed-tools: Read, Glob, Grep, Bash, Write, Edit
context: fork
agent: general-purpose
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill analyzing-audio-video-transcripts started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill analyzing-audio-video-transcripts ended '{"stage": "discovery"}'
---

# Analyze Audio/Video

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill analyzing-audio-video-transcripts instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Discovery_AnalyzeAudioVideo
- **Version**: 3.0.0
- **Created**: 2025-01-15
- **Updated**: 2025-12-28
- **Author**: Milos Cigoj
- **Change History**:
  - v3.0.0 (2025-12-28): Added support for audio transcription using openai-whisper
  - v2.1.0 (2025-12-19): Added version control metadata per VERSION_CONTROL_STANDARD.md
  - v2.0.0 (2025-01-15): Initial skill version for Discovery Skills Framework v2.0

## Description
Analyzes audio/video content by **first transcribing it** using Whisper AI, then analyzing the transcript.

## Execution Logging

This skill uses **deterministic lifecycle logging** via frontmatter hooks.

**Events logged automatically:**
- `skill:analyzing-audio-video-transcripts:started` - When skill begins
- `skill:analyzing-audio-video-transcripts:ended` - When skill finishes

**Log file:** `_state/lifecycle.json`

---

## Prerequisites
- `openai-whisper` python package installed
- `ffmpeg` installed on system

---

## 🚨 CRITICAL: WHAT THIS SKILL DOES AND DOES NOT DO

### ⛔ CANNOT PROCESS (Skip Immediately - Don't Even Try)

| Type | Action |
|------|--------|
| YouTube URLs | Log skip, continue |
| Vimeo URLs | Log skip, continue |
| Any video URL | Log skip, continue |

### ✅ CAN PROCESS

| Type | Action |
|------|--------|
| .mp3, .wav, .m4a files | **TRANSCRIBE** then Analyze |
| .mp4, .mov, .avi files | **TRANSCRIBE** then Analyze |
| .txt transcript files | Read and analyze |
| .md transcript files | Read and analyze |
| .vtt caption files | Read and analyze |
| .srt subtitle files | Read and analyze |

---

## Processing Pattern

```
FOR EACH item:
    
    # Check if it's a video/audio URL - SKIP IMMEDIATELY
    IF is_youtube_url(item) OR is_video_url(item):
        log_skip(item, "Video URLs not supported")
        CONTINUE
    
    # If Audio/Video File -> TRANSCRIBE FIRST
    IF is_audio_file(item) OR is_video_file(item):
        TRY:
            transcript_path = Transcribe(item)
            content = Read(transcript_path)
            analyze(content)
        CATCH:
            log_skip(item, "Transcription failed")
        CONTINUE
    
    # If Transcript File -> PROCESS DIRECTLY
    IF is_transcript_file(item):
        TRY:
            content = Read(item)
            analyze(content)
        CATCH:
            log_skip(item, "Read failed")
        CONTINUE

END FOR
```

## Transcription Instructions

If the file is an audio or video file, follow these steps to transcribe it:

1.  **Check Dependencies**: Ensure `ffmpeg` and `openai-whisper` are installed.
2.  **Convert to WAV (if needed)**:
    ```bash
    ffmpeg -i "<input_file>" -ar 16000 -ac 1 "<input_file>.wav"
    ```
3.  **Transcribe with Whisper**:
    ```bash
    .venv/bin/whisper "<input_file>.wav" --model small --language en --output_format txt --output_dir "<directory_of_input_file>"
    ```
4.  **Read Transcript**:
    - The output file will be `<input_file>.wav.txt`.
    - Read this file using the `Read` tool.

5.  **Analyze**:
    - Treat the content as a meeting transcript or interview.
    - Extract insights (Pain Points, User Types, Workflows, etc.) just like any other document.

---

## URL Detection

```python
# These patterns = SKIP IMMEDIATELY
video_urls = [
    "youtube.com",
    "youtu.be", 
    "vimeo.com",
    "dailymotion.com",
    "twitch.tv",
    "tiktok.com"
]

if any(pattern in url for pattern in video_urls):
    log_skip(url, "Video URLs not supported")
    continue  # DO NOT try to fetch, DO NOT retry
```

## File Extension Detection

```python
# These extensions = TRANSCRIBE
video_exts = ['.mp4', '.mov', '.avi', '.webm', '.mkv', '.wmv', '.flv']
audio_exts = ['.mp3', '.wav', '.m4a', '.aac', '.ogg', '.flac', '.wma']
```

---

## 🚨 ERROR HANDLING

> **STRICT RULE**: Follow the global error handling rules in `.claude/rules/error-handling.md`.

### Skipped Media Files Log
In `FAILURES_LOG.md`:

**Version**: 3.0