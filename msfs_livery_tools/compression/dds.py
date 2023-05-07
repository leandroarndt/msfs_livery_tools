"""Deals with DDS compression using Microsoft's texconv (https://github.com/Microsoft/DirectXTex/wiki/Texconv)."""
import subprocess, json
from pathlib import Path

def convert(input:str|Path, output_dir:str|Path, texconv_path:str|Path, out_type:str='dds', out_format:str='',
            overwrite:bool=True):
    """Converts image types."""
    command = [texconv_path, '-o', output_dir, '-ft', out_type,]
    if out_format:
        command += ['-f', out_format]
    if overwrite:
        command += ['-y']
    command += [input]
    proc = subprocess.run(command)
    return proc.returncode

def from_glft(input_gltf:str|Path, input_dir:str|Path, output_dir:str|Path, texconv_path:str|Path, out_format:str='png'):
    """Converts glTF DDS textures into another format."""
    # Open glTF
    with Path(input_gltf).open('r') as f:
        gltf = json.load(f)
    
    # Uncompress
    for image in gltf['images']:
        try:
            # uncompresses DDS into PNG
            convert(Path(input_dir) / image['uri'], output_dir, texconv_path, out_format)
            
        except KeyError: # not compressed, continue working!
            pass
