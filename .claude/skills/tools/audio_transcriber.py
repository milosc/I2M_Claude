import argparse
import os
import whisper
import warnings
import sys

# Suppress warnings
warnings.filterwarnings("ignore")

def transcribe_audio(input_path, output_dir, model_name="base"):
    try:
        print(f"🎤 Loading Whisper model: {model_name}...")
        model = whisper.load_model(model_name)
        
        print(f"🎧 Transcribing: {input_path}")
        # Use fp16=False to avoid warnings on CPU if CUDA is not available
        result = model.transcribe(input_path, fp16=False)
        
        # Create output filename
        base_name = os.path.basename(input_path)
        name_without_ext = os.path.splitext(base_name)[0]
        output_filename = f"{name_without_ext}_transcript.md"
        output_path = os.path.join(output_dir, output_filename)
        
        # Ensure output dir exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Format as Markdown with timestamps
        md_content = f"# Transcript: {base_name}\n\n"
        md_content += f"**Source File**: {input_path}\n"
        # Handle case with empty segments
        duration = 0
        if result['segments']:
            duration = result['segments'][-1]['end']
        
        md_content += f"**Duration**: {duration:.2f} seconds\n\n"
        md_content += "---\n\n"
        
        for segment in result["segments"]:
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            text = segment["text"].strip()
            md_content += f"**[{start} - {end}]**: {text}\n\n"
            
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_content)
            
        print(f"✅ Transcript saved to: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error transcribing {input_path}: {str(e)}")
        return False

def format_timestamp(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe audio file to Markdown.")
    parser.add_argument("input_path", help="Path to audio file")
    parser.add_argument("output_dir", help="Directory to save transcript")
    parser.add_argument("--model", default="base", help="Whisper model size (tiny, base, small, medium, large)")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_path):
        print(f"❌ Input file not found: {args.input_path}")
        sys.exit(1)
        
    success = transcribe_audio(args.input_path, args.output_dir, args.model)
    if not success:
        sys.exit(1)
