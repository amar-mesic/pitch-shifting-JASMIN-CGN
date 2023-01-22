from audiomentations import Compose, AddGaussianNoise, PitchShift, Shift
import numpy as np
import os
import librosa
import soundfile as sf
import time

shift_up = Compose([
    # p - probability of shift being applied
    PitchShift(min_semitones=4, max_semitones=5, p=1)
])

shift_down = Compose([
    # p - probability of shift being applied
    PitchShift(min_semitones=-7, max_semitones=-6, p=1)
])


# sample = np.random.uniform(low=-0.2, high=0.2, size=(32000,)).astype(np.float32)
# augmented = shift_up(samples=sample, sample_rate=16000)
# sf.write('./original_noise.wav', sample, 16000)
# sf.write('./augmented_noise.wav', augmented, 16000)


# orig_audio, sr = sf.read('./comp-q-speech.wav')
# augmented = shift_down(samples=orig_audio, sample_rate=sr)
# sf.write('./shift_down_speech.wav', augmented, sr)

print("Starting....")

#orignal speech files directories
wavDirP = "/Users/amarmesic/Documents/TUDelft/Research Project/orig-audio/comp-p"
wavDirQ = "/Users/amarmesic/Documents/TUDelft/Research Project/orig-audio/comp-q"

#augmented speech files directories
augDirP = "/Users/amarmesic/Documents/TUDelft/Research Project/aug-audio/comp-p"
augDirQ = "/Users/amarmesic/Documents/TUDelft/Research Project/aug-audio/comp-q"

start = time.time()
#Run augmentation for dialogue speech
for file in os.listdir(wavDirP):
    if file.endswith(".wav"):
        print("processing " + file)
        orig_audio, sr = sf.read(wavDirP+"/"+file)
        aug_audio = shift_up(samples=orig_audio, sample_rate=sr)
        augmentName = os.path.splitext(file)[0]+"ps.wav"
        sf.write(augDirP+"/"+augmentName, aug_audio, sr)
end_p = time.time()
print("done with spoken!\nTime taken: {} seconds".format(end_p - start))

start_q = time.time()
#Run augmentation for read speech
for file in os.listdir(wavDirQ):
    if file.endswith(".wav"):
        print("processing " + file)
        orig_audio, sr = librosa.load(wavDirQ+"/"+file, sr=16000)
        aug_audio = shift_up(orig_audio, sr)
        augmentName = os.path.splitext(file)[0]+"ps.wav"
        sf.write(augDirQ+"/"+augmentName, aug_audio, sr)
end = time.time()
print("done with read!\nTime taken: {} seconds".format(end - start_q))

print("all done!\nTime taken: {} seconds".format(end - start))