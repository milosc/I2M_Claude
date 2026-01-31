# Error Handling Patterns for Discovery Skills

> **CRITICAL**: All Discovery skills MUST follow these error handling patterns to prevent execution loops.

---

## 🔴 ABSOLUTE RULE #1: NEVER LOOP

**When you see ANY of these errors, SKIP THE FILE IMMEDIATELY and continue to next:**

```
"PDF too large"
"Please double press esc"
"ModuleNotFoundError"
"command not found"
"Exit code 1"
"Exit code 127"
"Timeout"
"Cannot read file"
"Permission denied"
```

**DO NOT:**
- ❌ Try another library
- ❌ Try pip install
- ❌ Ask user what to do
- ❌ Wait for user input
- ❌ Retry the same operation
- ❌ Try a different approach

**DO:**
- ✅ Log: `⛔ SKIPPED: [filename] - [error reason]`
- ✅ Immediately proceed to next file
- ✅ Continue analysis with remaining files

---

## 🔴 ABSOLUTE RULE #2: Maximum 1 Attempt Per File

```
Attempt to read file
    ↓
SUCCESS? → Process it, continue to next file
    ↓
FAILED? → Log failure, SKIP, continue to next file
```

**There is NO step 2. There is NO retry. There is NO alternative approach.**

---

## The "PDF too large" Error

When Claude's Read tool returns:
```
"PDF too large. Please double press esc to edit your message and try again."
```

### CORRECT Response:
```
I cannot read this PDF as it has too many pages. Logging failure and continuing.

⛔ SKIPPED: manual.pdf - PDF has too many pages for processing

Moving to next file...
```

### INCORRECT Responses:
```
❌ "Let me try pdfplumber..."
❌ "Let me try PyPDF2..."
❌ "Let me install a library..."
❌ "What should I do instead?"
❌ "Please provide the file in a different format..."
```

---

## Complete File Processing Pattern

```
FOR EACH file IN files_to_process:
    
    # === SINGLE ATTEMPT ===
    TRY:
        content = Read(file)
        process(content)
        log_success(file)
    
    CATCH any_error:
        log_failure(file, error)
        # DO NOT RETRY
        # DO NOT TRY ALTERNATIVES
        # DO NOT ASK USER
    
    # === ALWAYS CONTINUE ===
    CONTINUE to next file

END FOR

# === AFTER ALL FILES ===
Proceed with analysis using successfully read files
```

---

## Error → Action Mapping

| Error Contains | Action | Say This |
|----------------|--------|----------|
| "PDF too large" | SKIP | "Skipping [file] - too many pages. Continuing..." |
| "too large" | SKIP | "Skipping [file] - file too large. Continuing..." |
| "ModuleNotFoundError" | SKIP | "Skipping [file] - required tool unavailable. Continuing..." |
| "command not found" | SKIP | "Skipping [file] - required tool unavailable. Continuing..." |
| "Exit code" | SKIP | "Skipping [file] - processing failed. Continuing..." |
| "Timeout" | SKIP | "Skipping [file] - timeout. Continuing..." |
| "Permission denied" | SKIP | "Skipping [file] - access denied. Continuing..." |
| "double press esc" | SKIP | "Skipping [file] - cannot process. Continuing..." |
| Any other error | SKIP | "Skipping [file] - error occurred. Continuing..." |

---

## What NOT To Do (Common Mistakes)

### ❌ WRONG: Trying multiple libraries
```
Let me try pdfplumber... [fails]
Let me try pypdf... [fails]  
Let me try PyPDF2... [fails]
Let me try markitdown... [fails]
```

### ✅ CORRECT: Skip on first failure
```
Cannot read this PDF. Skipping and continuing to next file.
```

---

### ❌ WRONG: Installing packages
```
pip install PyPDF2...
```

### ✅ CORRECT: Skip if tools unavailable
```
Required tools not available. Skipping file and continuing.
```

---

### ❌ WRONG: Asking user
```
What should Claude do instead?
```

### ✅ CORRECT: Just continue
```
Skipped 1 file due to processing error. Continuing with remaining files.
```

---

### ❌ WRONG: Retrying after "continue" command
```
User: continue
Claude: [tries same file again] → "PDF too large"
```

### ✅ CORRECT: Move to next file
```
User: continue
Claude: Moving to next file... [processes next file]
```

---

## FAILURES_LOG.md Format

When files are skipped, log them:

```markdown
## Skipped Files

| File | Reason | Impact |
|------|--------|--------|
| manual.pdf | PDF has too many pages | May miss documentation details |
| video.mp4 | Video files not supported | Provide transcript instead |

## Recommendation

For large PDFs, manually extract text using:
- Adobe Acrobat: File → Export → Text
- Online tool: pdf2text converters
- macOS Preview: Select All → Copy → Paste to text file
```

---

## Pre-Processing Skip List

Skip these BEFORE attempting to read:

| Type | Extensions/Patterns | Log Message |
|------|---------------------|-------------|
| Video URLs | youtube.com, vimeo.com | "Video URLs not supported" |
| Video files | .mp4, .mov, .avi, .webm, .mkv | "Video files not supported" |
| Audio files | .mp3, .wav, .m4a, .aac | "Audio files not supported" |
| Archives | .zip, .tar, .gz, .rar | "Archive files not supported" |
| Executables | .exe, .app, .dmg | "Executable files not supported" |
| Very large | >10MB any file | "File too large" |

---

## Summary: The Only Rule You Need

```
IF file_read_fails:
    log_failure()
    CONTINUE  ← This is the ONLY valid response to any error
```

---

**Version**: 2.0
**Key Change**: Removed all retry/recovery logic. One attempt per file, then skip.
