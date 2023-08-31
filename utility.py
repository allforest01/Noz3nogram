import ctypes
from ctypes import wintypes
from consts import *

kernel32 = ctypes.windll.kernel32
user32 = ctypes.windll.user32

def GetProcId(processName):
    hGameWindow = user32.FindWindowA(NULL, ctypes.c_char_p(processName))
    if hGameWindow == NULL:
        print("Game isn't running!")
        return NULL
    processID = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hGameWindow, ctypes.byref(processID))
    return processID.value

def GetModuleBaseAddress(szModuleName, processID):
    dwModuleBaseAddress = wintypes.DWORD()
    hSnapshot = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPMODULE | TH32CS_SNAPMODULE32, processID)
    print(f"hSnapshot    = {hSnapshot}")
    if hSnapshot != INVALID_HANDLE_VALUE:
        ModuleEntry32 = MODULEENTRY32()
        ModuleEntry32.dwSize = ctypes.sizeof(MODULEENTRY32)
        if kernel32.Module32First(hSnapshot, ctypes.byref(ModuleEntry32)):
            while True:
                # print(f"{ModuleEntry32.szModule} - {ModuleEntry32.modBaseAddr}")
                if ModuleEntry32.szModule == szModuleName:
                    dwModuleBaseAddress = ModuleEntry32.modBaseAddr
                    break
                if not kernel32.Module32Next(hSnapshot, ctypes.byref(ModuleEntry32)):
                    break
    kernel32.CloseHandle(hSnapshot)
    return wintypes.DWORD(ctypes.addressof(dwModuleBaseAddress.contents))

def ReadMemory(hProcess, baseAddress, offsets, buffers):
    tempAddress = wintypes.DWORD(baseAddress)
    for i in range(len(offsets) - 1):
        kernel32.ReadProcessMemory(
            hProcess,
            wintypes.DWORD(tempAddress.value + offsets[i]),
            ctypes.byref(tempAddress),
            ctypes.sizeof(tempAddress),
            NULL)
        # print(f"baseAddress = {hex(tempAddress.value)}")
    kernel32.ReadProcessMemory(
        hProcess,
        wintypes.DWORD(tempAddress.value + offsets[-1]),
        ctypes.byref(buffers[0]),
        ctypes.sizeof(buffers[0]),
        NULL)

def WriteMemory(hProcess, baseAddress, offsets, buffer):
    tempAddress = wintypes.DWORD(baseAddress)
    for i in range(len(offsets) - 1):
        kernel32.ReadProcessMemory(
            hProcess,
            wintypes.DWORD(tempAddress.value + offsets[i]),
            ctypes.byref(tempAddress),
            ctypes.sizeof(tempAddress),
            NULL)
        # print(f"baseAddress = {hex(baseAddress.value)}")
    kernel32.WriteProcessMemory(
        hProcess,
        wintypes.DWORD(tempAddress.value + offsets[-1]),
        ctypes.byref(buffer),
        ctypes.sizeof(buffer),
        NULL)
