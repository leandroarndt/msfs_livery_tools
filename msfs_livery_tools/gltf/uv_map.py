from pathlib import Path
from gltf_python_io.imp.gltf2_io_binary import BinaryData
from gltf_python_io.imp.gltf2_io_gltf import glTFImporter
from gltf_python_io.com.gltf2_io import MeshPrimitive, Accessor
from gltf_python_io.com.gltf2_io_constants import ComponentType
from PIL import Image, ImageDraw
import queue
import numpy
from . import search_image

def draw_uv_map(image:Image, model:glTFImporter, primitive:MeshPrimitive,
                fill=(127,127,127,127), outline=(0,0,0,255), tc_map:int=0):
    """Draws a UV map at image based on data from primitive. `model` should be a glTFImporter,
    since the common glTF class does not have a `data` attribute. Tries to support Asobo
    undocumented extension.

    Args:
        image (Image): _description_
        model (gltf2_io_gltf.glTFImporter): _description_
        primitive (gltf_io.MeshPrimitive): _description_
        map (int, defaults to 0): which UV map to use (usually 0 or 1 on MSFS glTF files)
    """
    
    if f'TEXCOORD_{tc_map}' not in primitive.attributes.keys():
        raise ValueError(f'Primitive does not have texture coordinates map #{tc_map}.')
    
    if primitive.mode != 4:
        raise NotImplemented('Can only work with triangles now.')
    
    if not hasattr(model, 'data'):
        if not hasattr(model, 'read'):
            model.data = model # This should be populated on a glTFImporter, but we should be tolerant to glTF class
        model.read()
    
    tc_accessor:Accessor = model.data.accessors[primitive.attributes[f'TEXCOORD_{tc_map}']]
    indices = BinaryData.decode_accessor_obj(model, model.data.accessors[primitive.indices])
    tc = BinaryData.decode_accessor_obj(model, model.data.accessors[primitive.attributes[f'TEXCOORD_{tc_map}']])
    
    if 'ASOBO_primitive' in primitive.extras.keys():
        count = primitive.extras['ASOBO_primitive']['PrimitiveCount']
        if 'StartIndex' in primitive.extras['ASOBO_primitive'].keys():
            offset = primitive.extras['ASOBO_primitive']['StartIndex']
        else:
            offset = 0
    else:
        count = indices.count
        offset = 0
    
    match tc_accessor.component_type:
        case 5120:
            component_size = 255
            displacement = 0.5
        case 5121:
            component_size = 255
            displacement = 0
        case 5122:
            component_size = 65535 // 6
            displacement = -0.5
        case 5123:
            component_size = 65535
            displacement = 0
        case 5125:
            component_size = 65535
            displacement = 0
        case 5126:
            component_size = 1
            displacement = 0
    
    if 'ASOBO_primitive' in primitive.extras.keys():
        # MSFS compiles to 5122 (int), but uses 5126 (float16) as it should be
        component_size = 1
        displacement = 0
        # Hack component type
        to_type_code = ComponentType.to_type_code
        def type_code(*args, **kwargs):
            return 'e'
        ComponentType.to_type_code = type_code
        to_numpy_dtype = ComponentType.to_numpy_dtype
        def numpy_dtype(*args, **kwargs):
            return numpy.float16
        ComponentType.to_numpy_dtype = numpy_dtype
        tc = BinaryData.decode_accessor_obj(model, model.data.accessors[primitive.attributes[f'TEXCOORD_{tc_map}']])
        ComponentType.to_type_code = to_type_code
        ComponentType.to_numpy_dtype = to_numpy_dtype
    
    ratio = image.size[0] / component_size
    
    draw = ImageDraw.Draw(image)
    
    for i in range(count):
        vertexes = (indices[i*3+offset][0], indices[i*3+1+offset][0], indices[i*3+2+offset][0])
        draw.polygon([
            (tc[vertexes[0]][0]*ratio+displacement*image.size[0], tc[vertexes[0]][1]*ratio+displacement*image.size[1]),
            (tc[vertexes[1]][0]*ratio+displacement*image.size[0], tc[vertexes[1]][1]*ratio+displacement*image.size[1]),
            (tc[vertexes[2]][0]*ratio+displacement*image.size[0], tc[vertexes[2]][1]*ratio+displacement*image.size[1]),
        ], fill=fill, outline=outline)

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
