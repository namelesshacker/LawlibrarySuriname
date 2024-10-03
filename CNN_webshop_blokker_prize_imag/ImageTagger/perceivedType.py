"""
    Name:

        perceivedType.py

    Description:

        This is a set of methods that use the Windows registry to return a string
        describing how Windows interprets the given file. The current methods will
        return a string description as provided by Windows, or "unknown" if Windows
        does not have an associated file type. The auxiliary functions return True
        or False for tests for specific file types.

     Auxiliary Functions:

          isVideo(file)   -   returns True if PerceivedType = "video"
          isAudio(file)   -   returns True if PerceivedType = "audio"
          isImage(file)   -   returns True if PerceivedType = "image"
          isText (file)   -   returns True if PerceivedType = "text"

    Parameters:

        file:str    a file name
        degug:bool  print debug info if True (default=False)

    Audit:

        2021-07-17  rj  original code

"""

import os
import winreg


def perceivedType(file: str, debug: bool = False) -> str:
    """Returns the windows registry perceived type string for the given file"""

    if debug:
        print(f'\nchecking {file=}')

    try:
        key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, os.path.splitext(file)[-1])
        inf = winreg.QueryInfoKey(key)

        for i in range(0, inf[1]):
            res = winreg.EnumValue(key, i)
            if debug:
                print(f'    {res=}')
            if res[0] == 'PerceivedType':
                return res[1].lower()
    except:
        pass

    return "unknown"

def isVideo(file: str) -> str: return perceivedType(file) == 'video'
def isAudio(file: str) -> str: return perceivedType(file) == 'audio'
def isImage(file: str) -> str: return perceivedType(file) == 'image'
def isText(file: str) -> str: return perceivedType(file) == 'text'


if __name__ == '__main__':
    for file in ('file.avi', 'file.mov', 'file.txt', 'file.jpg', 'file.mp3', 'file.pdf', 'file.xyz'):
        print('Perceived type of "%s" is %s' % (file, perceivedType(file, debug=True)))