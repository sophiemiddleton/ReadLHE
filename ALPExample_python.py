# Example of how to use the LHE Reader for an ALP decay (diphoton) example
from lhereader import readLHEF
from ROOT import TCanvas, TH1F, TH2F, TLorentzVector, TF1
import math
import matplotlib.pyplot as plt
import numpy as np
# Extract electrons:
data=[]
data=readLHEF('/Users/sophie/LDMX/software/test/m200_PF.lhe')
photons=data.getParticlesByIDs([22])

# make an empty vector to fill with the quantity you want to plot
pt = []
angle = []
nphoton=0
# Loop over all photons:
for g in photons:
    nphoton+=1
    # Outgoing photons (status ==1):
    if (g.status == 1):
        # all photons
        pt.append(g.p4.Pt())
        # to get details of each photon:
        if nphoton%2!=0:
            print("this is the first photon in event")
            gamma1_4mom = g.p4
        if nphoton%2==0:
            print("this is the second photon in event")
            gamma2_4mom = g.p4
            angle.append(gamma1_4mom.Angle(gamma2_4mom.Vect()))

fig, ax = plt.subplots(1,1)
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
