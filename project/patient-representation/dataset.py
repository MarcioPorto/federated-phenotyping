import torch
import numpy as np
import pickle


class Patient():
    def __init__(self, train_text_path, cui2idx_path, valid_cuis_path, cuis_path):
        f = open(train_text_path) # train.txt
        self.patients = None
        for line in f:
            self.patients = line.split(' ')
        f.close()
        
        f = open(valid_cuis_path) # valid_cuis.txt
        self.valid_cuis = None
        for line in f:
            self.valid_cuis = set(line.split(' '))
        f.close()
        
        self.cui2idx = pickle.load(open(cui2idx_path,'rb')) # cui2idx.pt

        self.cuis_path = cuis_path
        
    def __getitem__(self, index):
        pat = self.patients[index]
        
        f = open(self.cuis_path + pat) # './cuis/'
        cuis = None
        for line in f:
            cuis = line.split(' ')
        f.close()
        
        cuis_final = []
        
        for cui in cuis:
            if cui in self.valid_cuis:
                cuis_final.append(cui)
        
        idx_list = []
        
        for cui in cuis_final:
            if cui in self.cui2idx:
                idx_list.append(self.cui2idx[cui])
        
        padding_idx = 109053 # this is the index where embeddings are all zero
        
        while(len(idx_list) < 4726): # this is the max valid CUIs for a single patient
            idx_list.append(padding_idx)
        
        return torch.tensor(idx_list, dtype = torch.long)
    
    def __len__(self):
        return len(self.patients)