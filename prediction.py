import torch
from torchdrug import data, datasets
from Data import DataSet,Toxcity,rounder,ajout
from torchdrug import core, models, tasks, utils
smi="C1=CC=CC=C1"
def torchDrug(smi:str):
    dataset = DataSet("./classification/data_wassim_imputed_encoded.csv")
    Toxic = Toxcity("./classification/tox.csv")
    Tox = models.GIN(input_dim=Toxic.node_feature_dim,
                   hidden_dims=[256, 256, 256, 256,256,256],
                   short_cut=True, batch_norm=True, concat_hidden=True)
    taskT = tasks.PropertyPrediction(Tox, task=Toxic.tasks,
                                criterion="bce", metric=("auroc","auprc"))
    optimizerT= torch.optim.Adam(taskT.parameters(), lr=1e-3)
    solverT= core.Engine(taskT, Toxic, Toxic, Toxic, optimizerT,
                     gpus=[0], batch_size=1024)
    solverT.load("./classification/clintox_ginToxcity.pth")
    model = models.GIN(input_dim=dataset.node_feature_dim,
                   hidden_dims=[256, 256, 256, 256,256,256,256],
                   short_cut=True, batch_norm=True, concat_hidden=True)
    task = tasks.PropertyPrediction(model, task=dataset.tasks,
                                criterion="bce", metric=( "auprc"))
    optimizer = torch.optim.Adam(task.parameters(), lr=1e-3)
    solver = core.Engine(task, dataset,dataset, dataset, optimizer,
                     gpus=[0], batch_size=1024)
    solver.load("./classification/clintox_ginMULTI.pth")
    mol = data.Molecule.from_smiles(smi)
    xT=Toxic[:1]
    xT[0]['graph']=mol
    xM=dataset[:1]
    xM[0]['graph']=mol
    batchT= data.graph_collate(xT)
    batchT= utils.cuda(batchT)
    predT= torch.nn.functional.sigmoid(taskT.predict(batchT))
    batchM= data.graph_collate(xM)
    batchM= utils.cuda(batchM)
    predM= torch.nn.functional.sigmoid(task.predict(batchM))
    a0=predT.tolist()
    a1=predM.tolist()
    Toxicity=[]
    for i in a0 :
        if(i[0]>=0.5):
            Toxicity.append(1)
        else:
            Toxicity.append(0)
        
    Multi=rounder(a1)

    Multi=ajout(Multi,Toxicity)
    return Multi[0]

print(type(torchDrug(smi)))
