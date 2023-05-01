"""Manipulates aircraft.cfg."""
import configparser, io
import io
from pathlib import Path
from .cfg_tools import get_section

def from_original(file_name:str, base_container:str, variation_name, suffix:str,
                    model:bool=False, panel:bool=False, sound:bool=False, texture:bool=True,
                    tail_number:str|None = None, creator:str|None=None, ui_variation:str|None=None):
    """Returns aircraft.cfg based on original and parameters."""
    
    # Reads the original aircraft.cfg
    original = configparser.ConfigParser()
    original.read(file_name)
    
    new_cfg = configparser.ConfigParser()
    
    # Defines the original aircraft virtual file system dir
    variation_section = get_section('VARIATION', original)
    variation_section['base_container'] = base_container
    new_cfg['VARIATION'] = variation_section
    
    # Updates FLTSIM.
    fltsim = get_section('FLTSIM.0', original)
    fltsim['title'] = f'"{variation_name}"'
    fltsim['model'] = f'"{suffix if model else ""}"'
    fltsim['panel'] = f'"{suffix if panel else ""}"'
    fltsim['sound'] = f'"{suffix if sound else ""}"'
    fltsim['texture'] = f'"{suffix if texture else ""}"'
    if ui_variation:
        fltsim['ui_variation'] = f'"{ui_variation}"'
    else:
        fltsim['ui_variation'] = f'"{variation_name}"'
    if tail_number:
        fltsim['atc_id'] = f'"{tail_number}"'
    if creator:
        fltsim['ui_createdby'] = f'"{creator}"'
    new_cfg['FLTSIM.0'] = fltsim
    
    cfg = io.StringIO()
    new_cfg.write(cfg)
    
    return cfg.getvalue()

def write_aircraft_cfg(destination_file:str, original_file:str='', *args, **kwargs):
    """Writes a new aircraft.cfg"""
    contents = from_original(original_file, *args, **kwargs)
    Path(destination_file).write_text(contents)