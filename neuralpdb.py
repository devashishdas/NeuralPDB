import sys
import argparse
import requests
import pandas as pd
from tqdm import tqdm


argparser = argparse.ArgumentParser(description="Get PDBID")
argparser.add_argument("-p", "--PDBID", help="PDBID of the protein")
argparser.add_argument("-o", "--output", help="Output file name", default="output.csv")
argparser.add_argument("-c", "--curated", help="Curated output", default=False)
args = argparser.parse_args()

class Atom:
    def __init__(self, initid:int, lines:str) -> None:
        self.initid = initid
        self.lines = lines
        self._parselines()
        self.all_prop = self.__dict__
        self.all_prop.pop("lines")
        self.resid = ""
    
    def _parselines(self):
        line = self.lines
        self.record_name = line[0:6].strip()
        self.atom_serial = int(line[6:11])
        self.atom_name = line[12:16].strip()
        self.alt_location = line[16:17]
        self.residue_name = line[17:20].strip()
        self.chain_id = line[21:22]
        self.residue_serial = int(line[22:26])
        self.insertion_code = line[26:27]
        self.x_coord = float(line[30:38])
        self.y_coord = float(line[38:46])
        self.z_coord = float(line[46:54])
        self.occupancy = float(line[54:60])
        self.temperature_factor = float(line[60:66])
        self.element_symbol = line[76:78].strip()
        self.charge = line[78:80].strip()

class Residue:
    def __init__(self, AtomObj:Atom) -> None:
        self.atom = AtomObj

# Decorator to check if the PDBID is valid
def ErrorCheck(func):
    def wrapper(ppx, arg):
        if arg != arg.strip():
            print("[WARN]: space in PDBID")
        if len(arg) != 4:
            print("[FError]: Cannot continue. PDBID not valid.")
            raise ValueError
        func(ppx, arg)
    return wrapper


class Protein:
    @ErrorCheck
    def __init__(self, Pdb) -> None:
        self.pdbid = Pdb
        self.url = f"https://files.rcsb.org/view/{self.pdbid}.pdb"
        # from url to list of lines 
        self.pdb = self._pdblines(self.url)
        self.store = self._pdb2atom()
        

    def _pdblines(self, url):
        pdb = requests.get(url).text.split("\n")
        return pdb
    
    def _pdb2atom(self):
        self.curated_store = {}
        self.curated_chain = {}
        self.curated_aminos = {}
        atoms = []
        count = 0
        for line in self.pdb:
            if line.startswith("ATOM") or line.startswith("HETATM"):
                AtomObj = Atom(count, line)
                atoms.append(AtomObj)
                residue_id = f"{AtomObj.residue_name}_{AtomObj.residue_serial}_{AtomObj.chain_id}"  # noqa: E501
                self.curated_store[residue_id] = Residue(AtomObj)
                if AtomObj.chain_id not in self.curated_chain.keys():
                    self.curated_chain[AtomObj.chain_id] = []
                if residue_id not in self.curated_chain[AtomObj.chain_id]:
                    self.curated_chain[AtomObj.chain_id].append(residue_id)
                
                if AtomObj.residue_name not in self.curated_aminos.keys():
                    self.curated_aminos[AtomObj.residue_name] = []
                if residue_id not in self.curated_aminos[AtomObj.residue_name]:
                    self.curated_aminos[AtomObj.residue_name].append(residue_id)

                count += 1
        return atoms
    


if __name__ == "__main__":
    try:
        pp = Protein(args.PDBID)
    except ValueError:
        sys.exit(1)
    # print(pp.store[0].all_prop)
    # pp.store to pandas and to csv
    #df = pd.DataFrame([atom.all_prop for atom in pp.store])
    #df.to_csv(args.output, index=False)
    
    # Use tqdm to show live progress while processing
    with tqdm(total=len(pp.store), desc="Processing") as pbar:
        df_data = []
        for atom in pp.store:
            df_data.append(atom.all_prop)
            pbar.update(1)

    df = pd.DataFrame(df_data)

    # Use tqdm to show live progress while writing the CSV
    with tqdm(total=1, desc="Saving CSV") as pbar:
        df.to_csv(args.output, index=False)
        pbar.update(1)
        
    print(f"[INFO]: {args.output} created.")
        
    # if args.curated:
    #     print(pp.curated_chain.keys())
    #     print(pp.curated_aminos.keys())
    #     print(pp.curated_aminos["FE"])

