"""Creates layout.json"""
from pathlib import Path
from .description_tools import win_time
import json

def create_layout(package_dir:str):
    """Creates layout.json at `package_dir`.

    Args:
        package_dir (str): package directory path.
    """
    layout = {'content': []}
    for file in Path(package_dir).glob('**/*'):
        if file.is_file():
            layout['content'].append({
                'path': file.relative_to(package_dir).as_posix(),
                'size': Path(file).stat().st_size,
                'date': win_time(Path(file).stat().st_mtime_ns),
            })
    with Path(package_dir, 'layout.json').open('w') as f:
        json.dump(layout, f, indent=4)