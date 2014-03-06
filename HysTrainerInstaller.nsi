!define APPNAME "HysTrainer"
!define DESCRIPTION "HysTrainer is a prototype application made to train hysteroscopic techniques."

!define VERSIONMAJOR 0
!define VERSIONMINOR 1
!define VERSIONBUILD 1

# Install directory
InstallDir "$PROGRAMFILES\${APPNAME}"

#License
LicenseData "LICENSE.TXT"

# This will be in the installer/uninstaller's title bar
Name "${APPNAME}"
Icon "resources/${APPNAME}.ico"
OutFile "${APPNAME}Installer.exe"

# Pages (steps) of the instalation
Page license
Page directory
Page instfiles

# Default section start
Section "install"
	# Popup box
	MessageBox MB_OK "This installer will install the HysTrainer simulator with embedded vtkESQui libraries in your system."

	# Install HysTrainer
	SetOutPath $INSTDIR
	
	# Files
	File "LICENSE.TXT"
	File /r "dist\*"

	# Create an unistaller to remove this installation
	WriteUninstaller "$INSTDIR\uninstall.exe"

	# Shortcut in start menu
	CreateDirectory "$SMPROGRAMS\${APPNAME}"
	CreateShortCut "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk" "$INSTDIR\${APPNAME}.exe" "" "$INSTDIR\resources\${APPNAME}.ico"
	CreateShortCut "$SMPROGRAMS\${APPNAME}\uninstall.lnk" "$INSTDIR\uninstall.exe"
	CreateShortCut "$SMPROGRAMS\${APPNAME}\LICENSE.lnk" "$INSTDIR\LICENSE.TXT"

	MessageBox MB_OK "HysTrainer has been installed successfully"

# Default section end
SectionEnd

# Uninstaller section
Function un.onInit
	MessageBox MB_OKCANCEL "Permanantly remove ${APPNAME}?" IDOK next
		Abort
	next:
FunctionEnd

Section "uninstall"
	# Remove shortcuts
	Delete "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk"
	Delete "$SMPROGRAMS\${APPNAME}\uninstall.lnk"
	Delete "$SMPROGRAMS\${APPNAME}\LICENSE.lnk"
	RMDir "$SMPROGRAMS\${APPNAME}"
	
	# Remove installation directory recursively
	RMDir /r $INSTDIR
SectionEnd