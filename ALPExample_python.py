# Example of how to use the LHE Reader for an ALP decay (diphoton) example
from lhereader import readLHEF
from ROOT import TCanvas, TH1F, TH2F, TLorentzVector, TF1
import math
import matplotlib.pyplot as plt
import numpy as np
import argparse

def main(args):
    # Extract photons:
    data=[]
    data=readLHEF(str(args.fullfilename))
    photons=data.getParticlesByIDs([22])
    ALPs=data.getParticlesByIDs([666])

    # make an empty vector to fill with the quantity you want to plot
    pt = []
    angle = []
    nphoton=0

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
            # to get details of each photon (assume two per event in even structure - this should be OK)
            if nphoton%2!=0:
                print("this is the first photon in event")
                gamma1_4mom = g.p4
            if nphoton%2==0:
                print("this is the second photon in event")
                gamma2_4mom = g.p4
                # angle between the two photons
                angle.append(gamma1_4mom.Angle(gamma2_4mom.Vect()))
    alp_pt = []
    for a in ALPs:
        alp_pt.append(a.p4.Pt())

    fig, ax = plt.subplots(1,1)
    plt.title("Transverse Momentum "+str(args.process)+" mALP = "+str(args.mass)+"MeV/c")
    n, bins, patches = ax.hist(pt,
                               bins=100,
                               range=(0,8),
                               label="ALPs")
    nentries = len(alp_pt)
    mean = np.mean(alp_pt)
    #rms = np.sqrt(np.mean(pt))
    #adding text inside the plot
    plt.text(6,40000, 'nentries = '+str(nentries), fontsize = 8)
    plt.text(6,20000, 'mean = '+str(np.round(mean,2)), fontsize = 8)
    ax.set_yscale('log')
    ax.set_ylabel('events per bin')
    ax.set_xlabel('pt of virtual ALP [MeV/c]')
    fig.savefig('ALPpt.pdf')


    fig, ax = plt.subplots(1,1)
    plt.title("Photon Transverse Momentum "+str(args.process)+" mALP = "+str(args.mass)+"MeV/c")
    n, bins, patches = ax.hist(pt,
                               bins=100,
                               range=(0,8),
                               label="photons")
    nentries = len(pt)
    mean = np.mean(pt)
    #rms = np.sqrt(np.mean(pt))
    #adding text inside the plot
    plt.text(6,40000, 'nentries = '+str(nentries), fontsize = 8)
    plt.text(6,20000, 'mean = '+str(np.round(mean,2)), fontsize = 8)
    ax.set_yscale('log')
    ax.set_ylabel('events per bin')
    ax.set_xlabel('pt of all photons [MeV/c]')
    fig.savefig('pt.pdf')

    fig, ax = plt.subplots(1,1)
    plt.title("Angle Between Photons "+str(args.process)+" mALP = "+str(args.mass)+"MeV/c")
    n, bins, patches = ax.hist(angle,
                               bins=100,
                               range=(0,math.pi),
                               label="photons")
    nentries = len(angle)
    mean = np.mean(angle)
    #rms = np.sqrt(np.mean(pt))
    #adding text inside the plot
    plt.text(1,40000, 'nentries = '+str(nentries), fontsize = 8)
    plt.text(1,20000, 'mean = '+str(np.round(mean,2)), fontsize = 8)
    ax.set_yscale('log')
    ax.set_ylabel('events per bin')
    ax.set_xlabel('angle between photons')
    fig.savefig('angle.pdf')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--fullfilename", help="full filename with path", default="/Users/sophie/LDMX/software/ALPs/m300_prima.lhe")
    parser.add_argument("--process", help="Primakoff or Photon Fusion")
    parser.add_argument("--mass", help="ALP mass")
    args = parser.parse_args()
    (args) = parser.parse_args()
    main(args)
