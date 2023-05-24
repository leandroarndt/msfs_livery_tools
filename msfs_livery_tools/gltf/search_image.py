from gltf_python_io.com.gltf2_io import Gltf, MeshPrimitive, Mesh, Material, Texture, Image

def importer_aware(func):
    def wrapper(model, *args, **kwargs):
        if hasattr(model, 'data'): # It's an importer
            model = model.data
        return func(model, *args, **kwargs)
    return wrapper

@importer_aware
def image_with_name(model:Gltf, name:str)->list[int]:
    image:Image
    
    image_list = []
    for i, image in enumerate(model.images):
        if image.uri.lower() == name.lower():
            image_list.append(i)
    
    return image_list

@importer_aware
def texture_with_image_name(model:Gltf, name:str)->list[int]:
    texture:Texture
    
    image_list = image_with_name(model, name)
    texture_list = []
    for i, texture in enumerate(model.textures):
        if texture.extensions['MSFT_texture_dds']['source'] in image_list:
            texture_list.append(i)
    
    return texture_list

@importer_aware
def material_with_image_name(model:Gltf, name:str)->list[int]:
    material:Material
    
    texture_list = texture_with_image_name(model, name)
    material_list = []
    for i, material in enumerate(model.materials):
        try:
            if material.pbr_metallic_roughness.base_color_texture.index in texture_list:
                material_list.append(i)
        except AttributeError:
            pass
    
    return material_list

@importer_aware
def mesh_primitive_with_image_name(model:Gltf, name:str)->dict:
    mesh:Mesh
    primitive:MeshPrimitive
    
    material_list = material_with_image_name(model, name)
    meshes = {}
    for i1, mesh in enumerate(model.meshes):
        for i2, primitive in enumerate(mesh.primitives):
            if primitive.material in material_list:
                if i1 not in meshes.keys():
                    meshes[i1] = [i2]
                else:
                    meshes[i1].append(i2)
    
    return meshes
