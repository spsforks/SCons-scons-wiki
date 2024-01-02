
This is the discussion page for MoreSiteSConsDirs.

Adding some notes on the Win32 case: (from .net API)

<!-- --> | <!-- -->
-------- | --------
`ApplicationData` | The directory that serves as a common repository for application-specific data for the current roaming user.
`CommonApplicationData` | The directory that serves as a common repository for application-specific data that is used by all users.
`LocalApplicationData` | The directory that serves as a common repository for application-specific data that is used by the current, non-roaming user.


Main point here is that windows has the view of current user roaming and current user non-roaming. This mean data could be installed per machine for a user and per user and roam with user.

Need to find the win32 api equals. Need to add code for accesing in Python ( ideally from ctypes so 64-bit python can be used)

-- [JasonKenny](JasonKenny)

Some info on finding the CommonApplicationData path (which I think is the right one for SCons) is here: [http://stackoverflow.com/questions/626796/how-do-i-find-the-windows-common-application-data-folder-using-python](http://stackoverflow.com/questions/626796/how-do-i-find-the-windows-common-application-data-folder-using-python)


```python
#!python

import ctypes
from ctypes import wintypes, windll

CSIDL_COMMON_APPDATA = 35

_SHGetFolderPath = windll.shell32.SHGetFolderPathW
_SHGetFolderPath.argtypes = [wintypes.HWND,
                            ctypes.c_int,
                            wintypes.HANDLE,
                            wintypes.DWORD, wintypes.LPCWSTR]


path_buf = wintypes.create_unicode_buffer(wintypes.MAX_PATH)
result = _SHGetFolderPath(0, CSIDL_COMMON_APPDATA, 0, 0, path_buf)
print path_buf.value
```
-- [GaryOberbrunner](GaryOberbrunner)

Yep I agree that looks right.I also have this code block I did to get the data in the recommended Vista and Win7 way


```python
#!python

import ctypes
from ctypes import windll, wintypes # seem to have to import wintypes this way else it does not load right
class GUID(ctypes.Structure):
    _fields_ = [
        ('Data1', wintypes.DWORD),
        ('Data2', wintypes.WORD),
        ('Data3', wintypes.WORD),
        ('Data4', wintypes.BYTE * 8)
        ]
    def __init__(self, l, w1, w2, b1, b2, b3, b4, b5, b6, b7, b8):
        self.Data1 = l
        self.Data2 = w1
        self.Data3 = w2
        self.Data4[:] = (b1, b2, b3, b4, b5, b6, b7, b8)
    def __repr__(self):
            b1, b2, b3, b4, b5, b6, b7, b8 = self.Data4
            return 'GUID(%x-%x-%x-%x%x%x%x%x%x%x%x)' % (
                self.Data1, self.Data2, self.Data3, b1, b2, b3, b4, b5, b6, b7, b8)

id= GUID(0x62AB5D82, 0xFDC1, 0x4DC3, 0xA9, 0xDD, 0x07, 0x0D, 0x1D, 0x49, 0x5D, 0x97) #ProgramData
ptr=ctypes.c_wchar_p()

ctypes.windll.shell32.SHGetKnownFolderPath(ctypes.byref(id),0,0,ctypes.byref(ptr))
print ptr.value

```
I think these are the key we will want based on SHGetKnownFolderPath KnownFolderID [http://msdn.microsoft.com/en-us/library/bb762584(VS.85).aspx](http://msdn.microsoft.com/en-us/library/bb762584(VS.85).aspx)

This is the per-machine case

**FOLDERID_ProgramData**

* **GUID** {62AB5D82-FDC1-4DC3-A9DD-070D1D495D97}
* **Display Name** ProgramData
* **Folder Type** FIXED
* **Default Path** %ALLUSERSPROFILE% (%ProgramData%, %SystemDrive%\ProgramData)
* **CSIDL Equivalent** CSIDL_COMMON_APPDATA
* **Legacy Display Name** Application Data
* **Legacy Default Path **%ALLUSERSPROFILE%\Application Data
This is the per-user case

**FOLDERID_LocalAppData **

* **GUID **{F1B32785-6FBA-4FCF-9D55-7B8E7F157091}
* **Display Name **Local
* **Folder Type **PERUSER
* **Default Path **%LOCALAPPDATA% (%USERPROFILE%\AppData\Local)
* **CSIDL Equivalent **CSIDL_LOCAL_APPDATA
* **Legacy Display Name **Application Data
* **Legacy Default Path **%USERPROFILE%\Local Settings\Application Data
I left out the roaming cases ( easy to find however) as they are useful on Corporate setups that allow for roaming account, or a login with data that follows the user to different boxes.

-- [JasonKenny](JasonKenny)

Fortunately I think we can just get the env vars (%ALLUSERSPROFILE%) on Vista and 7 and avoid all that hair.

-- [GaryOberbrunner](GaryOberbrunner)

It might be me but I read the order and it seems to be backwards, or incorrect. I believe we want the load order be this: ( from user point for view)

1. User provided path if given on Command line
1. SConstruct directory
1. User data location ( ie per user data)
1. System Data location ( per system/ all users)
Given what I said is correct. I think the Python path would be setup this way as well for when the code is imported from these locations.

-- [JasonKenny](JasonKenny)

I think since each dir has code to be executed, and we want the last one to "win" (i.e. be able to override variables and settings made in others), we want to execute them in the original order. However as far as sys.path is concerned, you're right -- the user dir should be first and the system data dir should be last. Do you actually think we should search per-user and systemwide dirs on Windows? I was thinking just per-machine. Anything more is just confusing IMHO.

-- [GaryOberbrunner](GaryOberbrunner)

I was thinking both. In cases of a laptop or a single user system the difference is mute as on one person will see it. However with server 2008, or user of remote powershell you can have more than one user using the system at a time. In these cases the difference between having a system wide setup vs. per user can be very useful. I know for me at work we have system that have stuff setup for the group, but some of the users work on different products and want to specialize certain items for their login. I do agree that the roaming user case can be more confusing, and I don't think it is very common setup for developers, that is why I did not add it. I know I find it very useful with feedback I have here to have the ability to setup system level and let user customize independently from the other users. This has also become useful for when some user help add internal work additions to our version of Parts ( via the pieces idea we have in Parts) as they can work on this enhancement without effecting or breaking the system level installs.

-- [JasonKenny](JasonKenny)
