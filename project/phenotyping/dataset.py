import pandas as pd

class DatasetProvider:
    
    def __init__(self,train_path,test_path):
        
        self.train_path = train_path
        self.test_path = test_path

        self.data_train = pd.read_csv(train_path)
        self.data_test = pd.read_csv(test_path)

    def split_data(self,data_stream,num_parts):
        """Divides the data into given number of parts"""
        
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

    def provide_data(self,dataset = 'train',splits = 3):

        if(dataset == 'train'):
            return self.split_data(self.data_train,splits)
        elif(dataset == 'test'):
            return self.split_data(self.data_test,splits)