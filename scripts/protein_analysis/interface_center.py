import numpy as np
from Bio.PDB import PDBParser, NeighborSearch, Selection
import argparse

def get_interface_residues(chain1, chain2, cutoff=5.0):
    atoms_chain1 = list(chain1.get_atoms())
    atoms_chain2 = list(chain2.get_atoms())
    
    ns_chain2 = NeighborSearch(atoms_chain2)
    ns_chain1 = NeighborSearch(atoms_chain1)
    
    interface_residues_chain1 = set()
    interface_residues_chain2 = set()
    
    for atom in atoms_chain1:
        neighbors = ns_chain2.search(atom.coord, cutoff)
        for neighbor in neighbors:
            if neighbor.get_parent() not in interface_residues_chain2:
                interface_residues_chain2.add(neighbor.get_parent())
            if atom.get_parent() not in interface_residues_chain1:
                interface_residues_chain1.add(atom.get_parent())
    
    return interface_residues_chain1, interface_residues_chain2

def calculate_geometric_center(residues):
    coords = []
    for residue in residues:
        for atom in residue:
            coords.append(atom.coord)
    
    if not coords:
        return None
    
    coords_array = np.array(coords)
    center = np.mean(coords_array, axis=0)
    return center, coords_array

def calculate_box_size(coords_array, margin=2.0):
    min_coords = np.min(coords_array, axis=0)
    max_coords = np.max(coords_array, axis=0)
    
    size_x = max_coords[0] - min_coords[0] + 2 
    size_y = max_coords[1] - min_coords[1] + 2 
    size_z = max_coords[2] - min_coords[2] + 2 
    
    return size_x, size_y, size_z

def main(pdb_file, chain_id1, chain_id2, cutoff):
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure('structure', pdb_file)
    
    model = structure[0]
    
    try:
        chain1 = model[chain_id1]
        chain2 = model[chain_id2]
    except KeyError as e:
        print(f"Error: Chain ID {e} not found in the structure.")
        return
    
    interface_residues_chain1, interface_residues_chain2 = get_interface_residues(chain1, chain2, cutoff)
    
    if not interface_residues_chain1:
        print(f"No interface residues found for chain {chain_id1}.")
        return
    if not interface_residues_chain2:
        print(f"No interface residues found for chain {chain_id2}.")
        return
    
    center_chain1, coords_chain1 = calculate_geometric_center(interface_residues_chain1)
    center_chain2, coords_chain2 = calculate_geometric_center(interface_residues_chain2)
    
    interface_center = (center_chain1 + center_chain2) / 2
    all_coords = np.vstack((coords_chain1, coords_chain2))
    
    size_x, size_y, size_z = calculate_box_size(all_coords)
    
    print(f"{interface_center[0]} {interface_center[1]} {interface_center[2]}")
    print(f"{size_x} {size_y} {size_z}")
    
    return interface_center, (size_x, size_y, size_z)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate the interface center and optimal box size between two protein chains in a PDB file.")
    parser.add_argument("pdb_file", help="Path to the PDB file")
    parser.add_argument("chain_id1", help="Chain ID of the first protein chain")
    parser.add_argument("chain_id2", help="Chain ID of the second protein chain")
    parser.add_argument("--cutoff", type=float, default=5.0, help="Distance cutoff in angstroms (default: 5.0)")
    
    args = parser.parse_args()
    
    main(args.pdb_file, args.chain_id1, args.chain_id2, args.cutoff)

