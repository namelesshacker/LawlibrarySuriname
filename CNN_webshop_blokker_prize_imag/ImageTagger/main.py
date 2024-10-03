"""
    Name:

        Tagger.pyw

    Description:

        This program implements an interface to easily maintain tags on image files.
        A tag in a file name will be any string of characters delimited by a blank.
        It is up to the user to avoid entering characters that are no valid in file
        names.

        The interface consists of three main panels. The left panel contains a tree
        from which all available drives and folders may be browsed. Selecting a folder
        from the tree will cause a list of all image files in that folder to be
        displayed in a list below the folder tree.

        Selecting a file from the file list will cause that image to be displayed
        in the upper portion of the centre panel. At the bottom of the centre panel
        the file name will be displayed in two parts, a base file name - no path, no
        file extension, and no index number. An index number is the end portion of a
        file of the form (##).

        The right panel consists of an upper list containing all of the tags in the
        currently selected file. The lower portion consists of a list of common tags
        that is maintained between runs.

        Tags can be added either by dragging tags from the common (lower) list to
        the current (upper) list, or by manually typing them into the file name
        below the displayed image. As new tags are added the file name and current
        tag list are kept in sync.

        Tags can also be copied between current and common lists by right clicking

        If you see a tag in the current list that you want to add to the common
        list you can drag it from the lower list to the upper list. Similarly, you
        can delete a tag from either list by selecting it, then pressing the delete
        key.

        As you make changes to the displayed file name the index will automatically
        be modified to avoid conflict with existing names in the file list.

        The first time a file is renamed with tagger, the original file name is saved
        in the alternate data stream ':tagger_undo'. If the current file has undo info
        available, it can be restored by clicking Restore or CTRL+R. If you find you 
        have totally botched a bunch of renames you can undo them by running 
        tagger_undo.py from a command shell in the picture folder. Please note that 
        running this without specifying a file or wildcard pattern will undo ALL 
        renames that were ever done to ALL files in that folder.


    source:
        https://www.daniweb.com/programming/software-development/tutorials/536115/image-file-tagging-app-in-python-wxpython

    updates:
        27-04-2023 replace 'wx' with 'wxPython'
        29-04-2023 filename history export
        29-04-2023 filename reverse/undo

    Audit:

        2021-07-13  rj  original code

"""

TITLE = 'Image Tagger (v 1.2)'

ADS   = ':tagger_undo'

import os
import re
import  wx
import inspect

import ImagePanel       as ip   # Control to display selected image file
import GetSpecialFolder as gs   # To determine Windows <My Pictures> folder
import perceivedType    as pt   # To determine (by extension) if file is an image file

from exif import Image          # For reading EXIF datetime stamp


DEBUG   = False
INSPECT = False

if INSPECT:
    import wx.lib.mixins.inspection


def iam():
    """
    Returns the name of the function that called this function. This
    is useful for printing out debug information, for example, you only
    need to code:

        if DEBUG: print('enter',iam())
    """

    return inspect.getouterframes(inspect.currentframe())[1].function


class MyTarget(wx.TextDropTarget):
    """
    Drag & drop implementation between two list controls in single column
    report mode. The two lists must have a custom property, 'type' with the
    values 'curr' and 'comm' (for this app meaning current and common tags).
    """

    def __init__(self, srce, dest):

        wx.TextDropTarget.__init__(self)

        self.srce = srce
        self.dest = dest

        if DEBUG: print(f'create target {srce.Name=} {dest.Name=}')

    def OnDropText(self, x, y, text):

        if DEBUG: print(iam(),f'{self.srce.Name=} {self.dest.Name=} {text=}')

        if self.dest.Name in ('curr', 'comm'):
            if self.dest.FindItem(-1,text) == -1:
                self.dest.InsertItem(self.dest.ItemCount, text)

        return True


