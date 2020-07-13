from csv import DictReader
from collections import defaultdict
from pre_process import preprocess_note
from tqdm import tqdm
import pandas as pd 
import os
from shutil import copy2

# notes_path = "/Users/saksham/Desktop/os/federated-phenotyping/project/patient-representation/NOTEEVENTS.csv"

# df = pd.read_csv("",low_memory=False)
# print(df.head())
""" 
 ROW_ID  SUBJECT_ID   HADM_ID   CHARTDATE  ... DESCRIPTION CGID ISERROR TEXT
"""

# d = defaultdict(str)

# with open(notes_path, 'r') as read_obj:
#     csv_dict_reader = DictReader(read_obj)
#     for row in csv_dict_reader:
#         if (row['CATEGORY'] == 'Discharge summary') :
#             d[row['SUBJECT_ID']] += row['TEXT']

# for key in tqdm(d):
#     text = preprocess_note(d[key])
#     file_path = "/Users/saksham/Desktop/os/federated-phenotyping/project/patient-representation/notes/" + key + ".txt"
#     f = open(file_path, "a")
#     f.write(text)
#     f.close() 


admission_path = "/Users/saksham/Desktop/os/federated-phenotyping/project/patient-representation/ADMISSIONS.csv"

with open(admission_path, 'r') as read_obj:
    csv_dict_reader = DictReader(read_obj)
    for row in csv_dict_reader:
        s = row['ADMISSION_TYPE']
        d = row['DIAGNOSIS']
        id = row['SUBJECT_ID']
        if (s != "NEWBORN" and len(d) > 0):
            file_path = "/Users/saksham/Desktop/os/federated-phenotyping/project/patient-representation/notes/" + id + ".txt"
            if (os.path.exists(file_path)):
                copy2(file_path,'./final')




