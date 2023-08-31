#include <Windows.h>
#include <TlHelp32.h>
#include <tchar.h>
#include <vector>
#include <iostream>
#include <iomanip>

DWORD GetModuleBaseAddress(TCHAR* szModuleName, DWORD pID) {
	DWORD dwModuleBaseAddress = 0;
	HANDLE hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE | TH32CS_SNAPMODULE32, pID);
	std::cout << "hSnapshot = " << hSnapshot << '\n';
	MODULEENTRY32 ModuleEntry32 = { 0 };
	ModuleEntry32.dwSize = sizeof(MODULEENTRY32);
	if (Module32First(hSnapshot, &ModuleEntry32)) {
		do {
			// std::wcout << std::setw(25) << ModuleEntry32.szModule << std::hex << std::setw(10) << (DWORD)ModuleEntry32.modBaseAddr << std::endl;
			if (_tcscmp(ModuleEntry32.szModule, szModuleName) == 0) {
				dwModuleBaseAddress = (DWORD)ModuleEntry32.modBaseAddr;
				std::cout << "Proc = " << ModuleEntry32.ProccntUsage << '\n';
				break;
			}
		} while (Module32Next(hSnapshot, &ModuleEntry32));
	}
	CloseHandle(hSnapshot);
	return dwModuleBaseAddress;
}

template <typename T>
void ReadMemory(HANDLE hProcess, DWORD baseAddress, std::vector<DWORD> &offsets, T &buffer) {
	for (size_t i = 0; i + 1 < offsets.size(); i++) {
		// std::cout << "PointTo = " << std::hex << baseAddress + offsets[i] << '\n';
		ReadProcessMemory(hProcess, (LPCVOID)(baseAddress + offsets[i]), &baseAddress, sizeof(baseAddress), NULL);
		// std::cout << "baseAddress = " << std::hex << baseAddress << '\n';
	}
	// std::cout << "READ " << baseAddress + offsets.back() << ' ' << buffer << '\n';
	ReadProcessMemory(hProcess, (LPCVOID)(baseAddress + offsets.back()), &buffer, sizeof(buffer), NULL);
}

template <typename T>
void WriteMemory(HANDLE hProcess, DWORD baseAddress, std::vector<DWORD>& offsets, T buffer) {
	for (size_t i = 0; i + 1 < offsets.size(); i++) {
		// std::cout << "PointTo = " << std::hex << baseAddress + offsets[i] << '\n';
		ReadProcessMemory(hProcess, (LPVOID)(baseAddress + offsets[i]), &baseAddress, sizeof(baseAddress), NULL);
		// std::cout << "baseAddress = " << std::hex << baseAddress << '\n';
	}
	// std::cout << "WRITE " << baseAddress + offsets.back() << ' ' << buffer << '\n';
	WriteProcessMemory(hProcess, (LPVOID)(baseAddress + offsets.back()), &buffer, sizeof(buffer), NULL);
}

int GetState(HANDLE hProcess, DWORD GridAddress, int x, int y) {
	DWORD calPos = (x + y * 15) * 4;
	std::vector<DWORD> offsets = { 0x70, 0x10 + calPos, 0x34 };
	DWORD state = 0;
	ReadMemory(hProcess, GridAddress, offsets, state);
	return state;
}

void SetState(HANDLE hProcess, DWORD GridAddress, int x, int y, DWORD state) {
	DWORD calPos = (x + y * 15) * 4;
	std::vector<DWORD> offsets = { 0x70, 0x10 + calPos, 0x34 };
	WriteMemory(hProcess, GridAddress, offsets, state);
}

void GetRowMetaData(HANDLE hProcess, DWORD GridAddress) {
	for (int i = 0; i < 15; i++) {
		for (int j = 4; j >= 0; j--) {
			std::vector<DWORD> offsets = { 0x34, 0x10 + (DWORD)i * 4, 0x08, 0x10 + (DWORD)j * 4 };
			DWORD num = 0;
			ReadMemory(hProcess, GridAddress, offsets, num);
			if (num) std::cout << num << ' ';
			else std::cout << "  ";
		}
		std::cout << '\n';
	}
}

void GetColMetaData(HANDLE hProcess, DWORD GridAddress) {
	for (int j = 4; j >= 0; j--) {
		for (int i = 0; i < 15; i++) {
			std::vector<DWORD> offsets = { 0x38, 0x10 + (DWORD)i * 4, 0x08, 0x10 + (DWORD)j * 4 };
			DWORD num = 0;
			ReadMemory(hProcess, GridAddress, offsets, num);
			if (num) std::cout << num << ' ';
			else std::cout << "  ";
		}
		std::cout << '\n';
	}
}

int main() {

	HWND hGameWindow = FindWindow(NULL, L"Picross Touch");
	if (hGameWindow == NULL) {
		std::cout << "Game isn't running!" << '\n';
		return 0;
	}

	DWORD pID = NULL;
	GetWindowThreadProcessId(hGameWindow, &pID);
	std::cout << "Process ID = " << pID << '\n';

	HANDLE hProcess = NULL;
	hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pID);
	std::cout << "hProcess = " << hProcess << '\n';

	if (hProcess == INVALID_HANDLE_VALUE || hProcess == NULL) {
		std::cout << "Cannot open process!" << '\n';
		return 0;
	}

	std::cout << "Open process success!" << '\n';

	TCHAR modName[] = L"mono.dll";
	// std::wcout << L"modName = " << modName << '\n';
	DWORD monoAddress = GetModuleBaseAddress(modName, pID);
	std::cout << "monoAddress = " << std::hex << monoAddress << '\n';

	std::vector<DWORD> GridOffsets = { 0x001F50AC, 0x84, 0x8, 0x74, 0x58, 0x2C, 0x18 };
	DWORD GridAddress = 0;
	ReadMemory(hProcess, monoAddress, GridOffsets, GridAddress);
	std::wcout << L"GridAddress = " << std::hex << GridAddress << '\n';
	std::cout << '\n';

	std::cout << "CURRENT STATE:" << '\n';
	for (int i = 0; i < 15; i++) {
		for (int j = 0; j < 15; j++) {
			int state = GetState(hProcess, GridAddress, i, j);
			if (state) std::cout << state << ' ';
			else std::cout << "- ";
		}
		std::cout << '\n';
	}
	std::cout << '\n';

	std::cout << "ROW META DATA:" << '\n';
	GetRowMetaData(hProcess, GridAddress);
	std::cout << '\n';

	std::cout << "COL META DATA:" << '\n';
	GetColMetaData(hProcess, GridAddress);
	std::cout << '\n';

}
