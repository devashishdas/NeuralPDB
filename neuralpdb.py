import sys
import argparse
from matplotlib import lines
import requests
import pandas as pd


argparser = argparse.ArgumentParser(description="Get PDBID")
argparser.add_argument("-p", "--PDBID", help="PDBID of the protein")
args = argparser.parse_args()

class Atom:
    def __init__(self, initid:int, lines:str) -> None:
        self.initid = initid
        self.lines = lines
        self._parselines()
        self.all_prop = self.__dict__
        self.all_prop.pop("lines")
    
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
    """
    """
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
        atoms = []
        count = 0
        for line in self.pdb:
            if line.startswith("ATOM") or line.startswith("HETATM"):
                atoms.append(Atom(count, line))
                count += 1
        return atoms



if __name__ == "__main__":
    try:
        pp = Protein(args.PDBID)
    except ValueError:
        sys.exit(1)
    # print(pp.store[0].all_prop)
    # pp.store to pandas and to csv
    df = pd.DataFrame([atom.all_prop for atom in pp.store])
    df.to_csv(f"{pp.pdbid}.csv", index=False)
    print(f"[INFO]: {pp.pdbid}.csv created.")


 # read csv and convert to mysql db using sqlalchemy
    # https://stackoverflow.com/questions/23103962/how-to-write-dataframe-to-mysql-table

#from sqlalchemy import create_engine  
#engine = create_engine('mysql://user:pass@localhost/dbname', echo=False)
#df.to_sql(name='table_name', con=engine, if_exists = 'append', index=False)
