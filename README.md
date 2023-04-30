[![Header image](resources/header.jpg)](https://github.com/leandroarndt/msfs_livery_tools)
# MSFS Livery Tools

MSFS Livery Tools is set of tools to help creating livery for existing aircrafts
on Microsoft Flight Simulator 2020. It deals with all bureaucratic steps of livery creations,
so that you can focus on your creative work:

* Converting texture images from and to DDS format.
* Creating the directory structure of a package.
* Creating an "aircraft.cfg" file based on the original aircraft and variation information.
* Creating a "manifest.json" file (optionally based on the original manifest).
* Creating a "panel.cfg" file and changing:
  * variation override;
  * external registration font color and stroke.
* Creating descriptive JSON files for DDS textures (.DDS.json).
* Creating flag file for textures (.FLAGS) – not on the graphical user interface
* Creating package layout files ("layout.json")

## Instalation

Download latest [release](https://github.com/leandroarndt/msfs_livery_tools/releases) and use the provided tools in a Python 3 interpreter.

## TODO

* Graphical user interface.
* glTF converter to remove MSFT extension, so that already built aircrafts can be
opened with [Asobo's Blender plugin](https://github.com/AsoboStudio/glTF-Blender-IO-MSFS).

## Requirements

MSFS Livery Tools uses [Python 3](https://python.org/) (3.11 is used on development) and
[Microsoft's texconv.exe](https://github.com/Microsoft/DirectXTex/wiki/Texconv).