class MyFrame(wx.Frame):

    def __init__(self, *args, **kwds):

        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        self.SetSize((1400, 800))
        self.SetTitle(TITLE)

        self.status = self.CreateStatusBar(2)
        self.status.SetStatusWidths([100, -1])        

        # split1 contains the folder/file controls on the left and all else on the right

        self.split1 = wx.SplitterWindow(self, wx.ID_ANY)
        self.split1.SetMinimumPaneSize(250)

        self.split1_pane_1 = wx.Panel(self.split1, wx.ID_ANY)

        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)

        # split2 contains the folder tree on the top, and the file list on the bottom

        self.split2 = wx.SplitterWindow(self.split1_pane_1, wx.ID_ANY)
        self.split2.SetMinimumPaneSize(200)
        sizer_1.Add(self.split2, 1, wx.EXPAND, 0)

        self.split2_pane_1 = wx.Panel(self.split2, wx.ID_ANY)

        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)

        self.folders = wx.GenericDirCtrl(self.split2_pane_1, wx.ID_ANY, style=wx.DIRCTRL_DIR_ONLY)
        sizer_2.Add(self.folders, 1, wx.EXPAND, 0)

        self.split2_pane_2 = wx.Panel(self.split2, wx.ID_ANY)

        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)

        self.lstFiles = wx.ListCtrl(self.split2_pane_2, wx.ID_ANY, style=wx.LC_NO_HEADER | wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.lstFiles.AppendColumn('', width=600)
        self.lstFiles.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Courier New"))
        sizer_3.Add(self.lstFiles, 1, wx.EXPAND, 0)

        self.split1_pane_2 = wx.Panel(self.split1, wx.ID_ANY)

        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)

        # split3 contains the image display and controls on the left, and the current/common tags on the right

        self.split3 = wx.SplitterWindow(self.split1_pane_2, wx.ID_ANY)
        self.split3.SetMinimumPaneSize(150)
        sizer_4.Add(self.split3, 1, wx.EXPAND, 0)

        self.split3_pane_1 = wx.Panel(self.split3, wx.ID_ANY)

        sizer_5 = wx.BoxSizer(wx.VERTICAL)

        self.pnlImage = ip.ImagePanel(self.split3_pane_1, wx.ID_ANY)
        sizer_5.Add(self.pnlImage, 1, wx.EXPAND, 0)

        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5.Add(sizer_6, 0, wx.EXPAND, 0)

        self.btnStrip = wx.Button(self.split3_pane_1, wx.ID_ANY, "Strip")
        self.btnStrip.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Segoe UI"))
        self.btnStrip.SetToolTip('Click or CTRL+1 to remove HH-MM, DSC*, IMG* tags')
        sizer_6.Add(self.btnStrip, 1, wx.ALL | wx.EXPAND, 4)

        sizer_6.Add((10,-1), 0, 0, 0)

        self.btnRestore = wx.Button(self.split3_pane_1, wx.ID_ANY, "Restore")
        self.btnRestore.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Segoe UI"))
        self.btnRestore.SetToolTip('Click or CTRL+R to restore original name')
        self.btnRestore.Disable()
        sizer_6.Add(self.btnRestore, 1, wx.ALL | wx.EXPAND, 4)

        sizer_6.Add((10,-1), 0, 0, 0)

        self.btnSave = wx.Button(self.split3_pane_1, wx.ID_ANY, "Save")
        self.btnSave.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Segoe UI"))
        self.btnSave.SetToolTip ('Click or CTRL+S to save file name changes')
        sizer_6.Add(self.btnSave, 1, wx.ALL | wx.EXPAND, 4)

        #Delete tag available by hotkey only
        self.btnDelete = wx.Button(self.split3_pane_1, wx.ID_ANY, 'Delete')
        self.btnDelete.Visible = False
        self.Bind(wx.EVT_BUTTON, self.evt_DeleteTag, self.btnDelete)

        #Home available by hotkey only
        self.btnHome = wx.Button(self.split3_pane_1, wx.ID_ANY, 'Home')
        self.btnHome.Visible = False
        self.Bind(wx.EVT_BUTTON, self.evt_Home, self.btnHome)

        #Next and prev available by hotkey only
        self.btnPrev = wx.Button(self.split3_pane_1, wx.ID_ANY, 'Prev')
        self.btnPrev.Visible = False
        self.Bind(wx.EVT_BUTTON, self.evt_Prev, self.btnPrev)

        self.btnNext = wx.Button(self.split3_pane_1, wx.ID_ANY, 'Next')
        self.btnNext.Visible = False
        self.Bind(wx.EVT_BUTTON, self.evt_Next, self.btnNext)

        #Help available by hotkey only
        self.btnHelp = wx.Button(self.split3_pane_1, wx.ID_ANY, 'Help')
        self.btnHelp.Visible = False
        self.Bind(wx.EVT_BUTTON, self.evt_Help, self.btnHelp)

        sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5.Add(sizer_7, 0, wx.EXPAND, 0)

        self.txtName = wx.TextCtrl(self.split3_pane_1, wx.ID_ANY, "", style=wx.TE_PROCESS_ENTER)
        self.txtName.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Segoe UI"))
        self.txtName.SetMinSize((400, -1))        
        sizer_7.Add(self.txtName, 1, wx.BOTTOM | wx.EXPAND | wx.LEFT | wx.RIGHT, 4)

        self.txtIndex = wx.TextCtrl(self.split3_pane_1, wx.ID_ANY, "")
        self.txtIndex.SetMinSize((40, -1))
        self.txtIndex.SetMaxSize((40, -1))
        self.txtIndex.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Segoe UI"))
        sizer_7.Add(self.txtIndex, 0, wx.BOTTOM | wx.EXPAND | wx.LEFT | wx.RIGHT, 4)

        self.split3_pane_2 = wx.Panel(self.split3, wx.ID_ANY)

        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)

        # split4 contains the current tags on the top and the common tags on the bottom

        self.split4 = wx.SplitterWindow(self.split3_pane_2, wx.ID_ANY)
        self.split4.SetMinimumPaneSize(20)
        sizer_8.Add(self.split4, 1, wx.EXPAND, 0)

        self.split4_pane_1 = wx.Panel(self.split4, wx.ID_ANY)

        sizer_9 = wx.BoxSizer(wx.HORIZONTAL)

        self.lstCurr = wx.ListCtrl(self.split4_pane_1, wx.ID_ANY, name='curr', style=wx.LC_NO_HEADER | wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.lstCurr.AppendColumn('', width=600)
        self.lstCurr.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Segoe UI"))
        self.lstCurr.SetToolTip ('Drag to lower pane or right-click to save in common tags\n(DEL or CTRL-X to delete tag)')
        sizer_9.Add(self.lstCurr, 1, wx.EXPAND, 0)

        self.split4_pane_2 = wx.Panel(self.split4, wx.ID_ANY)

        sizer_10 = wx.BoxSizer(wx.HORIZONTAL)

        self.lstComm = wx.ListCtrl(self.split4_pane_2, wx.ID_ANY, name='comm', style=wx.LC_NO_HEADER | wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_SORT_ASCENDING)
        self.lstComm.AppendColumn('', width=600)
        self.lstComm.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Segoe UI"))
        self.lstComm.SetToolTip ('Drag to upper pane or right-click to add to current tags\n(DEL or CTRL-X to delete tag)')
        sizer_10.Add(self.lstComm, 1, wx.EXPAND, 0)

        self.split4_pane_2.SetSizer(sizer_10)
        self.split4_pane_1.SetSizer(sizer_9)

        self.split4.SplitHorizontally(self.split4_pane_1, self.split4_pane_2)

        self.split3_pane_2.SetSizer(sizer_8)
        self.split3_pane_1.SetSizer(sizer_5)

        self.split3.SplitVertically(self.split3_pane_1, self.split3_pane_2)

        self.split1_pane_2.SetSizer(sizer_4)
        self.split2_pane_2.SetSizer(sizer_3)
        self.split2_pane_1.SetSizer(sizer_2)

        self.split2.SplitHorizontally(self.split2_pane_1, self.split2_pane_2)

        self.split1_pane_1.SetSizer(sizer_1)

        self.split1.SplitVertically(self.split1_pane_1, self.split1_pane_2)

        self.Layout()

        self.Bind(wx.EVT_DIRCTRL_SELECTIONCHANGED, self.evt_FolderSelected, self.folders)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.evt_FileSelected, self.lstFiles)
        self.Bind(wx.EVT_BUTTON, self.evt_Strip, self.btnStrip)
        self.Bind(wx.EVT_BUTTON, self.evt_Restore, self.btnRestore)
        self.Bind(wx.EVT_BUTTON, self.evt_Save, self.btnSave)
        self.Bind(wx.EVT_TEXT, self.evt_NameChanged, self.txtName)
        self.Bind(wx.EVT_TEXT_ENTER, self.evt_TextEnter, self.txtName)
        self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.evt_StartDrag, self.lstCurr)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.evt_RightClick, self.lstCurr)        
        self.Bind(wx.EVT_LIST_DELETE_ITEM, self.evt_TagDeleted, self.lstCurr)
        self.Bind(wx.EVT_LIST_INSERT_ITEM, self.evt_TagAdded, self.lstCurr)
        self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.evt_StartDrag, self.lstComm)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.evt_RightClick, self.lstComm)
        self.Bind(wx.EVT_LIST_DELETE_ITEM, self.evt_TagDeleted, self.lstComm)
        self.Bind(wx.EVT_LIST_INSERT_ITEM, self.evt_TagAdded, self.lstComm)
        self.Bind(wx.EVT_CLOSE, self.evt_Close, self)

        #Define drag & drop
        dtCurr = MyTarget(self.lstCurr, self.lstComm) 
        self.lstComm.SetDropTarget(dtCurr) 
        self.Bind(wx.EVT_LIST_BEGIN_DRAG,  self.evt_StartDrag,  self.lstCurr)
        self.Bind(wx.EVT_LIST_INSERT_ITEM, self.evt_TagAdded,   self.lstCurr)
        self.Bind(wx.EVT_LIST_DELETE_ITEM, self.evt_TagDeleted, self.lstCurr)

        dtComm = MyTarget(self.lstComm, self.lstCurr) 
        self.lstCurr.SetDropTarget(dtComm) 
        self.Bind(wx.EVT_LIST_BEGIN_DRAG,  self.evt_StartDrag,  self.lstComm)
        self.Bind(wx.EVT_LIST_DELETE_ITEM, self.evt_TagDeleted, self.lstComm)

        #Define hotkeys
        hotkeys = [wx.AcceleratorEntry() for i in range(9)]
        hotkeys[0].Set(wx.ACCEL_NORMAL, wx.WXK_DELETE, self.btnDelete.Id)
        hotkeys[1].Set(wx.ACCEL_CTRL, ord('X'), self.btnDelete.Id)
        hotkeys[2].Set(wx.ACCEL_CTRL, ord('S'), self.btnSave.Id)
        hotkeys[3].Set(wx.ACCEL_CTRL, ord('1'), self.btnStrip.Id)
        hotkeys[4].Set(wx.ACCEL_CTRL, ord('R'), self.btnRestore.Id)
        hotkeys[5].Set(wx.ACCEL_CTRL, ord('H'), self.btnHome.Id)
        hotkeys[6].Set(wx.ACCEL_NORMAL, wx.WXK_DOWN, self.btnNext.Id)
        hotkeys[7].Set(wx.ACCEL_NORMAL, wx.WXK_UP, self.btnPrev.Id)
        hotkeys[8].Set(wx.ACCEL_NORMAL, wx.WXK_F1, self.btnHelp.Id)
        accel = wx.AcceleratorTable(hotkeys)
        self.SetAcceleratorTable(accel)

        #Define state indicators
        self.currfile = None  #current unqualified file name                    
        self.currindx = None  #index of select file in file list                
        self.currextn = None  #current file extension                           
        self.currbase = None  #current unqualified base file name (no extension)
        self.fullfile = None  #current fully qualified file name                
        self.original = None  #original file name from ADS if available         

        #Set default config
        self.currpath = gs.myPictures()

        self.split1.SetSashPosition(300)
        self.split2.SetSashPosition(300)
        self.split3.SetSashPosition(900)
        self.split4.SetSashPosition(400)

        #Load last used config
        self.LoadConfig()

        self.folders.ExpandPath(self.currpath)

        if INSPECT: wx.lib.inspection.InspectionTool().Show()

    def LoadConfig(self):
        """Load the settings from the previous run."""     
        if DEBUG: print('enter',iam())

        self.config = os.path.splitext(__file__)[0] + ".ini"

        if DEBUG: print(f'LoadConfig {self.config=}')

        try:
            with open(self.config,'r') as file:
                for line in file.read().splitlines():
                    if DEBUG: print(line)

                    #Disable event handling during common tag restore
                    self.EvtHandlerEnabled = False
                    exec(line)
                    self.EvtHandlerEnabled = True
        except: 
            print("Error during ini read")
            self.EvtHandlerEnabled = True

    def SaveConfig(self):
        """Save the current settings for the next run"""        
        if DEBUG: print('enter',iam())

        x,y = self.GetPosition()
        w,h = self.GetSize()

        with open(self.config,'w') as file:

            file.write('#Window size and position\n\n')
            file.write('self.SetPosition((%d,%d))\n' % (x,y))
            file.write('self.SetSize((%d,%d))\n' % (w,h))

            file.write('\n#Splitter settings\n\n')
            file.write('self.split1.SetSashPosition(%d)\n' % (self.split1.GetSashPosition()))
            file.write('self.split2.SetSashPosition(%d)\n' % (self.split2.GetSashPosition()))
            file.write('self.split3.SetSashPosition(%d)\n' % (self.split3.GetSashPosition()))
            file.write('self.split4.SetSashPosition(%d)\n' % (self.split4.GetSashPosition()))

            file.write('\n#Last folder\n\n')
            file.write('self.currpath = "%s\"\n' % self.currpath.replace("\\","/"))

            file.write('\n#Common tags\n\n')
            for indx in range(self.lstComm.ItemCount):
                line = 'self.lstComm.InsertItem(%d,"%s")\n' % (indx,self.lstComm.GetItemText(indx))
                file.write(line)

    def evt_FolderSelected(self, event):
        """User selected a folder from the directory tree"""
        if DEBUG: print('enter',iam())

        self.lstFiles.DeleteAllItems()  #Clear file list        
        self.pnlImage.Clear()           #Clear displayed image  
        self.txtName.Clear()            #Clear new name         
        self.txtIndex.Value = '0'       #Reset index            
        self.lstCurr.DeleteAllItems()   #Clear current tags     

        #reset current state indicators
        self.currpath = self.folders.GetPath()
        self.currfile = None    
        self.currindx = None         
        self.currextn = None          
        self.currbase = None  
        self.fullfile = None              

        #read image files from new current folder
        self.RefreshFileList()
        self.Select(0)

        event.Skip()

    def evt_FileSelected(self, event):
        """User selected a file from the file list"""
        if DEBUG: print('enter',iam())

        #Update state indicators

        file,indx = self.GetSelected(self.lstFiles)

        self.currfile = file
        self.currindx = indx
        self.currextn = os.path.splitext(self.currfile)[-1]
        self.fullfile = os.path.join(self.folders.GetPath(), self.currfile)
        self.currbase = os.path.splitext(self.currfile)[0]
        self.original = self.GetOriginalName()

        self.SetStatus()

        self.pnlImage.Load(self.fullfile)
        self.GetNameFromFile()        
        self.RefreshTags()

        self.pnlImage.bmpImage.SetToolTip(self.GetExifDate(self.fullfile))

        event.Skip()

    def evt_Strip(self, event):
        """Strip HH-MM and DSC/IMG tags"""
        if DEBUG: print('enter',iam())

        name = self.txtName.Value

        name = re.sub(' \d\d\-\d\d', '', name)      #HH-MM time tag  
        name = re.sub(' DSC\d+', '', name)          #Sonk camera tag 
        name = re.sub(' DSCF\d+', '', name)         #Fuji camera tag 
        name = re.sub(' IMG_\d+_\d+', '', name)     #FIGO cell phone 
        name = re.sub(' IMG_\d+', '', name)         #other camera tag

        #If name starts with yyyy-mm-dd, make sure it is followed by a space
        if re.search('^\d\d\d\d\-\d\d\-\d\d', name):
            if len(name) > 10 and name[10] != ' ':
                name = name[:10] + ' ' + name[10:]

        #Add a trailing space so user doesn't have to when adding tags
        if name[-1] != ' ': name += ' '

        self.txtName.Value = name        
        self.txtName.SetFocus()
        self.txtName.SetInsertionPointEnd()

        event.Skip()

    def evt_Home(self, event):
        """Select My Pictures special folder"""
        if DEBUG: print('enter',iam())

        self.currpath = gs.myPictures()
        self.folders.ExpandPath(self.currpath)

        event.Skip()        

    def evt_Restore(self, event):
        """Restore original name if available"""
        if DEBUG: print('enter',iam())

        if not self.original:
            return

        oldname = self.fullfile
        newname = os.path.join(self.currpath, self.original)

        try:

            #Restore original name and remove undo ADS
            os.rename(oldname, newname)
            ads = newname + ADS
            os.remove(newname + ADS)

            #Update state variables
            self.currfile = os.path.split(newname)[-1]
            self.fullfile = os.path.join(self.folders.GetPath(), self.currfile)
            self.currbase = os.path.splitext(self.currfile)[0]
            self.currextn = os.path.splitext(self.currfile)[-1]
            self.original = ''
            self.SetStatus()

            self.GetNameFromFile()

            ##Update file list
            self.lstFiles.SetItemText(self.currindx, self.currfile)

        except OSError:
            self.Message('Could not restore original name. Undo info invalid')
        except FileExistsError:
            self.Message('Could not restore original name. A file with that name already exists')                  

        event.Skip()

    def evt_Save(self, event):
        """Rename the image file using new name plus index (if non-zero)"""
        if DEBUG: print('enter',iam())

        if self.txtName.Value == '':
            self.Message('New name can not be blank')
            return

        oldname = self.fullfile
        newname = os.path.join(self.currpath, self.CreateNewName())

        if DEBUG: print(f'{oldname=}\n{newname=}\n')

        try:
            os.rename(oldname, newname)

            #Save original file name for undo
            ads = newname + ADS

            if not os.path.isfile(ads):
                if DEBUG: print('save original name to',ads)
                open(ads, 'w').write(self.currfile)

            self.original = self.currfile            
            self.SetStatus()

            self.currfile = self.CreateNewName()
            self.fullfile = os.path.join(self.folders.GetPath(), self.currfile)
            self.currbase = os.path.splitext(self.currfile)[0]
            self.currextn = os.path.splitext(self.currfile)[-1]

            #Update the file list with the new name
            self.lstFiles.SetItemText(self.currindx, self.CreateNewName())
            self.SelectNext()
        except OSError:
            self.Message('The new name is not a valid file name')
        except FileExistsError:
            self.Message('A file with that name already exists')       

        event.Skip()

    def evt_NameChanged(self, event):
        """The new name has been changed either by dragging a tag from the common tag list
        or by manually typing in the new name text control. Because refreshing the current
        tag list can cause removal of extra blanks in the new name, we must disable events
        when calling RefreshTags from within this handler."""

        if DEBUG: print('enter',iam())

        if DEBUG: print(f'{self.txtName.Value=}')

        self.EvtHandlerEnabled = False
        ip = self.txtName.GetInsertionPoint()
        self.RefreshTags() 
        self.txtName.SetInsertionPoint(ip)            
        self.RecalcIndex()
        self.EvtHandlerEnabled = True

        try:    self.txtName.SetToolTip('NEW NAME: ' + self.CreateNewName())
        except: pass

        event.Skip()

    def evt_RightClick(self, event):
        """Common tag item right clicked"""
        if DEBUG: print('enter',iam()) 

        if self.currfile:

            srce = event.GetEventObject()
            text = self.GetSelected(srce)[0]
            dest = self.lstComm if srce == self.lstCurr else self.lstCurr

            #copy from srce to dest if not already in list

            if dest.FindItem(-1,text) == -1:
                dest.InsertItem(srce.ItemCount, text)

        event.Skip()

    def evt_StartDrag(self, event):
        """Starting drag from current or common tags control"""
        if DEBUG: print('enter',iam())

        obj  = event.GetEventObject()               #get the control initiating the drag
        text = obj.GetItemText(event.GetIndex())    #get the currently selected text    
        tobj = wx.TextDataObject(text)              #convert it to a text object        
        srce = wx.DropSource(obj)                   #create a drop source object        
        srce.SetData(tobj)                          #save text object in the new object 
        srce.DoDragDrop(True)                       #complete the drag/drop             

        event.Skip()

    def evt_DeleteTag(self, event):
        """Delete the tag from whichever list control currently has focus"""
        if DEBUG: print('enter',iam())

        if self.lstCurr.HasFocus():
            #delete from the current tag list
            text,indx = self.GetSelected(self.lstCurr)
            self.lstCurr.DeleteItem(indx)
            self.RefreshName()
        elif self.lstComm.HasFocus():
            #delete from the common tag list
            text,indx = self.GetSelected(self.lstComm)
            self.lstComm.DeleteItem(indx)
        else:
            return

        event.Skip()

    def evt_TagDeleted(self, event):
        if DEBUG: print('enter',iam())

        self.RefreshName()

        event.Skip()

    def evt_TagAdded(self, event):
        if DEBUG: print('enter',iam())

        self.RefreshName()

        event.Skip()

    def evt_Close(self, event):
        if DEBUG: print('enter',iam())

        self.SaveConfig()

        event.Skip()

    def evt_TextEnter(self, event):
        if DEBUG: print('enter',iam())
        event.Skip()

    def evt_Prev(self, event):
        if DEBUG: print('enter',iam())
        self.SelectPrevious()
        event.Skip()

    def evt_Next(self, event):
        if DEBUG: print('enter',iam())
        self.SelectNext()
        event.Skip()

    def evt_Help(self, event):
        self.Message(self.Help())
        event.Skip()

    def RefreshFileList(self):
        """Refresh the file list by reading all image files in the current folder"""
        if DEBUG: print('enter',iam())

        self.lstFiles.DeleteAllItems()

        for item in os.scandir(self.currpath):
            if pt.isImage(item.name):
                self.lstFiles.InsertItem(self.lstFiles.ItemCount, item.name)

        self.btnRestore.Disable()

    def Select(self, indx):
        """Select the file with the given zero-relative index"""
        if DEBUG: print('enter',iam())

        if indx < 0 or indx >= self.lstFiles.ItemCount:
            return

        if (focus := self.lstFiles.FocusedItem) != indx:
            #unselect the current item
            self.lstFiles.SetItemState(focus, 0, wx.LIST_STATE_SELECTED)

        #select the new item
        self.lstFiles.Focus(indx)
        self.lstFiles.SetItemState(indx, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)

    def SelectPrevious(self):
        """Select the previous file in the list if available"""
        if DEBUG: print('enter',iam())
        self.Select(self.lstFiles.FocusedItem - 1)

    def SelectNext(self):
        """Select the next file in the list if available"""
        if DEBUG: print('enter',iam())
        self.Select(self.lstFiles.FocusedItem + 1)

    def RefreshTags(self):
        """Rebuild current tag list from new file name"""
        if DEBUG: print('enter',iam())

        self.EvtHandlerEnabled = False

        self.lstCurr.DeleteAllItems()

        for tag in self.txtName.Value.split():
            if self.lstCurr.FindItem(-1,tag) == -1:
                self.lstCurr.InsertItem(self.lstCurr.ItemCount,tag)

        self.EvtHandlerEnabled = True


    def RefreshName(self):
        """Rebuild the new name by combining all tags in the current tag list"""
        if DEBUG: print('enter',iam())

        #combine all list items separated by one space
        name = ''
        for indx in range(self.lstCurr.ItemCount):
            name += self.lstCurr.GetItemText(indx) + ' '

        #disable events to prevent infinite recursion
        self.EvtHandlerEnabled = False
        self.txtName.Value = name
        self.EvtHandlerEnabled = True

        self.RecalcIndex()

        self.txtName.SetFocus()
        self.txtName.SetInsertionPointEnd()


    def GetSelected(self, lst):
        "Returns (text,index) of the currently selected item in a list control"""

        indx = lst.GetFocusedItem()
        text = lst.GetItemText(indx)

        return text, indx


    def GetNameFromFile(self):
        """
        Given a base file name (no path & no extension), strip off
        any index information at the end of the name (an integer enclosed
        in parentheses) and copy what is left to the NewName control. Any
        index found goes to the Index control.
        """
        if DEBUG: print('enter',iam())

        if (m := re.search('\(\d*\)$', self.currbase)):
            self.txtIndex.Value = self.currbase[m.start()+1:-1]
            self.txtName.Value = self.currbase[:m.start()-1].strip() + ' '
        else:
            self.txtIndex.Value = '0'
            self.txtName.Value = self.currbase + ' '

    def RecalcIndex(self):
        """Calculate an index to ensure unique file name"""
        if DEBUG: print('enter', iam())

        if self.txtName.Value == '': return

        #Look for the first free file name starting with index = 0       
        self.txtIndex.Value = '0'
        while self.FileExists(self.CreateNewName()):
            if DEBUG: print('trying',self.CreateNewName())
            self.txtIndex.Value = str(int(self.txtIndex.Value) + 1)       

    def CreateNewName(self):
        """Create a new name by combining the displayed new name with the index"""
        if DEBUG: print('enter', iam())

        indx = int(self.txtIndex.Value)

        if indx != 0:
            name = self.txtName.Value.strip() + (' (%02d)' % indx) + self.currextn.lower()
        else:
            name = self.txtName.Value.strip() + self.currextn.lower()

        return name.replace('  ',' ')

    def FileExists(self, file):
        """
        Scans the current file list (except for the currently selected
        file) and returns True if the given file is in the list.
        """
        if DEBUG: print(f'look for {file=}')
        for i in range(self.lstFiles.ItemCount):
            if i != self.currindx:
                if file.lower() == self.lstFiles.GetItemText(i).lower():
                    return True
        return False

    def GetExifDate(self, file):
        """Returns the EXIF data/time stamp if found in the file"""
        try:
            with open(file, 'rb') as fh:
                img = Image(fh)
                return 'EXIF date/time: ' + img.datetime
        except:
            return 'No EXIF data'

    def GetOriginalName(self):
        """Get original name if available"""

        ads = self.fullfile + ADS

        if os.path.isfile(ads):
            with open(ads) as fh:
                return fh.read()
        else:
            return ''

    def SetStatus(self):

        if self.original:            
            self.status.SetStatusText('Original Name:', 0)
            self.status.SetStatusText(self.original, 1)
            self.btnRestore.Enable()
        else:
            self.status.SetStatusText('No undo', 0)
            self.status.SetStatusText('', 1)
            self.btnRestore.Disable()

    def Message(self, text):
        wx.MessageBox(text, TITLE, wx.OK)

    def Help(self):
        return"""
        Tags from the selected file are displayed in the current (upper right panel) list. The
        lower right panel contains commonly used tags. Both lists can be modified by

        1. dragging tags from one to the other
        2. pressing DEL or CTRL+X to delete

        Deleting a tag from the current list will remove it fron the edited file name. Typing
        in the edited file name will update the current tag list. Changes to the common tag list
        will be retained for future use.

        The original file name is saved and may be restored by either

        1. clicking Restore
        2. pressing CTRL+R

        The file will not be renamed until you either

        1. Click Save
        2. press CTRL-S

        You will not be prompted to apply unsaved changes.

        Hotkeys are:

            Arrow Up   - select previous file
            Arrow Down - select next file
            CTRL+1     - strip camera crud
            CTRL+S     - save file name changes
            CTRL+X     - delete selected current or common tag
            CTRL+R     - restore original file name
            CTRL+H     - select home (My Pictures) folder
        """

from gevent import monkey
from selenium import webdriver
from lxml import etree

monkey.patch_socket()
import time
import requests
from stem import Signal
from stem.control import Controller
from bs4 import BeautifulSoup
import scrapy

from lxml import etree
from bs4 import BeautifulSoup
import requests
from lxml import etree
import requests

import requests
import re
import sys
import time
import math
# import urllib2
# import urlparse
import optparse
import hashlib
# from cgi import escape
from traceback import format_exc

import scrapy
# from Queue import Queue, Empty as QueueEmpty
from bs4 import BeautifulSoup
import gevent
import asyncio
from lxml import html
from urllib.parse import urlparse
import os
# data = requests.get("www.remyvastgoed.com/wp-content/uploads/2023/03/1-16.jpg").content
from PIL import Image  # pillow library
import requests
import urllib.request
from gevent import Greenlet
from gevent import monkey
from selenium import webdriver
from lxml import etree

monkey.patch_socket()
import time
import requests
from stem import Signal
from stem.control import Controller
from bs4 import BeautifulSoup
import scrapy
from dataclasses import dataclass
from lxml import etree
from bs4 import BeautifulSoup
import requests
from lxml import etree
import requests

#
import asyncio
import json
import posixpath
import re
from typing import Callable, Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlparse

#from scrapfly import ScrapflyClient, ScrapeConfig, ScrapeApiResponse
from loguru import logger as log
from tldextract import tldextract
from w3lib.url import canonicalize_url
"""
A function to download the page source of the given URL.
"""


HOME_PAGE = "https://www.remyvastgoed.com/104371"

# source = get_source(HOME_PAGE)


HOME_PAGE = "https://www.remyvastgoed.com/104371"
URL = "https://www.remyvastgoed.com/104371"
resp = requests.get(URL)
# Create DOM from HTML text
dom = etree.HTML(resp.text)
domain = urlparse("https://www.remyvastgoed.com/102536").netloc
print(domain)
domain = urlparse("https://www.remax.sr/nl/woningen/koopwoningen/hs877/la-recontre-5e-straat.html").netloc
print(domain)
domain = urlparse("https://osonangadjari.com/properties/lelydorperweg-3/").netloc
print(domain)
domain = urlparse("https://www.affidata.com/sh/huizen-te-koop/surinam/woning/287794").netloc
print(domain)

r = requests.get(HOME_PAGE)
source = html.fromstring(r.content)

