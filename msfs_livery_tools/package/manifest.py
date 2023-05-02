"""Deals with manifest.json"""
import json
from pathlib import Path

def create_manifest(file_name:str, title:str, manufacturer:str, creator:str, version:str='1.0',
                    minimum_game_version:str='1.0.0', dependencies:list=[]):
    manifest = {
        'dependencies': dependencies,
        'content_type': 'AIRCRAFT',
        'title': title,
        'manufacturer': manufacturer,
        'creator': creator,
        'package_version': version,
        'minimum_game_version': minimum_game_version,
        'release_notes': {
            'neutral': {
                'LastUpdate': '',
                'OlderHistory': ''
            }
        }
    }
    file = Path(file_name).open('w', encoding='utf8')
    json.dump(manifest, file, indent=4, ensure_ascii=False)
    file.close()

def from_original(original_file:str, destination_file:str, **kwargs):
    with Path(original_file).open(encoding='utf8') as original:
        manifest = json.load(original)
    manifest['total_package_size'] = 0
    for file in Path(destination_file).parent.glob('**/*'):
        if file.is_file():
            if not (file.name.lower() == 'layout.json' or file.name.lower() == 'manifest.json'):
                manifest['total_package_size'] += Path(file).stat().st_size
    manifest['total_package_size'] = f'{manifest["total_package_size"]:020d}'
    manifest.update(kwargs)
    destination = Path(destination_file).open('w', encoding='utf8')
    json.dump(manifest, destination, indent=4)
    destination.close()
