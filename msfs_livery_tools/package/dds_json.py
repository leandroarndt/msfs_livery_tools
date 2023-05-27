"""Creation of json descriptors for DDS files."""
import json
from pathlib import Path
from enum import Enum
from . import description_tools

class Name_Flags_Alpha(object):
    names:list[str]
    flags:list[str] = ['FL_BITMAP_COMPRESSION', 'FL_BITMAP_MIPMAP']
    alpha:bool = False
    
    def __init__(self, names:list[str]=[], flags:list[str]=[], alpha:bool=False):
        self.names = names
        self.flags = __class__.flags + flags
        self.alpha = alpha

class Uses(Enum):
    """Enumeration of uses of texture files."""
    Unknown = Name_Flags_Alpha()
    Albedo = Name_Flags_Alpha(['_ALBD', '_ALBEDO', '_ALB'], alpha=True)
    Emissive = Name_Flags_Alpha(['_LIT', '_EMIT'], alpha=True)
    Normal_Map = Name_Flags_Alpha(['_NORM', '_NRM', '_NORMAL'],
                            ['FL_BITMAP_TANGENT_DXT5N', 'FL_BITMAP_NO_GAMMA_CORRECTION'])
    Composite = Name_Flags_Alpha(['_COMP', '_PBR'], ['FL_BITMAP_NO_GAMMA_CORRECTION','FL_BITMAP_METAL_ROUGH_AO_DATA'])

def create_description(dds_file:str, use=Uses.Unknown, alpha=None):
    """Creates a JSON description of dds_file as "dds_file.json".

    Args:
        dds_file (str): path to DDS file.
        use: use of file, according to `Uses`.
        alpha (bool or None): override default transparency info.
    """
    if use == Uses.Unknown:
        name = Path(dds_file).name
        for u in Uses:
            for n in u.value.names:
                if n in name:
                    use = u
        if use == Uses.Unknown:
            use = Uses.Albedo
    if alpha is None:
        alpha = use.value.alpha
    description_file = Path(f'{dds_file}.json').open('w', encoding='utf8')
    description = {
        'Version': 2,
        'SourceFileDate': description_tools.win_time(Path(dds_file).stat().st_mtime_ns),
        'Flags': use.value.flags,
    }
    if alpha:
        description['HasTransp'] = True
    json.dump(description, description_file)
    description_file.close()