site_links = ["https://www.affidata.com/sh/huizen-te-koop/surinam/woning/487739",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/463488",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/463487",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/463484",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/463483",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/463027",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/463026",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/463025",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/463024",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/463023",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/463022",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/463020",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/463019",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/463018",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/463017",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/463015",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/462922",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/462921",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/462918",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/462916",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/413870",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/408858",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/397523",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/397520",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/397519",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/397393",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/397392",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/394988",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/394680",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/394679",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/389950",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/384677",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/383922",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/381950",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/369100",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/368048",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/365186",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/363937",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/354268",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/353142",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/352716",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/350401",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/349659",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/343435",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/321950",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/321668",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/321184",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/320844",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/319833",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/316023",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/314600",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/309031",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/300751",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/300680",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/299776",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/299614",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/298919",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/295178",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/292072",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/288776",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/287794",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/286977",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/285386",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/283001",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/282788",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/281739",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/279744",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/15717",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/15492",
              "https://www.affidata.com/sh/huizen-te-koop/surinam/woning/13029",
              "https://osonangadjari.com/properties/lelydorperweg-3/",
              "https://osonangadjari.com/properties/vivian-ornastraat-2/",
              "https://osonangadjari.com/properties/doebe-project-2/",
              "https://osonangadjari.com/properties/monzonietstraat/",
              "https://osonangadjari.com/properties/boeskikowtoe/",
              "https://osonangadjari.com/properties/rampersadweg/",
              "https://osonangadjari.com/properties/6569/",
              "https://osonangadjari.com/properties/paragdhaniramsingweg/",
              "https://osonangadjari.com/properties/vredenburg-serie-b/",
              "https://osonangadjari.com/properties/johan-abdoelrahimstraat/",
              "https://osonangadjari.com/properties/sahadewweg/",
              "https://osonangadjari.com/properties/leiding-8-2/",
              "https://osonangadjari.com/properties/ramanandweg/",
              "https://osonangadjari.com/properties/leiding-11-2/",
              "https://osonangadjari.com/properties/ethaanstraat-2/",
              "https://osonangadjari.com/properties/ethaanstraat/",
              "https://osonangadjari.com/properties/leiding-8-3/",
              "https://osonangadjari.com/properties/indira-gandhiweg/",
              "https://osonangadjari.com/properties/mangriestraat/",
              "https://osonangadjari.com/properties/wanestraat/",
              "https://osonangadjari.com/properties/elizabeths-hof/",
              "https://osonangadjari.com/properties/pontbuiten/",
              "https://osonangadjari.com/properties/jamaludinstraat/",
              "https://osonangadjari.com/properties/vredenburg-serie-b-2/",
              "https://osonangadjari.com/properties/talsmastraat/",
              "https://osonangadjari.com/properties/tamanredjo/",
              "https://osonangadjari.com/properties/morgenstond-3/",
              "https://osonangadjari.com/properties/ringweg-noord-2/",
              "https://osonangadjari.com/properties/bhoendeiweg/",
              "https://osonangadjari.com/properties/bhramstraat/",
              "https://osonangadjari.com/properties/robbylaan-2/",
              "https://osonangadjari.com/properties/tajerbladweg/",
              "https://osonangadjari.com/properties/welgedacht-a-2/",
              "https://osonangadjari.com/properties/coesewijnestraat/",
              "https://osonangadjari.com/properties/nbm-project/",
              "https://osonangadjari.com/properties/estrellastraat/",
              "https://osonangadjari.com/properties/10382/",
              "https://osonangadjari.com/properties/brokopondolaan/",
              "https://osonangadjari.com/properties/tweelingenweg/",
              "https://osonangadjari.com/properties/zorg-en-hoop-5/",
              "https://osonangadjari.com/properties/nieuw-weergevondenweg/",
              "https://osonangadjari.com/properties/franchepanestraat-3/",
              "https://osonangadjari.com/properties/abachiweg/",
              "https://osonangadjari.com/properties/djitinderweg/",
              "https://osonangadjari.com/properties/4e-rijweg/",
              "https://osonangadjari.com/properties/welgedacht-c-3/",
              "https://osonangadjari.com/properties/4400/",
              "https://osonangadjari.com/properties/mohameddienweg/",
              "https://osonangadjari.com/properties/watrakanoestraat/",
              "https://osonangadjari.com/properties/charlesburg-3/",
              "https://osonangadjari.com/properties/ecoresort/",
              "https://osonangadjari.com/properties/1934/",
              "https://osonangadjari.com/properties/margarethalaan/",
              "https://osonangadjari.com/properties/15944/",
              "https://osonangadjari.com/properties/15804/",
              "https://osonangadjari.com/properties/kartaramstraat/",
              "https://osonangadjari.com/properties/houtzagerij-saramaccakanaal/",
              "https://osonangadjari.com/properties/assuriaproject/",
              "https://osonangadjari.com/properties/swarankumar-baldewsingweg/",
              "https://osonangadjari.com/properties/nijbroek-molgoweg/",
              "https://osonangadjari.com/properties/marijkestraat/",
              "https://osonangadjari.com/properties/14385/",
              "https://osonangadjari.com/properties/6710/",
              "https://osonangadjari.com/properties/hk-toevluchtwegchitoestr/",
              "https://osonangadjari.com/properties/verlengde-welgedacht-a/",
              "https://osonangadjari.com/properties/boedhiastraat/",
              "https://osonangadjari.com/properties/aquariusstraat-5/",
              "https://osonangadjari.com/properties/makelaar-breeveldstraat/",
              "https://osonangadjari.com/properties/walabastraat/",
              "https://osonangadjari.com/properties/8701/",
              "https://osonangadjari.com/properties/boeskikowtu-straat-2/",
              "https://osonangadjari.com/properties/cocobiacoweg/",
              "https://osonangadjari.com/properties/abdoelstraat/",
              "https://osonangadjari.com/properties/jibodh-project-4/",
              "https://osonangadjari.com/properties/columbiastraat/",
              "https://osonangadjari.com/properties/okrodam-2/",
              "https://osonangadjari.com/properties/vijfde-rijweg-2/",
              "https://osonangadjari.com/properties/sabanapark/",
              "https://osonangadjari.com/properties/jos-josi-don-fowroestraat/",
              "https://osonangadjari.com/properties/babunnootweg/",
              "https://osonangadjari.com/properties/marsaweg/",
              "https://osonangadjari.com/properties/anand-nagarweg/",
              "https://osonangadjari.com/properties/8083/",
              "https://osonangadjari.com/properties/spinnebloemstraat/",
              "https://osonangadjari.com/properties/sidodadistraat/",
              "https://osonangadjari.com/properties/wonderbladstraat-2/",
              "https://osonangadjari.com/properties/jibodh-project/",
              "https://osonangadjari.com/properties/clementineweg/",
              "https://osonangadjari.com/properties/4639/",
              "https://osonangadjari.com/properties/kalikastraat/",
              "https://osonangadjari.com/properties/10634/",
              "https://osonangadjari.com/properties/10295/",
              "https://osonangadjari.com/properties/10007/",
              "https://osonangadjari.com/properties/9925/",
              "https://osonangadjari.com/properties/9519/",
              "https://osonangadjari.com/properties/9538/",
              "https://osonangadjari.com/properties/9446/",
              "https://osonangadjari.com/properties/8678/",
              "https://osonangadjari.com/properties/8379/",
              "https://osonangadjari.com/properties/8354/",
              "https://osonangadjari.com/properties/8150/",
              "https://osonangadjari.com/properties/8113/",
              "https://osonangadjari.com/properties/7522/",
              "https://osonangadjari.com/properties/4824/",
              "https://osonangadjari.com/properties/5786/",
              "https://osonangadjari.com/properties/5877/",
              "https://osonangadjari.com/properties/337/",
              "https://osonangadjari.com/properties/5525/",
              "https://osonangadjari.com/properties/5435/",
              "https://osonangadjari.com/properties/5123/",
              "https://osonangadjari.com/properties/4745/",
              "https://osonangadjari.com/properties/3788/",
              "https://osonangadjari.com/properties/3200/",
              "https://www.remyvastgoed.com/104371",
              "https://www.remyvastgoed.com/87042",
              "https://www.remyvastgoed.com/72637",
              "https://www.remyvastgoed.com/28103",
              "https://www.remyvastgoed.com/101706",
              "https://www.remyvastgoed.com/104552",
              "https://www.remyvastgoed.com/101883",
              "https://www.remyvastgoed.com/101693",
              "https://www.remyvastgoed.com/101509",
              "https://www.remyvastgoed.com/92433",
              "https://www.remyvastgoed.com/104206",
              "https://www.remyvastgoed.com/81396",
              "https://www.remyvastgoed.com/104251",
              "https://www.remyvastgoed.com/104161",
              "https://www.remyvastgoed.com/103825",
              "https://www.remyvastgoed.com/99394",
              "https://www.remyvastgoed.com/92321",
              "https://www.remyvastgoed.com/78175",
              "https://www.remyvastgoed.com/103794",
              "https://www.remyvastgoed.com/103543",
              "https://www.remyvastgoed.com/103642",
              "https://www.remyvastgoed.com/50568",
              "https://www.remyvastgoed.com/91901",
              "https://www.remyvastgoed.com/93599",
              "https://www.remyvastgoed.com/99948",
              "https://www.remyvastgoed.com/94033",
              "https://www.remyvastgoed.com/36356",
              "https://www.remyvastgoed.com/87535",
              "https://www.remyvastgoed.com/102645",
              "https://www.remyvastgoed.com/102536",
              "https://www.remyvastgoed.com/102501",
              "https://www.remyvastgoed.com/100859",
              "https://www.remyvastgoed.com/100857",
              "https://www.remyvastgoed.com/102301",
              "https://www.remyvastgoed.com/102263",
              "https://www.remyvastgoed.com/84295",
              "https://www.remyvastgoed.com/59191",
              "https://www.remyvastgoed.com/102027",
              "https://www.remyvastgoed.com/63267",
              "https://www.remyvastgoed.com/50737",
              "https://www.remyvastgoed.com/100108",
              "https://www.remyvastgoed.com/99869",
              "https://www.remyvastgoed.com/101748",
              "https://www.remyvastgoed.com/88937",
              "https://www.remyvastgoed.com/97968",
              "https://www.remyvastgoed.com/96799",
              "https://www.remyvastgoed.com/95492",
              "https://www.remyvastgoed.com/101104",
              "https://www.remyvastgoed.com/100927",
              "https://www.remyvastgoed.com/99323",
              "https://www.remyvastgoed.com/100836",
              "https://www.remyvastgoed.com/99293",
              "https://www.remyvastgoed.com/99793",
              "https://www.remyvastgoed.com/100709",
              "https://www.remyvastgoed.com/100612",
              "https://www.remyvastgoed.com/100633",
              "https://www.remyvastgoed.com/69166",
              "https://www.remyvastgoed.com/100560",
              "https://www.remyvastgoed.com/54917",
              "https://www.remyvastgoed.com/99703",
              "https://www.remyvastgoed.com/82075",
              "https://www.remyvastgoed.com/91839",
              "https://www.remyvastgoed.com/86462",
              "https://www.remyvastgoed.com/64803",
              "https://www.remyvastgoed.com/96877",
              "https://www.remyvastgoed.com/92905",
              "https://www.remyvastgoed.com/99174",
              "https://www.remyvastgoed.com/86077",
              "https://www.remyvastgoed.com/98714",
              "https://www.remyvastgoed.com/98593",
              "https://www.remyvastgoed.com/98096",
              "https://www.remyvastgoed.com/95566",
              "https://www.remyvastgoed.com/96524",
              "https://www.remyvastgoed.com/97692",
              "https://www.remyvastgoed.com/97741",
              "https://www.remyvastgoed.com/96879",
              "https://www.remyvastgoed.com/97381",
              "https://www.remyvastgoed.com/66899",
              "https://www.remyvastgoed.com/83566",
              "https://www.remyvastgoed.com/97243",
              "https://www.remyvastgoed.com/97197",
              "https://www.remyvastgoed.com/78861",
              "https://www.remyvastgoed.com/97125",
              "https://www.remyvastgoed.com/96811",
              "https://www.remyvastgoed.com/70077",
              "https://www.remyvastgoed.com/96587",
              "https://www.remyvastgoed.com/96587",
              "https://www.remyvastgoed.com/96679",
              "https://www.remyvastgoed.com/96379",
              "https://www.remyvastgoed.com/49563",
              "https://www.remyvastgoed.com/96614",
              "https://www.remyvastgoed.com/96136",
              "https://www.remyvastgoed.com/96394",
              "https://www.remyvastgoed.com/96299",
              "https://www.remyvastgoed.com/95912",
              "https://www.remyvastgoed.com/95693",
              "https://www.remyvastgoed.com/93835",
              "https://www.remyvastgoed.com/95319",
              "https://www.remyvastgoed.com/94873",
              "https://www.remyvastgoed.com/84441",
              "https://www.remyvastgoed.com/44117",
              "https://www.remyvastgoed.com/94197",
              "https://www.remyvastgoed.com/87008",
              "https://www.remyvastgoed.com/94157",
              "https://www.remyvastgoed.com/94132",
              "https://www.remyvastgoed.com/93731",
              "https://www.remyvastgoed.com/93831",
              "https://www.remyvastgoed.com/92852",
              "https://www.remyvastgoed.com/87996",
              "https://www.remyvastgoed.com/93555",
              "https://www.remyvastgoed.com/93358",
              "https://www.remyvastgoed.com/89041",
              "https://www.remyvastgoed.com/93258",
              "https://www.remyvastgoed.com/88824",
              "https://www.remyvastgoed.com/48757",
              "https://www.remyvastgoed.com/92979",
              "https://www.remyvastgoed.com/82584",
              "https://www.remyvastgoed.com/92625",
              "https://www.remyvastgoed.com/39386",
              "https://www.remyvastgoed.com/92712",
              "https://www.remyvastgoed.com/91729",
              "https://www.remyvastgoed.com/92545",
              "https://www.remyvastgoed.com/91791",
              "https://www.remyvastgoed.com/91915",
              "https://www.remyvastgoed.com/91850",
              "https://www.remyvastgoed.com/84017",
              "https://www.remyvastgoed.com/52176",
              "https://www.remyvastgoed.com/91446",
              "https://www.remyvastgoed.com/59317",
              "https://www.remyvastgoed.com/90550",
              "https://www.remyvastgoed.com/91174",
              "https://www.remyvastgoed.com/91113",
              "https://www.remyvastgoed.com/84210",
              "https://www.remyvastgoed.com/90973",
              "https://www.remyvastgoed.com/90961",
              "https://www.remyvastgoed.com/90954",
              "https://www.remyvastgoed.com/90911",
              "https://www.remyvastgoed.com/90876",
              "https://www.remyvastgoed.com/90898",
              "https://www.remyvastgoed.com/79829",
              "https://www.remyvastgoed.com/90304",
              "https://www.remyvastgoed.com/90120",
              "https://www.remyvastgoed.com/90422",
              "https://www.remyvastgoed.com/90237",
              "https://www.remyvastgoed.com/90218",
              "https://www.remyvastgoed.com/47411",
              "https://www.remyvastgoed.com/90125",
              "https://www.remyvastgoed.com/90149",
              "https://www.remyvastgoed.com/89975",
              "https://www.remyvastgoed.com/89872",
              "https://www.remyvastgoed.com/89752",
              "https://www.remyvastgoed.com/89365",
              "https://www.remyvastgoed.com/89120",
              "https://www.remyvastgoed.com/42332",
              "https://www.remyvastgoed.com/89135",
              "https://www.remyvastgoed.com/50168",
              "https://www.remyvastgoed.com/58648",
              "https://www.remyvastgoed.com/83560",
              "https://www.remyvastgoed.com/88626",
              "https://www.remyvastgoed.com/88511",
              "https://www.remyvastgoed.com/84574",
              "https://www.remyvastgoed.com/74262",
              "https://www.remyvastgoed.com/78847",
              "https://www.remyvastgoed.com/75654",
              "https://www.remyvastgoed.com/88112",
              "https://www.remyvastgoed.com/47192",
              "https://www.remyvastgoed.com/87860",
              "https://www.remyvastgoed.com/60824",
              "https://www.remyvastgoed.com/87409",
              "https://www.remyvastgoed.com/87193",
              "https://www.remyvastgoed.com/87050",
              "https://www.remyvastgoed.com/39461",
              "https://www.remyvastgoed.com/34194",
              "https://www.remyvastgoed.com/39743",
              "https://www.remyvastgoed.com/86615",
              "https://www.remyvastgoed.com/55923",
              "https://www.remyvastgoed.com/55569",
              "https://www.remyvastgoed.com/52166",
              "https://www.remyvastgoed.com/52052",
              "https://www.remyvastgoed.com/68693",
              "https://www.remyvastgoed.com/68967",
              "https://www.remyvastgoed.com/86027",
              "https://www.remyvastgoed.com/85922",
              "https://www.remyvastgoed.com/49055",
              "https://www.remyvastgoed.com/72126",
              "https://www.remyvastgoed.com/85249",
              "https://www.remyvastgoed.com/84917",
              "https://www.remyvastgoed.com/84764",
              "https://www.remyvastgoed.com/84257",
              "https://www.remyvastgoed.com/82745",
              "https://www.remyvastgoed.com/83827",
              "https://www.remyvastgoed.com/83842",
              "https://www.remyvastgoed.com/83712",
              "https://www.remyvastgoed.com/83732",
              "https://www.remyvastgoed.com/83557",
              "https://www.remyvastgoed.com/83393",
              "https://www.remyvastgoed.com/83303",
              "https://www.remyvastgoed.com/55543",
              "https://www.remyvastgoed.com/77782",
              "https://www.remyvastgoed.com/83010",
              "https://www.remyvastgoed.com/82726",
              "https://www.remyvastgoed.com/82644",
              "https://www.remyvastgoed.com/81421",
              "https://www.remyvastgoed.com/5390",
              "https://www.remyvastgoed.com/81817",
              "https://www.remyvastgoed.com/63639",
              "https://www.remyvastgoed.com/75999",
              "https://www.remyvastgoed.com/81451",
              "https://www.remyvastgoed.com/81133",
              "https://www.remyvastgoed.com/40537",
              "https://www.remyvastgoed.com/79482",
              "https://www.remyvastgoed.com/76539",
              "https://www.remyvastgoed.com/78058",
              "https://www.remyvastgoed.com/962",
              "https://www.remyvastgoed.com/78424",
              "https://www.remyvastgoed.com/78265",
              "https://www.remyvastgoed.com/16393",
              "https://www.remyvastgoed.com/77698",
              "https://www.remyvastgoed.com/77348",
              "https://www.remyvastgoed.com/76408",
              "https://www.remyvastgoed.com/77117",
              "https://www.remyvastgoed.com/36795",
              "https://www.remyvastgoed.com/76545",
              "https://www.remyvastgoed.com/37750",
              "https://www.remyvastgoed.com/76133",
              "https://www.remyvastgoed.com/51158",
              "https://www.remyvastgoed.com/75469",
              "https://www.remyvastgoed.com/75412",
              "https://www.remyvastgoed.com/32753",
              "https://www.remyvastgoed.com/74958",
              "https://www.remyvastgoed.com/74818",
              "https://www.remyvastgoed.com/74469",
              "https://www.remyvastgoed.com/74511",
              "https://www.remyvastgoed.com/74275",
              "https://www.remyvastgoed.com/71928",
              "https://www.remyvastgoed.com/74287",
              "https://www.remyvastgoed.com/68364",
              "https://www.remyvastgoed.com/74062",
              "https://www.remyvastgoed.com/73259",
              "https://www.remyvastgoed.com/73261",
              "https://www.remyvastgoed.com/35424",
              "https://www.remyvastgoed.com/72492",
              "https://www.remyvastgoed.com/8279",
              "https://www.remyvastgoed.com/71668",
              "https://www.remyvastgoed.com/71727",
              "https://www.remyvastgoed.com/28983",
              "https://www.remyvastgoed.com/70004",
              "https://www.remyvastgoed.com/69645",
              "https://www.remyvastgoed.com/69096",
              "https://www.remyvastgoed.com/68794",
              "https://www.remyvastgoed.com/68816",
              "https://www.remyvastgoed.com/68827",
              "https://www.remyvastgoed.com/35563",
              "https://www.remyvastgoed.com/45740",
              "https://www.remyvastgoed.com/68016",
              "https://www.remyvastgoed.com/67928",
              "https://www.remyvastgoed.com/66988",
              "https://www.remyvastgoed.com/64171",
              "https://www.remyvastgoed.com/66767",
              "https://www.remyvastgoed.com/66485",
              "https://www.remyvastgoed.com/66166",
              "https://www.remyvastgoed.com/66360",
              "https://www.remyvastgoed.com/66010",
              "https://www.remyvastgoed.com/62676",
              "https://www.remyvastgoed.com/65544",
              "https://www.remyvastgoed.com/65223",
              "https://www.remyvastgoed.com/55921",
              "https://www.remyvastgoed.com/65089",
              "https://www.remyvastgoed.com/65028",
              "https://www.remyvastgoed.com/63818",
              "https://www.remyvastgoed.com/59825",
              "https://www.remyvastgoed.com/62310",
              "https://www.remyvastgoed.com/62094",
              "https://www.remyvastgoed.com/62029",
              "https://www.remyvastgoed.com/61588",
              "https://www.remyvastgoed.com/61324",
              "https://www.remyvastgoed.com/33801",
              "https://www.remyvastgoed.com/60098",
              "https://www.remyvastgoed.com/41831",
              "https://www.remyvastgoed.com/59431",
              "https://www.remyvastgoed.com/58292",
              "https://www.remyvastgoed.com/57757",
              "https://www.remyvastgoed.com/39775",
              "https://www.remyvastgoed.com/50827",
              "https://www.remyvastgoed.com/56667",
              "https://www.remyvastgoed.com/44891",
              "https://www.remyvastgoed.com/55840",
              "https://www.remyvastgoed.com/55363",
              "https://www.remyvastgoed.com/54825",
              "https://www.remyvastgoed.com/54402",
              "https://www.remyvastgoed.com/49626",
              "https://www.remyvastgoed.com/52887",
              "https://www.remyvastgoed.com/41453",
              "https://www.remyvastgoed.com/50669",
              "https://www.remyvastgoed.com/51321",
              "https://www.remyvastgoed.com/49582",
              "https://www.remyvastgoed.com/48755",
              "https://www.remyvastgoed.com/48467",
              "https://www.remyvastgoed.com/48296",
              "https://www.remyvastgoed.com/48075",
              "https://www.remyvastgoed.com/46261",
              "https://www.remyvastgoed.com/46109",
              "https://www.remyvastgoed.com/45411",
              "https://www.remyvastgoed.com/45332",
              "https://www.remyvastgoed.com/14805",
              "https://www.remyvastgoed.com/43093",
              "https://www.remyvastgoed.com/42864",
              "https://www.remyvastgoed.com/42389",
              "https://www.remyvastgoed.com/40517",
              "https://www.remyvastgoed.com/7500",
              "https://www.remyvastgoed.com/39234",
              "https://www.remyvastgoed.com/38601",
              "https://www.remyvastgoed.com/38506",
              "https://www.remyvastgoed.com/38252",
              "https://www.remyvastgoed.com/38320",
              "https://www.remyvastgoed.com/38308",
              "https://www.remyvastgoed.com/37544",
              "https://www.remyvastgoed.com/35997",
              "https://www.remyvastgoed.com/35489",
              "https://www.remyvastgoed.com/34880",
              "https://www.remyvastgoed.com/34827",
              "https://www.remyvastgoed.com/34279",
              "https://www.remyvastgoed.com/30194",
              "https://www.remyvastgoed.com/29580",
              "https://www.remyvastgoed.com/29257",
              "https://www.remyvastgoed.com/28822",
              "https://www.remyvastgoed.com/16247",
              "https://www.remyvastgoed.com/15603",
              "https://www.remyvastgoed.com/12867",
              "https://www.remyvastgoed.com/12690",
              "https://www.remyvastgoed.com/12271",
              "https://www.remyvastgoed.com/4692",
              "https://www.remyvastgoed.com/4692",
              "https://www.remyvastgoed.com/27810",
              "https://www.mahanvastgoed.com/property/okro-uduweg-te-wanica/",
              "https://www.mahanvastgoed.com/property/zwartenhovenburgstraat-te-paramaribo/",
              "https://www.mahanvastgoed.com/property/kwattaweg-te-paramaribo-3/",
              "https://www.mahanvastgoed.com/property/kwattaweg-te-paramaribo/",
              "https://www.mahanvastgoed.com/property/nejalweg-te-wanica/",
              "https://www.mahanvastgoed.com/property/mamboelastraat-te-paramaribo/",
              "http://www.apurahousing.com/uitgebreidzoeken.aspx?zoekenop=va&st1=1&st2=1&pi=2",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs893/poerwodadi-weg.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs894/hendrikstraat-47.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs890/rahemal-70a.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs734/sadiodam-34.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs889/indira-gandhiweg.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs888/izaak-burnetstraat-69.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs875/chinitiestraat.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs887/kapitein-a-philipstraat-49.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs886/pommerosestraat-6.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs854/idoeweg-no-44.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs859/karanweg.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs884/chopinstraat-83.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs779/grandostraat-53.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs883/advocaatstraat-11.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs820/verkocht/laan-van-vertrouwen-pc-84b-gated-community.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs881/stippelvarensweg.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs793/oost-westverbinding-tamansari.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs874/calliopsestraat-12.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs858/verkocht/koolestraat-72.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs879/gated-community-villa-park-kwatta-waterkersstraat-50.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs699/anniestraat-32-hoek-hardeveldstraat.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs750/khadiweg-45.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs877/la-recontre-5e-straat.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs878/gogomangostraat-17.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs815/rijsdijkweg-462.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs871/monizstraat-5-bennies-park.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs872/la-recontre-4e-straat.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs831/tweelingenweg-hoek-steenbokweg.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs861/wc-kennedystraat-9.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs397/hugostraat-13.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs870/bhattoeweg-178a.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs707/chamroeweg-89.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs862/laan-van-louiseshof-38.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs805/prodjosoekartoweg-21-lelydorp.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs866/razabsekhweg-42-46.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs855/masoesastraat-31.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs674/lakeland-tout-lui-faut-colettelaan-13.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs840/baboe-sewrajsingweg-43.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs826/saltatiestraat-26.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs819/goosenweg-34-vredenburg-serie-b.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs637/bhattoeweg-178.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs860/mosstraat-3.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs856/eikvarensweg-10-12.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs795/ro-carstersstraat-16.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs848/woonproject-catharina-sophia-no-11.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs828/panchamweg-8.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs736/eduardstraat-24.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs851/boekoestraat-hoek-kwamikondrestraat.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs702/zegellakpalmlaan-29-palm-village.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs846/gompertsstraat-166.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs845/soepgroenteweg-71.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs785/verkocht/laan-van-steendam-07-gated-community-de-schuilplaats.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs774/vredenburgweg-56.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs749/zwartebondstraat-116-reeberg-project.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs835/fabrikaatstraat-88.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs806/helstonestraat-11-hoek-sewbarath-misserstraat.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs780/welgedacht-a-weg-394b.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs782/porfierstraat-39.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs813/lashkarweg-78-a-omgeving-vierde-rijweg.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs741/commissaris-roblesweg-pc-413-commewijne.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs827/eusieweg-6.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs824/leiding-8-br-139.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs791/laan-van-nobelheid.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs766/saprapiweg-3.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs685/sitalweg-109.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs787/afobakalaan-7-hoek-phedralaan.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs810/kankawastraat-19-zijstraat-toekomstweg.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs755/overbrugweg-10.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs796/bananenweg-87-jarikaba.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs747/wicherstraat-35.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs527/colony-31.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs801/hardwarsingweg-04.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs799/mangolaan-86c.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs783/gonggrijpstraat-184.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs781/maanviweg-19-welgedacht-b.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs776/surya-nagarweg-12.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs705/bieslookstraat-2.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs772/hoek-uranus-en-plejadenstraat-62.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs771/eusieweg-38.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs770/boxel-sir-winston-churchillweg-673.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs733/hanna-slustweg-149.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs753/weg-naar-reeberg-112.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs744/cordialaan-21.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs313/etnalaan-19.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs618/nijbroek-molgoweg-21.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs725/braamshoopweg-04.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs743/segansistraat-08.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs727/anton-mauvestraat-02-hoek-mesdagstraat-07.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs730/patnaweg-29.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs724/van-brussellaan-14.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs728/van-varseveldweg-30.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs489/monzonietstraat-3.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs700/mangrovestraat-17.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs713/eusieweg-39.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs651/commissarisweg-9.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs719/tayerbladweg-06-district-saramacca.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs596/fijne-klaroenweg-25.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs687/stondoifistraat-9-hoek-sriostraat.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs693/curacao-de-nederlandse-antillen.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs622/anton-dragtenweg.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs588/perzikbonenweg-302.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs660/javaweg-perc-199.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs679/overbrugweg-24.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs528/ramalaan-37.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs577/hardwarsingweg-28.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs404/powisistraat-109.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs476/kwattaweg-28.html",
              "https://www.remax.sr/nl/woningen/koopwoningen/hs491/commissaris-weytinghweg-59i.html"]


