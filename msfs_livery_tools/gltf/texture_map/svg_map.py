from pathlib import Path
from gltf_python_io.imp.gltf2_io_gltf import glTFImporter
import queue, drawsvg, colorsys
from .uv_map import draw_uv_map
from .. import search_image

def draw_svg_map(dest:str|Path, model_file:str|Path, texture_file:str|Path|None=None,
                            fill=None, outline='black', fill_opacity=0.3, size:int=2048,
                            tc_map:int=0, queue:queue.Queue|None=None)->int:
    dest = Path(dest)
    model_file = Path(model_file)
    model = glTFImporter(model_file, {'import_user_extensions': []})
    model.read()
    n = 0
    
    images = []
    if texture_file:
        images = [Path(texture_file).with_suffix('.DDS').name]
    else:
        for image in model.data.images:
            images.append(image.uri)
    
    for image in images:
        n += 1
        print(f'Unwrapping meshes for texture "{image}"…')
        
        base_name = Path(image)
        while ('.' in base_name.name):
            base_name = base_name.with_suffix('')
        file = (dest / base_name.name).with_suffix('.svg')
        
        drawing = drawsvg.Drawing(size, size)
        
        meshes = search_image.mesh_primitive_with_image_name(model, image)
        primitive_count = 0
        for mesh in meshes.values():
            primitive_count += len(mesh)
        h = 0
        for mesh in meshes:
            mesh_group = drawsvg.Group(id=model.data.meshes[mesh].name)
            for primitive in meshes[mesh]:
                h += 1 / primitive_count
                group = drawsvg.Group(id=f'{model.data.meshes[mesh].name}_{primitive}')
                
                if not fill:
                    group_fill = colorsys.hsv_to_rgb(h, 1, 1)
                    group_fill = (int(group_fill[0] * 255), int(group_fill[1] * 255), int(group_fill[2] * 255))
                    group_fill = f'rgb({group_fill[0]},{group_fill[1]},{group_fill[2]})'
                else:
                    if not isinstance(group_fill, str):
                        group_fill = f'rgb({group_fill[0]},{group_fill[1]},{group_fill[2]})'
                    group_fill = fill
                
                if not isinstance(outline, str):
                    outline = f'rgb({outline[0]},{outline[1]},{outline[2]})'
                
                draw_uv_map(
                    group, model, model.data.meshes[mesh].primitives[primitive],
                    fill=group_fill, outline=outline, fill_opacity=fill_opacity, svg_size=size
                )
                mesh_group.append(group)
            drawing.append(mesh_group)
        
        if queue:
            try:
                queue.put_nowait(f'Saving "{file.name}".')
            except:
                pass
        print(f'Saving "{file.name}".')
        drawing.save_svg(file)
    
    return n
