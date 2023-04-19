"""Deals with DDS compression using Microsoft's texconv (https://github.com/Microsoft/DirectXTex/wiki/Texconv)."""
import os, subprocess, json

def convert(input:str, output_dir:str, texconv_path:str, out_type:str='dds', out_format:str=''):
    """Converts image types."""
    if out_format:
        proc = subprocess.run([texconv_path, '-o', output_dir, '-ft', out_type, '-f', out_format, input])
    else:
        proc = subprocess.run([texconv_path, '-o', output_dir, '-ft', out_type, input])
    return proc.returncode

def from_glft(input_gltf:str, input_dir:str, output_dir:str, texconv_path:str, type:str='png'):
    """Converts glTF DDS textures into another format."""
    # Open glTF
    f = open(input_gltf)
    gltf = json.load(f)
    f.close()
    
    # Uncompress
    for image in gltf['images']:
        try:
            # uncompresses DDS into PNG
            convert(
                    os.path.join(input_dir, image['uri']),
                    output_dir, texconv_path, type
            )
            
        except KeyError: # not compressed, continue working!
            pass