def makeRowLineOfFile(self, url):
        if resp.status_code == 200:
            # Using straatnaam
            dom = etree.HTML(resp.text)
            straatnaam = dom.xpath("//*[@id=""top_section""]/h2[1]")
            print(straatnaam)

            # Using BeautifulSoup
            soup = BeautifulSoup(resp.text, "lxml")
            straatnaam = soup.select('#top_section > h2.title')
            print(straatnaam[0].string)

            # Using prijs
            dom = etree.HTML(resp.text)
            elements = dom.xpath("//*[@id=""top_section""]/h2[2]")
            print(elements)

            # Using BeautifulSoup
            soup = BeautifulSoup(resp.text, "lxml")
            elements = soup.select('#top_section > h2.prijs')
            print(elements[0].text)

            # Using kamers
            dom = etree.HTML(resp.text)
            elements = dom.xpath("//*[@id=""bottom_section""]/div/div[1]/table/tbody/tr[5]/td[2]")
            print(elements)

            # Using BeautifulSoup
            soup = BeautifulSoup(resp.text, "lxml")
            elements = soup.select(
                '#bottom_section > div > div.kenmerken > table > tbody > tr:nth-child(5) > td:nth-child(2)')
            print(elements)

            # Using slaapkamers
            dom = etree.HTML(resp.text)
            elements = dom.xpath("//*[@id=""bottom_section""]/div/div[1]/table/tbody/tr[6]/td[2]")
            print(elements)

            # Using BeautifulSoup
            soup = BeautifulSoup(resp.text, "lxml")
            elements = soup.select(
                '#bottom_section > div > div.kenmerken > table > tbody > tr:nth-child(6) > td:nth-child(2)')
            print(elements)

            # Using perceeloppervlakte
            dom = etree.HTML(resp.text)
            elements = dom.xpath("//*[@id=""bottom_section""]/div/div[1]/table/tbody/tr[3]/td[2]")
            print(elements)

            # Using BeautifulSoup
            soup = BeautifulSoup(resp.text, "lxml")
            elements = soup.select(
                '#bottom_section > div > div.kenmerken > table > tbody > tr:nth-child(3) > td:nth-child(2)')
            print(elements)

            # Using bouwoppervlakte
            dom = etree.HTML(resp.text)
            elements = dom.xpath("//*[@id=""bottom_section""]/div/div[1]/table/tbody/tr[4]/td[2]")
            print(elements)

            # Using BeautifulSoup
            soup = BeautifulSoup(resp.text, "lxml")
            elements = soup.select(
                '#bottom_section > div > div.kenmerken > table > tbody > tr:nth-child(4) > td:nth-child(2)')
            print(elements)

            # Using class
            dom = etree.HTML(resp.text)
            elements = dom.xpath("//*[@id=""bottom_section""]/div/div[1]")
            # print(elements)

            # Using BeautifulSoup
            soup = BeautifulSoup(resp.text, "lxml")
            elements = soup.select('#bottom_section > div > div.kenmerken')
            print(elements[0])
            type = (soup.find("td", text="Type").find_next_sibling("td").string)
            print(type)
            title = (soup.find("td", text="Titel").find_next_sibling("td").string)
            print(title)
            Perceeloppervlakte = (soup.find("td", text="Perceeloppervlakte").find_next_sibling("td").string)
            print(Perceeloppervlakte)
            Bouwoppervlakte = (soup.find("td", text="Bouwoppervlakte").find_next_sibling("td").string)
            print(Bouwoppervlakte)
            aantal_kamers = (soup.find("td", text="Aantal kamers").find_next_sibling("td").string)
            print(aantal_kamers)
            aantal_slaapkamers = (soup.find("td", text="Aantal slaapkamers").find_next_sibling("td").string)
            print(aantal_slaapkamers)

            # print("a={0}".format(straatnaam))
            # print(b"hi there, straatnaam=%s\n,  ", straatnaam)
            # print("hi there, straatnaam=%s\n", straatnaam)
            # print("Hello, this is my name %s and my age %d", "Martin", 20)

            divs = soup.findAll("galleria-image")
            print(divs)
            divs = soup.findAll("galleria-images")
            print(divs)
            divs = soup.findAll("table", {"class": "kenmerken"})
            print(divs)
            images = soup.find_all('img')
            print(images)
            images_url = images[0]['src']
            images = soup.findAll('img')
            for image in images:
                print(image['src'])

            # images_url
            # print(images_url)
            # #data = requests.get("www.remyvastgoed.com/wp-content/uploads/2023/03/1-16.jpg").content
            # from PIL import Image #pillow library
            # import requests
            # import urllib.request

            # im = Image.open(requests.get("www.remyvastgoed.com/wp-content/uploads/2023/03/1-16.jpg", stream=True).raw)

            # Opening a new file named img with extension .jpg
            # This file would store the data of the image file
            # f = open('img.jpg', 'wb')
            # Storing the image data inside the data variable to the file
            # f.write(im)
            # f.close()
            img_data = requests.get("www.remyvastgoed.com/wp-content/uploads/2023/03/1-16.jpg").content
            with open('netflix.jpg', 'wb') as handler:
                handler.write(img_data)
            with open('pic1.jpg', 'wb') as handle:
                response = requests.get('www.remyvastgoed.com/wp-content/uploads/2023/03/1-16.jpg', stream=True)

                if not response.ok:
                    print(response)

                for block in response.iter_content(1024):
                    if not block:
                        break

                    handle.write(block)
            urllib.request.urlretrieve(
                'remyvastgoed.com/wp-content/uploads/2023/03/1-16.jpg',
                "gfg.png")
            #
            img = Image.open("gfg.png")
            img.show()

            # find image with '1-' and  followed up with any number that ends with .jpg
            r = requests.get("http://www.remyvastgoed.com/wp-content/uploads/2023/03/1-16.jpg", allow_redirects=True)
            dir_name =straatnaam[0].string
            image_name = straatnaam[0].string + ".jpg"
            full_file_path=dir_name+"/"+image_name
            #open(full_file_path, 'wb').write(r.content)
            #filename = "/foo/bar/baz.txt"

            os.makedirs(os.path.dirname(full_file_path), exist_ok=True)
            with open(full_file_path, "wb") as f:
                f.write(r.content)
            print(straatnaam[0].string, type, title, Perceeloppervlakte, Bouwoppervlakte, aantal_kamers,
                  aantal_slaapkamers)
            line = straatnaam[
                       0].string + "," + type + "," + title + "," + Perceeloppervlakte + "," + Bouwoppervlakte + "," + aantal_kamers + "," + aantal_slaapkamers + "\n"
            with open('somefile.txt', 'a') as the_file:
                the_file.write(line)

            divs = soup.findAll("table", {"class": "kenmerken"})
            for div in divs:
                row = ''
                rows = div.findAll('tr')
                for row in rows:
                    print(row)
                    # if (row.text.find("PHONE") > -1):
                    #     print(row.text)

            li_list = source.xpath("//li[contains(@class, 'fpGridBox grid')]")
            item_names = [
                li.xpath(".//a[@class='itemTitle bp-p-dealLink bp-c-link']") for li in li_list
            ]
        return url
