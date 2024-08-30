import os
import numpy as np
import pandas as pd
from tqdm import tqdm

tankbind_src_folder_path = "tankbind/"
import sys
sys.path.insert(0, tankbind_src_folder_path)

prot = sys.argv[1]
chain = sys.argv[2]
# For MD
num = sys.argv[3]
random_benchmark=sys.argv[4]
base_pre = f"./examples/HTVS/"
d = pd.read_csv("./examples/HTVS/all_smiles.csv",delimiter=',', encoding='utf-8', error_bad_lines=False)
reduced_df = d[d['Entry Name'].str.contains(random_benchmark+'.*'+prot+'|'+prot+'.*'+random_benchmark, regex=True)]


from torch_geometric.data import Dataset
from feature_utils import get_protein_feature
from Bio.PDB import PDBParser
from feature_utils import get_clean_res_list


parser = PDBParser(QUIET=True)
protein_dict = {}
proteins=[]
# For PDB and AF
proteinName = prot.lower()+chain
proteinFile = f"{base_pre}/structures/AF/{proteinName}.pdb"
s = parser.get_structure(proteinName, proteinFile)
res_list = list(s.get_residues())
clean_res_list = get_clean_res_list(res_list, ensure_ca_exist=True)
protein_dict[proteinName] = get_protein_feature(clean_res_list)

# For MD
#proteinName = prot.lower()+"A-"+prot.lower()+'B_MD'+str(num)+"_"+chain
#proteinFile = f"{base_pre}/structures/MD/{proteinName}.pdb"
#s = parser.get_structure(proteinName, proteinFile)
#res_list = list(s.get_residues())
#clean_res_list = get_clean_res_list(res_list, ensure_ca_exist=True)
#protein_dict[proteinName] = get_protein_feature(clean_res_list)


# To segment the protein using p2rank

ds = f"{base_pre}/protein_list.ds"
with open(ds, "w") as out:
    out.write(f"/structures/AF/{proteinName}.pdb\n")

p2rank = "bash p2rank_2.3/prank"
cmd = f"{p2rank} predict {ds} -o {base_pre}/p2rank -threads 1"
os.system(cmd)



info = []

with open(f"{base_pre}/grids/grid_AF.txt", 'rt') as f:
    lines = f.readlines() 
 
    for line in lines:
        if prot.lower()+chain in line:
            interface_coords = line.split(" ")[1:]
            print(prot+chain,interface_coords)
            break
    

            
for i, line in tqdm(reduced_df.iterrows(), total=reduced_df.shape[0]):
    smiles = line['SMILES']
    compound_name = ""
    protein_name = proteinName
    
    # Interface as protein center (MIRAR SI ES NECESARIO CAMBIAR EL "" POR "," YA QUE SON LAS COMAS QUE SEPARAN LAS COORDENADAS)
    #com = "".join([a for a in interface_coords])
    #info.append([protein_name, compound_name, smiles, "protein_interface", com])
    
    # Center of protein as pocket center
    #com = ",".join([str(a.round(3)) for a in protein_dict[proteinName][0].mean(axis=0).numpy()])
    #info.append([protein_name, compound_name, smiles, "protein_center", com])
    
    # These options are for completely blind docking, where only the pockets identified by p2rank are used for docking.
    p2rankFile = f"{base_pre}/p2rank/{proteinName}.pdb_predictions.csv"
    pocket = pd.read_csv(p2rankFile)
    pocket.columns = pocket.columns.str.strip()
    pocket_coms = pocket[['center_x', 'center_y', 'center_z']].values
    for ith_pocket, com in enumerate(pocket_coms):
        com = ",".join([str(a.round(3)) for a in com])
        info.append([protein_name, compound_name, smiles, f"pocket_{ith_pocket+1}", com])


info = pd.DataFrame(info, columns=['protein_name', 'compound_name', 'SMILES', 'pocket_name', 'pocket_com'])

import torch
from torch_geometric.data import Dataset
from utils import construct_data_from_graph_gvp
import rdkit.Chem as Chem    # conda install rdkit -c rdkit if import failure.
from feature_utils import extract_torchdrug_feature_from_mol, get_canonical_smiles    

torch.set_num_threads(1)

