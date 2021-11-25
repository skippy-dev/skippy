;--------------------------------
;Include Modern UI

	!include "MUI2.nsh"
	!include "Sections.nsh"
	!include "LogicLib.nsh"

;--------------------------------
;General

	;Name and file
	Name "Skippy"
	OutFile "output\Windows.installer.exe"
	Unicode True

	;Default installation folder
	InstallDir "C:\Program Files\skippy"

	;Get installation folder from registry if available
	InstallDirRegKey HKCU "Software\skippy" ""

	;Request application privileges for Windows Vista
	RequestExecutionLevel admin

;--------------------------------
;Interface Settings

	!define MUI_ABORTWARNING
	!define MUI_FINISHPAGE_RUN "$INSTDIR\run.exe"

;--------------------------------
;Pages

	!insertmacro MUI_PAGE_WELCOME
	!insertmacro MUI_PAGE_LICENSE "..\LICENSE"
	!insertmacro MUI_PAGE_COMPONENTS
	!insertmacro MUI_PAGE_DIRECTORY
	!insertmacro MUI_PAGE_INSTFILES
	!insertmacro MUI_PAGE_FINISH

	!insertmacro MUI_UNPAGE_WELCOME
	!insertmacro MUI_UNPAGE_CONFIRM
	!insertmacro MUI_UNPAGE_INSTFILES
	!insertmacro MUI_UNPAGE_FINISH

;--------------------------------
;Languages

	!insertmacro MUI_LANGUAGE "English" ; The first language is the default language

;--------------------------------
;Installer Sections

Section "Skippy core" SecCore

	SetOutPath "$INSTDIR"

	;ADD YOUR OWN FILES HERE...
	File /r "build\exe.win-amd64-3.9\*"

	;Store installation folder
	WriteRegStr HKCU "Software\skippy" "" $INSTDIR

	AccessControl::GrantOnFile "$INSTDIR\logs" "(BU)" "FullAccess"
	AccessControl::GrantOnFile "$INSTDIR\property" "(BU)" "FullAccess"

	;Create uninstaller
	WriteUninstaller "$INSTDIR\Uninstall.exe"
SectionEnd

Section "Desktop shortcut" SecShortcut

	;create desktop shortcut
	CreateShortCut "$DESKTOP\Skippy.lnk" "$INSTDIR\run.exe" "" "$INSTDIR\run.exe"

SectionEnd

;--------------------------------
;Descriptions

	;Assign language strings to sections
	!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
		!insertmacro MUI_DESCRIPTION_TEXT ${SecCore} "Skippy Core Files (required)."
		!insertmacro MUI_DESCRIPTION_TEXT ${SecShortcut} "Create a desktop shortcut."
	!insertmacro MUI_FUNCTION_DESCRIPTION_END

;--------------------------------
;Uninstaller Section

Section "Uninstall"

	;ADD YOUR OWN FILES HERE...
	RMDir /r "$INSTDIR\*"

	Delete "$INSTDIR\Uninstall.exe"

	RMDir "$INSTDIR"

	DeleteRegKey /ifempty HKCU "skippy"

SectionEnd

;--------------------------------
;OnInit

Function .onInit
	UserInfo::GetAccountType
	pop $0
	${If} $0 != "admin" ;Require admin rights on NT4+
    	MessageBox mb_iconstop "Administrator rights required!"
   	 	SetErrorLevel 740 ;ERROR_ELEVATION_REQUIRED
		quit
	${EndIf}

	!insertmacro SetSectionFlag ${SecCore} ${SF_RO}
FunctionEnd