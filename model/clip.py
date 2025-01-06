import torch
import torch.nn as nn

class MusicCLIP(nn.Module):
    def __init__(self, audio_encoder, text_encoder, projection_dim):
        super().__init__()
        self.audio_encoder = audio_encoder
        self.text_encoder = text_encoder
        
        # Projection layers
        self.audio_projection = nn.Linear(audio_encoder.output_dim, projection_dim)
        self.text_projection = nn.Linear(text_encoder.output_dim, projection_dim)
        
    def forward(self, audio, text):
        # Get embeddings
        audio_features = self.audio_encoder(audio)
        text_features = self.text_encoder(text)
        
        # Project to same dimension
        audio_features = self.audio_projection(audio_features)
        text_features = self.text_projection(text_features)
        
        # Normalize
        audio_features = audio_features / audio_features.norm(dim=-1, keepdim=True)
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)
        
        return audio_features, text_features

def train_step(model, audio_batch, text_batch, optimizer, temperature=1.0):
    # Get embeddings
    audio_features, text_features = model(audio_batch, text_batch)
    
    # Calculate similarity matrix
    logits = (audio_features @ text_features.t()) * temperature
    
    # Contrastive loss
    labels = torch.arange(len(audio_batch)).to(audio_features.device)
    loss_i = nn.CrossEntropyLoss()(logits, labels)
    loss_t = nn.CrossEntropyLoss()(logits.t(), labels)
    loss = (loss_i + loss_t) / 2
    
    # Backward pass
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    return loss.item()
