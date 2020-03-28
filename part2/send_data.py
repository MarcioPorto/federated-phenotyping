import pandas as pd
import syft as sy
import torch
import syfertext
from syft.generic.string import String


def generate_workers(num_workers):
    workers_list = []
    # init workers
    for i in range(n_workers):
        worker = sy.VirtualWorker(hook, id=str(i))
        workers_list.append(worker)
    
    return workers_list

def split_data(data_stream,num_parts):
    
    list_data = []
    
    start = 0
    part = len(data_stream) // num_parts 

    for i in range(num_parts):
        if(i == num_parts - 1):
            list_data.append(data_stream[start:])
        else:
            list_data.append(data_stream[start:start + part])
            start += part

    return list_data

def send_text_data(data_list,worker_list):
    """Takes in data list and return a list of list of pointers"""

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
    """Takes in data list and return a list of list of pointers"""

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


hook = sy.TorchHook(torch)
me = hook.local_worker

# no of workers
n_workers = 3

# generate workers
workers = generate_workers(n_workers)

# send the train data
data_train = pd.read_csv('../data/train.csv')
    
data_splits = split_data(data_train,n_workers)

train_text_ptr = send_text_data(data_splits,workers)

train_label_ptr = send_label_data(data_splits,workers)

# send the test data
data_test = pd.read_csv('../data/test.csv')

data_splits_t = split_data(data_test,n_workers)

test_text_ptr = send_text_data(data_splits_t,workers)

test_label_ptr = send_label_data(data_splits_t,workers)