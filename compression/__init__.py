"""_summary_

* Texturas:
    In [13]: com_dds['textures'][0]
    Out[13]: {'extensions': {'MSFT_texture_dds': {'source': 0}}}

    In [39]: sem_dds['textures'][0]
    Out[39]: {'sampler': 0, 'source': 0}
    
* Imagens:
    In [43]: com_dds['images'][0]
    Out[43]:
    {'uri': 'CAP10C_AIRFRAME_WING_ALBD.PNG.DDS',
    'extras': 'ASOBO_image_converted_meta'}

    In [44]: sem_dds['images'][0]
    Out[44]:
    {'mimeType': 'image/png',
    'name': 'CAP10C_AIRFRAME_WING_NORM.PNG',
    'uri': 'CAP10C_AIRFRAME_WING_NORM_PNG.png'}

* Extensões requeridas:
    In [15]: com_dds['extensionsRequired']
    Out[15]: ['MSFT_texture_dds']
    
    In [40]: sem_dds['extensionsRequired']
    ---------------------------------------------------------------------------
    KeyError                                  Traceback (most recent call last)
    Cell In[40], line 1
    ----> 1 sem_dds['extensionsRequired']

    KeyError: 'extensionsRequired'

* Extensões utilizadas:
    In [18]: sem_dds['extensionsUsed']
    Out[18]: ['ASOBO_normal_map_convention']

    In [19]: com_dds['extensionsUsed']
    Out[19]:
    ['ASOBO_normal_map_convention',
    'ASOBO_material_detail_map',
    'ASOBO_material_windshield',
    'ASOBO_material_draw_order',
    'ASOBO_material_blend_gbuffer',
    'ASOBO_material_shadow_options',
    'ASOBO_material_fresnel_fade',
    'ASOBO_tags',
    'ASOBO_material_invisible',
    'MSFT_texture_dds',
    'ASOBO_asset_optimized']
        


"""