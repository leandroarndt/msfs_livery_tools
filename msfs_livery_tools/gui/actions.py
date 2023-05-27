import configparser, shutil, time
from pathlib import Path, PureWindowsPath
from tkinter import ttk, filedialog
from typing import Callable
from threading import Thread
from msfs_livery_tools.project import Project
from msfs_livery_tools.settings import AppSettings
from msfs_livery_tools.compression import dds
from msfs_livery_tools.package import dds_json, aircraft_cfg, manifest, layout, panel_cfg, thumbnail
from msfs_livery_tools.vfs import VFSFile, VFSFolder, VFS
from .helpers import NOT_SET

class ConfigurationError(Exception):
    """"""

class Runner(Thread):
    """Abstract thread for tasks with indeterminate length/accomplishment."""
    task:Callable
    args:list
    kwargs:dict
    
    def __init__(self, task:Callable, *args, **kwargs):
        super().__init__()
        self.task = task
        self.args = args
        self.kwargs = kwargs
    
    def run(self):
        self.task(*self.args, **self.kwargs)

class Agent(object):
    project:Project
    settings:AppSettings
    progress_bar:ttk.Progressbar
    progress_bar_maximum:int
    running:bool = False
    error:Exception|None = None
    
    def __init__(self, progress_bar):
        self.settings = AppSettings()
        self.progress_bar = progress_bar
        self.progress_bar_maximum = self.progress_bar['maximum']
    
    def _texture_dir(self)->Path:
        if self.project.join_model_and_textures:
            return Path(self.project.file).parent / 'model'
        else:
            return Path(self.project.file).parent / 'texture'
    
    def _copy(self, source:str|Path, dest:str|Path, pattern='*', overwrite=True)->list[str]:
        source, dest = Path(source), Path(dest)
        files = []
        
        if not dest.exists():
            dest.mkdir()
        
        if source.is_file():
            if Path(dest, source.name).exists() and overwrite:
                Path(dest, source.name).unlink()
            shutil.copy(source, dest)
            return [source.name]
        
        for file in source.glob(pattern):
            print(f'Copying "{file}" to "{dest / file.name}"…')
            if file.is_file():
                if Path(dest, file.name).exists() and overwrite:
                    Path(dest, file.name).unlink()
                shutil.copy(file, dest)
                files.append(file.name)
        
        return files
    
    def _move(self, source:str|Path, dest:str|Path, pattern='*', overwrite=True):
        source, dest = Path(source), Path(dest)
        if not dest.exists():
            dest.mkdir()
        if source.is_file():
            if Path(dest, source.name).exists() and overwrite:
                Path(dest, source.name).unlink()
            print(f'Moving temporary "{source}" to "{dest / source.name}"…')
            shutil.move(source, dest)
        else:
            raise ValueError(f'"{source}" is not a file.')
    
    def monitor(self, thread:Runner):
        if thread.is_alive():
            self.running = True
            if self.progress_bar['mode'] != 'indeterminate':
                self.progress_bar['mode'] = 'indeterminate'
                self.progress_bar.start()
            self.progress_bar.after(30, lambda: self.monitor(thread))
        else:
            self.progress_bar.stop()
            self.restore_progress_bar()
            self.running = False
    
    def prepare_progress_bar(self, maximum):
        self.progress_bar['maximum'] = maximum
        self.progress_bar['value'] = 0
        self.progress_bar['mode'] = 'determinate'
    
    def restore_progress_bar(self):
        self.progress_bar['mode'] = 'determinate'
        self.progress_bar['maximum'] = self.progress_bar_maximum
        self.progress_bar['value'] = 0
    
    def extract_textures(self, gltf:str|Path, vfs:VFS):
        thread = Runner(self._do_extract_textures, gltf, vfs)
        thread.start()
        self.monitor(thread)
    
    def _do_extract_textures(self, gltf:str|Path, vfs:VFS):
        descriptor:VFSFile
        
        # Prepare path variables
        gltf = Path(gltf)
        original_suffix = gltf.parent.suffix
        texture_dir = gltf.parent.parent / ('texture' + original_suffix)
        output_dir = self._texture_dir()
        
        # Prepare texture copying
        if gltf.resolve().as_posix().lower().startswith(self.settings.msfs_package_path.lower()):
            try:
                texture_dir = vfs['SimObjects']['Airplanes'][gltf.parent.parent.name][texture_dir.name]
                
            except KeyError:
                pass
        
        # Fallbacks:
        fallbacks = []
        texture_config = configparser.ConfigParser()
        if isinstance(texture_dir, VFSFolder):
            texture_config.read(texture_dir['texture.cfg'].real_path())
        else:
            texture_config.read(texture_dir / 'texture.cfg')
        for path in texture_config[texture_config.sections()[0]].values():
            fallbacks.append(path)
        
        # Flag variables
        flags_dir = [texture_dir]
        try:
            if isinstance(texture_dir, VFSFolder):
                for path in texture_config[texture_config.sections()[0]].values():
                    try:
                        flags_dir.append(texture_dir.navigate(path))
                    except FileNotFoundError:
                        print(f'Could not find "{path}" on VFS!')
            else:
                # texture_config.read(texture_dir / 'texture.cfg')
                for path in texture_config[texture_config.sections()[0]].values():
                    flags_dir.append((texture_dir / path).resolve())
                flags_dir.reverse()
        except FileNotFoundError:
            pass
        flags = []
        
        # Assures the existence of output dir
        if not output_dir.is_dir():
            output_dir.mkdir()
        
        # Copy flags in reverse order
        for dir in flags_dir:
            if isinstance(dir, VFSFolder):
                for child in dir.keys():
                    if child.lower().endswith('.flags'):
                        flags += self._copy(dir[child].real_path(), output_dir)
            else:
                flags += self._copy(dir, output_dir, '*.flags')
        
        # Copy textures
        thread = Runner(dds.from_glft, gltf, texture_dir, output_dir, self.settings.texconv_path,
                        fallbacks=fallbacks)
        thread.start()
        self.monitor(thread)
        
        # Wait
        while thread.is_alive():
            time.sleep(1/30)
        
        # Get rid of unneeded flags
        png_list = list(output_dir.glob('*.png'))
        for flag in flags:
            f = output_dir / Path(Path(Path(flag).stem).stem + '.png')
            if output_dir / Path(Path(Path(flag).stem).stem + '.png') not in png_list:
                print(f'Unlink "{flag}"!')
                try:
                    (output_dir / flag).unlink()
                except:
                    pass
        
        # Copy JSON texture descriptors
        print('Copying texture descriptors.')
        for texture in png_list:
            if isinstance(texture_dir, VFSFolder):
                # if texture.name.lower().startswith('glass_') or texture.name.lower().startswith('frost_'):
                try:
                    descriptor = texture_dir.find(texture.stem + '.DDS.json', fallbacks=fallbacks)
                    self._copy(descriptor.real_path(), self._texture_dir())
                    print(f'Copied texture descriptor for "{texture.stem + ".DDS"}".')
                except FileNotFoundError:
                    print(f'Could not find original descriptor for "{texture.stem + ".DDS"}".')
            else:
                try:
                    self._copy(texture_dir / (texture.stem + '.DDS.json'), self._texture_dir())
                    print(f'Copied texture descriptor for "{texture.stem + ".DDS"}".')
                except FileNotFoundError:
                    print(f'Could not find original descriptor for "{texture.stem + ".DDS"}".')
    
    def convert_dds_file(self, path:Path|str, copy_flags:bool=True):
        path = Path(path)
        dds.convert(path, self._texture_dir(), self.settings.texconv_path, out_type='png')
        if copy_flags and (path / (path.stem + '.flags')).is_file():
            self._copy((path / (path.stem + '.flags')), self._texture_dir())
    
    def compress_textures(self, only_new:bool=False):
        texture_dir = self._texture_dir()
        textures = list(texture_dir.glob('*.png'))
        self.prepare_progress_bar(len(textures))
        for file in textures:
            self.progress_bar['value'] += 1
            self.progress_bar.update()
            if only_new:
                try:
                    if file.stat().st_mtime < (file.parent / f'{file.stem}.dds').stat().st_mtime:
                        print(f'"{file.stem}.dds" is newer than "{file.name}". Skipping.')
                        continue
                except FileNotFoundError:
                    pass
            print(f'Compressing "{file}"…')
            dds.convert(file, texture_dir, self.settings.texconv_path)
        self.restore_progress_bar()
    
    def create_dds_descriptors(self):
        texture_dir = self._texture_dir()
        textures = list(texture_dir.glob('*.dds'))
        self.prepare_progress_bar(len(textures))
        for file in textures:
            self.progress_bar['value'] += 1
            self.progress_bar.update()
            exists = (file.parent / (file.name + '.json')).is_file()
            if not (file.parent / (file.name + '.json')).is_file():
                print(f'Describing "{file}"…')
                dds_json.create_description(file)
        self.restore_progress_bar()
        if not textures:
            raise FileNotFoundError
    
    def create_texture_cfg(self, original:str|None=None):
        cfg = configparser.ConfigParser()
        if not original:
            try:
                source_folder:Path = Path(self.project.origin) / 'SimObjects' / 'Airplanes' / Path(self.project.base_container).name
            except KeyError:
                raise ConfigurationError('Project improperly configured: origin or base_container not set.')
            for folder in source_folder.glob('texture*'):
                # fallback:Path = Path('..') / self.project.base_container / folder.name
                original = folder / 'texture.cfg'
                break
            # cfg.add_section('fltsim')
            # cfg['fltsim']['fallback.1'] = str(PureWindowsPath(fallback))
        cfg.read(original)
        fallbacks = list(cfg['fltsim'].keys())
        fallbacks.reverse()
        for fb in fallbacks:
            nothing, n = fb.split('.')
            n = int(n) + 1
            cfg['fltsim'][f'fallback.{n}'] = cfg['fltsim'][fb]
        cfg['fltsim']['fallback.1'] = str(PureWindowsPath('..', '..', Path(original).parent.parent.name, Path(original).parent.name))
        file_name = self._texture_dir() / 'texture.cfg'
        with file_name.open('w') as f:
            cfg.write(f)
    
    def copy_thumbnail_placeholder(self):
        thumbnail.placeholder(self._texture_dir())
        thumbnail.resize_thumbnail(self._texture_dir() / 'thumbnail.jpg')
    
    def resize_thumbnail(self):
        thumbnail.resize_thumbnail(self._texture_dir() / 'thumbnail.jpg')
    
    def create_aircraft_cfg(self, path:str|None=None):
        kwargs = {}
        try:
            if self.project.title:
                variation_name = self.project.title
            else:
                raise KeyError
        except KeyError:
            variation_name = 'Alternative livery'
        try:
            if self.project.suffix:
                suffix = self.project.suffix
            else:
                raise KeyError
        except KeyError:
            suffix = 'livery'
        try:
            kwargs['model'] = self.project.include_model
        except KeyError:
            pass
        try:
            kwargs['panel'] = self.project.include_panel
        except KeyError:
            pass
        try:
            kwargs['sound'] = self.project.include_sound
        except KeyError:
            pass
        try:
            kwargs['texture'] = self.project.include_texture
        except KeyError:
            pass
        try:
            if self.project.tail_number:
                kwargs['tail_number'] = self.project.tail_number
            else:
                raise KeyError
        except KeyError:
            pass
        try:
            if self.project.creator:
                kwargs['creator'] = self.project.creator
            else:
                raise KeyError
        except KeyError:
            pass
        try:
            if self.project.display_name:
                kwargs['ui_variation'] = self.project.display_name
            else:
                raise KeyError
        except KeyError:
            pass
        
        if path is None:
            try:
                path = Path(self.project.origin) / 'SimObjects' / 'Airplanes' / Path(self.project.base_container).name / 'aircraft.cfg'
            except KeyError:
                raise ConfigurationError('Project improperly configured: origin or base_container not set.')
        else:
            self.project.base_container = Path(path).parent
        aircraft = aircraft_cfg.from_original(path, base_container=self.project.base_container,
                                            variation_name=variation_name, suffix=suffix, **kwargs)
        file_name = Path(self.project.file).parent / 'aircraft.cfg'
        with file_name.open('w') as file:
            file.write(aircraft)
    
    def create_empty_panel(self):
        panel_cfg.create_empty(Path(self.project.file).parent / 'panel' / 'panel.cfg')
    
    def copy_panel(self, path:str|None=None):
        if not path:
            try:
                path = Path(self.project.origin) / 'SimObjects' / 'Airplanes' / Path(self.project.base_container).name / 'panel' / 'panel.cfg'
            except KeyError:
                raise ConfigurationError('Project improperly configured: origin or base_container not set.')
        panel_cfg.copy_original(Path(self.project.file).parent / 'panel' / 'panel.cfg', path)
    
    def set_registration_colors(self):
        if not (Path(self.project.file).parent / 'panel' / 'panel.cfg').is_file():
            self.create_empty_panel()
        try:
            stroke = self.project.registration_stroke_color
        except KeyError:
            stroke = ''
        try:
            stroke_size = self.project.registration_stroke_size
        except KeyError:
            stroke_size = 0
        try:
            if stroke_size:
                panel_cfg.set_registration_colors(Path(self.project.file).parent / 'panel' / 'panel.cfg',
                                        font=self.project.registration_font_color,
                                        stroke=stroke,
                                        stroke_size=stroke_size)
            else:
                panel_cfg.set_registration_colors(Path(self.project.file).parent / 'panel' / 'panel.cfg',
                                        font=self.project.registration_font_color,
                                        stroke=stroke)
        except KeyError:
            raise ConfigurationError('Registration font color not configured.')
    
    def create_manifest(self, path:str|None=None):
        kwargs = {}
        try:
            if self.project.title:
                kwargs['title'] = self.project.title
            else:
                raise KeyError
        except KeyError:
            kwargs['title'] = 'Alternative livery'
        try:
            if self.project.manufacturer:
                kwargs['manufacturer'] = self.project.manufacturer
            else:
                raise KeyError
        except KeyError:
            pass
        try:
            if self.project.creator:
                kwargs['creator'] = self.project.creator
            else:
                raise KeyError
        except KeyError:
            pass
        try:
            if self.project.version:
                kwargs['version'] = self.project.version
            else:
                raise KeyError
        except KeyError:
            kwargs['version'] = '0.1'
        try:
            kwargs['minimum_game_version'] = self.project.minimum_game_version
        except KeyError:
            pass
        
        if path is None:
            try:
                path = Path(self.project.origin, 'manifest.json')
            except KeyError:
                raise ConfigurationError('Project improperly configured: origin not set.')
        manifest.from_original(path, Path(self.project.file).parent / 'manifest.json', **kwargs)
    
    def package(self, path:str):
        thread = Runner(self._do_package, path)
        thread.start()
        self.monitor(thread)
    
    def _do_package(self, path:str):
        path:Path = Path(path)
        path.mkdir(exist_ok=True)
        try:
            airplane_path:Path = path / 'SimObjects' / 'Airplanes' / self.project.airplane_folder
            airplane_path.mkdir(parents=True, exist_ok=True)
        except KeyError:
            self.error = ConfigurationError('Airplane folder not set.')
            raise self.error
        try:
            suffix = self.project.suffix
        except KeyError:
            suffix = 'livery'
        
        # aircraft.cfg
        if not Path(self.project.file, 'aircraft.cfg').is_file():
            self.create_aircraft_cfg()
            if  (airplane_path / 'aircraft.cfg').exists():
                (airplane_path / 'aircraft.cfg').unlink()
            self._move(Path(self.project.file).parent / 'aircraft.cfg', airplane_path)
        else:
            self._copy(Path(self.project.file, 'aircraft.cfg'), airplane_path)
        
        # Copy panel folder if needed
        if self.project.include_panel:
            self._copy(Path(self.project.file).parent / 'panel', airplane_path / f'panel.{suffix}')
        
        # Copy sound folder if needed
        if self.project.include_sound:
            self._copy(Path(self.project.file).parent / 'sound', airplane_path / f'sound.{suffix}')
        
        # Copy model files if needed
        if self.project.include_model:
            model_source:Path = Path(self.project.file).parent / 'model'
            model_dest:Path = Path(airplane_path, f'model.{suffix}')
            model_dest.mkdir(exist_ok=True)
            for pattern in ('model.cfg', '*.xml', '*.gltf', '*.bin'):
                for file in model_source.glob(pattern):
                    self._copy(file, model_dest)
        
        # Copy texture files if needed
        if self.project.include_texture:
            texture_source:Path = self._texture_dir()
            texture_source.mkdir(exist_ok=True)
            texture_dest:Path = Path(airplane_path, f'texture.{suffix}')
            texture_dest.mkdir(exist_ok=True)
            if not Path(texture_source, 'texture.cfg').exists():
                self.create_texture_cfg()
                if (texture_dest / 'texture.cfg').exists():
                    (texture_dest / 'texture.cfg').unlink()
                self._move(Path(texture_source, 'texture.cfg'), texture_dest)
            else:
                self._copy(texture_source / 'texture.cfg', texture_dest)
            if self.settings.compress_textures_on_build or \
                (len(list(texture_source.glob('*.dds'))) == 0 and len(list(texture_source.glob('*.png'))) > 0):
                self.compress_textures(only_new=True)
                self.create_dds_descriptors()
            for pattern in (
                'texture.cfg',
                '*.dds',
                '*.dds.json',
                '*.dds.flags',
                'thumbnail.jpg',
                'thumbnail-small.jpg'
            ):
                for file in texture_source.glob(pattern):
                    self._copy(file, texture_dest)
        
        # Create or copy manifest.json
        manifest_file = Path(self.project.file).parent / 'manifest.json'
        if not manifest_file.is_file():
            self.create_manifest()
            if (path / 'manifest.json').exists():
                (path / 'manifest.json').unlink()
            self._move(manifest_file, path)
        else:
            self._copy(manifest_file, path)
        
        # Create layout.json
        self.update_layout(path / 'layout.json')
    
    def update_layout(self, path:str):
        layout.create_layout(Path(path).parent)
