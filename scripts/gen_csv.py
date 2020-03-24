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


dic = {} 

# read the first training data
tree = ElementTree.parse('./text1.xml')
root = tree.getroot()
docs  = root.findall('docs')[0]
for doc in docs:
    text_data = doc.findall('text')[0].text  # extract texxt data
    pat = Patient() # create pateint
    pat.text = text_data
    pat.id = int(doc.attrib['id'])
    dic[pat.id] = pat

# read the second training data
tree = ElementTree.parse('./text2.xml')
root = tree.getroot()
docs  = root.findall('docs')[0]
for doc in docs:
    text_data = doc.findall('text')[0].text  # extract texxt data
    pat = Patient() # create pateint
    pat.text = text_data
    pat.id = int(doc.attrib['id'])
    dic[pat.id] = pat

# read the annotations 1
tree = ElementTree.parse('./label1.xml')
root = tree.getroot()
diseases  = root.findall('diseases')[0]
for disease in diseases:
    dis_name = disease.attrib['name'].split(' ')[0]
    print(dis_name)
    for doc in disease:
        id_ = int(doc.attrib['id'])
        setattr(dic[id_] , dis_name, doc.attrib['judgment'])

# read the annotations 2
tree = ElementTree.parse('./label2.xml')
root = tree.getroot()
diseases  = root.findall('diseases')[0]
for disease in diseases:
    dis_name = disease.attrib['name'].split(' ')[0]
    for doc in disease:
        id_ = int(doc.attrib['id'])
        setattr(dic[id_] , dis_name, doc.attrib['judgment'])

# read the annotations 3
tree = ElementTree.parse('./label3.xml')
root = tree.getroot()
diseases  = root.findall('diseases')[0]
for disease in diseases:
    dis_name = disease.attrib['name'].split(' ')[0]
    for doc in disease:
        id_ = int(doc.attrib['id'])
        setattr(dic[id_] , dis_name, doc.attrib['judgment'])


d_train = {
    'id' : [],
    'text' : [],
    'Asthma': [],
    'CAD': [],
    'CHF': [],
    'Depression': [],
    'Diabetes': [],
    'Gallstones': [],
    'GERD': [],
    'Gout': [],
    'Hypercholesterolemia': [],
    'Hypertension': [],
    'Hypertriglyceridemia': [],
    'OA': [],
    'Obesity': [],
    'OSA': [],
    'PVD': [],
    'Venous' : [],
}

for pat in dic.values():
    d_train['id'].append(pat.id)
    d_train['text'].append(pat.text)
    d_train['Asthma'].append(pat.Asthma)
    d_train['CAD'].append(pat.CAD)
    d_train['CHF'].append(pat.CHF)
    d_train['Depression'].append(pat.Depression)
    d_train['Diabetes'].append(pat.Diabetes)
    d_train['Gallstones'].append(pat.Gallstones)
    d_train['GERD'].append(pat.GERD)
    d_train['Gout'].append(pat.Gout)
    d_train['Hypercholesterolemia'].append(pat.Hypercholesterolemia)
    d_train['Hypertension'].append(pat.Hypertension)
    d_train['Hypertriglyceridemia'].append(pat.Hypertriglyceridemia)
    d_train['OA'].append(pat.OA)
    d_train['Obesity'].append(pat.Obesity)
    d_train['OSA'].append(pat.OSA)
    d_train['PVD'].append(pat.PVD)
    d_train['Venous'].append(pat.Venous)

data_train = pd.DataFrame(d_train)

data_train.to_csv('train.csv', sep=',') # spit the data to a csv

dic_t = {}

# read the first test data
tree = ElementTree.parse('./test_text.xml')
root = tree.getroot()
docs  = root.findall('docs')[0]
for doc in docs:
    text_data = doc.findall('text')[0].text  # extract texxt data
    pat = Patient() # create pateint
    pat.text = text_data
    pat.id = int(doc.attrib['id'])
    dic_t[pat.id] = pat

# read the test annotations
tree = ElementTree.parse('./test_label.xml')
root = tree.getroot()
diseases  = root.findall('diseases')[0]
for disease in diseases:
    dis_name = disease.attrib['name'].split(' ')[0]
    print(dis_name)
    for doc in disease:
        id_ = int(doc.attrib['id'])
        setattr(dic_t[id_] , dis_name, doc.attrib['judgment'])

d_test = {
    'id' : [],
    'text' : [],
    'Asthma': [],
    'CAD': [],
    'CHF': [],
    'Depression': [],
    'Diabetes': [],
    'Gallstones': [],
    'GERD': [],
    'Gout': [],
    'Hypercholesterolemia': [],
    'Hypertension': [],
    'Hypertriglyceridemia': [],
    'OA': [],
    'Obesity': [],
    'OSA': [],
    'PVD': [],
    'Venous' : [],
}

for pat in dic_t.values():
    d_test['id'].append(pat.id)
    d_test['text'].append(pat.text)
    d_test['Asthma'].append(pat.Asthma)
    d_test['CAD'].append(pat.CAD)
    d_test['CHF'].append(pat.CHF)
    d_test['Depression'].append(pat.Depression)
    d_test['Diabetes'].append(pat.Diabetes)
    d_test['Gallstones'].append(pat.Gallstones)
    d_test['GERD'].append(pat.GERD)
    d_test['Gout'].append(pat.Gout)
    d_test['Hypercholesterolemia'].append(pat.Hypercholesterolemia)
    d_test['Hypertension'].append(pat.Hypertension)
    d_test['Hypertriglyceridemia'].append(pat.Hypertriglyceridemia)
    d_test['OA'].append(pat.OA)
    d_test['Obesity'].append(pat.Obesity)
    d_test['OSA'].append(pat.OSA)
    d_test['PVD'].append(pat.PVD)
    d_test['Venous'].append(pat.Venous)

data_test = pd.DataFrame(d_test) 

data_test.to_csv('test.csv', sep=',') # spit the test data to the csv