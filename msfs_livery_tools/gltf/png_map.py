from pathlib import Path
from gltf_python_io.imp.gltf2_io_gltf import glTFImporter
from PIL import Image
import queue
from . import search_image
from .uv_map import *

def draw_uv_for_texture(image:Image, texture_name:str, model:glTFImporter, fill=(127,127,127,127), outline=(0,0,0,255), tc_map:int=0):
    for mesh, primitives in search_image.mesh_primitive_with_image_name(model, texture_name).items():
        for primitive in primitives:
            draw_uv_map(image, model, model.data.meshes[mesh].primitives[primitive], fill, outline, tc_map)

def draw_uv_on_texture(file:str|Path, model:glTFImporter, fill=(127,127,127,127), outline=(0,0,0,255), tc_map:int=0)->Image:
    file = Path(file)
    image = Image.open(file)
    draw_uv_for_texture(image, file.name, model, fill, outline, tc_map)
    
    return image

def draw_uv_layers_for_texture(dest:str|Path, texture_file:str|Path, model_file:str|Path, fill=(127,127,127,127), outline=(0,0,0,255), tc_map:int=0, queue:queue.Queue|None=None)->int:
    dest = Path(dest)
    base_name = Path(texture_file)
    while ('.' in base_name.name):
        base_name = Path(base_name).with_suffix('')
    base_name = base_name.name
    texture_file = Path(texture_file)
    texture_name = texture_file.with_suffix('.DDS').name
    texture_image = Image.open(texture_file)
    model_file = Path(model_file)
    model = glTFImporter(model_file, {'import_user_extensions': []})
    model.read()
    
    print(f'Unwrapping textures for {texture_name}.')
    i = 0
    meshes = search_image.mesh_primitive_with_image_name(model, texture_name).items()
    for mesh, primitives in meshes:
        for primitive in primitives:
            file = dest / f'{base_name} - {i} - {model.data.meshes[mesh].name}.png'
            uv_image = Image.new('RGBA', size=texture_image.size, color=(0,0,0,0))
            draw_uv_map(uv_image, model, model.data.meshes[mesh].primitives[primitive], fill, outline, tc_map)
            if queue:
                try:
                    queue.put_nowait(f'Saving "{file.name}".')
                except:
                    pass
            print(f'Saving {file}.')
            uv_image.save(file)
            i += 1
    
    return len(meshes)