#
#
# for web_url in site_links:
#     if re.search('remyvastgoed.com', web_url):
#         try:
#             print(web_url)
#
#             # ################
#             # #
#             # #
#             # ################
#             URL = web_url
#             resp = requests.get(URL)
#             soup = BeautifulSoup(resp.text, "lxml")
#
#             divs = soup.findAll("table", {"class": "kenmerken"})
#             # for div in divs:
#             #     row = ''
#             #     rows = div.findAll('td')
#             #     for row in rows:
#             #         print(row[0].string)
#             #         print(row[1].string)
#             # ################
#             # #
#             # #
#             # ################
#             # Using straatnaam
#             soup = BeautifulSoup(resp.text, "lxml")
#             straatnaam = soup.select('#top_section > h2.title')
#
#             try:
#                 print(straatnaam[0].string)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#
#             # Using prijs
#             prijs = soup.select('#top_section > h2.prijs')
#
#             try:
#                 print(prijs[0].text)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#
#             # # Using kamers
#             aantal_kamers = soup.select(
#                 '#bottom_section > div > div.kenmerken > table > tbody > tr:nth-child(5) > td:nth-child(2)')
#             print(aantal_kamers)
#             #
#             # # Using slaapkamers
#             aantal_slaapkamers = soup.select(
#                 '#bottom_section > div > div.kenmerken > table > tbody > tr:nth-child(6) > td:nth-child(2)')
#             print(aantal_slaapkamers)
#             #
#             # # Using perceeloppervlakte
#             perceel_opp = soup.select(
#                 '#bottom_section > div > div.kenmerken > table > tbody > tr:nth-child(3) > td:nth-child(2)')
#             print(perceel_opp)
#             #
#             # # Using bouwoppervlakte
#             bouwoppervlakte = soup.select(
#                 '#bottom_section > div > div.kenmerken > table > tbody > tr:nth-child(4) > td:nth-child(2)')
#             print(bouwoppervlakte)
#
#             # ################
#             # #
#             # #
#             # ################
#             soup = BeautifulSoup(resp.text, "lxml")
#             elements = soup.select('#bottom_section > div > div.kenmerken')
#             # print(elements[0])
#             # type = (soup.find("td", text="Type").find_next_sibling("td").string)
#             # print(type)
#             # title = (soup.find("td", text="Titel").find_next_sibling("td").string)
#             # print(title)
#             # Perceeloppervlakte = (soup.find("td", text="Perceeloppervlakte").find_next_sibling("td").string)
#             # print(Perceeloppervlakte)
#             # Bouwoppervlakte = (soup.find("td", text="Bouwoppervlakte").find_next_sibling("td").string)
#             # print(Bouwoppervlakte)
#             # aantal_kamers = (soup.find("td", text="Aantal kamers").find_next_sibling("td").string)
#             # print(aantal_kamers)
#             # aantal_slaapkamers = (soup.find("td", text="Aantal slaapkamers").find_next_sibling("td").string)
#
#             # ################
#             # # ToDO
#             # #
#             # ################
#             regex_image_url = "(http?:\/\/.*\.(?:png|jpg))"
#             regex_image_filename = "([^\\s]+(\\.(?i)(jpe?g|png|gif|bmp))$)"
#             regex_image_name_from_url = "(/[\w-]+\.(jpg|png|txt)/g)"
#             # myimage_name = re.compile(', (.*)\n')
#             # use one of the following to find  the complete link to an image posted on the website
#             divs = soup.findAll("galleria-image")
#             # images_url = images[0]['src']
#             # images = soup.find_all('img')
#             divs = soup.findAll("galleria-images")
#             # image_urls = re.findall(r'http?:\/\/.*\.(?:png|jpg)')
#             # for found_image_url in image_urls:
#             #     resulted_filname = re.match(regex_image_filename, found_image_url)  # Returns Match object
#             #     print(resulted_filname)
#             #
#             divs = soup.findAll("galleria-images")
#             images = soup.find_all('img')
#             images_url = images[0]['src']
#             images = soup.findAll('img')
#             for image in images:
#                 print(image['src'])
#             # myimage.findall(images)
#             r = requests.get(web_url, allow_redirects=True)
#
#             try:
#                 image_name = straatnaam[0].string + ".jpg"
#                 open(image_name, 'wb').write(r.content)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#
#             # ################
#             # #
#             # #
#             # ################
#         except requests.exceptions.Timeout:
#             print(" ")
#         except requests.exceptions.TooManyRedirects:
#             print(" ")
#         except requests.exceptions.RequestException as e:
#             print(" ")
#             raise SystemExit(e)
#
#
#     if re.search('osonangadjari.com', web_url):
#         print(web_url)
#         try:
#             if resp.status_code == 200:
#                 # ################
#                 # #
#                 # #
#                 # ################
#                 URL = web_url
#                 resp = requests.get(URL)
#                 soup = BeautifulSoup(resp.text, "lxml")
#
#                 divs = soup.findAll("table", {"class": "kenmerken"})
#
#                 soup = BeautifulSoup(resp.text, "lxml")
#
#                 # body > div.page-wrapper > div.main > div > div > div.social-cons > span > a
#                 postid = soup.select('body > div.page-wrapper > div.main > div > div > div.social-cons > span > a')
#                 print(postid[0].string)
#
#                 straatnaam = soup.select('#post-13962 > h3')
#                 print(straatnaam[0].string)
#
#                 plaats = soup.select('#post-13962 > span')
#                 print(straatnaam[0].string)
#
#                 # Using prijs
#                 prijs = soup.select(
#                     '#post-9925 > div > div.row > div.col-sm-4 > div.table-group.overview.property-overview > table > tbody > tr:nth-child(1) > td:nth-child(2)')
#                 print(prijs[0].text)
#
#                 Type = soup.select(
#                     '#post-9925 > div > div.row > div.col-sm-4 > div.table-group.overview.property-overview > table > tbody > tr:nth-child(2) > td:nth-child(2)')
#                 print(Type[0].text)
#
#                 verkocht = soup.select(
#                     '#post-9925 > div > div.row > div.col-sm-4 > div.table-group.overview.property-overview > table > tbody > tr:nth-child(3) > td:nth-child(2)')
#                 print(verkocht[0].text)
#
#                 Overeenkomst = soup.select(
#                     '#post-9925 > div > div.row > div.col-sm-4 > div.table-group.overview.property-overview > table > tbody > tr:nth-child(4) > td:nth-child(2)')
#                 print(Overeenkomst[0].text)
#
#                 Status = soup.select(
#                     '#post-9925 > div > div.row > div.col-sm-4 > div.table-group.overview.property-overview > table > tbody > tr:nth-child(5) > td:nth-child(2)')
#                 print(Status[0].text)
#
#                 woonoppervlakte = soup.select(
#                     '#post-9925 > div > div.row > div.col-sm-4 > div.table-group.overview.property-overview > table > tbody > tr:nth-child(6) > td:nth-child(2)')
#                 print(woonoppervlakte[0].text)
#
#                 Perceel_Oppervlakte = soup.select(
#                     '#post-9925 > div > div.row > div.col-sm-4 > div.table-group.overview.property-overview > table > tbody > tr:nth-child(7) > td:nth-child(2)')
#                 print(Perceel_Oppervlakte[0].text)
#
#                 Materiaal = soup.select(
#                     '#post-9925 > div > div.row > div.col-sm-4 > div.table-group.overview.property-overview > table > tbody > tr:nth-child(8) > td:nth-child(2)')
#                 print(Materiaal[0].text)
#
#                 Aantal_kamers = soup.select(
#                     '#post-9925 > div > div.row > div.col-sm-4 > div.table-group.overview.property-overview > table > tbody > tr:nth-child(9) > td:nth-child(2)')
#                 print(Aantal_kamers[0].text)
#
#                 Slaapkamers = soup.select(
#                     '#post-9925 > div > div.row > div.col-sm-4 > div.table-group.overview.property-overview > table > tbody > tr:nth-child(10) > td:nth-child(2)')
#                 print(Slaapkamers[0].text)
#
#                 Badkamers = soup.select(
#                     '#post-9925 > div > div.row > div.col-sm-4 > div.table-group.overview.property-overview > table > tbody > tr:nth-child(11) > td:nth-child(2)')
#                 print(Badkamers[0].text)
#
#                 # ################
#                 # #
#                 # #
#                 # ################
#
#                 # property-detail-section-gallery > div > div.property-detail-gallery.owl-carousel.owl-theme.owl-loaded > div.owl-stage-outer.owl-height > div > div.owl-item.active > a > span
#                 image = soup.select(
#                     '#property-detail-section-gallery > div > div.property-detail-gallery.owl-carousel.owl-theme.owl-loaded > div.owl-stage-outer.owl-height > div > div.owl-item.active > a > span')
#
#                 r = requests.get(image, allow_redirects=True)
#                 image_name = straatnaam[0].string + ".jpg"
#                 open(image_name, 'wb').write(r.content)
#
#                 # ################
#                 # #
#                 # #
#                 # ################
#
#                 print(straatnaam[0].string, type, postid, straatnaam, plaats, prijs, Type, verkocht, Overeenkomst,
#                       Status, woonoppervlakte, Perceel_Oppervlakte, Materiaal, Aantal_kamers, Slaapkamers, Badkamers,
#                       aantal_kamers, aantal_slaapkamers)
#                 line = straatnaam[
#                            0].string + "," + type + "," + postid + "," + straatnaam + "," + plaats + "," + prijs + "," + Type + "," + verkocht + "," + Overeenkomst + "," + Status + "," + woonoppervlakte + "," + Perceel_Oppervlakte + "," + Materiaal + "," + Aantal_kamers + "," + Badkamers + "," + aantal_kamers + "," + aantal_slaapkamers + "\n"
#
#                 with open('somefile.txt', 'a') as the_file:
#                     the_file.write(line)
#         except ConnectionRefusedError:
#             requests.send_header('Content-Type', 'blabla')
#             requests.end_headers()
#             time.sleep(5)
#             print("Was a nice sleep, now let me continue...")
#             continue
#         except ConnectionAbortedError:
#             requests.send_header('Content-Type', 'blabla')
#             requests.end_headers()
#             time.sleep(5)
#             print("Was a nice sleep, now let me continue...")
#             continue
#         except ConnectionError:
#             requests.send_header('Content-Type', 'blabla')
#             requests.end_headers()
#             time.sleep(5)
#             print("Was a nice sleep, now let me continue...")
#             continue
#         except ConnectionResetError:
#             requests.send_header('Content-Type', 'blabla')
#             requests.end_headers()
#             time.sleep(5)
#             print("Was a nice sleep, now let me continue...")
#             continue
#         except requests.exceptions.Timeout:
#             print(" ")
#             requests.send_header('Content-Type', 'blabla')
#             requests.end_headers()
#         except requests.exceptions.TooManyRedirects:
#             print(" ")
#         except requests.exceptions.RequestException as e:
#             print(" ")
#             raise SystemExit(e)
#
#
#     if re.search('remax.sr', web_url):
#
#         try:
#             print(web_url)
#             # if resp.status_code == 200:
#             # ################
#             # #
#             # #
#             # ################
#             URL = web_url
#             resp = requests.get(URL)
#             soup = BeautifulSoup(resp.text, "lxml")
#
#             # ################
#             # #
#             # #
#             # ################
#             # Using straatnaam
#             soup = BeautifulSoup(resp.text, "lxml")
#             straatnaam = soup.select('#top_section > h2.title')
#
#             try:
#                 print(straatnaam[0].string)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#
#             # Using prijs
#             Vraagprijs = soup.select('#top_section > h2.prijs')
#
#             try:
#                 print(Vraagprijs[0].text)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#
#             Omgeving = soup.select('#top_section > h2.prijs')
#
#             try:
#                 print(Omgeving[0].text)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             Badkamers = soup.select('#top_section > h2.prijs')
#
#             try:
#                 print(Badkamers[0].text)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             Perceelgrootte = soup.select('#top_section > h2.prijs')
#
#             try:
#                 print(Perceelgrootte[0].text)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             Titel = soup.select('#top_section > h2.prijs')
#
#             try:
#                 print(Titel[0].text)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             District = soup.select('#top_section > h2.prijs')
#
#             try:
#                 print(District[0].text)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             Slaapkamers = soup.select('#top_section > h2.prijs')
#
#             try:
#                 print(Slaapkamers[0].text)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             Beschikbaarheid = soup.select('#top_section > h2.prijs')
#
#             try:
#                 print(Beschikbaarheid[0].text)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             Woonoppervlakte = soup.select('#top_section > h2.prijs')
#
#             try:
#                 print(Woonoppervlakte[0].text)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             # ################
#             # #
#             # #
#             # ################
#
#             r = requests.get(web_url, allow_redirects=True)
#
#             try:
#                 image_name = straatnaam[0].string + ".jpg"
#                 open(image_name, 'wb').write(r.content)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             # ################
#             # #
#             # #
#             # ################
#
#             try:
#                 print(straatnaam[0].string, type, Titel, Perceelgrootte, Woonoppervlakte, aantal_kamers,
#                       aantal_slaapkamers)
#                 line = straatnaam[
#                            0].string + "," + type + "," + Titel + "," + Perceelgrootte + "," + Woonoppervlakte + "," + aantal_kamers + "," + aantal_slaapkamers + "\n"
#                 with open('somefile.txt', 'a') as the_file:
#                     the_file.write(line)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#         except requests.exceptions.Timeout:
#             print(" ")
#         except requests.exceptions.TooManyRedirects:
#             print(" ")
#         except requests.exceptions.RequestException as e:
#             print(" ")
#             raise SystemExit(e)
#
#
#     if re.search('affidata.com', web_url):
#         try:
#             print(web_url)
#             # if resp.status_code == 200:
#             # ################
#             # #
#             # #
#             # ################
#             URL = web_url
#             resp = requests.get(URL)
#             soup = BeautifulSoup(resp.text, "lxml")
#
#             divs = soup.findAll("table", {"class": "kenmerken"})
#
#             # ################
#             # #
#             # #
#             # ################
#             # Using straatnaam
#             soup = BeautifulSoup(resp.text, "lxml")
#
#             titel = soup.select('body > div.container-fluid > div.aff-header > div > div.col-xs-12.col-sm-10 > h4')
#             print(titel)
#
#             omschrijving = soup.select(
#                 'body > div.container-fluid > div.aff-header > div > div.col-xs-12.col-sm-10 > h4')
#             print(omschrijving)
#
#             # straatnaam = soup.select('#top_section > h2.title')
#             # print(straatnaam)
#             #
#             #
#             #
#             straatnaam = soup.select('body > div.container-fluid > div.aff-header > div > div.col-xs-12.col-sm-10 > h4')
#             print(straatnaam)
#
#             # Using prijs
#             prijs = soup.select(
#                 'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(4) > div.col-xs-12.col-sm-8.nopadding')
#             print(prijs)
#
#             plaats = soup.select(
#                 'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(5) > div.col-xs-12.col-sm-8.nopadding')
#             print(plaats)
#
#             referentienummer = soup.select(
#                 'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(6) > div.col-xs-12.col-sm-8.nopadding')
#             print(referentienummer)
#
#             views = soup.select(
#                 'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(7) > div.col-xs-12.col-sm-8.nopadding')
#             print(views)
#
#             woonoppervlak = soup.select(
#                 'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(9) > div.col-xs-12.col-sm-8.nopadding')
#             print(woonoppervlak)
#
#             verdiepingen = soup.select(
#                 'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(10) > div.col-xs-12.col-sm-8.nopadding')
#             print(verdiepingen)
#
#             kamers = soup.select(
#                 'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(11) > div.col-xs-12.col-sm-8.nopadding')
#             print(kamers)
#
#             slaapkamers = soup.select(
#                 'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(12) > div.col-xs-12.col-sm-8.nopadding')
#             print(slaapkamers)
#
#             badkamers = soup.select(
#                 'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(13) > div.col-xs-12.col-sm-8.nopadding')
#             print(badkamers)
#
#             toiletten = soup.select(
#                 'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(14) > div.col-xs-12.col-sm-8.nopadding')
#             print(toiletten)
#
#             nutsvoorzieningen = soup.select(
#                 'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(16) > div.col-xs-12.col-sm-8.nopadding')
#             print(nutsvoorzieningen)
#
#             tuin = soup.select(
#                 'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(18) > div.col-xs-12.col-sm-8.nopadding')
#             print(tuin)
#
#             voorzieningen_buiten = soup.select(
#                 'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(19) > div.col-xs-12.col-sm-8.nopadding')
#             print(voorzieningen_buiten)
#
#             ligging = soup.select(
#                 'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(21) > div.col-xs-12.col-sm-8.nopadding')
#             print(ligging)
#
#             landschap = soup.select(
#                 'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(22) > div.col-xs-12.col-sm-8.nopadding')
#             print(landschap)
#
#             vervoer = soup.select(
#                 '#top_section > h2.prijsbody > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(23) > div.col-xs-12.col-sm-8.nopadding')
#             print(vervoer)
#
#             type_woning = soup.select(
#                 'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(3) > div.col-xs-12.col-sm-8.nopadding')
#             print(type_woning)
#
#             bouwperiode = soup.select(
#                 'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(26) > div.col-xs-12.col-sm-8.nopadding')
#             print(bouwperiode)
#
#             staat_van_onderhoud = soup.select(
#                 'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(27) > div.col-xs-12.col-sm-8.nopadding')
#             print(staat_van_onderhoud)
#
#             prijsklasse = soup.select(
#                 'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(29) > div.col-xs-12.col-sm-8.nopadding')
#             print(prijsklasse)
#
#             bijkomende_kosten = soup.select(
#                 'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(30) > div.col-xs-12.col-sm-4.nopadding.text-muted')
#             print(bijkomende_kosten)
#
#             perceel = soup.select(
#                 'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(31) > div.col-xs-12.col-sm-8.nopadding')
#             print(perceel)
#
#             divs = soup.findAll("#banner > div.ns-r4mg9-e-1.row-container > a > canvas")
#
#             # ################
#             # #
#             # #
#             # ################
#             soup = BeautifulSoup(resp.text, "lxml")
#             elements = soup.select('#bottom_section > div > div.kenmerken')
#             # try:
#             #     type = (soup.find("td", text="Type").find_next_sibling("td").string)
#             #     print(type)
#             # except IndexError:
#             #     print("list index out of range")
#             # except:
#             #     print("Something else went wrong")
#             #
#             #
#             # try:
#             #     title = (soup.find("td", text="Titel").find_next_sibling("td").string)
#             #     print(title)
#             # except IndexError:
#             #     print("list index out of range")
#             # except:
#             #     print("Something else went wrong")
#             #
#             # try:
#             #     Perceeloppervlakte = (soup.find("td", text="Perceeloppervlakte").find_next_sibling("td").string)
#             #     print(Perceeloppervlakte)
#             # except IndexError:
#             #     print("list index out of range")
#             # except:
#             #     print("Something else went wrong")
#             #
#             # try:
#             #     Bouwoppervlakte = (soup.find("td", text="Bouwoppervlakte").find_next_sibling("td").string)
#             #     print(Bouwoppervlakte)
#             # except IndexError:
#             #     print("list index out of range")
#             # except:
#             #     print("Something else went wrong")
#             #
#             # try:
#             #     aantal_kamers = (soup.find("td", text="Aantal kamers").find_next_sibling("td").string)
#             #     print(aantal_kamers)
#             # except IndexError:
#             #     print("list index out of range")
#             # except:
#             #     print("Something else went wrong")
#             #
#             # try:
#             #     aantal_slaapkamers = (soup.find("td", text="Aantal slaapkamers").find_next_sibling("td").string)
#             # except IndexError:
#             #     print("list index out of range")
#             # except:
#             #     print("Something else went wrong")
#
#             divs = soup.findAll("galleria-image")
#             print(divs)
#             divs = soup.findAll("galleria-images")
#             print(divs)
#             divs = soup.findAll("table", {"class": "kenmerken"})
#             print(divs)
#             images = soup.find_all('img')
#             print(images)
#             images_url = images[0]['src']
#             images = soup.findAll('img')
#             for image in images:
#                 print(image['src'])
#
#             images_url
#             print(images_url)
#             # data = requests.get("www.remyvastgoed.com/wp-content/uploads/2023/03/1-16.jpg").content
#             from PIL import Image  # pillow library
#             import requests
#             import urllib.request
#
#             try:
#                 im = Image.open(
#                     requests.get("www.remyvastgoed.com/wp-content/uploads/2023/03/1-16.jpg", stream=True).raw)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#
#             # Opening a new file named img with extension .jpg
#             # This file would store the data of the image file
#             # f = open('img.jpg', 'wb')
#             # # Storing the image data inside the data variable to the file
#             # f.write(im)
#             # f.close()
#             try:
#                 img_data = requests.get("www.remyvastgoed.com/wp-content/uploads/2023/03/1-16.jpg").content
#                 with open('netflix.jpg', 'wb') as handler:
#                     handler.write(img_data)
#                 with open('pic1.jpg', 'wb') as handle:
#                     response = requests.get('www.remyvastgoed.com/wp-content/uploads/2023/03/1-16.jpg', stream=True)
#
#                     if not response.ok:
#                         print(response)
#
#                     for block in response.iter_content(1024):
#                         if not block:
#                             break
#                         #
#                         handle.write(block)
#                 urllib.request.urlretrieve(
#                     'remyvastgoed.com/wp-content/uploads/2023/03/1-16.jpg',
#                     "gfg.png")
#
#                 img = Image.open("gfg.png")
#                 img.show()
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#
#             # find image with '1-' and  followed up with any number that ends with .jpg
#             r = requests.get(web_url, allow_redirects=True)
#             # image_name = straatnaam[0].string + ".jpg"
#             # open(image_name, 'wb').write(r.content)
#             # print(straatnaam[0].string, type, title, Perceeloppervlakte, Bouwoppervlakte, aantal_kamers,
#             #       aantal_slaapkamers)
#             # line = straatnaam[
#             #            0].string + "," + type + "," + title + "," + Perceeloppervlakte + "," + Bouwoppervlakte + "," + aantal_kamers + "," + aantal_slaapkamers + "\n"
#             # with open('somefile.txt', 'a') as the_file:
#             #     the_file.write(line)
#             #
#             # divs = soup.findAll("table", {"class": "kenmerken"})
#             # for div in divs:
#             #     row = ''
#             #     rows = div.findAll('tr')
#             #     for row in rows:
#             #         print(row)
#             #         # if (row.text.find("PHONE") > -1):
#             #         #     print(row.text)
#         except requests.exceptions.Timeout:
#             print(" ")
#             requests.send_header('Content-Type', 'blabla')
#             requests.end_headers()
#         except requests.exceptions.TooManyRedirects:
#             print(" ")
#         except requests.exceptions.RequestException as e:
#             print(" ")
#             raise SystemExit(e)
#
#
#     else:
#         if re.search('hello.sr|worldeconomics.com|waterkant.com', web_url):
#             print(" ")
#             # domain = urlparse(web_url).netloc
#         else:
#             print('Neither url is needed')
#
# print(web_url)



