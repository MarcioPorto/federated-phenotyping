import pandas as pd
import syft as sy
import torch
import syfertext
from syft.generic.string import String
from dataset import DatasetProvider


def generate_workers(num_workers):
    """Generate given number of workers and return their list"""
    workers_list = []
    # init workers
    for i in range(n_workers):
        worker = sy.VirtualWorker(hook, id=str(i))
        workers_list.append(worker)
    
    return workers_list

def send_text_data(data_list,worker_list):
    """Takes in text data list and returns a list of list of pointers"""

    main_list = []

    for i,data in enumerate(data_list):
        
        one_list = []
        
        for ind in data.index:
            text = String(data['text'][ind])
            text_ptr = text.send(worker_list[i])
            one_list.append(text_ptr)
        
        main_list.append(one_list)
    
    return main_list

def send_label_data(data_list,worker_list):
    """Takes in label data list and returns a list of list of pointers"""

    main_list = []

    dis_name = [col for col in data_list[0].columns][3:]    # get disease names

    for i,data in enumerate(data_list):
        
        one_list = []
        
        for ind in data.index:
           
            # now convert to one hot vector
            label = torch.ones(16).int() * -1
            
            # generate label
            for k,dis in enumerate(dis_name):
                if data[dis][ind] == 'Y':
                    label[k] = 1
                elif data[dis][ind] == 'N':
                    label[k] = 0
            
            # send the tensor
            label_ptr = label.send(worker_list[i])
            
            one_list.append(label_ptr)
        
        main_list.append(one_list)
    
    return main_list

# add hook
hook = sy.TorchHook(torch)
me = hook.local_worker

# no of workers
n_workers = 3

# generate workers
workers = generate_workers(n_workers)

# instantiate the dataset provider
data_provider = DatasetProvider(train_path='../data/train.csv',test_path='../data/test.csv')

# get the data
train_data = data_provider.provide_data(which='train',splits=n_workers)
test_data = data_provider.provide_data(which='test',splits=n_workers)

# send the train data and get back list of list of pointers
train_text_ptr = send_text_data(train_data,workers)
train_label_ptr = send_label_data(test_data,workers)

# send the test data and get back list of list of pointers 
test_text_ptr = send_text_data(test_data,workers)
test_label_ptr = send_label_data(test_data,workers)
