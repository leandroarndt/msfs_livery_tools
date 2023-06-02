"""Creation of json descriptors for DDS files."""
import json
from pathlib import Path
from enum import Enum
from . import description_tools

class Descriptor(object):
    COMPRESSED = 'FL_BITMAP_COMPRESSION'
    MIPMAP = 'FL_BITMAP_MIPMAP'
    NORMAL_MAP = 'FL_BITMAP_TANGENT_DXT5N'
    NO_GAMMA = 'FL_BITMAP_NO_GAMMA_CORRECTION'
    COMPOSITE = 'FL_BITMAP_METAL_ROUGH_AO_DATA'
    HIGH_QUALITY = 'FL_BITMAP_QUALITY_HIGH'
    
    file:Path
    flags:set
    alpha:bool = False
    
    def __init__(self, flags:list[str], alpha:bool=False, use_defaults:bool=True, file:str|Path|None=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file = file
        self.alpha = alpha
        self.flags = set()
        if use_defaults:
            self.flags.add(self.COMPRESSED)
            self.flags.add(self.MIPMAP)
        for flag in flags:
            self.flags.add(flag)
    
    @classmethod
    def for_texture(cls, texture_file:str|Path):
        use:Uses
        
        texture_file = Path(texture_file)
        use = Uses.Unknown
        for u in Uses:
            for name in u.value.names:
                if name in texture_file.name.upper():
                    use = u
        if use == Uses.Unknown:
            use = Uses.Albedo
        
        return cls(flags=use.value.flags, alpha=use.value.alpha, use_defaults=False, file=texture_file.with_suffix('.dds.json'))
    
    @classmethod
    def open(cls, file:str|Path):
        file = Path(file)
        with file.open('r', encoding='utf-8') as f:
            description = json.load(f)
        try:
            flags = description['Flags']
        except KeyError:
            flags =[]
        try:
            alpha = description['HasTransp']
        except KeyError:
            alpha = False
        return cls(flags=flags, alpha=alpha, use_defaults=False, file=file)
    
    def save(self, file:str|Path|None=None):
        if file:
            self.file = Path(file)
        if not self.file:
            raise ValueError('Cannot save without a file name.')
        if not self.file.with_suffix('').is_file():
            raise ValueError(f'Cannot describe non-existing DDS file "{file.with_suffix("")}". Compress texture first!')
        description = {
            'Version': 2,
            'SourceFileDate': description_tools.win_time(Path(self.file.with_suffix('')).stat().st_mtime_ns),
            'Flags': list(self.flags),
        }
        if self.alpha:
            description['HasTransp'] = True
        with self.file.open('w', encoding='utf-8') as f:
            json.dump(description, f)

class Name_Flags_Alpha(object):
    names:list[str]
    flags:list[str] = [Descriptor.COMPRESSED, Descriptor.MIPMAP]
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
                            [Descriptor.NORMAL_MAP, Descriptor.NO_GAMMA])
    Composite = Name_Flags_Alpha(['_COMP', '_PBR'], [Descriptor.NO_GAMMA,Descriptor.COMPOSITE])

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
