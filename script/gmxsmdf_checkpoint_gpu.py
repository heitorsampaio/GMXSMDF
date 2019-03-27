#!/usr/bin/python3
from gmxsmdscript import *
import argparse

GLOBAL_PATH='/Users/heitorsampaio/GMXSMDF/'

parser = argparse.ArgumentParser()
parser.add_argument("-f", dest="folder", required=True,
                    help="Project folder name")
args = parser.parse_args()

print(args.folder)

with system(GLOBAL_PATH+'Analysis/'+args.folder):

    mdrun(deffnm = 'md',
        s = 'md.tpr',
        cpi = 'md.cpt',
        append = 'true',
        ntmpi = 8,
        v = 'true',
        resethway = 'true',
        pin = 'on',
    )
