import os
import glob
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import concurrent.futures

def create_mel_spectrogram(audio_path, save_path=None):
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
        cmap='viridis'
    )
    plt.colorbar(format='%+2.0f dB')
    plt.title('Mel Spectrogram')
    
    # Save or show the plot
    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()

def process_mp3_file(mp3_file, mel_dir):
    """
    Process one mp3 file: convert it to a mel spectrogram image and
    delete the original mp3 file after conversion.
    """
    base = os.path.splitext(os.path.basename(mp3_file))[0]
    output_path = os.path.join(mel_dir, f"{base}_mel_spectrogram.png")
    print(f"Converting {mp3_file} -> {output_path}")
    create_mel_spectrogram(mp3_file, output_path)
    
    # # Delete the original file after processing
    # os.remove(mp3_file)
    # print(f"Deleted original file: {mp3_file}")

if __name__ == "__main__":
    # Define the downloads directory. Updating this to the home Downloads folder.
    downloads_dir = os.path.expanduser("~/music-matching/utils/downloads")
    
    # Create a new directory for mel spectrogram images if it doesn't already exist.
    mel_dir = os.path.join(downloads_dir, "mel_spectrogram")
    if not os.path.exists(mel_dir):
        os.makedirs(mel_dir)
    
    # Grab all .mp3 files in the downloads directory.
    mp3_files = glob.glob(os.path.join(downloads_dir, "*.mp3"))
    
    if not mp3_files:
        print("No .mp3 files found in", downloads_dir)
    
    # Process each .mp3 file concurrently using ProcessPoolExecutor.
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_mp3_file, mp3_file, mel_dir)
                   for mp3_file in mp3_files]
        # Optionally wait for all futures to complete and handle exceptions.
        for future in concurrent.futures.as_completed(futures):
             try:
                 future.result()
             except Exception as e:
                 print("Error processing file:", str(e))