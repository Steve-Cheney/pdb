import argparse
from Bio import PDB

header_default = 'Atom_ID Residue_Name Chain_ID Residue_ID X Y Z'

def get_coordinates_and_descriptions(pdb_file):
    # Create a parser object
    parser = PDB.PDBParser(QUIET=True)

    # Load the PDB file
    structure = parser.get_structure('protein', pdb_file)

    # Create a dictionary to store atom descriptions and coordinates
    atom_data = {}

    # Iterate through the structure and extract descriptions and coordinates
    for model in structure:
        for chain in model:
            for residue in chain:
                for atom in residue:
                    atom_id = atom.get_id()
                    atom_coord = atom.get_coord()
                    description = f"{atom_id[0]} {residue.get_resname()} {chain.get_id()} {residue.get_id()[1]}"

                    atom_data[description] = atom_coord

    return atom_data

def write_coordinates_to_file(atom_data, output_file, header, noheader):
    with open(output_file, 'w') as file:
        # Write header if provided and not blank
        if noheader:
            if header is not None and header.strip() != '':
                file.write(header + '\n')
            else:
                file.write(header_default  + '\n')

        # Write data
        for description, coord in atom_data.items():
            file.write("{} {:.5f} {:.5f} {:.5f}\n".format(description, coord[0], coord[1], coord[2]))

def main():
    parser = argparse.ArgumentParser(description='Extract 3D coordinates and descriptions from a PDB file.')
    parser.add_argument('pdb_file', help='Path to the PDB file')
    parser.add_argument('--output_file', default='output_coordinates.txt', help='Path to the output file')
    parser.add_argument('--header', nargs='?', const=header_default, help='Header line for the output file. Leaving blank will return default: "Atom_ID Residue_Name Chain_ID Residue_ID X Y Z"')
    parser.add_argument('--noheader', action='store_false', help='If --noheader is set, output file will have no header. Otherwise will return default header. This overrides --header')

    args = parser.parse_args()

    try:
        atom_data = get_coordinates_and_descriptions(args.pdb_file)
        write_coordinates_to_file(atom_data, args.output_file, args.header, args.noheader)

        print("Successfully wrote coordinates and descriptions to {}".format(args.output_file))
    
    except Exception as e:
        print("Error:", str(e))


if __name__ == "__main__":
    main()
