import pandas as pd
import syft as sy
import torch
import syfertext
from syft.generic.string import String
from .dataset import DatasetProvider
from .util import send_text_data,send_label_data,generate_workers

# add hook
hook = sy.TorchHook(torch)
me = hook.local_worker

# no of workers
n_workers = 3

# generate workers
workers = generate_workers(n_workers)

# instantiate the dataset provider
data_provider = DatasetProvider(train_path='./data/train.csv',test_path='./data/test.csv')

# get the data
train_data = data_provider.provide_data(dataset='train',splits=n_workers)
test_data = data_provider.provide_data(dataset='test',splits=n_workers)

# send the train data and get back list of (list of pointers)
train_text_worker_ptrs = send_text_data(train_data,workers)
train_label_worker_ptrs = send_label_data(test_data,workers)

# send the test data and get back list of (list of pointers)
test_text_worker_ptrs = send_text_data(test_data,workers)
test_label_worker_ptrs = send_label_data(test_data,workers)
