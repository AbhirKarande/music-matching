import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt

def create_melspectrogram(audio_path, save_path=None):
    # Load the audio file
    y, sr = librosa.load(audio_path)
    
    # Create mel spectrogram
    mel_spect = librosa.feature.melspectrogram(
        y=y,
        sr=sr,
        n_mels=128,  # Number of mel bands
        fmax=8000    # Maximum frequency
    )
    
    # Convert to log scale
    mel_spect_db = librosa.power_to_db(mel_spect, ref=np.max)
    
    # Create the plot
    plt.figure(figsize=(12, 8))
    librosa.display.specshow(
        mel_spect_db,
        sr=sr,
        x_axis='time',
        y_axis='mel',
        fmax=8000
    )
    
    if save_path:
        plt.savefig(save_path)
        plt.close()
    return mel_spect_db