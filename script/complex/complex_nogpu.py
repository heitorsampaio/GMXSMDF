#!/usr/bin/python3

from gmxsmdscript import *
import sys
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("-s", dest="structure", required=True,
                    help="Structure filename directory '/home/patgen/Documentos/Dynamics/ProjectName'", type=lambda f: open(f))
parser.add_argument("-f", dest="folder", required=True,
                    help="Desired project folder name")
parser.add_argument("-mdt", dest="mdtime", required=True,
                    help="MD simulation time in nsteps (2 * 500000 = 1000 ps (1 ns)")
parser.add_argument("-l", dest="ligname", required=False,
                    help="Ligand filename .gro")
parser.add_argument("-grps", dest="grps", required=True,
                    help="TC-TGRPS for simulation (ligand name ex: DLG)")
args = parser.parse_args()

def yes_or_no(question):
    reply = str(input(question+' (y/n): ')).lower().strip()
    if reply[0] == 'y':
        return 1
    elif reply[0] == 'n':
        raise SystemExit
    else:
        return yes_or_no("Would you like to run the simulation? (y/n) ")

print("This Script was made by Heitor Sampaio")
while True:
    print("The pourpose of this script is to run a Simple MD simulation...")
    if(yes_or_no('Would you like to run the simulation?  ')):
        break
print("done")

print(args.structure.name)
print(args.folder)
print(args.mdtime)
print(args.ligname)
print(args.grps)

with system(args.folder):

    # System preparation
    pdb2gmx(
        ff    = 'gromos53a6',
        water = 'spce',
        f     = [args.structure.name],
        o     = 'protein.gro',
        p     = 'topol.top',
        ignh = 'true'
    )

    def yes_or_no(question):
        reply = str(input(question+' (y/n): ')).lower().strip()
        if reply[0] == 'y':
            return 1
        elif reply[0] == 'n':
            raise SystemExit
        else:
            return yes_or_no("Are you combine the protein and ligand to complex.gro and add the Protein-Ligand Topologies to topol.top? (y/n) ")

    print(
    "Please combine the protein.gro and the ligand.gro to a complex using the following command 'python combineGRO.py protein.gro ligand.gro' and then "
    )
    while True:
        print("Combine the Protein-Ligand Topologies to topol.top as showed in tutorial")
        if(yes_or_no('Are you combine the protein and ligand to complex.gro and add the Protein-Ligand Topologies to topol.top? ')):
            break
    print("done")

    editconf(
        f  = 'complex.gro',
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
        maxwarn = 2,
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

    make_ndx(
        f = [args.ligname],
        o = 'index_lig.ndx',
        stdin = '''
            0 & ! a H*
            q | q
        '''
    )

    genrestr(
        f =  [args.ligname],
        n = 'index_lig.ndx',
        o = 'posre_lig.itp',
        fc = [1000 , 1000 , 1000],
        stdin = """
            0
        """
    )

    def yes_or_no(question):
        reply = str(input(question+' (y/n): ')).lower().strip()
        if reply[0] == 'y':
            return 1
        elif reply[0] == 'n':
            raise SystemExit
        else:
            return yes_or_no("Are you add the ligand position restrain to topol.top? (y/n) ")

    print(
    "Please add the ligand position restrain to topol.top "
    )
    while True:
        print("Please add the ligand position restrain to topol.top as showed in tutorial")
        if(yes_or_no('Are you add the ligand position restrain to topol.top? ')):
            break
    print("done")

    make_ndx(
        f = 'em.gro',
        o = 'index.ndx',
        stdin = '''
            1 | 13
            q | q
        '''
    )

    #nvt
    grompp(
        f = MDP['nvt.mdp', {
            'tc-grps'       : [args.grps , 'Water_and_ions'] ,
        }],
        c = 'em.gro',
        o = 'nvt.tpr',
        p = 'topol.top',
	    r = 'em.gro',
        n = 'index.ndx',
        maxwarn = 2
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
        f = MDP['npt.mdp', {
            'tc-grps'       : [args.grps , 'Water_and_ions'] ,
        }],
        c = 'nvt.gro',
        o = 'npt.tpr',
        p = 'topol.top',
        t = 'nvt.cpt',
	    r = 'nvt.gro',
        n = 'index.ndx',
        maxwarn = 2
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
            'tc-grps'       : [args.grps , 'Water_and_ions'] ,
        }],
        c = 'npt.gro',
        o = 'md.tpr',
        p = 'topol.top',
        t = 'npt.cpt',
	    r = 'npt.gro',
        n = 'index.ndx',
        maxwarn = 2
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
