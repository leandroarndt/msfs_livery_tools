[![Header image](resources/header.jpg)](https://github.com/leandroarndt/msfs_livery_tools)

# MSFS Livery Tools

MSFS Livery Tools is a Windows application to help creating liveries for existing aircrafts on Microsoft Flight Simulator 2020. It deals with all bureaucratic steps of livery creation, so that you can focus on your creative work:

* Package your livery and automatically create the needed files and folders.
* Create texture maps from glTF files (including those already built for MSFS).
* Extract images from glTF JSON files and compress them again to DDS format.
* Convert selected DDS images to PNG and back to DDS.
* Creating the directory structure of a package.
* Creating an "aircraft.cfg" file based on the original aircraft and variation information.
* Creating a "manifest.json" file (optionally based on the original manifest).
* Creating a "panel.cfg" file and changing:
  * variation override;
  * external registration font color and stroke.
* Creating and editing descriptive JSON files for DDS textures (.DDS.json).
* Creating and editing flag file for textures (.FLAGS).
* Creating and updating package layout files ("layout.json").
* Managing thumbnails (converting from capture tool, resizing and adding a placeholder).

## Instalation and usage

Download and install latest [release](https://github.com/leandroarndt/msfs_livery_tools/releases). A shortcut will be created in your windows menu. Refer to the [wiki](https://github.com/leandroarndt/msfs_livery_tools/wiki) for help.

You may also download source code and use a Python interpreter.

## Requirements

MSFS Livery Tools uses [Microsoft's texconv.exe](https://github.com/Microsoft/DirectXTex/wiki/Texconv)
in order to extract and compress texture files.

## Support MSFS Livery Tools

This application has been created in order to facilitate the customization of liveries for [the
author's YouTube channel](https://youtube.com/@fswt). Please consider subscribing, watching and
liking the videos there!
