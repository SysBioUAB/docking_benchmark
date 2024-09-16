# Scripts

Here you can find the scripts and protocols used for docking, protein analysis, molecular dynamics (MD) simulations, and AlphaFlow predictions. All input files required to run the analysis and the resulting outputs can be downloaded from [Zenodo](https://zenodo.org/records/13757872).

## Docking

### Vina

To run AutoDock Vina 1.2.5, use the `run_vina.sh` script. The input files required include:
- Protein and ligand files in PDBQT format
- Source or method used to obtain the protein structure (PDB, AF, MD, or AFlow)
- Path to the Vina pre-built binary
- Path to an input file with simulation box coordinates and sizes (`data/input_files/interface_center.txt`)

Example:
```bash
bash run_vina.sh -p data/input_files/Protein_structures/Vina/PDB/ -m PDB -o data/output_files/docking/outputs_vina/ -c data/input_files/interface_center.txt -v tools/vina_1.2.5_linux -l data/input_files/Ligands/ligands_vina
```

### Gnina
To run Gnina 1.0, use the run_gnina.sh script. The input files are similar to AutoDock Vina but can use PDB for proteins and SDF for ligands. 

Example:
```bash
bash run_gnina.sh -p data/input_files/Protein_structures/Gnina_tankbind_diffdock/PDB/ -m PDB -o data/output_files/docking/gnina/ [-c] data/input_files/interface_center.txt -v tools/gnina -l data/input_files/Ligands/ligands/ligands_benchmark_1E50.sdf
```

### EquiBind
Use the multiligand_inference.py script from the EquiBind repository to infer multiple ligands from a single SDF file and a single receptor.

Example:
```python
python multiligand_inference.py -o data/output_files/docking/equibind/ -r data/input_files/Protein_structures/Gnina_tankbind_diffdock/PDB/1e50A.pdb -l data/input_files/Ligands/ligands/ligands_benchmark_1E50.sdf
```

### DiffDock
Follow the protocol in the [DiffDock README](https://github.com/gcorso/DiffDock) for inference with default search space options. 

### TankBind
Refer to the prediction_example_using_PDB_6hd6.ipynb notebook in their [repository](https://github.com/luwei0917/TankBind) to predict poses using TankBind in two modes:

-TankBind_local: Protein interface as a binding pocket using interface coordinates.
-TankBind_blind: Only binding pockets predicted by p2rank.

### Glide and Glide-IFD
Use the run_glide.sh script in the glide_scripts folder to carry out protein-ligand docking with Glide and Glide-IFD. The script prepares input files and returns results in a CSV file.

### Output Extraction
For Vina, Gnina, and DiffDock, use the retrieve_*_score.sh scripts to extract scores/affinities/energies. Glide's results are prepared by the run_glide.sh script, and TankBind provides a CSV file with affinities.

For ROC curve plotting and auROC values, use roc.py. Output CSV files containing pose energies and auROC values are located in data/output_files/roc, separated by protein source and chain. 

## Figures

Scripts to reproduce the figures in the paper are available in the figures directory. The datasets used are in data/input_files/figure_datasets/.

## Protein analysis

Scripts for computing quality and similarity metrics:

-TM-score: Computed using MMalign.
-DockQ and iRMS: Computed using DockQ.py and pDockQ2.py.
-ipTM+pTM score from AlphaFold outputs: Use retrieve_AF_ptm.sh.
-Protein interface coordinates and simulation box sizes: interface_center.py.
-Intrinsically disordered regions in AFfull complexes: percentage_IDR.py.

## MD

The autogmx_proteinwater.sh script automates MD simulations using GROMACS. Forcefield and parameter files are in data/input_files/forcefields_and_parameters/. Other scripts analyze simulation trajectories and generate figures for the paper, including RMSF, RMSD, free energy landscapes, potential energy, and radius of gyration.

## AlphaFlow
Generate input files by following the "preparing input files" steps in their [repository](https://github.com/bjing2016/alphaflow). Input files are located in data/input_files/alphaflow/, and outputs are in data/output_files/alphaflow/.

To run the model:

```python
python predict.py --mode alphafold --input_csv data/input_files/alphaflow/benchmark.csv --msa_dir data/input_files/alphaflow/MSA/ --weights alphaflow_md_base_202402.pt --samples 250 --outpdb data/output_files/alphaflow/outputs
```
Split all the 250 ensembles for each protein:
```bash
for protein in data/output_files/alphaflow/outputs/*.pdb; do mkdir data/output_files/alphaflow/ensembles/$(basename $protein .pdb); csplit -z $protein '/^MODEL/' '{*}'; for file in data/output_files/alphaflow/ensembles/xx*; do mv "$file" data/output_files/alphaflow/ensembles/$(basename $protein .pdb)/"${file}.pdb"; done ; done
```
Generate files with the list of ensembles (used by maxcluster):
```bash
for ensemble in data/output_files/alphaflow/ensembles/*; do for protein in $ensemble/*; do echo $protein >> data/output_files/alphaflow/maxcluster_input/$(basename $ensemble .pdb).list; done ; done
```
Run maxcluster to make all-versus-all RMSD matrix and near neighbour clustering:
```bash
for protein in data/output_files/alphaflow/maxcluster_input/; do ./maxcluster64bit -l $(basename $protein).list -rmsd -C 5 >> data/output_files/alphaflow/maxcluster_output/$(basename $protein)_clusters.out; done
```
Select top 10 most representative clusters:
```bash
for clusters in data/output_files/alphaflow/maxcluster_output/*.out; do for i in $(cat $clusters | grep INFO | grep Cluster -A10 | head -n 11 | tail -n10 | cut -d':' -f3 | awk '{print $4}'); do cp $i data/output_files/alphaflow/ensembles/$(basename $clusters _clusters.out)/top10/; done; done
```

