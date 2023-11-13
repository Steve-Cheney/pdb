from Bio import PDB

def find_close_atoms(pdb_file_path, cutoff_distance=2.0):
    # Create a parser object
    parser = PDB.PDBParser(QUIET=True)

    # Load the PDB file
    structure = parser.get_structure('protein', pdb_file_path)

    # Create a list to store close atoms
    close_atoms = []

    # Iterate through the structure and compare distances between atoms
    for atom1 in structure.get_atoms():
        for atom2 in structure.get_atoms():
            if atom1 != atom2:
                distance = atom1-atom2
                if distance <= cutoff_distance:
                    close_atoms.append((atom1, atom2))

    return close_atoms

def main():
    pdb_file_path = '1XFC.pdb'  # Replace with the path to your PDB file
    close_atoms = find_close_atoms(pdb_file_path)

    for atom_pair in close_atoms:
        print("Atoms within 2 angstroms:", atom_pair)

if __name__ == "__main__":
    main()
