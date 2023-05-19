"""Deals with application settings."""
import configparser
from pathlib import Path

class AppSettings(object):
    _config_parser:configparser.ConfigParser = None
    file:Path
    
    @property
    def msfs_package_path(self)->Path:
        try:
            return __class__._config_parser['PACKAGES']['msfs_package_path']
        except KeyError:
            return ''

    @msfs_package_path.setter
    def msfs_package_path(self, path:str):
        print(path)
        __class__._config_parser['PACKAGES']['msfs_package_path'] = path
    
    @property
    def scan_all_folders(self)->bool:
        try:
            return True if __class__._config_parser['PACKAGES']['scan_all_folders'] == 'True' else False
        except KeyError:
            return False
    
    @scan_all_folders.setter
    def scan_all_folders(self, value:bool):
        __class__._config_parser['PACKAGES']['scan_all_folders'] = str(value)
    
    @property
    def scan_depth(self)->int:
        try:
            return int(__class__._config_parser['PACKAGES']['scan_depth'])
        except (KeyError, ValueError):
            return 3
    
    @scan_depth.setter
    def scan_depth(self, value:int):
        __class__._config_parser['PACKAGES']['scan_depth'] = str(value)
    
    @property
    def use_fallbacks(self)->bool:
        try:
            return True if __class__._config_parser['TEXTURES']['use_fallbacks'] == 'True' else False
        except KeyError:
            return False
    
    @use_fallbacks.setter
    def use_fallbacks(self, value:bool):
        __class__._config_parser['TEXTURES']['use_fallbacks'] = value
    
    @property
    def compress_textures_on_build(self)->bool:
        try:
            return True if __class__._config_parser['BUILD']['compress_textures'] == 'True' else False
        except KeyError:
            return True
    
    @compress_textures_on_build.setter
    def compress_textures_on_build(self, value:bool):
        __class__._config_parser['BUILD']['compress_textures'] = str(value)
    
    @property
    def texconv_path(self)->str:
        try:
            return __class__._config_parser['GENERAL']['texconv_path']
        except KeyError:
            return ''
    
    @texconv_path.setter
    def texconv_path(self, path:str):
        __class__._config_parser['GENERAL']['texconv_path'] = path
    
    @property
    def recent_files(self)->list[str]:
        try:
            return __class__._config_parser['GENERAL']['recent'].split('|')
        except KeyError:
            return []
    
    @recent_files.setter
    def recent_files(self, path:str):
        try:
            recent = __class__._config_parser['GENERAL']['recent'].split('|')
            if path in recent:
                recent.remove(path)
            recent = [path] + recent
            recent = recent[:5]
            __class__._config_parser['GENERAL']['recent'] = '|'.join(recent)
        except KeyError:
            __class__._config_parser['GENERAL']['recent'] = str(path)
    
    def __init__(self, *args, **kwargs):
        self.file = Path(Path.home(), '.msfs_livery_tools.cfg')
        if __class__._config_parser is None:
            __class__._config_parser = configparser.ConfigParser()
        __class__._config_parser.read(self.file)
        for section in ('GENERAL', 'BUILD', 'PACKAGES', 'TEXTURES'):
            if section not in __class__._config_parser.sections():
                __class__._config_parser.add_section(section)
                self.save()
        
    def save(self, *args, **kwargs):
        with open(self.file, 'w') as f:
            __class__._config_parser.write(f, *args, **kwargs)