class MyDataset_VS(Dataset):
    def __init__(self, root, data=None, protein_dict=None, proteinMode=0, compoundMode=1,
                pocket_radius=20, shake_nodes=None,
                 transform=None, pre_transform=None, pre_filter=None):
        self.data = data
        self.protein_dict = protein_dict
        super().__init__(root, transform, pre_transform, pre_filter)
        print(self.processed_paths)
        self.data = torch.load(self.processed_paths[0])
        self.protein_dict = torch.load(self.processed_paths[1])
        self.proteinMode = proteinMode
        self.pocket_radius = pocket_radius
        self.compoundMode = compoundMode
        self.shake_nodes = shake_nodes
    @property
    def processed_file_names(self):
        return ['data.pt', 'protein.pt']

    def process(self):
        torch.save(self.data, self.processed_paths[0])
        torch.save(self.protein_dict, self.processed_paths[1])

    def len(self):
        return len(self.data)

    def get(self, idx):

        line = self.data.iloc[idx]
        smiles = line['SMILES']
        pocket_com = line['pocket_com']
        pocket_com = np.array(pocket_com.split(",")).astype(float) if type(pocket_com) == str else pocket_com
        pocket_com = pocket_com.reshape((1, 3))
        use_whole_protein = line['use_whole_protein'] if "use_whole_protein" in line.index else False

        protein_name = line['protein_name']
        protein_node_xyz, protein_seq, protein_node_s, protein_node_v, protein_edge_index, protein_edge_s, protein_edge_v = self.protein_dict[protein_name]

        try:
            smiles = get_canonical_smiles(smiles)
            mol = Chem.MolFromSmiles(smiles)
            mol.Compute2DCoords()
            coords, compound_node_features, input_atom_edge_list, input_atom_edge_attr_list, pair_dis_distribution = extract_torchdrug_feature_from_mol(mol, has_LAS_mask=True)
        except:
            print("something wrong with ", smiles, "to prevent this stops our screening, we repalce it with a placeholder smiles 'CCC'")
            smiles = 'CCC'
            mol = Chem.MolFromSmiles(smiles)
            mol.Compute2DCoords()
            coords, compound_node_features, input_atom_edge_list, input_atom_edge_attr_list, pair_dis_distribution = extract_torchdrug_feature_from_mol(mol, has_LAS_mask=True)
        # y is distance map, instead of contact map.
        data, input_node_list, keepNode = construct_data_from_graph_gvp(protein_node_xyz, protein_seq, protein_node_s, 
                              protein_node_v, protein_edge_index, protein_edge_s, protein_edge_v,
                              coords, compound_node_features, input_atom_edge_list, input_atom_edge_attr_list,
                              pocket_radius=self.pocket_radius, use_whole_protein=use_whole_protein, includeDisMap=True,
                              use_compound_com_as_pocket=False, chosen_pocket_com=pocket_com, compoundMode=self.compoundMode)
        data.compound_pair = pair_dis_distribution.reshape(-1, 16)

        return data
        
dataset_path = f"{base_pre}/dataset/"
os.system(f"rm -r {dataset_path}")
os.system(f"mkdir -p {dataset_path}")
dataset = MyDataset_VS(dataset_path, data=info, protein_dict=protein_dict)

import logging
from torch_geometric.loader import DataLoader
from tqdm import tqdm    # pip install tqdm if fails.
from model import get_model

batch_size = 5
device = 'cuda' if torch.cuda.is_available() else 'cpu'
# device= 'cpu'
logging.basicConfig(level=logging.INFO)
model = get_model(0, logging, device)
# modelFile = "../saved_models/re_dock.pt"
# self-dock model
modelFile = "saved_models/self_dock.pt"

model.load_state_dict(torch.load(modelFile, map_location=device))
_ = model.eval()

data_loader = DataLoader(dataset, batch_size=batch_size, follow_batch=['x', 'y', 'compound_pair'], shuffle=False, num_workers=8)
affinity_pred_list = []
y_pred_list = []

for data in tqdm(data_loader):
   
    data = data.to(device)
    y_pred, affinity_pred = model(data)
    affinity_pred_list.append(affinity_pred.detach().cpu())
   

affinity_pred_list = torch.cat(affinity_pred_list)
info = dataset.data
info['affinity'] = affinity_pred_list
info.to_csv(f"{base_pre}/outputs/AF/{proteinName}_"+random_benchmark+"_tankbind.csv")





