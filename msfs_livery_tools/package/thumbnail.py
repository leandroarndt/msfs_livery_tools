"""Thumbnail management"""
from pathlib import Path
from PIL import Image
import shutil
import __main__

def placeholder(path:str|Path):
    shutil.copy(__main__.RESOURCES_DIR / 'thumbnail.jpg', path)

def gap(image:Image, size:tuple[int])->dict:
    ratio = max(size[0] / image.size[0], size[1] / image.size[1])
    return {
        'xmin': int(((image.size[0] * ratio - size[0]) / 2) / ratio),
        'xmax': int((image.size[0] * ratio - (image.size[0] * ratio - size[0]) / 2) / ratio),
        'ymin': int(((image.size[1] * ratio - size[1]) / 2) / ratio),
        'ymax': int((image.size[1] * ratio - (image.size[1] * ratio - size[1]) / 2) / ratio),
    }

def resize_thumbnail(path:str|Path):
    # https://docs.flightsimulator.com/html/Samples_And_Tutorials/Tutorials/Creating_A_Livery_Package.ht
    path = Path(path)
    size_big = (1618, 582)
    size_small = (600, 216)
    
    # Search for in-game capture
    if Path(path.parent, f'{path.stem}.png').exists():
        path = Path(path.parent, f'{path.stem}.png')
        thumbnail = Image.open(path)
        thumbnail.save(Path(path.parent, f'{path.stem}.jpg'))
        path.unlink() # Prevents converting to DDS
    else:
        thumbnail = Image.open(path)
        
    # Resizes to small
    resize_gap = gap(thumbnail, size_small)
    resized = thumbnail.resize(size_small, box=(resize_gap['xmin'], resize_gap['ymin'], resize_gap['xmax'], resize_gap['ymax']))
    resized.save(Path(path).parent / 'thumbnail_small.jpg')

    # Resizes to big
    resize_gap = gap(thumbnail, size_big)
    resized = thumbnail.resize(size_big, box=(resize_gap['xmin'], resize_gap['ymin'], resize_gap['xmax'], resize_gap['ymax']))
    resized.save(Path(path).parent / 'thumbnail.jpg')
