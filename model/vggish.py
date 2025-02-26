import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from PIL import Image
import torchvision.transforms as transforms

class VGGish(nn.Module):
    """
    PyTorch implementation of the VGGish model for audio embeddings.
    
    This model takes mel spectrograms as input and outputs embeddings
    that can be used for audio similarity, classification, etc.
    """
    def __init__(self, embedding_dim=128):
        super(VGGish, self).__init__()
        
        # VGG-like architecture
        self.features = nn.Sequential(
            # Conv Block 1
            nn.Conv2d(3, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            # Conv Block 2
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            # Conv Block 3
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            # Conv Block 4
            nn.Conv2d(256, 512, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        
        # Fully connected layers
        self.fc = nn.Sequential(
            nn.Linear(512 * 8 * 8, 4096),  # Assuming input size is 128x128
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(4096, embedding_dim)
        )
        
        self.output_dim = embedding_dim
        
    def forward(self, x):
        x = self.features(x)
        x = torch.flatten(x, 1)
        x = self.fc(x)
        return x
    
    def load_mel_spectrogram(self, image_path, target_size=(128, 128)):
        """
        Load a mel spectrogram image and preprocess it for the model.
        
        Args:
            image_path: Path to the mel spectrogram image
            target_size: Size to resize the image to
            
        Returns:
            Tensor ready for model input
        """
        # Define transforms
        transform = transforms.Compose([
            transforms.Resize(target_size),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                                std=[0.229, 0.224, 0.225])
        ])
        
        # Load and transform image
        image = Image.open(image_path).convert('RGB')  # Convert to RGB
        image_tensor = transform(image).unsqueeze(0)  # Add batch dimension
        
        return image_tensor
    
    def get_embedding(self, image_path):
        """
        Generate an embedding for a mel spectrogram image.
        
        Args:
            image_path: Path to the mel spectrogram image
            
        Returns:
            Numpy array containing the embedding
        """
        # Set model to evaluation mode
        self.eval()
        
        # Load and preprocess the image
        image_tensor = self.load_mel_spectrogram(image_path)
        
        # Generate embedding
        with torch.no_grad():
            embedding = self(image_tensor)
            
        return embedding.cpu().numpy()


# Example usage
if __name__ == "__main__":
    import os
    from pathlib import Path
    
    # Initialize the model
    model = VGGish()
    
    # Path to mel spectrogram directory
    mel_dir = os.path.expanduser("~/music-matching/utils/downloads/mel_spectrogram")
    
    # Get the first mel spectrogram image
    mel_files = list(Path(mel_dir).glob("*.png"))
    if mel_files:
        # Get embedding for the first image
        image_path = mel_files[0]
        print(f"Processing: {image_path}")
        
        embedding = model.get_embedding(image_path)
        print(f"Embedding shape: {embedding.shape}")
        print(f"Embedding sample: {embedding[0, :5]}")  # Print first 5 values
    else:
        print("No mel spectrogram images found in the directory.")
