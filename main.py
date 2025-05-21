import argparse
import os
import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr

def record_audio(output_path, duration, sample_rate=44100):
    print(f"Recording for {duration} seconds...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    write(output_path, sample_rate, audio_data)

def transcribe_file(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        return "Could not understand the audio."
    except sr.RequestError as e:
        return f"Could not request results from Google API; {e}"

def save_transcript(path, text):
    with open(path, 'w') as f:
        f.write(text)

def main():
    parser = argparse.ArgumentParser(description="Speech-to-Text Converter")
    parser.add_argument('--record', type=int, help='Record audio from microphone')
    parser.add_argument('--input', type=str, help='Path to an existing audio file (WAV format)')
    parser.add_argument('--output', type=str, default='output/transcript.txt', help='File to save the transcription')

    args = parser.parse_args()

    if not os.path.exists('output'):
        os.makedirs('output')

    transcript = ""

    if args.record:
        print("Recording audio from microphone...")
        audio_file = 'output/recorded.wav'
        record_audio(audio_file, duration=args.record)
        print("Audio recording complete. Please wait, this may take a few seconds ...")
        transcript = transcribe_file(audio_file)
    elif args.input:
        if not os.path.isfile(args.input):
            print("Error: Input file does not exist.")
            return
        transcript = transcribe_file(args.input)
    else:
        print("Please specify either --record to record audio or --input to provide an audio file.")
        return

    print("\nTranscription:")
    print(transcript)

    save_transcript(args.output, transcript)
    print(f"\nTranscript saved to {args.output}")

if __name__ == "__main__":
    main()
