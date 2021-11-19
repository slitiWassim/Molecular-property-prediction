import torch
from torchdrug import data, datasets

import os

from torchdrug import data, utils
from torchdrug.core import Registry as R
from torchdrug.utils import doc





from torchdrug import data, datasets

import os

from torchdrug import data, utils
from torchdrug.core import Registry as R
from torchdrug.utils import doc



@doc.copy_args(data.MoleculeDataset.load_csv, ignore=("smiles_field", "target_fields"))
class DataSet(data.MoleculeDataset):
    """
    Qualitative data of drugs approved by the FDA and those that have failed clinical
    trials for toxicity reasons.

    Statistics:
        - #Molecule: 1,478
        - #Classification task: 2

    Parameters:
        path (str): path to store the dataset
        verbose (int, optional): output verbose level
        **kwargs
    """

    
    target_fields = ["Activity_IC50","Activity_EC50","Activity_EC90"]

    def __init__(self, path, verbose=1, **kwargs):
        path = os.path.expanduser(path)
        if not os.path.exists(path):
            os.makedirs(path)
        self.path = path

        #zip_file = utils.download(self.url, path, md5=self.md5)
        csv_file = path

        self.load_csv(csv_file, smiles_field="smiles", target_fields=self.target_fields,
                      verbose=verbose, **kwargs)
                           
                      
                      
@doc.copy_args(data.MoleculeDataset.load_csv, ignore=("smiles_field", "target_fields"))
class Toxcity(data.MoleculeDataset):
    """
    Qualitative data of drugs approved by the FDA and those that have failed clinical
    trials for toxicity reasons.

    Statistics:
        - #Molecule: 1,478
        - #Classification task: 2

    Parameters:
        path (str): path to store the dataset
        verbose (int, optional): output verbose level
        **kwargs
    """

    
    target_fields = ["Toxicity"]

    def __init__(self, path, verbose=1, **kwargs):
        path = os.path.expanduser(path)
        if not os.path.exists(path):
            os.makedirs(path)
        self.path = path

        #zip_file = utils.download(self.url, path, md5=self.md5)
        csv_file = path

        self.load_csv(csv_file, smiles_field="smiles", target_fields=self.target_fields,
                      verbose=verbose, **kwargs)
                      


                      
def ensemble_torchDrug(a0,a1,a2,a3:list):
    final_result=[]
    for i in range(len(a0)):
        insert=[]
        result_0=a0[i]
        result_1=a1[i]
        result_2=a2[i]
        result_3=a3[i]
        insert.append(comp(result_0[0],result_1[0],result_2[0]))
        insert.append(comp(result_0[1],result_1[1],result_3[0]))
        insert.append(comp(result_0[2],result_2[1],result_3[1]))
        final_result.append(insert)
        
    return  final_result
    
def ajout(a,b:list):
    for i in range(len(b)):
        a[i].append(b[i])
    return a          
    
def rounder(a:list):
    result=[]
    for i in a :
        res=[]
        for j in range(len(i)):
            if(i[j]>=0.5):
                res.append(1)
            else:
                res.append(0)
        result.append(res)
    return result    
          
def comp(val1,val2,val3:int):
    if(val1==val2):
        return val1
    else:
        if(val1==val3):
            return val1
        else:
            return val3                                                                                               
