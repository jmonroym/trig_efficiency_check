from logging.handlers import NTEventLogHandler
from ROOT import TCanvas, TFile, TProfile, TNtuple, TH1F, TH2F, TPad, TH1D
from ROOT import gROOT, gBenchmark, gRandom, gSystem, gStyle
from ROOT import TStyle, TF1, gDirectory, TTree, TBrowser, gMinuit, TText, TCut, TPaveText
import cppyy
from cppyy.gbl.std import vector, pair
import ctypes
import sys

if len (sys.argv) != 3:
    print (" USAGE : %s <input file > <output file >"%(sys.argv[0]))
    sys.exit (1)

#'Mchi-60p0_dMchi-20p0_ctau-1.root'

FileName = sys.argv[1]
plotFileName = sys.argv[2]
print(" Reading from ", FileName , "and writing to", plotFileName)


f = TFile.Open(FileName, "READ")
mytree=f.Get('ntuples_gbm/genT')
myfriendtree = f.Get('ntuples_gbm/recoT')
mytree.AddFriend(myfriendtree)

nentry = mytree.GetEntries()
mentry = myfriendtree.GetEntries()
trigfired=[] # triggers fired   
pt=[]  # pt[0] : leading gen pt


c1 = TCanvas('c1','The Ntuple canvas',200,10,700,780)
#c2 = TCanvas('c2','The Ntuple canvas',200,10,700,780)
#c3 = TCanvas('c3','The Ntuple canvas',200,10,700,780)
#c4 = TCanvas('c4','The Ntuple canvas',200,10,700,780)

hgen_pt = TH1F("gen_pt", "gen_pt", 100, 0, 250) # pt generation level
hgen_pt.Sumw2()

hgen_t_pt = TH1F("gen_pt", "gen_pt & trigger", 100, 0, 250) # pt generation level & firing the trigger . 
hgen_t_pt.Sumw2()


hgen_eta = TH1F("gen_eta", "gen_eta", 100, -6, 6)
hgen_eta.Sumw2()

hgen_t_eta = TH1F("gen_trig_eta", "gen_trig_eta", 100, -6, 6)
hgen_t_eta.Sumw2()

hgen_phi = TH1F("gen_phi", "gen_phi", 100, -3.7, 3.7)
hgen_phi.Sumw2()

hgen_t_phi = TH1F("gen_trig_phi", "gen_trig_phi", 100, -3.7, 3.7)
hgen_t_phi.Sumw2()

hgen_vxy = TH1F("gen_vxy", "gen_vxy", 100, 0, 4)
hgen_vxy.Sumw2()

hgen_t_vxy = TH1F("gen_trig_vxy", "gen_trig_vxy", 100, 0, 4)
hgen_t_vxy.Sumw2()


ngent = 0 # number of gen + trig fired

ngen=0 # number of events generated 
ngent=0  #number of events generated AND passing the trigger 

for event in mytree:
    trig_bitpos=19
    evl=len(event.gen_ID)

    if -13 in event.gen_ID and 13 in event.gen_ID:
        ngen+=1  # count events, denominator for trigger effeciency

        if event.gen_pt[evl-2] > event.gen_pt[evl-1]: 
            hgen_pt.Fill(mytree.gen_pt[evl-2])
            hgen_eta.Fill(mytree.gen_eta[evl-2])
            hgen_phi.Fill(mytree.gen_phi[evl-2])
            hgen_vxy.Fill(mytree.gen_vxy[evl-2])

            print('leading pt (-13): ',event.gen_pt[evl-2] ,' compared to: ', event.gen_pt[evl-1])
        else:
            hgen_pt.Fill(mytree.gen_pt[evl-1])
            hgen_eta.Fill(mytree.gen_eta[evl-1])
            hgen_phi.Fill(mytree.gen_phi[evl-1])
            hgen_vxy.Fill(mytree.gen_vxy[evl-1])
            print('leading pt (13): ',event.gen_pt[evl-1],' comp', event.gen_pt[evl-2])

        if ((event.trig_fired >> trig_bitpos) & 1) == 1:

            ngent +=1 # count events, numeraator for trigger effeciency

            if event.gen_pt[evl-2] > event.gen_pt[evl-1]: 

                hgen_t_pt.Fill(mytree.gen_pt[evl-2])
                hgen_t_eta.Fill(mytree.gen_eta[evl-2])
                hgen_t_phi.Fill(mytree.gen_phi[evl-2])
                hgen_t_vxy.Fill(mytree.gen_vxy[evl-2])

                print('leading pt (-13): ',event.gen_pt[evl-2] ,' compared to: ', event.gen_pt[evl-1])
            else:

                hgen_t_pt.Fill(mytree.gen_pt[evl-1])
                hgen_t_eta.Fill(mytree.gen_eta[evl-1])
                hgen_t_phi.Fill(mytree.gen_phi[evl-1])
                hgen_t_vxy.Fill(mytree.gen_vxy[evl-1])
                print('leading pt (13): ',event.gen_pt[evl-1],' comp', event.gen_pt[evl-2])


