!include MUI2.nsh

!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_LANGUAGE "English"

Name 'MSFS Livery Tools'

# define name of installer
OutFile "MSFS Livery Tools.exe"
 
# define installation directory
InstallDir "$PROGRAMFILES\MSFS Livery Tools"
 
# For removing Start Menu shortcut in Windows 7
RequestExecutionLevel user
 
# start default section
Section
 
    # set the installation directory as the destination for the following actions
    SetOutPath $INSTDIR

    File /r dist\*.*
    CreateShortcut "$SMPROGRAMS\MSFS Livery Tools.lnk" "$INSTDIR\livery_tools.exe" "" "$INSTDIR\resources\msfs livery tools.ico" 0 SW_SHOWMINIMIZED
 
    # create the uninstaller
    WriteUninstaller "$INSTDIR\uninstall.exe"
 
    # create a shortcut named "new shortcut" in the start menu programs directory
    # point the new shortcut at the program uninstaller
    CreateShortcut "$SMPROGRAMS\MSFS Livery Tools uninstaller.lnk" "$INSTDIR\uninstall.exe"
SectionEnd
 
# uninstaller section start
Section "uninstall"
 
    Delete "$INSTDIR\*.*"
	# first, delete the uninstaller
    # Delete "$INSTDIR\uninstall.exe"
 
    # second, remove the link from the start menu
	Delete "$SMPROGRAMS\MSFS Livery Tools.lnk"
    Delete "$SMPROGRAMS\MSFS Livery Tools uninstaller.lnk"
 
    RMDir /r $INSTDIR
# uninstaller section end
SectionEnd
