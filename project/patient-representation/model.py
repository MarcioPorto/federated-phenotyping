import torch
import torch.nn as nn


#TODO: Need To Check The Shapes Of Layers.
class Model(nn.Module):
    """Model definition"""

    #TODO: Add Support to read parameters from configuration file.
    def __init__(self,num_of_features,output_dim,hidden,classes):

        super(Model,self).__init__()
        self.encoder = nn.Embedding(num_of_features,output_dim)
        #TODO: Need to add dimension of number of channels/steps.
        self.avg = nn.AvgPool1d()
        self.l1 == nn.Linear(hidden)
        self.l2 = nn.Linear(classes)
    
    def forward(self,x):
        x = self.encoder(x)
        x = self.avg(x)
        x = self.l1(x)
        x = nn.ReLU(x)
        x = self.l2(x)
        x = nn.Sigmoid(x)
        return x