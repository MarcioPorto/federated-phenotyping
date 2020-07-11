# Patient Representation using SyferText

In order to use the **QuickUMLS** pipeline, we need two database files, one is a dictionary of terms and the other is a pickled file cotaining CUIs of each term. You can download both files here and extract them. 

Now while creating the `QuickUMLS` object, mention the location of the two files in the `__init__` method to load them.

Below is an example how to use the pipeline.

```python
import syft as sy  
import torch  
import syfertext

hook = sy.TorchHook(torch) 
me = hook.local_worker

nlp = syfertext.load('en_core_web_lg', owner = me)

from syfertext.pipeline.medical import QuickUMLS  

quick_umls = QuickUMLS(
	quick_umls_database='./database_umls_lower/umls-terms.simstring', # location to the dictionary of terms file
    knowledge_base='./string_to_cui_lower.pt', # location to pickled file
    threshold=0.75,  # threshold above which a term will be considered a match
    overlapping_criteria='score' # There are two options here, 'score' : gives priority to the similarity, 'length' : gives priority to the length of the match
    )

# Then add it to pipeline
nlp.add_pipe(quick_umls,name = 'quicky',last=True)

text = """Spinal and bulbar muscular atrophy (SBMA) is an inherited motor neuron disease caused by the expansion of a polyglutamine tract within the androgen receptor (AR). SBMA can be caused by this easily."""

doc = nlp(text)

# print the detected the entities
for ent in doc.ents:
	print(ent.start, ent.end, ent.text, ent._.cuis[0]) 

# ent._.cuis is actually a list containing all CUIs for a term, I just print the first one here
```

So we take all the notes and extract CUIs out of them and then dumped them to a file.
I am not sharing the link to the dumped CUIs here.

Then we need couple of more files whose link is here.

In `train.py` file, we look at the following train data loader, we provide the respective paths to the files. Same is done for val_data loader as well.
```python
train_data = Patient('../patient-representation/train_pat.txt', # only this is different in train and val data loaders, rest is same.
'../patient-representation/cui2idx.pt',
'../patient-representation/label2idx.pt',
'../patient-representation/valid_cuis.txt',
'../patient-representation/cuis/', # Folder where extracted patient cuis are
'../patient-representation/labels/') # Folder where patient labels are
```

Also when creating the model, we need the pretrained embeddings, so we provide the path for those as well.
```python
model  =  pat_embed('../patient-representation/pretrained_cuis.npy')
```
Now we are ready to begin training. To start, navigate to `project/patient-representation/` and do `python train.py`. Make sure to change `path` variable in `train.py` accordingly. To change hyper-parameters, look at `config.py`.