# for web_url in site_links:
#
#     if re.search('osonangadjari.com', web_url):
#         print(web_url)
#         try:
#             if resp.status_code == 200:
#                 # ################
#                 # #
#                 # #
#                 # ################
#                 URL = web_url
#                 resp = requests.get(URL)
#                 soup = BeautifulSoup(resp.text, "lxml")
#
#                 divs = soup.findAll("table", {"class": "kenmerken"})
#
#                 soup = BeautifulSoup(resp.text, "lxml")
#
#                 # body > div.page-wrapper > div.main > div > div > div.social-cons > span > a
#                 postid = soup.select('body > div.page-wrapper > div.main > div > div > div.social-cons > span > a')
#                 print(postid[0].string)
#
#                 straatnaam = soup.select('#post-13962 > h3')
#                 print(straatnaam[0].string)
#
#                 plaats = soup.select('#post-13962 > span')
#                 print(straatnaam[0].string)
#
#                 # Using prijs
#                 prijs = soup.select(
#                     '#post-9925 > div > div.row > div.col-sm-4 > div.table-group.overview.property-overview > table > tbody > tr:nth-child(1) > td:nth-child(2)')
#                 print(prijs[0].text)
#
#                 Type = soup.select(
#                     '#post-9925 > div > div.row > div.col-sm-4 > div.table-group.overview.property-overview > table > tbody > tr:nth-child(2) > td:nth-child(2)')
#                 print(Type[0].text)
#
#                 verkocht = soup.select(
#                     '#post-9925 > div > div.row > div.col-sm-4 > div.table-group.overview.property-overview > table > tbody > tr:nth-child(3) > td:nth-child(2)')
#                 print(verkocht[0].text)
#
#                 Overeenkomst = soup.select(
#                     '#post-9925 > div > div.row > div.col-sm-4 > div.table-group.overview.property-overview > table > tbody > tr:nth-child(4) > td:nth-child(2)')
#                 print(Overeenkomst[0].text)
#
#                 Status = soup.select(
#                     '#post-9925 > div > div.row > div.col-sm-4 > div.table-group.overview.property-overview > table > tbody > tr:nth-child(5) > td:nth-child(2)')
#                 print(Status[0].text)
#
#                 woonoppervlakte = soup.select(
#                     '#post-9925 > div > div.row > div.col-sm-4 > div.table-group.overview.property-overview > table > tbody > tr:nth-child(6) > td:nth-child(2)')
#                 print(woonoppervlakte[0].text)
#
#                 Perceel_Oppervlakte = soup.select(
#                     '#post-9925 > div > div.row > div.col-sm-4 > div.table-group.overview.property-overview > table > tbody > tr:nth-child(7) > td:nth-child(2)')
#                 print(Perceel_Oppervlakte[0].text)
#
#                 Materiaal = soup.select(
#                     '#post-9925 > div > div.row > div.col-sm-4 > div.table-group.overview.property-overview > table > tbody > tr:nth-child(8) > td:nth-child(2)')
#                 print(Materiaal[0].text)
#
#                 Aantal_kamers = soup.select(
#                     '#post-9925 > div > div.row > div.col-sm-4 > div.table-group.overview.property-overview > table > tbody > tr:nth-child(9) > td:nth-child(2)')
#                 print(Aantal_kamers[0].text)
#
#                 Slaapkamers = soup.select(
#                     '#post-9925 > div > div.row > div.col-sm-4 > div.table-group.overview.property-overview > table > tbody > tr:nth-child(10) > td:nth-child(2)')
#                 print(Slaapkamers[0].text)
#
#                 Badkamers = soup.select(
#                     '#post-9925 > div > div.row > div.col-sm-4 > div.table-group.overview.property-overview > table > tbody > tr:nth-child(11) > td:nth-child(2)')
#                 print(Badkamers[0].text)
#
#                 # ################
#                 # #
#                 # #
#                 # ################
#
#                 # property-detail-section-gallery > div > div.property-detail-gallery.owl-carousel.owl-theme.owl-loaded > div.owl-stage-outer.owl-height > div > div.owl-item.active > a > span
#                 image = soup.select(
#                     '#property-detail-section-gallery > div > div.property-detail-gallery.owl-carousel.owl-theme.owl-loaded > div.owl-stage-outer.owl-height > div > div.owl-item.active > a > span')
#
#                 r = requests.get(image, allow_redirects=True)
#                 image_name = straatnaam[0].string + ".jpg"
#                 open(image_name, 'wb').write(r.content)
#
#                 # ################
#                 # #
#                 # #
#                 # ################
#
#                 print(straatnaam[0].string, type, postid, straatnaam, plaats, prijs, Type, verkocht, Overeenkomst,
#                       Status, woonoppervlakte, Perceel_Oppervlakte, Materiaal, Aantal_kamers, Slaapkamers, Badkamers,
#                       aantal_kamers, aantal_slaapkamers)
#                 line = straatnaam[
#                            0].string + "," + type + "," + postid + "," + straatnaam + "," + plaats + "," + prijs + "," + Type + "," + verkocht + "," + Overeenkomst + "," + Status + "," + woonoppervlakte + "," + Perceel_Oppervlakte + "," + Materiaal + "," + Aantal_kamers + "," + Badkamers + "," + aantal_kamers + "," + aantal_slaapkamers + "\n"
#
#                 with open('somefile.txt', 'a') as the_file:
#                     the_file.write(line)
#         except ConnectionRefusedError:
#             requests.send_header('Content-Type', 'blabla')
#             requests.end_headers()
#             time.sleep(5)
#             print("Was a nice sleep, now let me continue...")
#             continue
#         except ConnectionAbortedError:
#             requests.send_header('Content-Type', 'blabla')
#             requests.end_headers()
#             time.sleep(5)
#             print("Was a nice sleep, now let me continue...")
#             continue
#         except ConnectionError:
#             requests.send_header('Content-Type', 'blabla')
#             requests.end_headers()
#             time.sleep(5)
#             print("Was a nice sleep, now let me continue...")
#             continue
#         except ConnectionResetError:
#             requests.send_header('Content-Type', 'blabla')
#             requests.end_headers()
#             time.sleep(5)
#             print("Was a nice sleep, now let me continue...")
#             continue
#         except requests.exceptions.Timeout:
#             print(" ")
#             requests.send_header('Content-Type', 'blabla')
#             requests.end_headers()
#         except requests.exceptions.TooManyRedirects:
#             print(" ")
#         except requests.exceptions.RequestException as e:
#             print(" ")
#             raise SystemExit(e)
#
#
#
#
#
#     else:
#         if re.search('hello.sr|worldeconomics.com|waterkant.com', web_url):
#             print(" ")
#             # domain = urlparse(web_url).netloc
#         else:
#             print('Neither url is needed')
#
# print(web_url)
#
# for web_url in site_links:
#     if re.search('remax.sr', web_url):
#         try:
#             print(web_url)
#             # if resp.status_code == 200:
#             # ################
#             # #
#             # #
#             # ################
#             URL = web_url
#             resp = requests.get(URL)
#             soup = BeautifulSoup(resp.text, "lxml")
#
#             # ################
#             # #
#             # #
#             # ################
#             # Using straatnaam
#             soup = BeautifulSoup(resp.text, "lxml")
#             straatnaam = soup.select('#top_section > h2.title')
#
#             try:
#                 straatnaam = soup.select('//*[@id="wrap"]/div[3]/div[1]/ul/li[3]')
#                 print(straatnaam)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#
#             # Using prijs
#             Vraagprijs = soup.select('#top_section > h2.prijs')
#             #  <td> € 310.000</td>
#             #
#             #
#             #
#             #
#
#             try:
#                 Vraagprijs = soup.select('#top_section > h2.prijs')
#                 print(soup.select('document.querySelector("#propertytable > table > tbody > tr:nth-child(1) > td:nth-child(2)")'))
#                 Vraagprijs = soup.select('//*[@id="propertytable"]/table/tbody/tr[1]/td[2]')
#                 print(Vraagprijs[0].text)
#                 print(Vraagprijs.text)
#                 # Vraagprijs = soup.select('/html/body/div[1]/div[3]/div[1]/div[2]/div/div[2]/table/tbody/tr[1]/td[2]')
#                 # print(Vraagprijs)
#                 # Vraagprijs = soup.select('#propertytable > table')
#                 # print(Vraagprijs)
#                 # Vraagprijs = soup.select('document.querySelector("#propertytable > table")')
#                 # print(Vraagprijs)
#                 # Vraagprijs = soup.select('//*[@id="propertytable"]/table')
#                 # print(Vraagprijs)
#                 # Vraagprijs = soup.select('/html/body/div[1]/div[3]/div[1]/div[2]/div/div[2]/table')
#                 # print(Vraagprijs)
#                 # print(soup.select(''))
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#
#             Omgeving = soup.select('#top_section > h2.prijs')
#
#             # #propertytable > table > tbody > tr:nth-child(2) > td:nth-child(2)
#             # //*[@id="propertytable"]/table/tbody/tr[2]/td[2]
#             # /html/body/div[1]/div[3]/div[1]/div[2]/div/div[2]/table/tbody/tr[2]/td[2]
#             #
#             try:
#                 Vraagprijs = soup.select('')
#                 print(Vraagprijs)
#                 print(Omgeving[0].text)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             Badkamers = soup.select('#top_section > h2.prijs')
#
#             # #propertytable > table > tbody > tr:nth-child(3) > td:nth-child(2)
#             # //*[@id="propertytable"]/table/tbody/tr[3]/td[2]
#             # /html/body/div[1]/div[3]/div[1]/div[2]/div/div[2]/table/tbody/tr[3]/td[2]
#             #
#             try:
#                 Vraagprijs = soup.select('')
#                 print(soup.select('#propertytable > table > tbody > tr:nth-child(3) > td:nth-child(2)'))
#                 print(soup.select('//*[@id="propertytable"]/table/tbody/tr[3]/td[2]'))
#                 print(soup.select('/html/body/div[1]/div[3]/div[1]/div[2]/div/div[2]/table/tbody/tr[3]/td[2]'))
#                 print(Badkamers[0].text)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             Perceelgrootte = soup.select('#top_section > h2.prijs')
#
#             # #propertytable > table > tbody > tr:nth-child(4) > td:nth-child(4)
#             # //*[@id="propertytable"]/table/tbody/tr[4]/td[4]
#             # /html/body/div[1]/div[3]/div[1]/div[2]/div/div[2]/table/tbody/tr[4]/td[4]
#             #
#             try:
#                 Vraagprijs = soup.select('#propertytable > table > tbody > tr:nth-child(4) > td:nth-child(4)')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('//*[@id="propertytable"]/table/tbody/tr[4]/td[4]')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[1]/div[3]/div[1]/div[2]/div/div[2]/table/tbody/tr[4]/td[4]')
#                 print(Vraagprijs)
#                 print(Perceelgrootte[0].text)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             Titel = soup.select('#top_section > h2.prijs')
#
#             #
#             #
#             #
#             #
#             try:
#                 Vraagprijs = soup.select('')
#                 print(Vraagprijs)
#                 print(Titel[0].text)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             District = soup.select('#top_section > h2.prijs')
#
#             # #propertytable > table > tbody > tr:nth-child(1) > td:nth-child(4)
#             # //*[@id="propertytable"]/table/tbody/tr[1]/td[4]
#             # /html/body/div[1]/div[3]/div[1]/div[2]/div/div[2]/table/tbody/tr[1]/td[4]
#             #
#             try:
#                 Vraagprijs = soup.select('#propertytable > table > tbody > tr:nth-child(1) > td:nth-child(4)')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('//*[@id="propertytable"]/table/tbody/tr[1]/td[4]')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[1]/div[3]/div[1]/div[2]/div/div[2]/table/tbody/tr[1]/td[4]')
#                 print(Vraagprijs)
#                 print(District[0].text)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             Slaapkamers = soup.select('#top_section > h2.prijs')
#
#             # #propertytable > table > tbody > tr:nth-child(2) > td:nth-child(4)
#             # //*[@id="propertytable"]/table/tbody/tr[2]/td[4]
#             # /html/body/div[1]/div[3]/div[1]/div[2]/div/div[2]/table/tbody/tr[2]/td[4]
#             #
#             try:
#                 Vraagprijs = soup.select('#propertytable > table > tbody > tr:nth-child(2) > td:nth-child(4)')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('//*[@id="propertytable"]/table/tbody/tr[2]/td[4]')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[1]/div[3]/div[1]/div[2]/div/div[2]/table/tbody/tr[2]/td[4]')
#                 print(Vraagprijs)
#                 print(Slaapkamers[0].text)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             Beschikbaarheid = soup.select('#top_section > h2.prijs')
#
#             # #propertytable > table > tbody > tr:nth-child(4) > td:nth-child(2)
#             # //*[@id="propertytable"]/table/tbody/tr[4]/td[2]
#             # /html/body/div[1]/div[3]/div[1]/div[2]/div/div[2]/table/tbody/tr[4]/td[2]
#             #
#             try:
#                 Vraagprijs = soup.select('#propertytable > table > tbody > tr:nth-child(4) > td:nth-child(2)')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('//*[@id="propertytable"]/table/tbody/tr[4]/td[2]')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[1]/div[3]/div[1]/div[2]/div/div[2]/table/tbody/tr[4]/td[2]')
#                 print(Vraagprijs)
#                 print(Beschikbaarheid[0].text)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             Woonoppervlakte = soup.select('#top_section > h2.prijs')
#
#             # #propertytable > table > tbody > tr:nth-child(5) > td:nth-child(2)
#             # //*[@id="propertytable"]/table/tbody/tr[5]/td[2]
#             # /html/body/div[1]/div[3]/div[1]/div[2]/div/div[2]/table/tbody/tr[5]/td[2]
#             #
#             try:
#                 Vraagprijs = soup.select('#propertytable > table > tbody > tr:nth-child(5) > td:nth-child(2)')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('//*[@id="propertytable"]/table/tbody/tr[5]/td[2]')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[1]/div[3]/div[1]/div[2]/div/div[2]/table/tbody/tr[5]/td[2]')
#                 print(Vraagprijs)
#                 print(Woonoppervlakte[0].text)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             # ################
#             # #
#             # #
#             # ################
#
#             r = requests.get(web_url, allow_redirects=True)
#             #
#             #
#             #
#             #
#             try:
#                 Vraagprijs = soup.select('')
#                 print(Vraagprijs)
#                 image_name = straatnaam[0].string + ".jpg"
#                 open(image_name, 'wb').write(r.content)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             # ################
#             # #
#             # #
#             # ################
#
#             try:
#                 # print(straatnaam[0].string, type, Titel, Perceelgrootte, Woonoppervlakte, aantal_kamers,
#                 #       aantal_slaapkamers)
#                 # line = straatnaam[
#                 #            0].string + "," + type + "," + Titel + "," + Perceelgrootte + "," + Woonoppervlakte + "," + aantal_kamers + "," + aantal_slaapkamers + "\n"
#                 line=" "
#                 with open('somefile.txt', 'a') as the_file:
#                     the_file.write(line)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#         except requests.exceptions.Timeout:
#             print(" ")
#         except requests.exceptions.TooManyRedirects:
#             print(" ")
#         except requests.exceptions.RequestException as e:
#             print(" ")
#             raise SystemExit(e)
#
#
#     else:
#         if re.search('hello.sr|worldeconomics.com|waterkant.com', web_url):
#             print(" ")
#             # domain = urlparse(web_url).netloc
#         else:
#             print('Neither url is needed')
#
# print(web_url)

