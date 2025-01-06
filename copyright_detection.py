def compare_songs(model, song1_path, song2_path, threshold=0.8):
    # Convert both songs to mel spectrograms
    mel1 = create_melspectrogram(song1_path)
    mel2 = create_melspectrogram(song2_path)
    
    # Get embeddings
    with torch.no_grad():
        emb1 = model.audio_encoder(mel1)
        emb2 = model.audio_encoder(mel2)
    
    # Calculate similarity
    similarity = torch.cosine_similarity(emb1, emb2)
    
    return similarity.item() > threshold
