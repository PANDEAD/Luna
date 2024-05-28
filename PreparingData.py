import sounddevice as sd
from scipy.io.wavfile import write
import os

print(sd.query_devices())

input_device_index = 0  # Replace with the correct index
fs = 44100
seconds = 2

def get_next_available_index(folder_path):
    files = os.listdir(folder_path)
    indices = []
    for file in files:
        if file.endswith(".wav"):
            try:
                index = int(file.split('.')[0])
                indices.append(index)
            except ValueError:
                pass
    if indices:
        return max(indices) + 1
    else:
        return 0

def record_audio_and_save(save_path, n_times=100):
    input("To start recording Wake Word press Enter: ")
    next_index = get_next_available_index(save_path)
    for i in range(next_index, next_index + n_times):
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, device=input_device_index)
        sd.wait()
        write(save_path + str(i) + ".wav", fs, myrecording)
        input(f"Press Enter to record next or press ctrl + C to stop ({i - next_index + 1}/{n_times}): ")

def record_background_sound(save_path, n_times=50):
    input("To start recording your background sounds press Enter: ")
    next_index = get_next_available_index(save_path)
    for i in range(next_index, next_index + n_times):
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, device=input_device_index)
        sd.wait()
        write(save_path + str(i) + ".wav", fs, myrecording)
        print(f"Currently on {i - next_index + 1}/{n_times}")

# Step 1: Record yourself saying the Wake Word
print("Recording the Wake Word:\n")
record_audio_and_save("audio_data/", n_times=50)

# Step 2: Record your background sounds (Just let it run, it will automatically record)
print("Recording the Background sounds:\n")
record_background_sound("background_sound/", n_times=50)