# for web_url in site_links:
#
#     if re.search('affidata.com', web_url):
#         try:
#             print(web_url)
#             # if resp.status_code == 200:
#             # ################
#             # #
#             # #
#             # ################
#             URL = web_url
#             resp = requests.get(URL)
#             soup = BeautifulSoup(resp.text, "lxml")
#
#             divs = soup.findAll("table", {"class": "kenmerken"})
#
#             # ################
#             # #
#             # #
#             # ################
#             # Using straatnaam
#             soup = BeautifulSoup(resp.text, "lxml")
#
#             titel = soup.select('body > div.container-fluid > div.aff-header > div > div.col-xs-12.col-sm-10 > h4')
#             print(titel)
#
#             omschrijving = soup.select(
#                 'body > div.container-fluid > div.aff-header > div > div.col-xs-12.col-sm-10 > h4')
#             print(omschrijving)
#
#             # straatnaam = soup.select('#top_section > h2.title')
#             # print(straatnaam)
#             #
#             #
#             #
#             # straatnaam = soup.select('body > div.container-fluid > div.aff-header > div > div.col-xs-12.col-sm-10 > h4')
#             # print(straatnaam)
#             #
#             # # Using prijs
#             # prijs = soup.select(
#             #     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(4) > div.col-xs-12.col-sm-8.nopadding')
#             # print(prijs)
#             #
#             # plaats = soup.select(
#             #     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(5) > div.col-xs-12.col-sm-8.nopadding')
#             # print(plaats)
#             #
#             # referentienummer = soup.select(
#             #     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(6) > div.col-xs-12.col-sm-8.nopadding')
#             # print(referentienummer)
#             #
#             # views = soup.select(
#             #     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(7) > div.col-xs-12.col-sm-8.nopadding')
#             # print(views)
#             #
#             # woonoppervlak = soup.select(
#             #     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(9) > div.col-xs-12.col-sm-8.nopadding')
#             # print(woonoppervlak)
#             #
#             # verdiepingen = soup.select(
#             #     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(10) > div.col-xs-12.col-sm-8.nopadding')
#             # print(verdiepingen)
#             #
#             # kamers = soup.select(
#             #     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(11) > div.col-xs-12.col-sm-8.nopadding')
#             # print(kamers)
#             #
#             # slaapkamers = soup.select(
#             #     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(12) > div.col-xs-12.col-sm-8.nopadding')
#             # print(slaapkamers)
#             #
#             # badkamers = soup.select(
#             #     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(13) > div.col-xs-12.col-sm-8.nopadding')
#             # print(badkamers)
#             #
#             # toiletten = soup.select(
#             #     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(14) > div.col-xs-12.col-sm-8.nopadding')
#             # print(toiletten)
#             #
#             # nutsvoorzieningen = soup.select(
#             #     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(16) > div.col-xs-12.col-sm-8.nopadding')
#             # print(nutsvoorzieningen)
#             #
#             # tuin = soup.select(
#             #     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(18) > div.col-xs-12.col-sm-8.nopadding')
#             # print(tuin)
#             #
#             # voorzieningen_buiten = soup.select(
#             #     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(19) > div.col-xs-12.col-sm-8.nopadding')
#             # print(voorzieningen_buiten)
#             #
#             # ligging = soup.select(
#             #     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(21) > div.col-xs-12.col-sm-8.nopadding')
#             # print(ligging)
#             #
#             # landschap = soup.select(
#             #     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(22) > div.col-xs-12.col-sm-8.nopadding')
#             # print(landschap)
#             #
#             # vervoer = soup.select(
#             #     '#top_section > h2.prijsbody > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(23) > div.col-xs-12.col-sm-8.nopadding')
#             # print(vervoer)
#             #
#             # type_woning = soup.select(
#             #     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(3) > div.col-xs-12.col-sm-8.nopadding')
#             # print(type_woning)
#             #
#             # bouwperiode = soup.select(
#             #     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(26) > div.col-xs-12.col-sm-8.nopadding')
#             # print(bouwperiode)
#             #
#             # staat_van_onderhoud = soup.select(
#             #     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(27) > div.col-xs-12.col-sm-8.nopadding')
#             # print(staat_van_onderhoud)
#             #
#             # prijsklasse = soup.select(
#             #     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(29) > div.col-xs-12.col-sm-8.nopadding')
#             # print(prijsklasse)
#             #
#             # bijkomende_kosten = soup.select(
#             #     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(30) > div.col-xs-12.col-sm-4.nopadding.text-muted')
#             # print(bijkomende_kosten)
#             #
#             # perceel = soup.select(
#             #     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(31) > div.col-xs-12.col-sm-8.nopadding')
#             # print(perceel)
#             #
#             # divs = soup.findAll("#banner > div.ns-r4mg9-e-1.row-container > a > canvas")
#
#             # Type             woning
#
#
#             try:
#                 Vraagprijs = soup.select(
#                     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(3) > div.col-xs-12.col-sm-8.nopadding')
#                 print(Vraagprijs)
#                 # Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[3]/div[2]')
#                 # print(Vraagprijs)
#                 # Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[2]/div[2]')
#                 # print(Vraagprijs)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             #Prijs
#
#             try:
#                 Vraagprijs = soup.select(
#                     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(4) > div.col-xs-12.col-sm-8.nopadding')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[3]/div[2]')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[3]/div[2]')
#                 print(Vraagprijs)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             #Plaats
#
#             try:
#                 Vraagprijs = soup.select(
#                     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(5) > div.col-xs-12.col-sm-8.nopadding')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[4]/div[2]')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[4]/div[2]')
#                 print(Vraagprijs)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             # Referentienummer
#
#             try:
#                 Vraagprijs = soup.select(
#                     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(6) > div.col-xs-12.col-sm-8.nopadding')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[5]/div[2]')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[5]/div[2]')
#                 print(Vraagprijs)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             #Views
#
#             try:
#                 Vraagprijs = soup.select(
#                     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(7) > div.col-xs-12.col-sm-8.nopadding')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[6]/div[2]')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[6]/div[2]')
#                 print(Vraagprijs)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             #Interieur
#             #Woonoppervlak
#
#             try:
#                 Vraagprijs = soup.select(
#                     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(9) > div.col-xs-12.col-sm-8.nopadding')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[8]/div[2]')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[8]/div[2]')
#                 print(Vraagprijs)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             #Verdiepingen
#
#             try:
#                 Vraagprijs = soup.select(
#                     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(10) > div.col-xs-12.col-sm-8.nopadding')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[9]/div[2]')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[9]/div[2]')
#                 print(Vraagprijs)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             #
#
#             try:
#                 Vraagprijs = soup.select(
#                     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(11) > div.col-xs-12.col-sm-8.nopadding')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[10]/div[2]')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[10]/div[2]')
#                 print(Vraagprijs)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             #Slaapkamers
#
#             try:
#                 Vraagprijs = soup.select(
#                     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(12) > div.col-xs-12.col-sm-8.nopadding')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[11]/div[2]')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[11]/div[2]')
#                 print(Vraagprijs)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             # Badkamer(s)
#
#             try:
#                 Vraagprijs = soup.select(
#                     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(13) > div.col-xs-12.col-sm-8.nopadding')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[12]/div[2]')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[12]/div[2]')
#                 print(Vraagprijs)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             # Toilet(ten)
#
#             try:
#                 Vraagprijs = soup.select(
#                     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(14) > div.col-xs-12.col-sm-8.nopadding')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[13]/div[2]')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[13]/div[2]')
#                 print(Vraagprijs)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#
#             # Keukenapparatuurgasfornuis - oven - koelkast - wasmachine
#
#             try:
#                 Vraagprijs = soup.select(
#                     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(16) > div.col-xs-12.col-sm-8.nopadding')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[15]/div[2]')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[15]/div[2]')
#                 print(Vraagprijs)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             #Airconditioning
#
#             try:
#                 Vraagprijs = soup.select(
#                     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(17) > div.col-xs-12.col-sm-8.nopadding')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[16]/div[2]')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[16]/div[2]')
#                 print(Vraagprijs)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             # Nutsvoorzieningen
#
#             try:
#                 Vraagprijs = soup.select(
#                     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(18) > div.col-xs-12.col-sm-8.nopadding')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[17]/div[2]')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[17]/div[2]')
#                 print(Vraagprijs)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             # Exterieur
#             # Tuintuin
#             #rondom - bijgebouw(en) - schuur
#
#             try:
#                 Vraagprijs = soup.select(
#                     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(20) > div.col-xs-12.col-sm-8.nopadding')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[19]/div[2]')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[19]/div[2]')
#                 print(Vraagprijs)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             # Balkon / dakterrasbalkon(s)
#
#             try:
#                 Vraagprijs = soup.select(
#                     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(21) > div.col-xs-12.col-sm-8.nopadding')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[20]/div[2]')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[20]/div[2]')
#                 print(Vraagprijs)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             # Voorzieningen
#             # buitenberging - parkeerplaats
#
#             try:
#                 Vraagprijs = soup.select(
#                     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(22) > div.col-xs-12.col-sm-8.nopadding')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[21]/div[2]')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[21]/div[2]')
#                 print(Vraagprijs)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             # Omgeving
#             # Ligging
#
#             try:
#                 Vraagprijs = soup.select(
#                     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(24) > div.col-xs-12.col-sm-8.nopadding')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[23]/div[2]')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[23]/div[2]')
#                 print(Vraagprijs)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             # Omgeving
#
#             try:
#                 Vraagprijs = soup.select(
#                     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(25) > div.col-xs-12.col-sm-8.nopadding')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[24]/div[2]')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[24]/div[2]')
#                 print(Vraagprijs)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             # Landschap
#
#             try:
#                 Vraagprijs = soup.select(
#                     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(26) > div.col-xs-12.col-sm-8.nopadding')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[25]/div[2]')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[25]/div[2]')
#                 print(Vraagprijs)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             # Vervoersmogelijkheden
#
#             try:
#                 Vraagprijs = soup.select(
#                     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(27) > div.col-xs-12.col-sm-8.nopadding')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[26]/div[2]')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[26]/div[2]')
#                 print(Vraagprijs)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#
#             # Type             woning
#
#             try:
#                 Vraagprijs = soup.select(
#                     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(29) > div.col-xs-12.col-sm-8.nopadding')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[28]/div[2]')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[28]/div[2]')
#                 print(Vraagprijs)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#
#             try:
#                 # Bouwperiode
#                 Vraagprijs = soup.select(
#                     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(30) > div.col-xs-12.col-sm-8.nopadding')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[29]/div[2]')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[29]/div[2]')
#                 print(Vraagprijs)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             #Staat             van             onderhoud
#
#             try:
#                 Vraagprijs = soup.select(
#                     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(31) > div.col-xs-12.col-sm-8.nopadding')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[30]/div[2]')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[30]/div[2]')
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             #print(Vraagprijs)
#             #Prijsklasse
#
#             try:
#                 Vraagprijs = soup.select(
#                     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(33) > div.col-xs-12.col-sm-8.nopadding')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[32]/div[2]')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[32]/div[2]')
#                 print(Vraagprijs)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             #Bijkomende
#             #kosten
#
#             try:
#                 Vraagprijs = soup.select(
#                     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(34) > div.col-xs-12.col-sm-8.nopadding')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[33]/div[2]')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[33]/div[2]')
#                 print(Vraagprijs)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             #Perceel
#
#             try:
#                 Vraagprijs = soup.select(
#                     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(35) > div.col-xs-12.col-sm-8.nopadding')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[34]/div[2]')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[34]/div[2]')
#                 print(Vraagprijs)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#             #Beleggingspand
#
#             try:
#                 Vraagprijs = soup.select(
#                     'body > div.container-fluid > div:nth-child(4) > div.col-sm-8 > div:nth-child(5) > div:nth-child(36) > div.col-xs-12.col-sm-8.nopadding')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[35]/div[2]')
#                 print(Vraagprijs)
#                 Vraagprijs = soup.select('/html/body/div[2]/div[4]/div[2]/div[3]/div[35]/div[2]')
#                 print(Vraagprijs)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#
#             # ################
#             # #
#             # #
#             # ################
#             soup = BeautifulSoup(resp.text, "lxml")
#             elements = soup.select('#bottom_section > div > div.kenmerken')
#             # try:
#             #     type = (soup.find("td", text="Type").find_next_sibling("td").string)
#             #     print(type)
#             # except IndexError:
#             #     print("list index out of range")
#             # except:
#             #     print("Something else went wrong")
#             #
#             #
#             # try:
#             #     title = (soup.find("td", text="Titel").find_next_sibling("td").string)
#             #     print(title)
#             # except IndexError:
#             #     print("list index out of range")
#             # except:
#             #     print("Something else went wrong")
#             #
#             # try:
#             #     Perceeloppervlakte = (soup.find("td", text="Perceeloppervlakte").find_next_sibling("td").string)
#             #     print(Perceeloppervlakte)
#             # except IndexError:
#             #     print("list index out of range")
#             # except:
#             #     print("Something else went wrong")
#             #
#             # try:
#             #     Bouwoppervlakte = (soup.find("td", text="Bouwoppervlakte").find_next_sibling("td").string)
#             #     print(Bouwoppervlakte)
#             # except IndexError:
#             #     print("list index out of range")
#             # except:
#             #     print("Something else went wrong")
#             #
#             # try:
#             #     aantal_kamers = (soup.find("td", text="Aantal kamers").find_next_sibling("td").string)
#             #     print(aantal_kamers)
#             # except IndexError:
#             #     print("list index out of range")
#             # except:
#             #     print("Something else went wrong")
#             #
#             # try:
#             #     aantal_slaapkamers = (soup.find("td", text="Aantal slaapkamers").find_next_sibling("td").string)
#             # except IndexError:
#             #     print("list index out of range")
#             # except:
#             #     print("Something else went wrong")
#
#             divs = soup.findAll("galleria-image")
#             print(divs)
#             divs = soup.findAll("galleria-images")
#             print(divs)
#             divs = soup.findAll("table", {"class": "kenmerken"})
#             print(divs)
#             images = soup.find_all('img')
#             print(images)
#             images_url = images[0]['src']
#             images = soup.findAll('img')
#             for image in images:
#                 print(image['src'])
#
#             images_url
#             print(images_url)
#             # data = requests.get("www.remyvastgoed.com/wp-content/uploads/2023/03/1-16.jpg").content
#             from PIL import Image  # pillow library
#             import requests
#             import urllib.request
#
#             try:
#                 im = Image.open(
#                     requests.get("www.remyvastgoed.com/wp-content/uploads/2023/03/1-16.jpg", stream=True).raw)
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#
#             # Opening a new file named img with extension .jpg
#             # This file would store the data of the image file
#             # f = open('img.jpg', 'wb')
#             # # Storing the image data inside the data variable to the file
#             # f.write(im)
#             # f.close()
#             try:
#                 img_data = requests.get("www.remyvastgoed.com/wp-content/uploads/2023/03/1-16.jpg").content
#                 with open('netflix.jpg', 'wb') as handler:
#                     handler.write(img_data)
#                 with open('pic1.jpg', 'wb') as handle:
#                     response = requests.get('www.remyvastgoed.com/wp-content/uploads/2023/03/1-16.jpg', stream=True)
#
#                     if not response.ok:
#                         print(response)
#
#                     for block in response.iter_content(1024):
#                         if not block:
#                             break
#                         #
#                         handle.write(block)
#                 urllib.request.urlretrieve(
#                     'remyvastgoed.com/wp-content/uploads/2023/03/1-16.jpg',
#                     "gfg.png")
#
#                 img = Image.open("gfg.png")
#                 img.show()
#             except IndexError:
#                 print("list index out of range")
#             except:
#                 print("Something else went wrong")
#
#             # find image with '1-' and  followed up with any number that ends with .jpg
#             r = requests.get(web_url, allow_redirects=True)
#             # image_name = straatnaam[0].string + ".jpg"
#             # open(image_name, 'wb').write(r.content)
#             # print(straatnaam[0].string, type, title, Perceeloppervlakte, Bouwoppervlakte, aantal_kamers,
#             #       aantal_slaapkamers)
#             # line = straatnaam[
#             #            0].string + "," + type + "," + title + "," + Perceeloppervlakte + "," + Bouwoppervlakte + "," + aantal_kamers + "," + aantal_slaapkamers + "\n"
#             # with open('somefile.txt', 'a') as the_file:
#             #     the_file.write(line)
#             #
#             # divs = soup.findAll("table", {"class": "kenmerken"})
#             # for div in divs:
#             #     row = ''
#             #     rows = div.findAll('tr')
#             #     for row in rows:
#             #         print(row)
#             #         # if (row.text.find("PHONE") > -1):
#             #         #     print(row.text)
#         except requests.exceptions.Timeout:
#             print(" ")
#             requests.send_header('Content-Type', 'blabla')
#             requests.end_headers()
#         except requests.exceptions.TooManyRedirects:
#             print(" ")
#         except requests.exceptions.RequestException as e:
#             print(" ")
#             raise SystemExit(e)
#
#
#     else:
#         if re.search('hello.sr|worldeconomics.com|waterkant.com', web_url):
#             print(" ")
#             # domain = urlparse(web_url).netloc
#         else:
#             print('Neither url is needed')
#
# print(web_url)
#
#
#
#
# try:
#     start = "https://www.affidata.com/sh/nav"
#     url = "https://www.affidata.com/sh/nav"
#     #soup = BeautifulSoup(requests.get(start).content)
#     soup = BeautifulSoup(resp.text, "lxml")
#     pages = int(soup.select("select.pagination__pages__selector option")[-1].text.split(None, 1)[1])
#     print([a.text for a in soup.select("a.search__results__list__item__entity")])
#
#     for page in range(2, pages):
#         #soup = BeautifulSoup(requests.get(url.format(page)).content)
#         soup = BeautifulSoup(resp.text, "lxml")
#         print([a.text for a in soup.select("a.search__results__list__item__entity")])
# except IndexError:
#     print("list index out of range")
# except:
#     print("Something else went wrong")
#
# start_url = "https://www.affidata.com/sh/nav"
#
# def scrape_page(url):
#     #print("URL: " + url)
#     r = requests.get(url)
#     #soup = BeautifulSoup(r.content, "html.parser")
#     soup = BeautifulSoup(resp.text, "lxml")
#     get_data(soup)
#     next_page_link = soup.find("a", class_="next")
#     print(next_page_link)
#     next_page_link = soup.find('body > div.container-fluid > div:nth-child(5) > div.col-sm-8.extended-search-marge > form > div:nth-child(11) > a')
#     print(next_page_link)
#     next_page_link = soup.find('/html/body/div[2]/div[5]/div[2]/form/div[9]/a')
#     print(next_page_link)
#     next_page_link = soup.find('/html/body/div[2]/div[5]/div[2]/form/div[9]/a')
#     print(next_page_link)
#     if next_page_link is not None:
#         href = next_page_link.get("href")
#         #scrape_page(href)
#         print(href)
#     else:
#         print("Done")
#
#
# def get_data(content):
#     #we could do some scraping of web content here
#     pass
#
#
# scrape_page(start_url)
#
#
#
#
# # Get the first page.
# url = 'https://www.affidata.com/sh/nav'
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'lxml')
# page_link_el = soup.select('.pgr_nrs a')
#
# next_page_link = soup.find('body > div.container-fluid > div:nth-child(5) > div.col-sm-8.extended-search-marge > form > div:nth-child(11) > a')
# print(next_page_link)
# next_page_link = soup.find('/html/body/div[2]/div[5]/div[2]/form/div[9]/a')
# print(next_page_link)
# next_page_link = soup.find('/html/body/div[2]/div[5]/div[2]/form/div[9]/a')
# print(next_page_link)
#
#
#
#
# for a in soup.find_all('a', href=True):
#     print("Found the URL:", a['href'])
#
# for link in soup.find_all('a'):
#     print(link.get('href'))
# # Do more with the first page.
# links = soup.find_all("a") # Find all elements with the tag <a>
# for link in links:
#   print("Link:", link.get("href"), "Text:", link.string)
#
#
# # Make links for and process the following pages.
# for link_el in page_link_el:
#     link = urljoin(url, link_el.get('href'))
#     response = requests.get(link)
#     soup = BeautifulSoup(response.text, 'lxml')
#     next_page_link = soup.find(
#         'body > div.container-fluid > div:nth-child(5) > div.col-sm-8.extended-search-marge > form > div:nth-child(11) > a')
#     print(next_page_link)
#     next_page_link = soup.find('/html/body/div[2]/div[5]/div[2]/form/div[9]/a')
#     print(next_page_link)
#     next_page_link = soup.find('/html/body/div[2]/div[5]/div[2]/form/div[9]/a')
#     print(next_page_link)
#     print(response.url)
#     # Do more with each page.
#
#
#
#
#
#
# response = requests.get("https://www.affidata.com/sh/nav?cmd=browsesearchresults&range=4&refresh=false")
# soup = BeautifulSoup(response.content, 'html.parser')
# print(soup)
# next_page_link = soup.find('body > div.container-fluid > div:nth-child(5) > div.col-sm-8.extended-search-marge > form > div:nth-child(11) > a')
# print(next_page_link)
# next_page_link = soup.find('/html/body/div[2]/div[5]/div[2]/form/div[9]/a')
# print(next_page_link)
# next_page_link = soup.find('/html/body/div[2]/div[5]/div[2]/form/div[9]/a')
# print(next_page_link)
# next_page_link = soup.find('body > div.container-fluid > div:nth-child(5) > div.col-sm-8.extended-search-marge > form > div:nth-child(15) > a')
# print(next_page_link)
# response = requests.get("https://www.affidata.com/sh/nav?cmd=browsesearchresults&range=2&refresh=false")
# soup = BeautifulSoup(response.content, 'html.parser')
# next_page_link = soup.find('a')
# print(next_page_link)
# response = requests.get("https://www.affidata.com/sh/nav?cmd=browsesearchresults&range=3&refresh=false")
# soup = BeautifulSoup(response.content, 'html.parser')
# next_page_link = soup.find('a')
# print(next_page_link)
# response = requests.get("https://www.affidata.com/sh/nav?cmd=browsesearchresults&range=4&refresh=false")
# soup = BeautifulSoup(response.content, 'html.parser')
# next_page_link = soup.find('a')
# print(next_page_link)
#
# next_page_link = soup.find('a')
# print(next_page_link)
# links = soup.find_all("a") # Find all elements with the tag <a>
# for link in links:
#   print("Link:", link.get("href"), "Text:", link.string)

