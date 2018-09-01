#!/usr/bin/python3
from gmxsmdscript import *

with system('1AKI'):

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
