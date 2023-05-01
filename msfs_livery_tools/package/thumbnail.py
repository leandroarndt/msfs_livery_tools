"""Thumbnail management"""
from pathlib import Path
from PIL import Image
import shutil
import __main__

def placeholder(path:str|Path):
    shutil.copy(__main__.RESOURCES_DIR / 'thumbnail.jpg', path)

def resize_thumbnail(path:str|Path):
    size = (600, 216)
    thumbnail = Image.open(path)
    ratio = max(size[0] / thumbnail.size[0], size[1] / thumbnail.size[1])
    gap = {
        'xmin': int(((thumbnail.size[0] * ratio - size[0]) / 2) / ratio),
        'xmax': int((thumbnail.size[0] * ratio - (thumbnail.size[0] * ratio - size[0]) / 2) / ratio),
        'ymin': int(((thumbnail.size[1] * ratio - size[1]) / 2) / ratio),
        'ymax': int((thumbnail.size[1] * ratio - (thumbnail.size[1] * ratio - size[1]) / 2) / ratio),
    }
    resized = thumbnail.resize((600, 216), box=(gap['xmin'], gap['ymin'], gap['xmax'], gap['ymax']))
    resized.save(Path(path).parent / 'thumbnail-small.jpg')