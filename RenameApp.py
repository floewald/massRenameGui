import os
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import Menu

#### TO DO #####
# 1) filter - dropdown menu 
#       -> .pdf, .jpg, .png, ....
# 2) forbidden symbols in name
#       ~ " # % & * : < > ? / \ { | }.
# 3) enumeration of files only once
#       -> prefix / sufffix 0004_0004 bug
#######################################

class Settings(tk.Frame):
    def __init__(self, parent, sep, nod, setfilename, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent         = parent
        self.sep            = sep     # seperator of number of multiple lines
        self.nod            = nod     # number of digits after seperator
        self.setfilename    = setfilename

        self.SetWin = tk.Toplevel(self)
        self.SetFrame = tk.Frame(self.SetWin, relief='ridge')
        self.SetFrame.grid(row=0, column=0)
        self.configSetWin()

        self.Seplabel = tk.Label(self.SetFrame, text='Seperator:', anchor='w', width=15, height=1)
        self.Seplabel.grid(row=0, column=0, padx=(10,10), pady=(1,0))
        self.SepEnt = tk.Entry(self.SetFrame, width=15)
        self.SepEnt.grid(row=0, column=1)
        #self.SepEnt.insert(0, self.sep)
        
        self.Nodlabel = tk.Label(self.SetFrame, text='Number of Digits:', anchor='w', width=15, height=1)
        self.Nodlabel.grid(row=1, column=0, padx=(10,10), pady=(1,0))
        self.NodEnt = tk.Entry(self.SetFrame, width=15)
        self.NodEnt.grid(row=1, column=1)
        #self.NodEnt.insert(0, str(self.nod))

        self.sep, self.nod = self.parent.getSettingsRoot()
        
        self.updateSetEnt(self.sep, self.nod)

        self.SaveBut = tk.Button(self.SetFrame, text='Save', width=10, command=self.updateSettings)
        self.SaveBut.grid(row=2, column=0, columnspan=2, padx=(10,10), pady=(10,10))

        self.ExitBut = tk.Button(self.SetFrame, text='Exit', width=10, command=self.exitSettings)
        self.ExitBut.grid(row=3, column=0, columnspan=2, padx=(10,10), pady=(0,10))

    def updateSetEnt(self, sep, nod):
        self.SepEnt.delete(0, tk.END)
        self.NodEnt.delete(0, tk.END)
        self.SepEnt.insert(0, sep)
        self.NodEnt.insert(0, str(nod))

    def setSettingsParent(self):
        self.parent.setSettingsRoot(self.sep, self.nod)

    def updateSettings(self):
        self.sep = self.SepEnt.get()
        self.nod = int(self.NodEnt.get())
        self.writeSettings()
        self.setSettingsParent()

    def writeSettings(self):
        curdir = os.getcwd()
        os.chdir(self.parent.getWDR())
        setfile = open(self.setfilename, 'w')
        setfile.write('Second Line: Sparator, Third Line: number of digitd after separator\n')
        setfile.write('{}\n'.format(self.sep))
        setfile.write('{}'.format(self.nod))
        setfile.close()
        os.chdir(curdir)

    def getSettings(self):
        return self.sep, self.nod

    def configSetWin(self):
        self.SetWin.geometry('{}x{}'.format(300,140))
        self.SetWin.title('Settings')
        self.SetWin.resizable(False, False)

    def exitSettings(self):
        self.SetWin.destroy()

class Filter(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent     = parent
        #self.filter     = ''
        self.filter     = self.parent.getFilter() 

        self.Filterwin = tk.Toplevel(self)
        self.Title = tk.Label(self.Filterwin, text='Which Files do you want to rename?')
        self.Title.grid(row=0, column=0, columnspan=2, padx=10, pady=(1,1))
        self.filLab = tk.Label(self.Filterwin, text='Filter:')
        self.filLab.grid(row=1, column=0, padx=10, pady=(1,1))
        self.filEnt = tk.Entry(self.Filterwin, width=20)
        self.filEnt.delete(0, tk.END)
        self.filEnt.insert(0, self.filter)
        self.filEnt.focus_set()
        self.filEnt.grid(row=1, column=1, padx=10, pady=(1,1))
        self.filBut = tk.Button(self.Filterwin, text='Use Filter', command=self.useFilter)
        self.filBut.grid(row=2, column=0, columnspan=2, padx=10, pady=(1,1))
        self.configFilterWin()
        self.Filterwin.bind('<Return>', self.useFilter)

    def useFilter(self, *args, **kwargs):
        choice = messagebox.askyesnocancel(message='Are you sure you want to use the filter?')
        if choice == 1:
            self.parent.resetFilter()
            self.parent.setParentFilter(self.filEnt.get())
            self.Filterwin.destroy()
        elif choice == 0:
            self.Filterwin.destroy()

    def configFilterWin(self):
        #self.Filterwin.geometry('{}x{}'.format(300,150))
        self.Filterwin.title('Filter Files')
        self.Filterwin.resizable(False, False)

class Action(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.pathwdr    = os.getcwd()
        self.path       = os.getcwd()

        self.parent      = parent
        self.filter      = ''
        self.ExaName     = 'Filename'
        self.NewName     = ''
        self.filelist    = []
        self.filetypes   = ()
        self.filenames   = ()
        self.setfilename = 'settings.dat'
        self.nof         = 0     # number of files
        self.sep         = '_'   # separator
        self.nod         = 1     # number of digits after separator

        self.menubar = tk.Menu(parent)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='New', menu=self.filemenu)
        self.filemenu.add_command(label='Select Path', command=self.PathCMD)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Filter', command=self.openSetFilter)
        self.filemenu.add_command(label='Reset Filter', command=self.resetFilter)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Exit', command=exit)
        self.parent.config(menu=self.menubar)
        self.settingsmenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Settings', menu=self.settingsmenu)
        self.settingsmenu.add_command(label='Edit Settings', command=self.openSettings)

        self.progressWin = tk.Toplevel(self)
        self.progressWin.title('Loading')
        self.progressWin.resizable(False, False)
        self.progressWin.geometry('{}x{}'.format(130, 20))
        self.progressWin.focus_set()
        self.progressbar = ttk.Progressbar(self.progressWin, orient='horizontal', length=100, mode='determinate')
        self.progressbar.pack()

        self.PathBut = tk.Button(self, text='Select Path', command=self.PathCMD)
        self.PathBut.grid(row=1, column=1, pady=10)


        self.Scrollbary = tk.Scrollbar(self, width=5)
        self.Scrollbarx = tk.Scrollbar(self, width=10, orient='horizontal',)
        self.Filelist  = tk.Listbox(self, width=25, height=8, xscrollcommand=self.Scrollbarx.set, yscrollcommand=self.Scrollbary.set)
        self.Scrollbary.grid(row=2, column=2, sticky='nswe')
        self.Scrollbarx.grid(row=3, column=1, padx=(12,0), columnspan=2, sticky='wens')
        self.Filelist.grid(row=2, column=1, padx=(10,0), sticky='nswe')
        self.Scrollbary.config(command=self.Filelist.yview)
        self.Scrollbarx.config(command=self.Filelist.xview)

        self.NameFrame = tk.LabelFrame(self, text='Name Options', fg='grey')
        self.NameFrame.grid(row=5, column=1, columnspan=3, padx=(10,10), pady=(10,10), sticky='wens')

        self.NameVar = tk.IntVar()
        self.NameVar.set(0)
        self.NameAppRad = tk.Radiobutton(self.NameFrame, text='Keep Name', variable=self.NameVar, value=0, command=self.updateStateName)
        self.NameAppRad.grid(row=1, column=1, sticky='w')

        self.NameNewRad = tk.Radiobutton(self.NameFrame, text='New Name', variable=self.NameVar, value=1, command=self.updateStateName)
        self.NameNewRad.grid(row=1, column=2, sticky='w')

        self.prebool    = tk.IntVar()
        self.prebool.set(1)
        self.prebut     = tk.Checkbutton(self.NameFrame, text='Add Prefix', variable=self.prebool, command=self.updateStateApp)
        self.prebut.grid(row=2, column=1, sticky='w')

        self.preEnt = tk.Entry(self.NameFrame, width=12, state='disabled')
        self.preEnt.bind('<Return>', self.ShowNameEvent)
        self.preEnt.grid(row=3, column=1, padx=5, pady=(0,5), sticky='w')

        self.sufbool    = tk.IntVar()
        self.sufbool.set(0)
        self.sufbut     = tk.Checkbutton(self.NameFrame, text='Add Suffix', variable=self.sufbool, command=self.updateStateApp)
        self.sufbut.grid(row=2, column=2, sticky='w')

        self.sufEnt = tk.Entry(self.NameFrame, width=12, state='disabled')
        self.sufEnt.bind('<Return>', self.ShowNameEvent)
        self.sufEnt.grid(row=3, column=2, padx=5, pady=(0,5), sticky='w')

        self.NewNaEnt = tk.Entry(self.NameFrame, width=26, state='disabled')
        self.NewNaEnt.bind('<Return>', self.ShowNameEvent)
        self.NewNaEnt.grid(row=4, column=1, columnspan=2, padx=5, pady=(0,5), sticky='w')

        self.ViewNaFra = tk.LabelFrame(self, text='New Name', fg='grey')
        self.ViewNaFra.grid(row=5, column=4, padx=(10,10), pady=(10, 10), sticky='wens')

        self.ViewNa1 = tk.Label(self.ViewNaFra, width=15, height=1, text='Example:', anchor='w')
        self.ViewNa1.grid(row=0, column=0, sticky='w')

        self.ViewNa2 = tk.Label(self.ViewNaFra, width=30, height=1, text='')
        self.ViewNa2.grid(row=0, column=1)

        self.ViewNof1 = tk.Label(self.ViewNaFra, width=15, text='Number of files:', anchor='w')
        self.ViewNof1.grid(row=1, column=0, sticky='w')

        self.ViewNof2 = tk.Label(self.ViewNaFra, text='')
        self.ViewNof2.grid(row=1, column=1)


        self.ViewBut = tk.Button(self.ViewNaFra, text='Show example', width=15, height=1, command=self.ShowNewName)
        self.ViewBut.grid(row=2, column=0, columnspan=2)

        self.RenameBut = tk.Button(self.ViewNaFra, text='Rename files', width=15, height=1, command=self.renameFilelist)
        self.RenameBut.grid(row=3, column=0, columnspan=2)
        

        self.loadSettings()
        self.fillBox()
        self.updateStateName()
        self.updateStateApp()

    def exit(self):
        sys.exit()

    def getWDR(self):
        return self.pathwdr

    def getFilelist(self):
        filelist = os.listdir(self.path)
        filelist = [filename for filename in filelist if os.path.isfile(filename)]
        if self.filter != '':
            filtered = []
            for filename in filelist:
                if filename[-len(self.filter):] == self.filter:
                    filtered.append(filename)
            filtered = sorted(filtered)
            return tuple(filtered)
        filelist = sorted(filelist)
        return filelist
      
    def fillBox(self):
        self.filelist   = self.getFilelist()
        self.filenames  = ()
        self.filetypes  = ()
        self.nof        = len(self.filelist)
        for counter, filename in enumerate(self.filelist):
            [names, typ] = os.path.splitext(filename)
            self.filenames += (names,)# str(counter))
            self.filetypes += (typ,)
            #if '0123456789' in self.filenames[counter][0]:
            #    self.filenames[counter][0] = self.filenames[counter][0:-(len(self.sep) + self.nod)]
            self.Filelist.insert(tk.END, filename)

    def clearBox(self):
        self.Filelist.delete(0, tk.END)
    
    def PathCMD(self):
        self.path = filedialog.askdirectory()
        os.chdir(self.path)
        self.clearBox()
        self.fillBox()

    def setParentFilter(self, filter):
        self.filter = filter
        self.clearBox()
        self.fillBox()

    def openSetFilter(self):
        FilWin = Filter(self)

    def resetFilter(self):
        self.filter = ''
        self.clearBox()
        self.fillBox()

    def getFilter(self):
        return self.filter

    def stateChoice(self, statebool):
        if statebool == 0:
            statecmd = 'disabled'
        elif statebool == 1:
            statecmd = 'normal'        
        return statecmd

    def updateStateName(self):
        statebool  = self.NameVar.get()
        prebool    = 0
        sufbool    = 0
        appbutcmd  = 'normal'
        NameEntcmd = 'disabled'
        if statebool == 0:
            prebool    = 1
            sufbool    = 0
            appbutcmd  = 'normal'
            NameEntcmd = 'disabled'
        elif statebool == 1:
            prebool    = 0
            sufbool    = 0
            appbutcmd  = 'disabled'
            NameEntcmd = 'normal'

        self.prebut.configure(state=appbutcmd)
        self.preEnt.configure(state=appbutcmd)
        self.prebool.set(prebool)
        self.sufbut.configure(state=appbutcmd)
        sufEntcmd = self.stateChoice(sufbool)
        self.sufEnt.configure(state=sufEntcmd)
        self.sufbool.set(sufbool)
        self.NewNaEnt.configure(state=NameEntcmd)

    def updateStateApp(self):
        statebool = self.prebool.get()
        activestate = self.stateChoice(statebool)
        self.preEnt.configure(state=activestate)

        statebool = self.sufbool.get()
        activestate = self.stateChoice(statebool)
        self.sufEnt.configure(state=activestate)

    def ShowNameEvent(self, event):
        self.ShowNewName()

    def ShowNewName(self):
        NameExample = self.ExaName

        state = self.NameVar.get()
        if state == 0:
            prebool = self.prebool.get()
            sufbool = self.sufbool.get()
            if prebool == 1:
                NameExample = self.preEnt.get() + NameExample
            if sufbool == 1:
                NameExample = NameExample + self.sufEnt.get()
        elif state == 1:
            NameExample = self.NewNaEnt.get()
        NameExample = NameExample + self.sep + '0'*self.nod + self.filetypes[0]

        self.ViewNa2.configure(text=NameExample)
        self.ViewNof2.configure(text=str(self.nof))
        self.NewName = NameExample

    def renameFilelist(self):
        choice = messagebox.askyesnocancel(title='Rename Files', message='Are you sure to rename {} files?'.format(self.nof))
        NewName = ''
        os.chdir(self.path)
        if choice == True:
            files = self.filenames
            for counter, file_num in enumerate(iterable=files, start=0):
                NewName = file_num
                state = self.NameVar.get()
                if state == 0:
                    prebool = self.prebool.get()
                    sufbool = self.sufbool.get()
                    if prebool == 1:
                        NewName = self.preEnt.get() + NewName
                    if sufbool == 1:
                        NewName = NewName + self.sufEnt.get()
                elif state == 1:
                    NewName = self.NewNaEnt.get()
                formatstr = '{'+':0{}d'.format(self.nod) + '}'
                NewName = NewName + self.sep + formatstr.format(counter) + self.filetypes[counter]
                os.rename(self.filelist[counter], NewName)
        self.clearBox()
        self.fillBox()
        os.chdir(self.pathwdr)

    def openSettings(self):
        SetWin = Settings(self, self.sep, self.nod, self.setfilename)

    def loadSettings(self):
        curdir = os.getcwd()
        os.chdir(self.pathwdr)
        if not(os.path.isfile(self.setfilename)):
            setfile = open(self.setfilename, 'w')
            setfile.write('Second Line: Sparator, Third Line: number of digit after separator\n')
            setfile.write('{}\n'.format(self.sep))
            setfile.write('{}'.format(self.nod))
            setfile.close()
        
        setfile     = open(self.setfilename, 'r')
        self.progressbar['value'] = 50
        content     = setfile.readlines()
        setfile.close()
        os.chdir(curdir)
        for counter, line in enumerate(content):
            content[counter] = line.replace('\n', '')

        self.progressbar['value'] = 75
        self.sep    = content[1]
        self.nod    = int(content[2])

        self.progressbar['value'] = 100
        self.progressWin.destroy()

    def setSettingsRoot(self, sep, nod):
        self.sep = sep
        self.nod = nod
        self.ShowNewName()
        
    def getSettingsRoot(self):
        return self.sep, self.nod

class RenameApp(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent         = parent
        self.PathButton     = Action(self.parent)
        self.PathButton.grid(row=1, column=1)
        self.configureGUI()

    def configureGUI(self):
        self.parent.geometry('{}x{}'.format(650,400))
        self.parent.title('Rename App')
        self.parent.resizable(False, False)

if __name__ == '__main__':
    root = tk.Tk()
    App = RenameApp(root)
    root.mainloop()