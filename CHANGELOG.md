# MSFS Livery Tools changelog

## v1.6

* Create texture UV maps.
* Added "Tools" menu.

### v1.6.1

* Added check for "texconv.exe" path before executing actions that need this setting.
* Cancels panel copy on "cancel" button at file dialog.
* Checks if the airplane folder has been configured before packing.

### v1.6.2

* Corrected DDS descriptor creation routine.
* Does not overwrite DDS descriptors anymore (editions on them will now be reflected on the final package).

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
