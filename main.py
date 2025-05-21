import argparse
import os
import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr
from deep_translator import GoogleTranslator

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

def translate_and_save(text, translations):
    for lang_code, filename in translations.items():
        try:
            translator = GoogleTranslator(source='auto', target=lang_code)
            translated = translator.translate(text)
            output_path = os.path.join('output', filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(translated)
            print(f"Translated transcript saved to {output_path}")
        except Exception as e:
            print(f"Translation to {lang_code} failed: {e}")

def main():
    parser = argparse.ArgumentParser(description="Speech-to-Text Converter")
    parser.add_argument('--record', type=int, help='Record audio from microphone')
    parser.add_argument('--input', type=str, help='Path to an existing audio file (WAV format)')
    parser.add_argument('--output', type=str, default='output/english.txt', help='File to save the transcription')

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
    print(f"\nTranscript saved to {args.output}\n")

    save_transcript(args.output, transcript)
    translations = {
        'kn': 'kannada.txt',
        'de': 'german.txt',
        'fr': 'french.txt',
        'hi': 'hindi.txt',
        'ta': 'tamil.txt',
        'ja': 'japanese.txt'
    }
    translate_and_save(transcript, translations)

if __name__ == "__main__":
    main()
