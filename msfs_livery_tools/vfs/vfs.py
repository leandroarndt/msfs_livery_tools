"""Implements a parallel of MSFS package virtual file system."""
import json
from pathlib import Path

class _VFSObject(object):
    name:str
    parent:object
    
    def __init__(self, name:str, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name.lower()
        self.parent = parent
        self.parent.contents.add(self)

class VFSFolder(_VFSObject):
    contents:set[_VFSObject]
    
    def __hash__(self):
        return id(self)
    
    def __eq__(self, other:_VFSObject):
        try:
            return self.name == other.name and self.parent == other.parent
        except AttributeError:
            return False
    
    def __ne__(self, other):
        return self.folder != other.folder
    
    def __contains__(self, name:str):
        for item in self.contents:
            if item.name == name:
                return(True)
        return False
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.contents = set()
    
    @classmethod
    def new(cls, name, parent, layout:Path|None=None, *args, **kwargs):
        if name in parent:
            for content in parent.contents:
                if content.name == name:
                    return content
        return VFSFolder(name, parent)
    
    def find(file_name:str, paths:list[str])->Path:
        """Finds a file "file_name" in "paths" and returns the corresponding real file system path.

        Args:
            file_name (str): file name to search for
            paths (list[str]): list of VFS folders to search relative to VFSFolder object.

        Returns:
            Path: real file system path for "file_name" in "paths".
        """
        pass

class VFSFile(_VFSObject):
    file:Path
    
    def __init__(self, file:str|Path, parent:VFSFolder, *args, **kwargs):
        self.file = Path(file)
        super().__init__(name=self.file.name, parent=parent, *args, **kwargs)
    
    def open(self, mode:str, *args, **kwargs):
        return self.file.open(mode, *args, **kwargs)

class VFS(object):
    contents:set[VFSFolder]
    package_folder:Path
    _instance = None
    
    @classmethod
    def new(cls, package_folder:str|Path, include_all:bool=False):
        
        if cls._instance is None:
            cls._instance = cls()
            cls._instance.package_folder = Path(package_folder)
            cls._instance.contents = set()
            cls._instance.scan(include_all)
        
        return cls._instance
    
    def __hash__(self):
        return id(self)
    
    def __eq__(self, other):
        return self.package_folder == other.package_folder
    
    def _ne__(self, other):
        return self.package_folder != other.package_folder
    
    def __contains__(self, name:str):
        for item in self.contents:
            if item.name == name:
                return(True)
        return False
    
    def scan(self, include_all:bool=False):
        if include_all:
            packages = list(self.package_folder.glob('**/layout.json'))
        else:
            packages = list((self.package_folder / 'Official').glob('**/layout.json')) + list((self.package_folder / 'Community').glob('**/layout.json'))
        for package in packages:
            print(f'Adding {package.parent.name} into VFS root.')
            VFSFolder.new(package.parent.name, self, package)
