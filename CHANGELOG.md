# MSFS Livery Tools changelog

## v1.7

* Allows editing of texture descriptors and flags (".dds.json" and ".flags" files).
* Updates texture descriptors when packaging, so that they have information about the current version of the texture file.
* Checks for updates at startup.
* Creates UV maps for all texture types: albedo, composite, emissive and normal.

### v1.7.1

* Corrected texture extraction and packaging routines when it cannot find a "texture.cfg" file in the original livery.

### v1.7.2

* Fixed bug which prevented app loading after the first launch depending on the system language settings.

## v1.6

* Create texture UV maps.
* Added "Tools" menu.

### v1.6.5

* Deals with unicode characters at previously unexpected places.
* Deals with textures missing a proper "MSFS_texture_dds" extension.
* Searches for texture directory at aircraft.cfg if a "texture" dir is not found when extracting from glTF.
* Copes with packages without a texture.cfg file or without fallbacks in it while extracting textures from glTF.

### v1.6.4

* Texture map creator can deal with path components on image URIs too.
* Better messaging after UV maps creation.
* Texture map creator now runs on a separate process with a different window.

### v1.6.3

* Can deal with bogus "texture.cfg" (with non-existent folders) and glTF (with path components on image URI) like Asobo F/A-18.
* Corrected interface restoration after canceled texture map creation or when there is no open project.

### v1.6.2

* Corrected DDS descriptor creation routine.
* Does not overwrite DDS descriptors anymore (editions on them will now be reflected on the final package).
* Copies DDS descriptors when extracting textures.

### v1.6.1

* Added check for "texconv.exe" path before executing actions that need this setting.
* Cancels panel copy on "cancel" button at file dialog.
* Checks if the airplane folder has been configured before packing.

## v1.5

* New action to convert selected DDS files to PNG.
  * **Attention:** converting selected DDS files to PNG copies the respective `.FLAGS`
  file.

### v1.5.1

* Reduced start up time with limited scan depth (new setting available)..

## v1.4

* Prevents duplicating the airplane folder (which caused different liveries to overlap).
* Extracts textures from fallback directories listed in texture.cfg.
* Scans MSFS package folder (must be configured).
* Minor interface changes.

### v1.4.1

* Corrected a bug which prevented texture extraction in some cases

## v1.3

* Resizes thumbnail for both small and full-size formats.
* Skips unmodified texture compression during package build (speeds package build).
* Added alert for uniqueness of airplane folder.
* Asks before exiting application, opening or creating project if the current project has been modified.
* Save button and menu entry now indicate if the project has been modified.
* Bug correction:
  * Doesn't keep closed projects in memory anymore.
  * Corrected registration number configuration.
  * Now overwrites existing configuration files even if they're not present on project dir (not overwriting was a bad design choice).

## v1.2

* Converts `thumbnail.png` (from MSFS developer mode aircraft capture tool) into JPEG before resizing
the thumbnail.
* Adding a placeholder thumbnail adds it's "small" version too.
* Don't join model and textures by default anymore.

## v1.1

* Fixed a bug which prevented some composite textures loading in the simulator.
* `manifest.json` now has the calculated package size.

## v1.0

* Thumbnail management implemented, including resizing and adding placeholder image (only works on graphical user interface).
* Added "display name" property: this is the livery name displayed at the "select livery" window on the
simulator.
* "Update layout.json" button available on start up.
* User can now add a registration color section to `panel.cfg` even without such section on the
original file, but is warned to review it.

## v0.4

* Corrected a `layout.json` generator bug, which prevented correct texture loading by the simulator.

## v0.3

* Basic container chooser now expects an aircraft folder.
* Corrected bug related to packaging process and folders choices.

## v0.2

* Graphical user interface.
* Executable file.
* Installer.

## v0.1

* Initial version. Works on Python interpreter only.
