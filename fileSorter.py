import os, shutil, time
from tkinter import *
from tkinter import ttk, filedialog, messagebox


def sorter():
    rootPath = str(path.get())
    choice = int(choose.get())
    checkSub = int(check.get())
    if not rootPath:
        error.set("Please Enter Or Choose A Location Where Sorting is Required.")
    elif choice == 0:
        error.set("Please Choose From One Of The Given Sorting Options")
    elif os.path.exists(rootPath):
        error.set("")
        os.chdir(rootPath)
        fileList = os.scandir(rootPath)
        fileNames = []
        fileDirs = []
        for files in fileList:
            if files.is_file():
                fileNames.append(files.name.upper())
            elif files.is_dir():
                fileDirs.append(files.name.upper())
        # choice = int(input("\nPlease choose how you would like your files sorted? "))
        if  checkSub == 0 and choice == 1:
            alphabetSort(fileNames)
            sortDone()
        elif  checkSub == 0 and choice == 2:
            timeSort(fileNames)
            sortDone()    
        elif  checkSub == 1 and choice == 1:
            alphabetSort(fileNames)
            for dirs in fileDirs:
                os.chdir(f"{rootPath}\\"+dirs)
                fileList = os.scandir(f"{rootPath}\\"+dirs)
                createdFileDir = []
                level2FileDirs = []
                fileNames = []
                for files in fileList:
                    if files.is_file():
                        fileNames.append(files.name.upper())
                    elif files.is_dir():
                        level2FileDirs.append(files.name.upper())
                alphabetSort(fileNames)
            sortDone()
        elif checkSub == 1 and choice == 2:
            createdFileDir = []
            for i in range(len(fileNames)):
                date = time.ctime(os.path.getmtime(fileNames[i]))
                dirName = date[4:10] + " " + date[20:24]
                if dirName in createdFileDir:
                    shutil.move(fileNames[i], dirName)
                else:
                    os.mkdir(dirName)
                    createdFileDir.append(dirName)
                    shutil.move(fileNames[i], dirName)  
            for dirs in fileDirs:
                os.chdir(f"{rootPath}\\"+dirs)
                fileList = os.scandir(f"{rootPath}\\"+dirs)
                level2FileDirs = []
                fileNames = [] 
                createdFileDir = []
                for files in fileList:
                    if files.is_file():
                        fileNames.append(files.name.upper())
                    elif files.is_dir():
                        level2FileDirs.append(files.name.upper())
                timeSort(fileNames)
            sortDone()
    else:
        error.set("Please Enter A Valid Path.")                            

def browseFiles():
    filename = filedialog.askdirectory(initialdir = "/", title = "Select a Folder Where Sorting is Required.")
    path_entry.insert(0,filename)



def alphabetSort(fileNames):
    createdFileDir = []
    for i in range(len(fileNames)):
        if fileNames[i][0] in createdFileDir:
            shutil.move(fileNames[i], fileNames[i][0])
        else:
            os.mkdir(fileNames[i][0])
            createdFileDir.append(fileNames[i][0].upper())
            shutil.move(fileNames[i], fileNames[i][0])

def timeSort(fileNames):
    createdFileDir = []
    for i in range(len(fileNames)):
        date = time.ctime(os.path.getmtime(fileNames[i]))
        dirName = date[4:10] + " " + date[20:24]
        if dirName in createdFileDir:
            shutil.move(fileNames[i], dirName)
        else:
            os.mkdir(dirName)
            createdFileDir.append(dirName)
            shutil.move(fileNames[i], dirName)
def sortDone():
    return messagebox.showinfo(title="Files Have Been Sorted", detail='Your Files Have Been Sorted', parent=mainframe)
    
root = Tk()
root.title("File Sorter")

mainframe = ttk.Frame(root) 
mainframe.grid(column=0, row=0)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

path = StringVar()
path_label = ttk.Label(mainframe, text="Enter Path Where Sorting Is Required: ").grid(column=0, row=1, sticky=(N,S,E,W))
path_entry = ttk.Entry(mainframe, width=50, textvariable=path)
path_entry.grid(column=3, row=1, sticky=(N,S,E,W))
path_entry.focus()
chooseFolder = ttk.Button(mainframe, text="Choose Folder", command=browseFiles).grid(column=3, row=2, sticky=(N, S, W, E))
sort = ttk.Button(mainframe, text="Sort", command=sorter).grid(column=3, row=3,rowspan=2, sticky=(N, S, W, E))

error = StringVar()
errorPrompt = ttk.Label(mainframe,width=60, textvariable=error, foreground="red")
choose = StringVar(value="0")
alphabetic = ttk.Radiobutton(mainframe, text="Sort In Alphabetic Order", variable=choose, value = "1").grid(column=0, row=2, sticky=(W, E))
dateWise = ttk.Radiobutton(mainframe, text="Sort By Modification Date", variable=choose, value = "2").grid(column=0, row=3, sticky=(W, E))

check = StringVar()
subFolder = ttk.Checkbutton(mainframe, text="Include Subfolders In Given Path", variable=check).grid(column= 0, row=4, sticky=(W,E))
check.set(0)


for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

root.mainloop()