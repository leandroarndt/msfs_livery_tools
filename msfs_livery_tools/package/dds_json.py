"""Creation of json descriptors for DDS files."""
import json
from pathlib import Path
from enum import Enum
from . import description_tools

class DescriptorFlags:
    compressed = 'FL_BITMAP_COMPRESSION'
    mipmap = 'FL_BITMAP_MIPMAP'
    normal_map = 'FL_BITMAP_TANGENT_DXT5N'
    no_gamma = 'FL_BITMAP_NO_GAMMA_CORRECTION'
    composite = 'FL_BITMAP_METAL_ROUGH_AO_DATA'
    high_quality = 'FL_BITMAP_QUALITY_HIGH'

class Name_Flags_Alpha(object):
    names:list[str]
    flags:list[str] = [DescriptorFlags.compressed, DescriptorFlags.mipmap]
    alpha:bool = False
    
    def __init__(self, names:list[str]=[], flags:list[str]=[], alpha:bool=False, no_default=False):
        self.names = names
        if no_default:
            self.flags = flags
        else:
            self.flags = __class__.flags + flags
        self.alpha = alpha

class Uses(Enum):
    """Enumeration of uses of texture files."""
    Unknown = Name_Flags_Alpha()
    Albedo = Name_Flags_Alpha(['_ALBD', '_ALBEDO', '_ALB'], alpha=True)
    Emissive = Name_Flags_Alpha(['_LIT', '_EMIT'], alpha=True)
    Normal_Map = Name_Flags_Alpha(['_NORM', '_NRM', '_NORMAL'],
                            [DescriptorFlags.normal_map, DescriptorFlags.no_gamma])
    Composite = Name_Flags_Alpha(['_COMP', '_PBR'], [DescriptorFlags.no_gamma,DescriptorFlags.composite])

def create_description(dds_file:str, use=Uses.Unknown, alpha=None):
    """Creates a JSON description of dds_file as "dds_file.json".

    Args:
        dds_file (str): path to DDS file.
        use: use of file, according to `Uses`.
        alpha (bool or None): override default transparency info.
    """
    if use == Uses.Unknown:
        name = Path(dds_file).name.upper()
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
