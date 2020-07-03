# File for debugging purposes

import torch
from dataset import Patient
from model import pat_embed

from torch.utils import data

model = pat_embed('~/Desktop/patient-representation/pretrained_cuis.npy')
model.cuda()

print(model)

train_data = Patient('~/Desktop/patient-representation/train.txt', 
                    '~/Desktop/patient-representation/cui2idx.pt', 
                    '~/Desktop/patient-representation/valid_cuis.txt',
                    '~/Desktop/patient-representation/cuis/') # Folder where extracted patient cuis are

train_loader = data.DataLoader(train_data, batch_size=50, num_workers=6, shuffle=True)

for patients_cuis in train_loader:
    print(patients_cuis.shape)

    patients_cuis = patients_cuis.cuda()

    out = model(patients_cuis)

    print(out.shape)

    break