#!/usr/bin/python3
from gmxsmdscript import *

parser = argparse.ArgumentParser()
parser.add_argument("-f", dest="folder", required=True,
                    help="Project folder name")
args = parser.parse_args()

print(args.folder)

with system(args.folder):

    mdrun(deffnm = 'md',
        s = 'md.tpr',
        cpi = 'md.cpt',
        append = 'true',
        nt = 20,
        pinoffset = 1,
        pinstride = 2,
        gpu_id = "01",
        v = 'true',
        resethway = 'true',
        pin = 'on',
        nb = 'gpu'
    )
