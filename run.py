from subprocess import call
import subprocess
import os
import sys
import errno

GLOBAL_PATH='/Users/heitorsampaio/GMXSMDF/'

def logo():
    print(
        '''
██████╗  █████╗ ████████╗ ██████╗ ███████╗███╗   ██╗
██╔══██╗██╔══██╗╚══██╔══╝██╔════╝ ██╔════╝████╗  ██║
██████╔╝███████║   ██║   ██║  ███╗█████╗  ██╔██╗ ██║
██╔═══╝ ██╔══██║   ██║   ██║   ██║██╔══╝  ██║╚██╗██║
██║     ██║  ██║   ██║   ╚██████╔╝███████╗██║ ╚████║
╚═╝     ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚══════╝╚═╝  ╚═══╝
                                                                                                          
====================================================================
**                WebSite : patgen.com.br                         **
**           Organization : PatGen - UFPE                         **
**             Developer  : Heitor Sampaio                        **
**           Description  : GMXSMDF                               **
**               Licence  : MIT                                   **
====================================================================
        '''
    )

def menu():
    print(
        '''
██████╗  █████╗ ████████╗ ██████╗ ███████╗███╗   ██╗
██╔══██╗██╔══██╗╚══██╔══╝██╔════╝ ██╔════╝████╗  ██║
██████╔╝███████║   ██║   ██║  ███╗█████╗  ██╔██╗ ██║
██╔═══╝ ██╔══██║   ██║   ██║   ██║██╔══╝  ██║╚██╗██║
██║     ██║  ██║   ██║   ╚██████╔╝███████╗██║ ╚████║
╚═╝     ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚══════╝╚═╝  ╚═══╝
                                                                                                          
====================================================================
**                WebSite : patgen.com.br                         **
**           Organization : PatGen - UFPE                         **
**             Developer  : Heitor Sampaio                        **
**           Description  : GMXSMDF                               **
**               Licence  : MIT                                   **
====================================================================
    Select from the menu:
    1 : Run Simple MD with GPU
    2 : Run Simple MD without GPU
    3 : Run Complex MD with GPU
    4 : Run Complex MD without GPU
    5 : Run Checkpoint with GPU
    6 : Run Checkpoint without GPU
    99: Exit
        '''
    )
    choice = input("Enter Your Choice: ")
    if choice == '1':
        smdgpu()
    elif choice == '2':
        smdngpu()
    elif choice == '3':
        compmdgpu()
    elif choice == '4':
        compmdngpu()
    elif choice == '5':
        chkptgpu()
    elif choice == '6':
        chkptngpu
    elif choice == '99':
        clearSrc(),sys.exit()
    elif choice == '':
        menu()
    else:
        menu()

def folder_ana():
    ana = GLOBAL_PATH+'Analysis/'
    try:
        os.mkdir(ana)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass
        os.chdir(ana)

def smdgpu():
    struc = input('Enter the structure .pdb file: ')
    folder = input('Enter the folder name output: ')
    nsTIME = input('Enter the simulation time in NS: ')
    #ns = 0.001
    nSTE = 1000
    gM = 2

    nsPS = float(nsTIME) / (0.001)
    nsToNSTE = nsPS * nSTE
    mdTime = int(nsToNSTE / gM)
    folder_ana()
    call ([
        'python3',
        GLOBAL_PATH+'script/gmxsmdf_gpu.py',
        '-s',struc,
        '-f',folder,
        '-mdt',str(mdTime)

    ])
def smdngpu():
    struc = input('Enter the structure .pdb file: ')
    folder = input('Enter the folder name output: ')
    nsTIME = input('Enter the simulation time in NS: ')
    #ns = 0.001
    nSTE = 1000
    gM = 2

    nsPS = float(nsTIME) / (0.001)
    nsToNSTE = nsPS * nSTE
    mdTime = int(nsToNSTE / gM)
    folder_ana()
    call ([
        'python3',
        GLOBAL_PATH+'script/gmxsmdf_nogpu.py',
        '-s',struc,
        '-f',folder,
        '-mdt',str(mdTime)
    ])
def compmdgpu():
    struc = input('Enter the structure .pdb file: ')
    ligand = input('Enter the ligand .gro file: ')
    folder = input('Enter the folder name output: ')
    tcGroup = input('Enter the TC Group [EX:. Protein_LIGNAME]: ')
    nsTIME = input('Enter the simulation time in NS: ')
    #ns = 0.001
    nSTE = 1000
    gM = 2

    nsPS = float(nsTIME) / (0.001)
    nsToNSTE = nsPS * nSTE
    mdTime = int(nsToNSTE / gM)
    folder_ana()
    call([
        'python3',
        GLOBAL_PATH+'script/complex/complex_gpu.py',
        '-s',struc,
        '-f',folder,
        '-mdt',str(mdTime),
        '-l',ligand,
        '-tcgrps',tcGroup

    ])
def compmdngpu():
    struc = input('Enter the structure .pdb file: ')
    ligand = input('Enter the ligand .gro file: ')
    folder = input('Enter the folder name output: ')
    tcGroup = input('Enter the TC Group [EX:. Protein_LIGNAME]: ')
    nsTIME = input('Enter the simulation time in NS: ')
    #ns = 0.001
    nSTE = 1000
    gM = 2
    
    nsPS = float(nsTIME) / (0.001)
    nsToNSTE = nsPS * nSTE
    mdTime = int(nsToNSTE / gM)
    folder_ana()
    call([
        'python3',
        GLOBAL_PATH+'script/complex/complex_nogpu.py',
        '-s',struc,
        '-f',folder,
        '-mdt',str(mdTime),
        '-l',ligand,
        '-tcgrps',tcGroup

    ])
def chkptgpu():
    folder = input('Enter the folder name that contains md files: ')
    struc = input('Enter the structure .pdb file: ')
    folder_ana()
    call([
        'python3',
        GLOBAL_PATH+'script/gmxsmdf_checkpoint_gpu.py'
        '-f',folder,
        '-s',struc
    ])

def chkptngpu():
    folder = input('Enter the folder name that contains md files: ')
    struc = input('Enter the structure .pdb file: ')
    folder_ana()
    call([
        'python3',
        GLOBAL_PATH+'script/gmxsmdf_checkpoint_nogpu.py'
        '-f',folder,
        '-s',struc
    ])

def clearSrc():
    os.system('clear')

if __name__ == "__main__":
    menu()
