#!/usr/bin/python3

from gmxsmdscript import *
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-s", dest="structure", required=True,
                    help="Structure filename directory '/home/patgen/Documentos/Dynamics/ProjectName'", type=lambda f: open(f))
parser.add_argument("-f", dest="folder", required=True,
                    help="Desired project folder name")
parser.add_argument("-mdt", dest="mdtime", required=True,
                    help="MD simulation time in nsteps (2 * 500000 = 1000 ps (1 ns)")
args = parser.parse_args()

print(args.structure.name)
print(args.folder)
print(args.mdtime)

with system(args.folder):
    # System preparation
    pdb2gmx(
        ff    = 'gromos53a6',
        water = 'spce',
        f     = [args.structure.name],
        o     = 'prot.gro',
        p     = 'topol.top',
        ignh = 'true'
    )

    editconf(
        f  = 'prot.gro',
        o  = 'pbc.gro',
        bt = 'cubic',
        d  = 1.0
    )

    solvate(
        cp = 'pbc.gro',
        cs = 'spc216.gro',
        o  = 'sol.gro',
        p  = 'topol.top'
    )

    grompp(
	maxwarn = 2,
        f = MDP['ions.mdp'],
        c = 'sol.gro',
        o = 'ions.tpr',
        p = 'topol.top'
    )

    genion(
        s       = 'ions.tpr',
        o       = 'ions.gro',
        neutral = 1,
        p       = "topol.top",
        stdin   = """
            SOL
        """
    )

    # Steep descent energy minimization
    grompp(
        f = MDP['em.mdp'],
        c = 'ions.gro',
        o = 'em.tpr',
        p = 'topol.top',
    )
    mdrun(deffnm = 'em' ,
        cpi = 'md.cpt',
        #append = 'true',
        #nt = 20,
        #pinoffset = 1,
        #pinstride = 2,
        #gpu_id = "01",
        v = 'true',
        #resethway = 'true',
        #pin = 'on',
        #nb = 'gpu'
    )
    energy(
        f = 'em.edr',
        o = 'potential.xvg',
        stdin = """
            10 0
        """
    )

    #nvt
    grompp(
        f = MDP['nvt.mdp'],
        c = 'em.gro',
        o = 'nvt.tpr',
        p = 'topol.top',
	    r = 'em.gro'
    )
    mdrun(deffnm = 'nvt',
        cpi = 'md.cpt',
        #append = 'true',
        #nt = 20,
        #pinoffset = 1,
        #pinstride = 2,
        #gpu_id = "01",
        v = 'true',
        #resethway = 'true',
        #pin = 'on',
        #nb = 'gpu'
    )
    energy(
        f = 'nvt.edr',
        o = 'temperature.xvg',
        stdin = """
            15 0
        """
    )

    #npt
    grompp(
        f = MDP['npt.mdp'],
        c = 'nvt.gro',
        o = 'npt.tpr',
        p = 'topol.top',
        t = 'nvt.cpt',
	    r = 'nvt.gro'
    )
    mdrun(deffnm = 'npt' ,
        cpi = 'md.cpt',
        #append = 'true',
        #nt = 20,
        #pinoffset = 1,
        #pinstride = 2,
        #gpu_id = "01",
        v = 'true',
        #resethway = 'true',
        #pin = 'on',
        #nb = 'gpu'
    )
    energy(
        f = 'npt.edr',
        o = 'pressure.xvg',
        stdin = """
            16 0
        """
    )
    energy(
        f = 'npt.edr',
        o = 'density.xvg',
        stdin = """
            22 0
        """
    )

    # Molecular dynamics
    grompp(
        f = MDP['md.mdp', {
            'nsteps'       : args.mdtime ,
        }],
        c = 'npt.gro',
        o = 'md.tpr',
        p = 'topol.top',
        t = 'npt.cpt',
	    r = 'npt.gro'
    )
    mdrun(deffnm = 'md',
        cpi = 'md.cpt',
        #append = 'true',
        #nt = 20,
        #pinoffset = 1,
        #pinstride = 2,
        #gpu_id = "01",
        v = 'true',
        #resethway = 'true',
        #pin = 'on',
        #nb = 'gpu'
    )
    trjconv(
        s = 'md.tpr',
        f = 'md.xtc',
        o = 'md_noPBC.xtc',
        pbc = 'mol',
        ur = 'compact',
        stdin = """
            0
        """
    )
    rms(
        s = 'md.tpr',
        f = 'md_noPBC.xtc',
        o = 'rmsd.xvg',
        tu = 'ns',
        stdin = """
            4 4
        """
    )
    gyrate(
        s = 'md.tpr',
        f = 'md_noPBC.xtc',
        o = 'gyrate.xvg',
        stdin = """
            1
        """
    )
    sasa(
        s = 'md.tpr',
        f = 'md_noPBC.xtc',
        o = 'sasa.xvg',
        stdin = """
            1
        """
    )
    rmsf(
        s = 'md.tpr',
        f = 'md_noPBC.xtc',
        o = 'rmsf.xvg',
        res = 'true',
        stdin = """
            1
        """
    )
    rmsf(
        s = 'md.tpr',
        f = 'md_noPBC.xtc',
        o = 'bfactor.xvg',
        oq = 'bfactor.pdb',
        stdin = """
            1
        """
    )
    hbond(
        s = 'md.tpr',
        f = 'md_noPBC.xtc',
        dist = 'hbond.xvg',
        g = 'hbond.log',
        stdin = """
            1 1
        """
    )
