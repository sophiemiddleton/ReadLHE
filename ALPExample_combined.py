# Example of how to use the LHE Reader for an ALP decay (diphoton) example
from lhereader import readLHEF
from ROOT import TCanvas, TH1F, TH2F, TLorentzVector, TF1
import math
import matplotlib.pyplot as plt
import numpy as np
import argparse
from sklearn.preprocessing import normalize

path = "/Users/sophie/LDMX/software/ALPs/"

def main(args):
    # Extract photons:

    pts = []
    pzs = []
    angles = []
    alpenergies = []
    weightz = []
    for i, data in enumerate(args.fullfilename):
        data=[]
        data_list=readLHEF(str(path)+str(args.fullfilename[i]))
        photons=data_list.getParticlesByIDs([22])
        ALPs=data_list.getParticlesByIDs([666])

        # make an empty vector to fill with the quantity you want to plot
        pt = []
        pz = []
        angle = []
        nphoton=0
        weight = []
        # TLorentzVector for the two photons
        gamma1_4mom = TLorentzVector()
        gamma2_4mom = TLorentzVector()
        # Loop over all photons:
        for g in photons:
            # Outgoing photons (status ==1):
            if (g.status == 1):
                nphoton+=1
                # all photons
                pt.append(g.p4.Pt())
                pz.append(g.pz)
                # to get details of each photon (assume two per event in even structure - this should be OK)
                if nphoton%2!=0:
                    print(nphoton,"this is the first photon in event")
                    gamma1_4mom = g.p4
                if nphoton%2==0:
                    print(nphoton,"this is the second photon in event")
                    gamma2_4mom = g.p4
                    # angle between the two photons

                print("---------------------")
                angle.append(gamma1_4mom.Angle(gamma2_4mom.Vect()))

        alp_energy = []
        pts.append(pt)
        pzs.append(pz)
        angles.append(angle)
        nALPs = 1
        for a in ALPs:
            alp_energy.append(a.energy)
            weight.append(1/(nALPs))
            nALPs+=1
        alpenergies.append(alp_energy)
        weightz.append(weight)

    styles = ["solid","dashed","solid","dashed","solid","dashed","solid","dashed"]
    colors = ["green","green","blue","blue","orange","orange","red","red"]
    labels = ["primakoff","photonfusion","primakoff","photonfusion","primakoff","photonfusion","primakoff","photonfusion"]
    fig, ax = plt.subplots(1,1)
    for i, data in enumerate(pts):

        plt.title("Photon Transverse Momentum")
        n, bins, patches = ax.hist(pts[i],
                                   bins=100,
                                   range=(0,2),
                                   histtype = 'step',
                                   linestyle = styles[i],
                                   color = colors[i],
                                   label=str(args.fullfilename[i]))
    plt.legend()
    ax.set_yscale('log')
    ax.set_ylabel('events per bin')
    ax.set_xlabel('pt of all photons [MeV/c]')
    fig.savefig('pt.pdf')

    fig, ax = plt.subplots(1,1)
    for i, data in enumerate(pzs):

        plt.title("Photon Pz Momentum")
        n, bins, patches = ax.hist(pzs[i],
                                   bins=100,
                                   range=(0,8),
                                   histtype = 'step',
                                   linestyle = styles[i],
                                   color = colors[i],
                                   label=str(args.fullfilename[i]))
    plt.legend()
    ax.set_yscale('log')
    ax.set_ylabel('events per bin')
    ax.set_xlabel('pz of all photons [MeV/c]')
    fig.savefig('pz.pdf')

    fig, ax = plt.subplots(1,1)
    for i, data in enumerate(angles):

        plt.title("Angle between photons")
        n, bins, patches = ax.hist(pzs[i],
                                   bins=100,
                                   range=(-1,2*math.pi),
                                   histtype = 'step',
                                   linestyle = styles[i],
                                   color = colors[i],
                                   label=str(args.fullfilename[i]))
    plt.legend()
    ax.set_yscale('log')
    ax.set_ylabel('events per bin')
    ax.set_xlabel('angle between photons')
    fig.savefig('angle.pdf')

    fig, ax = plt.subplots(1,1)
    for i, data in enumerate(alpenergies):

        plt.title("mALP= "+str(args.mass)+" MeV")
        #normalize([alpenergies[i]])[0],
        n, bins, patches = ax.hist( alpenergies[i],
                                   bins=50,
                                   range=(0,10),
                                   histtype = 'step',
                                   linestyle = styles[i],
                                   color = colors[i],
                                   label=labels[i],
                                   weights=weightz[i])
    plt.legend()
    ax.set_yscale('log')
    ax.set_ylabel('Arb. Units')
    ax.set_xlabel('ALP Energy [MeV]')
    fig.savefig('alp_energy.pdf')
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    files = ["m10_prima.lhe","m10_PF.lhe","m100_prima.lhe","m100_PF.lhe","m300_prima.lhe","m300_PF.lhe","m500_prima.lhe","m500_PF.lhe"]
    parser.add_argument("--fullfilename", help="full filename with path", default=files)
    parser.add_argument("--process", help="Primakoff or Photon Fusion")
    parser.add_argument("--mass", help="ALP mass")
    args = parser.parse_args()
    (args) = parser.parse_args()
    main(args)
