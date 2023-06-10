from gltf_python_io.imp.gltf2_io_binary import BinaryData
from gltf_python_io.imp.gltf2_io_gltf import glTFImporter
from gltf_python_io.com.gltf2_io import MeshPrimitive, Accessor
from gltf_python_io.com.gltf2_io_constants import ComponentType
from PIL import Image, ImageDraw
import numpy, drawsvg

def draw_uv_map(image, model:glTFImporter, primitive:MeshPrimitive,
                fill=(127,127,127,127), outline=(0,0,0,255), svg_size:int=2048,
                fill_opacity=0.3, tc_map:int=0):
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
    
    
    
    if isinstance(image, Image.Image):
        size = image.size[0]
        ratio = image.size[0] / component_size
        draw = ImageDraw.Draw(image)
        draw_function = lambda coord: draw.polygon(coord, fill=fill, outline=outline)
    else:
        size = svg_size
        ratio = svg_size / component_size
        draw_function = lambda coord: image.append(
            drawsvg.Lines(
                coord[0][0], coord[0][1],
                coord[1][0], coord[1][1],
                coord[2][0], coord[2][1],
                close=True,
                fill=fill,
                stroke=outline,
                fill_opacity=fill_opacity
            )
        )
    
    for i in range(count):
        vertexes = (indices[i*3+offset][0], indices[i*3+1+offset][0], indices[i*3+2+offset][0])
        draw_function([
            (tc[vertexes[0]][0]*ratio+displacement*size, tc[vertexes[0]][1]*ratio+displacement*size),
            (tc[vertexes[1]][0]*ratio+displacement*size, tc[vertexes[1]][1]*ratio+displacement*size),
            (tc[vertexes[2]][0]*ratio+displacement*size, tc[vertexes[2]][1]*ratio+displacement*size),
        ])