#print(ngen, '-', ngent)


print("\n", "N_trig = ",ngent,"; N_total=", ngen, "; eff =", (ngent/ngen)*100 ,"% \n" )

eff_pt = hgen_t_pt.Clone()
eff_pt.Divide(hgen_pt)

eff_eta = hgen_t_eta.Clone()
eff_eta.Divide(hgen_eta)

eff_phi = hgen_t_phi.Clone()
eff_phi.Divide(hgen_phi)

eff_vxy = hgen_t_vxy.Clone()
eff_vxy.Divide(hgen_vxy)

#eff_pt.SetLineColor(ROOT.kRed)
nent=0
for i in range(eff_pt.GetSize()):
    ne_eff = eff_pt.GetBinContent(i)
    if ne_eff != 0: 
        nent += ne_eff
#        print(i , " " , ne_eff)

#print(nent)

hgen_pt.GetYaxis().SetTitle("Number of events")
hgen_pt.GetXaxis().SetTitle("gen_pt")
hgen_t_pt.GetYaxis().SetTitle("Number of events")
hgen_t_pt.GetXaxis().SetTitle("gen_pt")
hgen_eta.GetYaxis().SetTitle("Number of events")
hgen_eta.GetXaxis().SetTitle("gen_eta")
hgen_t_eta.GetYaxis().SetTitle("Number of events")
hgen_t_eta.GetXaxis().SetTitle("gen_eta")
hgen_phi.GetYaxis().SetTitle("Number of events")
hgen_phi.GetXaxis().SetTitle("gen_phi")
hgen_t_phi.GetYaxis().SetTitle("Number of events")
hgen_t_phi.GetXaxis().SetTitle("gen_phi")
hgen_vxy.GetYaxis().SetTitle("Number of events")
hgen_vxy.GetXaxis().SetTitle("gen_vxy")
hgen_t_vxy.GetYaxis().SetTitle("Number of events")
hgen_t_vxy.GetXaxis().SetTitle("gen_vxy")


eff_pt.GetYaxis().SetTitle("Efficiency")
eff_pt.GetXaxis().SetTitle("gen_pt")
eff_eta.GetYaxis().SetTitle("Efficiency")
eff_eta.GetXaxis().SetTitle("gen_eta")
eff_phi.GetYaxis().SetTitle("Efficiency")
eff_phi.GetXaxis().SetTitle("gen_phi")
eff_vxy.GetYaxis().SetTitle("Efficiency")
eff_vxy.GetXaxis().SetTitle("gen_vxy")


c1.cd()
c1. SetLogy(True)

c1.Print(plotFileName+"[")

hgen_pt.Draw("h")
c1.Print(plotFileName)

hgen_t_pt.Draw("h")
c1.Print(plotFileName)

c1.SetLogy(False)

eff_pt.Draw()
c1.Print(plotFileName)

hgen_eta.Draw("h")
c1.Print(plotFileName)

hgen_t_eta.Draw("h")
c1.Print(plotFileName)

eff_eta.Draw()
c1.Print(plotFileName)

hgen_phi.Draw("h")
c1.Print(plotFileName)

hgen_t_phi.Draw("h")
c1.Print(plotFileName)

eff_phi.Draw()
c1.Print(plotFileName)

c1.SetLogy(True)

hgen_vxy.Draw("h")
c1.Print(plotFileName)

hgen_t_vxy.Draw("h")
c1.Print(plotFileName)

c1.SetLogy(False)
eff_vxy.Draw()
c1.Print(plotFileName)

c1.Print(plotFileName+"]")
