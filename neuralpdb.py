import sys
def ErrorCheck(func):
    def wrapper(pp, arg):
        if arg != arg.strip():
            print("[WARN]: space in PDBID")
        if len(arg) != 4:
            print("[FError]: Cannot continue. PDBID not valid.")
            raise ValueError
        func(pp, arg)
        return wrapper


class Protein:
    """
    """
    @ErrorCheck
    def __init__(self, Pdb) -> None:
        self.pdbid = Pdb
        self.url = "https://files.rcsb.org/view/{self.pdbid}.pdb"


p = Protein(sys.argv[-1])
print(p.url)