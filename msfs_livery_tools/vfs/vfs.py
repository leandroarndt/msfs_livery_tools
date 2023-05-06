"""Implements a parallel of MSFS package virtual file system."""
import json
from pathlib import Path

class _VFSObject(object):
    name:str
    parent:object
    base_path:Path
    
    def __init__(self, name:str, parent, base_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name.lower()
        self.parent = parent
        self.parent.contents[self.name] = self
        self.base_path = base_path

class VFSFolder(_VFSObject):
    contents:dict = {}
    
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
        return name.lower() in self.contents
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.contents = {}
    
    @classmethod
    def new(cls, name:str, parent, base_path:Path, layout:Path|None=None, *args, **kwargs):
        if name.lower() in parent:
            instance = parent.contents[name.lower()]
        else:
            instance = VFSFolder(name, parent, base_path, *args, **kwargs)
        
        if isinstance(parent, VFS):
            instance.root = parent
        else:
            instance.root = parent.root
            
        if layout:
            instance.scan_layout(layout)
        
        return instance

    @classmethod
    def scan_layout(cls, layout_file:Path, root):
        with layout_file.open('r') as f:
            layout = json.load(f)
        for item in layout['content']:
            try:
                path = Path(item['path'])
                part_parent = root
                folder = VFSFolder # Avoid UnboundLocalError
                for part in path.parent.parts:
                    folder = VFSFolder.new(part, part_parent, base_path=layout_file.parent)
                    part_parent = folder
                VFSFile(path, folder, layout_file.parent)
            except KeyError:
                pass
    
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
    
    def __init__(self, file:str|Path, parent:VFSFolder, base_path:Path, *args, **kwargs):
        self.file = Path(file)
        super().__init__(name=self.file.name, parent=parent, base_path=base_path, *args, **kwargs)
    
    def open(self, mode:str, *args, **kwargs):
        return (self.base_path / self.file).open(mode, *args, **kwargs)

class VFS(object):
    contents:dict = {}
    package_folder:Path
    _instance = None
    
    @classmethod
    def new(cls, package_folder:str|Path, include_all:bool=False):
        
        if cls._instance is None:
            cls._instance = cls()
            cls._instance.package_folder = Path(package_folder)
            cls._instance.contents = {}
            cls._instance.scan(include_all)
        
        return cls._instance
    
    def __hash__(self):
        return id(self)
    
    def __eq__(self, other):
        return self.package_folder == other.package_folder
    
    def _ne__(self, other):
        return self.package_folder != other.package_folder
    
    def __contains__(self, name:str):
        return name.lower() in self.contents
    
    def scan(self, include_all:bool=False):
        if include_all:
            packages = list(self.package_folder.glob('**/layout.json'))
        else:
            packages = list((self.package_folder / 'Official').glob('**/layout.json')) + list((self.package_folder / 'Community').glob('**/layout.json'))
        for package in packages:
            print(f'Adding {package.parent.name} into VFS root.')
            VFSFolder.scan_layout(package, self)
