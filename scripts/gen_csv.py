import os
from xml.etree import ElementTree
import pandas as pd

class Patient:
    def __init__(self):
        
        self.text = None
        self.id = 0
        
        self.Asthma = None
        self.CAD = None
        self.CHF = None
        self.Depression = None
        self.Diabetes = None
        self.Gallstones = None
        self.GERD = None
        self.Gout = None
        self.Hypercholesterolemia = None
        self.Hypertension = None
        self.Hypertriglyceridemia = None
        self.OA = None
        self.Obesity = None
        self.OSA = None
        self.PVD = None
        self.Venous = None
    
    def get_attr(self):
        return {
            'text'          : self.text,
            'id'            : self.id,
            'Asthma'        : self.Asthma,
            'CAD'           : self.CAD,
            'CHF'           : self.CHF,
            'Depression'    : self.Depression,
            'Diabetes'      : self.Diabetes,
            'Gallstones'    : self.Gallstones,
            'GERD'          : self.GERD,
            'Gout'          : self.Gout,
            'Hypercholesterolemia': self.Hypercholesterolemia,
            'Hypertension'  : self.Hypertension,
            'Hypertriglyceridemia': self.Hypertriglyceridemia,
            'OA'            : self.OA,
            'Obesity'       : self.Obesity,
            'OSA'           : self.OSA,
            'PVD'           : self.PVD,
            'Venous'        : self.Venous,
        }

# check if data folder exists or not
if not os.path.isdir('../data'):
    os.mkdir('../data')

assert os.path.isdir('../downloads') , "no downloads folder found"
    

dic = {}

train_files = ['obesity_patient_records_training.xml','obesity_patient_records_training2.xml']

for file in train_files:
    # read the training data
    tree = ElementTree.parse('../downloads/' + file)
    root = tree.getroot()
    docs  = root.findall('docs')[0]
    for doc in docs:
        
        # extract text data
        text_data = doc.findall('text')[0].text  

        # create patient
        pat = Patient()

        pat.text = text_data
        pat.id = int(doc.attrib['id'])

        # store in dic
        dic[pat.id] = pat

train_labels = ['obesity_standoff_intuitive_annotations_training.xml',
                'obesity_standoff_annotations_training_addendum3.xml',
                'obesity_standoff_annotations_training_addendum.xml']

for file in train_labels:
    # read the annotations
    tree = ElementTree.parse('../downloads/' + file)
    root = tree.getroot()
    diseases  = root.findall('diseases')[0]
    for disease in diseases:
        dis_name = disease.attrib['name'].split(' ')[0]
        print(dis_name)
        for doc in disease:
            id_ = int(doc.attrib['id'])
            setattr(dic[id_] , dis_name, doc.attrib['judgment'])

data_train = pd.DataFrame([pat.get_attr() for pat in dic.values()])

data_train.to_csv('../data/train.csv', sep=',') # spit the data to a csv

dic_t = {}

# read the test data
tree = ElementTree.parse('../downloads/obesity_patient_records_test.xml')
root = tree.getroot()
docs  = root.findall('docs')[0]
for doc in docs:
    
    # extract text data
    text_data = doc.findall('text')[0].text
    
    # create pateint
    pat = Patient()

    pat.text = text_data
    pat.id = int(doc.attrib['id'])

    # store in dic
    dic_t[pat.id] = pat

# read the test annotations
tree = ElementTree.parse('../downloads/obesity_standoff_annotations_test_intuitive.xml')
root = tree.getroot()
diseases  = root.findall('diseases')[0]
for disease in diseases:
    dis_name = disease.attrib['name'].split(' ')[0]
    print(dis_name)
    for doc in disease:
        id_ = int(doc.attrib['id'])
        setattr(dic_t[id_] , dis_name, doc.attrib['judgment'])

data_test = pd.DataFrame([pat.get_attr() for pat in dic_t.values()])

data_test.to_csv('../data/test.csv', sep=',') # spit the test data to the csv