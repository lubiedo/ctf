#include <windows.h>
#include <tlhelp32.h>
#include <stdbool.h>
#include <stdio.h>

BOOL Patch(PROCESSENTRY32 proc)
{
	HANDLE target = OpenProcess(PROCESS_ALL_ACCESS, FALSE, proc.th32ProcessID);
	if (target == NULL)
		return false;

	unsigned char codes[2] = {
		0x75, // je
		0x85  // jne
	};

	WriteProcessMemory(target, (LPVOID)0x4020E3, (LPCVOID)&codes[0], 1, NULL);
	WriteProcessMemory(target, (LPVOID)0x4021EF, (LPCVOID)&codes[1], 1, NULL);
	return CloseHandle(target);
}

PROCESSENTRY32 FindProc(HWND hwnd, LPWSTR name)
{
	PROCESSENTRY32 proc;
	HANDLE snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
	
	proc.dwSize = sizeof(PROCESSENTRY32);
	Process32First(snapshot, &proc);
	do {
		if (wcscmp(proc.szExeFile, name) != 0)
			continue;
		return proc;
	} while (Process32Next(snapshot, &proc));

	proc.th32ProcessID = 0;
	return proc;
}

LRESULT CALLBACK MainWndProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam)
{
	switch(uMsg) {
		case WM_CREATE:
			{
				CreateWindowEx(
					0,
					L"BUTTON",
					L"Patch",
					WS_VISIBLE | WS_CHILD | BS_DEFPUSHBUTTON,
					110, 10, 80, 25,
					hwnd, 
					(HMENU)1,
					GetModuleHandle(0),
					NULL);
			}
			break;
		case WM_COMMAND:
			switch (LOWORD(wParam)) {
				case 1:
					wchar_t label[128];
					PROCESSENTRY32 proc = FindProc(hwnd, L"TryToSolveIt!.exe");

					if (proc.th32ProcessID == 0) {
						MessageBoxW(hwnd, L"Error: process not found.", L"Patch", MB_OK|MB_ICONERROR);
						return 0;
					}

					BOOL ret = Patch(proc);

					wsprintfW((LPWSTR)label, L"Process patched! Pid: %d", proc.th32ProcessID);
					MessageBoxW(hwnd, label, L"Patch", MB_OK|MB_ICONEXCLAMATION);
					break;
			}
			break;
		case WM_DESTROY:
			PostQuitMessage(0);
			return 0;
	}
	return DefWindowProc(hwnd, uMsg, wParam, lParam);
}

int WINAPI wWinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, PWSTR pCmdLine, int nCmdShow)
{
	const wchar_t WCLASS_NAME[] = L"Main class";
	WNDCLASS wc = {};
	wc.lpfnWndProc = MainWndProc;
	wc.hInstance = hInstance;
	wc.lpszClassName = WCLASS_NAME;
	wc.style = CS_SAVEBITS | CS_DROPSHADOW;

	RegisterClass(&wc);

	HWND hwnd = CreateWindowEx(
			0,
			WCLASS_NAME,
			L"TrySolveIt! Patch",
			((WS_OVERLAPPEDWINDOW) & ~WS_MINIMIZEBOX) & ~WS_MAXIMIZEBOX,
			CW_USEDEFAULT, CW_USEDEFAULT, 300, 90,
			NULL,
			NULL,
			hInstance,
			NULL);
	if (hwnd == NULL)
		return 1;
	ShowWindow(hwnd, nCmdShow);
	MSG wmsg = {};
	while (GetMessage(&wmsg, NULL, 0, 0) > 0) {
		TranslateMessage(&wmsg);
		DispatchMessage(&wmsg);
	}
	return 0;
}
