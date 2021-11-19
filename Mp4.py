import os
from rdkit import Chem
import tmap as tm
from map4 import MAP4Calculator
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem.Draw import SimilarityMaps
from IPython.display import SVG
import io
from PIL import Image
import numpy as np
import pandas as pd

import rdkit
dim = 1024
MAP4 = MAP4Calculator(dimensions=dim)
ENC = tm.Minhash(dim)
data = pd.read_csv("smiles.csv")
df= pd.read_csv('./smiles.csv')
#Importing Chem module
from rdkit import Chem 

#Method transforms smiles strings to mol rdkit object
df['mol'] = df['smiles'].apply(lambda x: Chem.MolFromSmiles(x)) 
def MP4(smiles_a:str):
    mol_a = Chem.MolFromSmiles(smiles_a)
    map4_a = MAP4.calculate(mol_a)
    listM=[]
    listMP4=[]
    for ch in data['smiles']:
        smiles_b = ch
        mol_b = Chem.MolFromSmiles(smiles_b)
        map4_b = MAP4.calculate(mol_b)
        listMP4.append(ENC.get_distance(map4_a, map4_b))
        listM.append(smiles_b)
    return  listMP4
def show_png(data):
    bio = io.BytesIO(data)
    img = Image.open(bio)
    return img
def finger(a,b):
    d = Draw.MolDraw2DCairo(400, 400)
    _, maxWeight = SimilarityMaps.GetSimilarityMapForFingerprint(b,df.mol[a],
                                        lambda m, i: SimilarityMaps.GetMorganFingerprint(m, i, radius=2, fpType='bv'), 
                                        draw2d=d)
    d.FinishDrawing()
    return show_png(d.GetDrawingText())

def pred_Map4(smiles_a):
    m=Chem.MolFromSmiles(smiles_a)
    source_folder = os.path.join(os.getcwd(), "static/detections")
    to_save_folder = os.path.join(source_folder,str(MP4(smiles_a)[0])+str(MP4(smiles_a)[1])+str(MP4(smiles_a)[2])+str(MP4(smiles_a)[3]))
    if not os.path.exists(to_save_folder):
        os.mkdir(to_save_folder)
    for i in range(len(df['mol'])):
        load=source_folder+"/"+"result"+"_"+str(i)+".jpg"
        finger(i,m).save(load)
    return MP4(smiles_a)
    
#print(pred_Map4('CC(C)OC(=O)C(C)NP(=O)(OCC1C(C(C(O1)N2C=CC(=O)NC2=O)(C)F)O)OC3=CC=CC=C3'))  
dl=[]
df1=pd.read_csv('test.csv')
smile = df1["smiles"][0] 
dl.append(pred_Map4(smile))
rs=pd.DataFrame(dl,columns=["1","2","3","4","5","6"])
rs[["1","2","3","4","5","6"]].to_csv("result.csv", index=False)
   
