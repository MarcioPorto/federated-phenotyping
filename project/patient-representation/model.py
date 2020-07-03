import torch
import torch.nn as nn
import numpy as np

class pat_embed(nn.Module):
    def __init__(self, pretrained_embed_path):
        super(pat_embed,self).__init__()
        
        embeddings = np.load(pretrained_embed_path) # 'pretrained_cuis.npy'

        # I attach a padding vector of zeros at the end of embeddings
        embeddings = torch.from_numpy(embeddings).float()
        temp = torch.zeros(1,500).float()
        embeddings = torch.cat((embeddings, temp), dim=0)
        
        self.embeds = nn.Embedding.from_pretrained(embeddings, padding_idx=embeddings.size(0)-1)
        
        self.fc = nn.Sequential(
            nn.Linear(500, 1000),
            nn.ReLU(),
            nn.Linear(1000,200)
        )
        
    def forward(self, x):
        x = self.embeds(x)
        x = torch.mean(x, dim=1)
        x = self.fc(x)
        return x