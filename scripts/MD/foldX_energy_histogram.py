import argparse
import matplotlib.pyplot as plt
import numpy as np


def read_data(file_path, protein_name):
    data = {'Model': [], 'Native': [], 'ensembles': []}
    with open(file_path, 'r') as file:
        for line in file:
            source, name, _ = line.strip().split('/')
           
            if name.lower() == protein_name.lower():
                try:
                    source, value = source, float(_.split()[-1])
                    data[source].append(value)
                except:
                    continue
    return data

def plot_histogram(data, protein_name):
    bins=np.histogram(np.hstack((data['Model'],data['Native'],data['ensembles'])),bins=40)[1]
    plt.hist(data['Model'], bins=bins, alpha=0.5, color='blue', label='MD-AF')
    plt.hist(data['Native'], bins=bins, alpha=0.5, color='green', label='MD-PDB')
    plt.hist(data['ensembles'], bins=bins, alpha=0.5, color='red', label='AlphaFlow')
    plt.xlabel('Energy (Kcal/mol)')
    plt.ylabel('Frequency')
    plt.legend(loc='upper right')
    plt.savefig(f"energy_histogram_{protein_name}.svg")
    #plt.show()

def main():
    parser = argparse.ArgumentParser(description='This script creates an energy histogram from foldX energy computations. he PDBs used were repaired beforehand with the "RepairPDB" command in FoldX. Then, the "Stability" command was used to obtain energies. for PDB_PATH in *.pdb; do echo $PDB_PATH $(../foldx_20241231 --command=Stability --pdb=$PDB_PATH | grep Total | grep = ) ; done  2> /dev/null See foldx_outputs_repairedpdb.txt')
    parser.add_argument('file_path', type=str, required=True, help='Path to the modified foldX file.')
    parser.add_argument('protein_name', type=str, required=True,help='Name of the protein')
    args = parser.parse_args()

    data = read_data(args.file_path, args.protein_name)
    plot_histogram(data, args.protein_name)

if __name__ == "__main__":
    main()

