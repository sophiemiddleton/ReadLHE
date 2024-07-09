# Example of how to use the LHE Reader for an electron scattering example
from lhereader import readLHEF
from ROOT import TCanvas, TH1F, TH2F, TLorentzVector, TF1
import math

# Extract electrons:
data=[]
data=readLHEF('/Users/sophie/LDMX/software/test/m200_PF.lhe')
photons=data.getParticlesByIDs([22])

# Make ROOT:
c=TCanvas()
c.Divide(2,2)

hist_out=TH1F("pz out", "Outgoing Photron Pz", 100,0,8)

# Loop over photons:
for g in photons:
    # Outgoing photons (status ==1):
    if (g.status == 1):
        hist_out.Fill(g.p4.Pt())

c.cd()
hist_out.GetXaxis().SetTitle("photon momentum [MeV/c]")
hist_out.Draw('HIST')
c.SaveAs("photons.root")
