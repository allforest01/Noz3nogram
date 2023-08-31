import ctypes, utility
from ctypes import wintypes
from consts import *

kernel32 = ctypes.windll.kernel32

class Game:
    def __init__(self):

        self.processID = utility.GetProcId(b"Picross Touch")
        print(f"processID    = {self.processID}")
        if self.processID == NULL:
            print("Failed get process ID!")
            exit(0)

        self.hProcess = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, self.processID)
        print(f"hProcess     = {self.hProcess}")
        if self.hProcess == INVALID_HANDLE_VALUE or self.hProcess == NULL:
            print("Cannot open process!")
            exit(0)

        self.monoAddress = utility.GetModuleBaseAddress(b"mono.dll", self.processID)
        print(f"monoAddress  = {self.monoAddress}")
        self.gridAddress   = wintypes.DWORD()
        self.currentWidth  = wintypes.DWORD()
        self.currentHeight = wintypes.DWORD()
        self.longestMeta   = wintypes.DWORD()
        self.tallestMata   = wintypes.DWORD()
        offsets = [0x001F50AC, 0x84, 0x8, 0x74, 0x58, 0x2C, 0x18]
        utility.ReadMemory(self.hProcess, self.monoAddress.value, offsets, [self.gridAddress])
        utility.ReadMemory(self.hProcess, self.gridAddress.value, [0x11c], [self.currentWidth])
        utility.ReadMemory(self.hProcess, self.gridAddress.value, [0x120], [self.currentHeight])
        utility.ReadMemory(self.hProcess, self.gridAddress.value, [0x13c], [self.longestMeta])
        utility.ReadMemory(self.hProcess, self.gridAddress.value, [0x140], [self.tallestMata])
        self.currentWidth  = self.currentWidth.value
        self.currentHeight = self.currentHeight.value
        self.longestMeta   = self.longestMeta.value
        self.tallestMata   = self.tallestMata.value
        print(f"gridAddress  = {self.gridAddress}")
        print(f"currenWidth  = {self.currentWidth}")
        print(f"currenHeight = {self.currentHeight}")
        print(f"longestMeta  = {self.longestMeta}")
        print(f"tallestMata  = {self.tallestMata}")

    def getState(self, x, y):
        pos = (x + y * self.currentHeight) * 4
        # print(pos)
        offsets = [0x70, 0x10 + pos, 0x34]
        state = wintypes.DWORD()
        # print(f"gridAddress = {hex(self.gridAddress.value)}")
        utility.ReadMemory(self.hProcess, self.gridAddress.value, offsets, [state])
        return state.value
    
    def setState(self, x, y, state):
        pos = (x + y * self.currentHeight) * 4
        offsets = [0x70, 0x10 + pos, 0x34]
        utility.WriteMemory(self.hProcess, self.gridAddress.value, offsets, wintypes.DWORD(state))
    
    def getRowMeta(self):
        rowMeta = [[] for i in range(self.currentHeight)]
        for i in range(self.currentHeight):
            for j in range(self.longestMeta):
                offsets = [0x34, 0x10 + i * 4, 0x08, 0x10 + j * 4]
                num = wintypes.DWORD()
                utility.ReadMemory(self.hProcess, self.gridAddress.value, offsets, [num])
                if not num:
                    break
                rowMeta[i].append(num.value)
        return rowMeta
    
    def getColMeta(self):
        colMeta = [[] for i in range(self.currentHeight)]
        for i in range(self.currentWidth):
            for j in range(self.tallestMata):
                offsets = [0x38, 0x10 + i * 4, 0x08, 0x10 + j * 4]
                num = wintypes.DWORD()
                utility.ReadMemory(self.hProcess, self.gridAddress.value, offsets, [num])
                if not num:
                    break
                colMeta[i].append(num.value)
        return colMeta
