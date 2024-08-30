# Script to compute the percentage of intrinsecally disordered regions. The path containing the PDB files must be provided.

from Bio.PDB import PDBParser
import os
import sys

# Check if the input argument is provided
if len(sys.argv) < 2:
    print("Error: Please provide a PDB file or a directory containing PDB files.")
    sys.exit(1)

# Get the input (either a PDB file or a directory)
input_path = sys.argv[1]

# Determine if the input is a file or a directory
if os.path.isfile(input_path):
    # Single PDB file
    pdb_files = [input_path]
elif os.path.isdir(input_path):
    # Directory containing PDB files
    pdb_files = [os.path.join(input_path, f) for f in os.listdir(input_path) if f.lower().endswith(".pdb")]
else:
    print("Error: The provided input is neither a PDB file nor a directory.")
    sys.exit(1)

# Process each PDB file
for pdb_file in pdb_files:
    total_len = 0
    IDR_res = 0
    
    # Create a PDB parser object
    parser = PDBParser()

    try:
        # Parse the PDB file
        structure = parser.get_structure("pdb_structure", pdb_file)
        
        # Iterate through the structure and extract B-factors
        for model in structure:
            for chain in model:
                for residue in chain:
                    try:
                        residue_name = residue.resname
                        b_factor = residue["CA"].get_bfactor()  # Assuming you want the B-factor of the alpha carbon (CA)
                        if float(b_factor) < 50:
                            IDR_res += 1
                        total_len += 1
                    except:
                        pass
        
        # Remove the extension from the pdb_file using strip()
        pdb_base_name = os.path.splitext(os.path.basename(pdb_file))[0]
        
        print(pdb_base_name + "\t" + str(IDR_res / total_len * 100))
    except Exception as e:
        print(f"Error processing file '{pdb_file}': {e}")

