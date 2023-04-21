"""Flags for texture files"""
from enum import Enum, unique
from pathlib import Path

@unique
class Flags(Enum):
    no_reduce = 'NOREDUCE'
    quality_high = 'QUALITYHIGH'
    precomputed_inverse_average = 'PRECOMPUTEDINVAVG'
    alpha_preservation = 'ALPHAPRESERVATION'

def create_flags(texture_file:str, flags:list[Flags]):
    """Creates .FLAGS file for textures.

    Args:
        texture_file (str): texture file.
        flags (list[Flags]): flag list.
    """
    f = []
    for flag in flags:
        f.append(flag.value)
    file = Path(f'{texture_file}.FLAGS').open('w')
    file.write(f'_DEFAULT={"+".join(f)}')
    file.close()
