"""Builds a livery tree structure with the proper config files."""
from pathlib import Path

def dir_tree(base_dir:str, suffix:str, aircraft_name:str, model_dir:bool=False,
                panel_dir:bool=False, texture_dir:bool=True, audio_dir:bool=False,
                overwrite=True):
    """Creates a directory structure for the livery package."""
    base_dir.replace('\\', '/') # We're going to use pathlib
    aircraft_dir = f'{base_dir}/SimObjects/Airplanes/{aircraft_name}'
    try:
        Path(base_dir).mkdir(parents=True)
    except FileExistsError:
        pass
    if not Path(base_dir).is_dir():
        raise ValueError(f'"{base_dir}" is not a directory!')
    
    try:
        Path(aircraft_dir).mkdir(parents=True)
        
        if model_dir:
            Path(f'{aircraft_dir}/model.{suffix}').mkdir()
        if panel_dir:
            Path(f'{aircraft_dir}/panel.{suffix}').mkdir()
        if texture_dir:
            Path(f'{aircraft_dir}/texture.{suffix}').mkdir()
        if audio_dir:
            Path(f'{aircraft_dir}/audio.{suffix}').mkdir()
            
    except FileExistsError as e:
        if not overwrite:
            raise e
