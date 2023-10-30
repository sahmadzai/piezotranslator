import librosa
import numpy as np

def print_progress(iteration, total, prefix='', length=50, fill='█', print_end='\r'):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'{prefix} |{bar}| {percent}% Complete', end=print_end)
    if iteration == total:
        print()

def generate_arduino_code(frequencies, durations):
    arduino_code = "void play_sound() {\n"
    for freq, dur in zip(frequencies, durations):
        arduino_code += f"  tone(BUZZER_PIN, {freq}, {dur});\n"
        arduino_code += f"  delay({dur});\n"
    arduino_code += "}\n"
    return arduino_code

def audio_to_piezo(filename):
    print("Loading audio file...")
    y, sr = librosa.load(filename, sr=None)
    print("Audio file loaded.")

    # Define the chunk size and number of chunks
    chunk_size = sr // 10  # 10 chunks for a 1 second audio file
    num_chunks = len(y) // chunk_size

    frequencies = []
    durations = []
    print("Analyzing audio chunks...")
    for i in range(num_chunks):
        print_progress(i + 1, num_chunks, prefix='Progress', length=50)
        chunk = y[i * chunk_size:(i + 1) * chunk_size]
        # Compute the FFT of the chunk
        fft_result = np.fft.fft(chunk)
        # Find the frequency of the peak with the highest magnitude
        dominant_frequency = np.argmax(np.abs(fft_result))
        # Convert the bin index to a frequency
        dominant_frequency = dominant_frequency * sr / len(fft_result)
        frequencies.append(int(dominant_frequency))
        durations.append(int(1000 * chunk_size / sr))  # duration in ms

    print("Generating Arduino code...")
    arduino_code = generate_arduino_code(frequencies, durations)
    print(arduino_code)

# Usage:
audio_to_piezo('starwars_blaster.wav')