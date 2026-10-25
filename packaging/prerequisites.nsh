; Keep per-user application install. The official Microsoft bootstrap elevates
; itself only when the shared VC++ runtime needs installation/update.
!include "WordFunc.nsh"

!macro customInit
  SetRegView 64
  ReadRegDWORD $0 HKLM "SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64" "Installed"
  ReadRegStr $1 HKLM "SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64" "Version"
  SetRegView 64
  ; Version registry strings begin with v, VersionCompare expects digits.
  StrCpy $1 $1 "" 1
  ${VersionCompare} "$1" "14.51.36247.0" $2
  ${If} $0 != 1
  ${OrIf} $2 == 2
    InitPluginsDir
    File /oname=$PLUGINSDIR\vc_redist.x64.exe "${PROJECT_DIR}\build\windows-deps\prerequisites\vc_redist.x64.exe"
    ClearErrors
    ExecWait '"$PLUGINSDIR\vc_redist.x64.exe" /install /passive /norestart' $0
    ${If} ${Errors}
      MessageBox MB_OK|MB_ICONSTOP "Could not start Microsoft Visual C++ Runtime installation."
      SetErrorLevel 1
      Quit
    ${EndIf}
    ${If} $0 == 3010
      SetRebootFlag true
    ${ElseIf} $0 != 0
      MessageBox MB_OK|MB_ICONSTOP "Microsoft Visual C++ Runtime installation failed (code $0). Neutral installation stopped."
      SetErrorLevel $0
      Quit
    ${EndIf}
  ${EndIf}
!macroend
