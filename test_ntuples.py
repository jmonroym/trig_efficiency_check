from ROOT import TCanvas, TFile, TProfile, TNtuple, TH1F, TH2F, TPad, TH1D
from ROOT import gROOT, gBenchmark, gRandom, gSystem, gStyle
from ROOT import TStyle, TF1, gDirectory, TTree, TBrowser, gMinuit, TText, TCut, TPaveText

import ctypes
import sys

if len (sys . argv ) != 3:
    print (" USAGE : %s <input file > <output file >"%( sys. argv [0]))
    sys.exit (1)

#'Mchi-60p0_dMchi-20p0_ctau-1.root'

FileName = sys.argv[1]
plotFileName = sys.argv[2]
print(" Reading from ", FileName , "and writing to", plotFileName)


f = TFile.Open(FileName, "READ")
mytree=f.Get('ntuples_gbm/recoT')
nentry = mytree.GetEntries()
trigfired=[] # triggers fired   
gmpt=[]  # gm_pt[0] : leading gm pt

c1 = TCanvas('c1','The Ntuple canvas',200,10,700,780)
#c2 = TCanvas('c2','The Ntuple canvas',200,10,700,780)
#c3 = TCanvas('c3','The Ntuple canvas',200,10,700,780)
#c4 = TCanvas('c4','The Ntuple canvas',200,10,700,780)

hat = TH1F("Trig_fired", "trig_fired all triggers", 100, 0, 18000000) # event firing the any trigger. 
#hat.Sumw2()

htf = TH1F("trig_fired", "trig_fired cross trigger ", 100, 0, 18000000) # event firing the trigger HLT_Mu3er1p5_PFJet100er2p5_PFMETXX_PFMHTXX IDTight
#htf.Sumw2()

hgmtpt = TH1F("reco_gm_pt", "reco_gm_pt & trigger", 100, 0, 8000) # event firing the trigger AND at least 1 gm. 
hgmtpt.Sumw2()

hgmpt = TH1F("reco_gm_pt", "reco_gm_pt", 100, 0, 8000) # event with at least 1 gm
hgmpt.Sumw2()

hgmeta = TH1F("reco_gm_eta", "reco_gm_eta", 100, -6, 6)
hgmeta.Sumw2()

hgmteta = TH1F("reco_gm_trig_eta", "reco_gm_trig_eta", 100, -6, 6)
hgmteta.Sumw2()

hgmphi = TH1F("reco_gm_phi", "reco_gm_phi", 100, -3.7, 3.7)
hgmphi.Sumw2()

hgmtphi = TH1F("reco_gm_trig_phi", "reco_gm_trig_phi", 100, -3.7, 3.7)
hgmtphi.Sumw2()


hgmdxy = TH1F("reco_gm_dxy", "reco_gm_dxy", 100, -110, 110)
hgmdxy.Sumw2()

hgmtdxy = TH1F("reco_gm_trig_dxy", "reco_gm_trig_dxy", 100, -110, 110)
hgmtdxy.Sumw2()


ngmt = 0 # number of gm + trig fired

for event in mytree:
    trig_bitpos=19
    
    hat.Fill(mytree.trig_fired)

    if ((event.trig_fired >> trig_bitpos) & 1) == 1:
        trigfired.append(format(event.trig_fired,'b'))
        htf.Fill(mytree.trig_fired)


    if (len(mytree.reco_gm_pt)!=0):
        gmpt.append(mytree.reco_gm_pt[0])
        hgmpt.Fill(mytree.reco_gm_pt[0])
        hgmeta.Fill(mytree.reco_gm_eta[0])
        hgmphi.Fill(mytree.reco_gm_phi[0])
        hgmdxy.Fill(mytree.reco_gm_dxy[0])
        

        if ((event.trig_fired >> trig_bitpos) & 1) == 1:
            hgmtpt.Fill(mytree.reco_gm_pt[0])
            hgmteta.Fill(mytree.reco_gm_eta[0])
            hgmtphi.Fill(mytree.reco_gm_phi[0])
            hgmtdxy.Fill(mytree.reco_gm_dxy[0])
            ngmt +=1


