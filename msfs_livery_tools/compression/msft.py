"""Removes Microsoft's DDS extensions in order to be importable by Asobo's MSFS Blender importer.

Uses Microsoft's texconv (https://github.com/Microsoft/DirectXTex/wiki/Texconv) to uncompress/compress images."""
import os, json, shutil
from . import dds

def uncompress(input_file:str, output_file:str, texconv_path:str, texture_input:str, texture_output:str):
    """Removes DDS compression from a glTF file."""
    
    # Loads glTF from file
    f = open(input_file)
    gltf:dict = json.load(f)
    f.close()
    
    # Remove MSFT_texture_dds from required extensions
    try:
        gltf['extensionsRequired'].remove('MSFT_texture_dds')
    except (KeyError, ValueError):
        raise ValueError('"{file_name}" does not require MSFT_texture_dds extension.')
    
    # Remove MSFT_texture_dds from used extensions
    try:
        gltf['extensionsUsed'].remove('MSFT_texture_dds')
    except (KeyError, ValueError):
        raise ValueError('"{file_name}" does not use MSFT_texture_dds extension.')
    
    # Remove MSFT_texture_dds from texture definitions
    for texture in gltf['textures']:
        try:
            source = texture['extensions']['MSFT_texture_dds']['source']
            texture['sampler'] = source
            texture['source'] = source
            del texture['extensions']
        except KeyError: # not compressed, continue working!
            pass
    
    # Uncompresses images and correct glTF
    for image in gltf['images']:
        name, type = os.path.splitext(image['uri'])
        if type.upper() == '.DDS':
            try:
                image.pop('extras')
                image['mimeType'] = 'image/png'
                image['name'] = name
                compressed_file = image['uri']
                if name.upper().endswith('.PNG'):
                    image['uri'] = name
                else:
                    image['uri'] = f'{name}.png'
                    
                # uncompresses DDS into PNG
                dds.convert(
                            os.path.join(texture_input, compressed_file),
                            texture_output, texconv_path, 'png'
                )
            except KeyError: # not compressed, continue working!
                pass
    
    # Write the resulting glTF
    f = open(output_file, 'w', encoding='utf-8')
    json.dump(gltf, f, indent=4)
    f.close()
    
    # Copy the binary file to the same location of the new glTF
    shutil.copy(f'{os.path.splitext(input_file)[0]}.bin', os.path.split(output_file)[0])
