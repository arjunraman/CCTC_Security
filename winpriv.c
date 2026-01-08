#include <windows.h>

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow)

{

    STARTUPINFO si = { sizeof(si) };

    PROCESS_INFORMATION pi;

    // Create user and add to admin group

    char cmd[] = "cmd.exe /C whoami > C:\\Users\\Public\\whoami.txt /add";

    BOOL success = CreateProcessA(NULL, cmd, NULL, NULL, FALSE, CREATE_NO_WINDOW, NULL, NULL, &si, &pi);

    if (success) {

        CloseHandle(pi.hProcess);

        CloseHandle(pi.hThread);

    }

    return 0;

}
