# this file contains some utility functions

def generate_workers(num_workers):
    """Generates a given number of PySyft's virtual workers"""
    
    workers_list = []
    # init workers
    for i in range(n_workers):
        worker = sy.VirtualWorker(hook, id=str(i))
        workers_list.append(worker)
    
    return workers_list

def send_text_data(data_list,worker_list):
    """Takes in data and returns a 2D list of pointers to the data at remote location
    For eg. `data_list = [["hello","there"],["whats","up"]]`, `worker_list = ['alice','bob']` then it will return
    `main_list = [ [StringPointer("hello"),StringPointer("there")], [StringPointer("whats"),StringPointer("up")] ]` where the first list of pointers
    point to data stored in `alice` and second to `bob`.

    Args:
        data_list : A 2D list of PySyft String
        worker_list : list of virtual workers

    Returns:
        A 2D list of pointers to Objects stored at virtual workers
    """

    assert len(data_list) == len(worker_list) , "The splits of data you are trying to send is not equal to the no. of workers"

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
    """Takes in label data and returns a 2D list of pointers to the label data at remote location
    For eg. `data_list = [[tensor(1.),tensor(2.)],[tensor(3.),tensor(4.)]]`, `worker_list = ['alice','bob']` then it will return
    `main_list = [ [TensorPointer(1.),TensorPointer(2.)], [TensorPointer(3.),TensorPointer(4.)] ]` where the first list of pointers
    point to label data stored in `alice` and second to `bob`.

    Args:
        data_list : A 2D list of torch tensors
        worker_list : list of virtual workers

    Returns:
        A 2D list of pointers to Objects stored at virtual workers
    """

    assert len(data_list) == len(worker_list) , "The splits of data you are trying to send is not equal to the no. of workers"

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