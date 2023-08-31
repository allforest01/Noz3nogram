import ctypes
from ctypes import wintypes

NULL                 =          0
INVALID_HANDLE_VALUE =         -1
PROCESS_ALL_ACCESS   = 0x001FFFFF
TH32CS_SNAPMODULE    = 0x00000008
TH32CS_SNAPMODULE32  = 0x00000010

class MODULEENTRY32(ctypes.Structure):
    _fields_ = [('dwSize'       , wintypes.DWORD               ), 
                ('th32ModuleID' , wintypes.DWORD               ),
                ('th32ProcessID', wintypes.DWORD               ),
                ('GlblcntUsage' , wintypes.DWORD               ),
                ('ProccntUsage' , wintypes.DWORD               ),
                ('modBaseAddr'  , ctypes.POINTER(wintypes.BYTE)),
                ('modBaseSize'  , wintypes.DWORD               ), 
                ('hModule'      , wintypes.HMODULE             ),
                ('szModule'     , ctypes.c_char * 256          ),
                ('szExePath'    , ctypes.c_char * 260          )]
