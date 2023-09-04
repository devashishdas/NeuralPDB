import sys
import argparse

argparser = argparse.ArgumentParser(description="Get PDBID")
argparser.add_argument("-p", "--PDBID", help="PDBID of the protein")
args = argparser.parse_args()


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
    #@ErrorCheck
    def __init__(self, Pdb) -> None:
        self.pdbid = Pdb
        self.url = f"https://files.rcsb.org/view/{self.pdbid}.pdb"


# write a argaprse to get pdbid and use it to create a protein object and print the url
if __name__ == "__main__":
    try:
        pp = Protein(args.PDBID)
    except ValueError:
        sys.exit(1)
    print(pp.url)

