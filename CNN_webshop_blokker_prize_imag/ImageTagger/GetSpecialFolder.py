from win32com.shell import shell, shellcon

#def myDocuments():
#    return shell.SHGetFolderPath(0, shellcon.CSIDL_MYDOCUMENTS, None, 0)

def myMusic():
    return shell.SHGetFolderPath(0, shellcon.CSIDL_MYMUSIC, None, 0)

def myPictures():
    return shell.SHGetFolderPath(0, shellcon.CSIDL_MYPICTURES, None, 0)

def myVideos():
    return shell.SHGetFolderPath(0, shellcon.CSIDL_MYVIDEO, None, 0)

if __name__ == "__main__":
    #myDocuments()
    print(myMusic())
    print(myPictures())
    print(myVideos())