#
def scrapeMySite():
    for web_url in site_links:
        if re.search('remyvastgoed.com', web_url):
            try:
                print(web_url)

                # ################
                # #
                # #
                # ################
                URL = web_url
                resp = requests.get(URL)
                soup = BeautifulSoup(resp.text, "lxml")

                divs = soup.findAll("table", {"class": "kenmerken"})
                # for div in divs:
                #     row = ''
                #     rows = div.findAll('td')
                #     for row in rows:
                #         print(row[0].string)
                #         print(row[1].string)
                # ################
                # #
                # #
                # ################
                # Using straatnaam
                soup = BeautifulSoup(resp.text, "lxml")
                straatnaam = soup.select('#top_section > h2.title')

                try:
                    print(straatnaam[0].string)
                except IndexError:
                    print("list index out of range")
                except:
                    print("Something else went wrong")

                # Using prijs
                prijs = soup.select('#top_section > h2.prijs')

                try:
                    print(prijs[0].text)
                except IndexError:
                    print("list index out of range")
                except:
                    print("Something else went wrong")

                # # Using kamers
                aantal_kamers = soup.select(
                    '#bottom_section > div > div.kenmerken > table > tbody > tr:nth-child(5) > td:nth-child(2)')
                print(aantal_kamers)
                #
                # # Using slaapkamers
                aantal_slaapkamers = soup.select(
                    '#bottom_section > div > div.kenmerken > table > tbody > tr:nth-child(6) > td:nth-child(2)')
                print(aantal_slaapkamers)
                #
                # # Using perceeloppervlakte
                perceel_opp = soup.select(
                    '#bottom_section > div > div.kenmerken > table > tbody > tr:nth-child(3) > td:nth-child(2)')
                print(perceel_opp)
                #
                # # Using bouwoppervlakte
                bouwoppervlakte = soup.select(
                    '#bottom_section > div > div.kenmerken > table > tbody > tr:nth-child(4) > td:nth-child(2)')
                print(bouwoppervlakte)

                # ################
                # #
                # #
                # ################
                soup = BeautifulSoup(resp.text, "lxml")
                elements = soup.select('#bottom_section > div > div.kenmerken')
                # print(elements[0])
                # type = (soup.find("td", text="Type").find_next_sibling("td").string)
                # print(type)
                # title = (soup.find("td", text="Titel").find_next_sibling("td").string)
                # print(title)
                # Perceeloppervlakte = (soup.find("td", text="Perceeloppervlakte").find_next_sibling("td").string)
                # print(Perceeloppervlakte)
                # Bouwoppervlakte = (soup.find("td", text="Bouwoppervlakte").find_next_sibling("td").string)
                # print(Bouwoppervlakte)
                # aantal_kamers = (soup.find("td", text="Aantal kamers").find_next_sibling("td").string)
                # print(aantal_kamers)
                # aantal_slaapkamers = (soup.find("td", text="Aantal slaapkamers").find_next_sibling("td").string)

                # ################
                # # ToDO
                # #
                # ################
                regex_image_url = "(http?:\/\/.*\.(?:png|jpg))"
                regex_image_filename = "([^\\s]+(\\.(?i)(jpe?g|png|gif|bmp))$)"
                regex_image_name_from_url = "(/[\w-]+\.(jpg|png|txt)/g)"
                # myimage_name = re.compile(', (.*)\n')
                # use one of the following to find  the complete link to an image posted on the website
                divs = soup.findAll("galleria-image")
                # images_url = images[0]['src']
                # images = soup.find_all('img')
                divs = soup.findAll("galleria-images")
                # image_urls = re.findall(r'http?:\/\/.*\.(?:png|jpg)')
                # for found_image_url in image_urls:
                #     resulted_filname = re.match(regex_image_filename, found_image_url)  # Returns Match object
                #     print(resulted_filname)
                #
                divs = soup.findAll("galleria-images")
                images = soup.find_all('img')
                images_url = images[0]['src']
                images = soup.findAll('img')
                for image in images:
                    print(image['src'])
                # myimage.findall(images)
                r = requests.get(web_url, allow_redirects=True)
                default_location = "jpg"
                dir_name = straatnaam[0].string
                image_name = straatnaam[0].string + ".jpg"
                full_file_path = default_location+"/"+dir_name + "/" + image_name
                # open(full_file_path, 'wb').write(r.content)
                # filename = "/foo/bar/baz.txt"



                try:
                    os.makedirs(os.path.dirname(full_file_path), exist_ok=True)
                    with open(full_file_path, "wb") as f:
                        f.write(r.content)
                except IndexError:
                    print("list index out of range")
                except:
                    print("Something else went wrong")

                # ################
                # #
                # #
                # ################
            except requests.exceptions.Timeout:
                print(" ")
            except requests.exceptions.TooManyRedirects:
                print(" ")
            except requests.exceptions.RequestException as e:
                print(" ")
                raise SystemExit(e)





        else:
            if re.search('hello.sr|worldeconomics.com|waterkant.com', web_url):
                print(" ")
                # domain = urlparse(web_url).netloc
            else:
                print('Neither url is needed')





url = "https://www.affidata.com/sh/nav?cmd=browsesearchresults&range=4&refresh=false"
open_page = urllib.request.urlopen(url)
soup = BeautifulSoup(open_page, "lxml")
print(soup)
class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True


if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
    print(" ")