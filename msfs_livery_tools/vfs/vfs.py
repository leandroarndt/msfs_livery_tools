"""Implements a parallel of MSFS package virtual file system."""
import json
from pathlib import Path
from queue import Queue

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

class _VFSContainer:
    contents:dict = {}
    
    def __contains__(self, name:str):
        return name.lower() in self.contents
    
    def __getitem__(self, key):
        if hasattr(key, 'lower'):
            return self.contents[key.lower()]
        return self.contents[key]
    
    def keys(self):
        return self.contents.keys()
    
    def navigate(self, path:str)->_VFSObject:
        sep = '/'
        if '\\' in path:
            sep = '\\'
        if path == '':
            return self
        path = path.lower()
        parts = path.split(sep)
        if parts:
            next_part = parts.pop(0)
            if next_part == '..':
                return self.parent.navigate(sep.join(parts))
            if parts:
                return self.contents[next_part.lower()].navigate(sep.join(parts))
            return self.contents[next_part]
        return self
    
    def find(self, file_name:str, fallbacks:list[str])->Path:
        """Finds a file "file_name" in this folder and in "fallbacks" and returns the corresponding VFSFile.
        
        Args:
            file_name (str): file name to search for
            fallbacks (list[str]): list of VFS folders to search relative to VFSFolder object.
        
        Returns:
            Path: real file system path for "file_name" in "fallbacks".
        """
        if file_name.lower() in self.contents:
            return self.contents[file_name.lower()]
        for fallback in fallbacks:
            try:
                fallback = Path(fallback)
                parts = fallback.parts
                folder = self
                for part in parts:
                    if part == '..':
                        folder = folder.parent
                    else:
                        folder = folder.contents[part.lower()]
                if file_name.lower() in folder.contents:
                    return folder.contents[file_name.lower()]
            except KeyError:
                pass
        raise FileNotFoundError

class VFSFolder(_VFSObject, _VFSContainer):
    
    def __hash__(self):
        return id(self)
    
    def __eq__(self, other:_VFSObject):
        try:
            return self.name == other.name and self.parent == other.parent
        except AttributeError:
            return False
    
    def __ne__(self, other):
        return self.folder != other.folder
    
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

class VFSFile(_VFSObject):
    file:Path
    
    def __init__(self, file:str|Path, parent:VFSFolder, base_path:Path, *args, **kwargs):
        self.file = Path(file)
        super().__init__(name=self.file.name, parent=parent, base_path=base_path, *args, **kwargs)
    
    def real_path(self):
        return (self.base_path / self.file)
    
    def open(self, mode:str, *args, **kwargs):
        return self.real_path().open(mode, *args, **kwargs)

class VFS(_VFSContainer, object):
    contents:dict = {}
    package_folder:Path
    _instance = None
    name = 'VFS root'
    
    @classmethod
    def new(cls, package_folder:str|Path, include_extra=[], include_all:bool=False, queue=None):
        
        if cls._instance is None:
            cls._instance = cls()
            cls._instance.package_folder = Path(package_folder)
            cls._instance.contents = {}
            cls._instance.scan(include_extra, include_all, queue)
        
        return cls._instance
    
    def __hash__(self):
        return id(self)
    
    def __eq__(self, other):
        return self.package_folder == other.package_folder
    
    def _ne__(self, other):
        return self.package_folder != other.package_folder
    
    def scan(self, include_extra=[], include_all:bool=False, queue:Queue=None, depth:int=3):
        self.contents = {} # Resets prior to scan
        print('Searching MSFS packages…')
        if isinstance(queue, Queue):
            queue.put('Searching MSFS packages…')
        if depth < 0:
            if include_all:
                packages = list(self.package_folder.glob('**/layout.json'))
            else:
                packages = list((self.package_folder / 'Official').glob('**/layout.json')) + list((self.package_folder / 'Community').glob('**/layout.json'))
            for extra in include_extra:
                packages += list(Path(extra).glob('**/layout.json'))
        else:
            packages = []
            for level in range(depth+1):
                if level == 0 and include_all:
                    packages += list(self.package_folder.glob('./' + '*/' * level + '/layout.json'))
                elif level > 0:
                    packages += list(self.package_folder.glob('Official/' + '*/' * (level - 1) + '/layout.json')) + list(self.package_folder.glob('Community/' + '*/' * (level - 1) + '/layout.json'))
                for extra in include_extra:
                    packages += list(Path(extra).glob('./' + '*/' * level + '/layout.json'))
        for package in packages:
            print(f'Adding {package.parent.name} into VFS root…')
            if isinstance(queue, Queue):
                if not queue.empty():
                    queue.get(block=False)
                queue.put(f'Adding {package.parent.name} into VFS root…')
            VFSFolder.scan_layout(package, self)
