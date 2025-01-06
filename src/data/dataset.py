import torch
from torch.utils.data import Dataset
from pathlib import Path
from ..utils.mel_spectrogram import create_melspectrogram

class AudioDataset(Dataset):
    def __init__(self, audio_dir, transform=None):
        self.audio_dir = Path(audio_dir)
        self.audio_files = list(self.audio_dir.glob("*.mp3"))  # or other formats
        self.transform = transform
        
    def __len__(self):
        return len(self.audio_files)
        
    def __getitem__(self, idx):
        audio_path = self.audio_files[idx]
        mel_spec = create_melspectrogram(str(audio_path))
        
        if self.transform:
            mel_spec = self.transform(mel_spec)
            
        return torch.from_numpy(mel_spec) 