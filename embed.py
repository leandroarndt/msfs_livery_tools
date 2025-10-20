from pathlib import Path
import shutil, zipfile, argparse, os

dest = Path('dist')
source_dir = Path('msfs_livery_tools')
base_script = Path('livery_tools.py')
shell_script = Path('MSFS Livery Tools.bat')
site_packages = Path('venv', 'Lib', 'site-packages')
python_zip = Path('python.zip')

def data_files(folder:str, patterns:list[str])->tuple:
    files = []
    path = Path(folder)
    for pattern in patterns:
        for file in path.glob(pattern):
            files.append(file)
    return (folder, files)

if __name__ == '__main__':
    if Path(os.getcwd()).resolve() != Path(__file__).parent.resolve():
        print(f'This script should not be run out of "{Path(__file__).parent.resolve()}"!')
        exit()
    
    parser = argparse.ArgumentParser(description='Packs an MSFS Livery Tools distribution.')
    parser.add_argument('python_zip', help='embed Python zip file')
    args = parser.parse_args()
    
    if dest.is_dir():
        print(f'Removing "{dest}".')
        shutil.rmtree(dest)
        
    print(f'Creating destribution folder ({dest}).')
    dest.mkdir()
    
    print(f'Copying packages from "{site_packages}":')
    for package in site_packages.iterdir():
        if 'pip' not in package.name:
            print(f'Copying package "{package.name}".')
            try:
                shutil.copytree(package, dest / package.name)
            except NotADirectoryError:
                shutil.copy(package, dest)
    
    print('Copying source files.')
    shutil.copytree(source_dir, dest / source_dir)
    
    print('Copying resource files:')
    (dest / 'resources').mkdir()
    resources = [(data_files('resources', ['*.png', '*.ico', 'thumbnail.jpg']))]
    resources.append((data_files('.', ['livery_tools.py', 'LICENSE', 'README.md', 'CHANGELOG.md'])))
    for r in resources:
        for file in r[1]:
            print(f'    {file} to {dest / r[0]}.')
            shutil.copy(file, dest / r[0])
    
    print('Copying base script.')
    shutil.copy(base_script, dest)
    
    print('Copying shell script.')
    shutil.copy(shell_script, dest)
    
    print('Copying tkinter and tcl packages and DLLs.')
    import tkinter, _tkinter # sys.executable does not work
    shutil.copytree(Path(tkinter.__file__).parent, dest / 'tkinter')
    print(f'tkinter copyed from "{Path(tkinter.__file__).parent}"')
    shutil.copytree(Path(tkinter.__file__).parent.parent.parent / 'tcl', dest / 'tcl')
    print(f'TCL copyed from "{Path(tkinter.__file__).parent.parent.parent / "tcl"}"')
    for file in ('_tkinter.pyd', 'tcl86t.dll', 'tk86t.dll', 'zlib1.dll'):
        shutil.copy(Path(_tkinter.__file__).parent / file, dest / file)
        print(f'Copied "{file}" from "{Path(_tkinter.__file__).parent / file}"')
    
    print('Copying idlelib package')
    import idlelib
    shutil.copytree(Path(idlelib.__file__).parent, dest / 'idlelib')
    
    print('Unzipping embedable Python.')
    with zipfile.ZipFile(args.python_zip, 'r') as zip_file:
        zip_file.extractall(dest)
