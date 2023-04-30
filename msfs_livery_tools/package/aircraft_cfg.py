"""Manipulates aircraft.cfg."""
import configparser, io
import io
from pathlib import Path
from .cfg_tools import get_section

def from_original(file_name:str, base_container:str, variation_name, suffix:str, model:bool=False,
                    panel:bool=False, sound:bool=False, texture:bool=True,
                    tail_number:str='ASGX'):
    """Returns aircraft.cfg based on original and parameters."""
    
    # Reads the original aircraft.cfg
    original = configparser.ConfigParser()
    original.read(file_name)
    
    # Defines the original aircraft virtual file system dir
    variation_section = get_section('VARIATION', original)
    variation_section['base_container'] = base_container
    
    # Updates FLTSIM.
    fltsim = get_section('FLTSIM.0', original)
    fltsim['title'] = f'"{variation_name}"'
    fltsim['model'] = f'"{suffix if model else ""}"'
    fltsim['panel'] = f'"{suffix if panel else ""}"'
    fltsim['sound'] = f'"{suffix if sound else ""}"'
    fltsim['texture'] = f'"{suffix if texture else ""}"'
    fltsim['atc_id'] = f'"{tail_number}"'
    
    cfg = io.StringIO()
    original.write(cfg)
    
    return cfg.getvalue()

def write_aircraft_cfg(destination_file:str, original_file:str='', *args, **kwargs):
    """Writes a new aircraft.cfg"""
    contents = from_original(original_file, *args, **kwargs)
    Path(destination_file).write_text(contents)