print("\n", "N_trig=", len(trigfired),"; N_total=", nentry, "; eff =", (len(trigfired)/nentry)*100 ,"% \n" )

print("\n", "N_gm_trig=", ngmt,"; N_gm_total=", len(gmpt), "; eff =", (ngmt/len(gmpt))*100 ,"% \n" )

eff_pt = hgmtpt.Clone()
eff_pt.Divide(hgmpt)

eff_eta = hgmteta.Clone()
eff_eta.Divide(hgmeta)

eff_phi = hgmtphi.Clone()
eff_phi.Divide(hgmphi)

eff_dxy = hgmtdxy.Clone()
eff_dxy.Divide(hgmdxy)




#eff_pt.SetLineColor(ROOT.kRed)
nent=0
for i in range(eff_pt.GetSize()):
    ne_eff = eff_pt.GetBinContent(i)
    if ne_eff != 0: 
        nent += ne_eff
        print(i , " " , ne_eff)

print(nent)

hat.GetYaxis().SetTitle("Number of events")
hat.GetXaxis().SetTitle("Trigger fired ")
htf.GetYaxis().SetTitle("Number of events")
htf.GetXaxis().SetTitle("Trigger fired")
hgmpt.GetYaxis().SetTitle("Number of events")
hgmpt.GetXaxis().SetTitle("Leading gm pt")
hgmtpt.GetYaxis().SetTitle("Number of events")
hgmtpt.GetXaxis().SetTitle("Leading gm pt")
hgmeta.GetYaxis().SetTitle("Number of events")
hgmeta.GetXaxis().SetTitle("Leading gm eta")
hgmteta.GetYaxis().SetTitle("Number of events")
hgmteta.GetXaxis().SetTitle("Leading gm eta")
hgmphi.GetYaxis().SetTitle("Number of events")
hgmphi.GetXaxis().SetTitle("Leading gm phi")
hgmtphi.GetYaxis().SetTitle("Number of events")
hgmtphi.GetXaxis().SetTitle("Leading gm phi")
hgmdxy.GetYaxis().SetTitle("Number of events")
hgmdxy.GetXaxis().SetTitle("Leading gm dxy")
hgmtdxy.GetYaxis().SetTitle("Number of events")
hgmtdxy.GetXaxis().SetTitle("Leading gm dxy")


eff_pt.GetYaxis().SetTitle("Efficiency")
eff_pt.GetXaxis().SetTitle("Leading gm pt")
eff_eta.GetYaxis().SetTitle("Efficiency")
eff_eta.GetXaxis().SetTitle("Leading gm eta")
eff_phi.GetYaxis().SetTitle("Efficiency")
eff_phi.GetXaxis().SetTitle("Leading gm phi")
eff_dxy.GetYaxis().SetTitle("Efficiency")
eff_dxy.GetXaxis().SetTitle("Leading gm dxy")


c1.cd()
c1. SetLogy(True)

c1.Print(plotFileName+"[")

hat.Draw("h")
c1.Print(plotFileName)

htf.Draw("h")
c1.Print(plotFileName)

hgmpt.Draw("h")
c1.Print(plotFileName)

hgmtpt.Draw("h")
c1.Print(plotFileName)

c1.SetLogy(False)

eff_pt.Draw()
c1.Print(plotFileName)

hgmeta.Draw("h")
c1.Print(plotFileName)

hgmteta.Draw("h")
c1.Print(plotFileName)

eff_eta.Draw()
c1.Print(plotFileName)

hgmphi.Draw("h")
c1.Print(plotFileName)

hgmtphi.Draw("h")
c1.Print(plotFileName)

eff_phi.Draw()
c1.Print(plotFileName)

c1.SetLogy(True)

hgmdxy.Draw("h")
c1.Print(plotFileName)

hgmtdxy.Draw("h")
c1.Print(plotFileName)

c1.SetLogy(False)
eff_dxy.Draw()
c1.Print(plotFileName)

c1.Print(plotFileName+"]")



#print("\n")
#print("N_trig=", len(trigfire),"; N_total=", nentry, "; eff =", (len(trigfire)/nentry)*100 ,"% \n" )
#for i in range(0,len(trigfire)):
#   print(trigfire[i])



