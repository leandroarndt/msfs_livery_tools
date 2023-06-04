"""Flags for texture files"""
from pathlib import Path

class Flags (object):
    NO_REDUCE = 'NOREDUCE'
    QUALITY_HIGH = 'QUALITYHIGH'
    PRECOMPUTED_INVERSE_AVERAGE = 'PRECOMPUTEDINVAVG'
    ALPHA_PRESERVATION = 'ALPHAPRESERVATION'
    
    file:Path
    flags:set
    
    def __init__(self, flags:list, file:str|Path|None=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if file:
            self.file = Path(file)
        self.flags = set()
        for flag in flags:
            self.flags.add(flag)
    
    def __str__(self)->str:
        return f'_DEFAULT=+{"+".join(self.flags)}'
    
    @classmethod
    def open(cls, file:str|Path):
        file = Path(file)
        with file.open('r', encoding='utf-8') as f:
            contents = f.read()
            contents = contents[10:] # remove "_DEFAULT=+"
            return cls(contents.split('+'), file)
    
    def save(self, file:str|Path|None=None):
        if file:
            self.file = Path(file)
        if self.file.is_file() and len(self.flags) == 0:
            self.file.unlink()
            print(f'Trying to save void "{self.file.name}". Deleting!')
            return
        if not self.file:
            raise ValueError('Cannot save without file path.')
        with self.file.open('w', encoding='utf-8') as f:
            f.write(str(self))
