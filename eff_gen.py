from logging.handlers import NTEventLogHandler
from ROOT import TCanvas, TFile, TProfile, TNtuple, TH1F, TH2F, TPad, TH1D
from ROOT import gROOT, gBenchmark, gRandom, gSystem, gStyle
from ROOT import TStyle, TF1, gDirectory, TTree, TBrowser, gMinuit, TText, TCut, TPaveText, TEfficiency 
import cppyy
from cppyy.gbl.std import vector, pair
import ctypes
import sys

if len (sys.argv) != 3:
    print (" USAGE : %s <input file > <output file >"%(sys.argv[0]))
    sys.exit (1)

#'Mchi-60p0_dMchi-20p0_ctau-1.root'
#"HLT_Mu3er1p5_PFJet100er2p5_PFMETNoMu100_PFMHTNoMu100_IDTight" -> alternative trigger : trig_bit position = 19
# main trigger : trig_bit positions: 3,4,5,7
# "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight" 
# "HLT_PFMETNoMu130_PFMHTNoMu130_IDTight"
# "HLT_PFMETNoMu140_PFMHTNoMu140_IDTight"
# "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60" 


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

hgen_mu_pt = TH1F("gen_mu_pt", "gen_mu_pt", 100, 0, 250) # pt generation level
hgen_mu_pt.Sumw2()

hgen_mu_t_pt = TH1F("gen_mu_pt", "gen_mu_pt & trigger", 100, 0, 250) # pt generation level & firing the trigger . 
hgen_mu_t_pt.Sumw2()


hgen_mu_eta = TH1F("gen_mu_eta", "gen_mu_eta", 100, -6, 6)
hgen_mu_eta.Sumw2()

hgen_mu_t_eta = TH1F("gen_mu_trig_eta", "gen_mu_trig_eta", 100, -6, 6)
hgen_mu_t_eta.Sumw2()

hgen_mu_phi = TH1F("gen_mu_phi", "gen_mu_phi", 100, -3.7, 3.7)
hgen_mu_phi.Sumw2()

hgen_mu_t_phi = TH1F("gen_mu_trig_phi", "gen_mu_trig_phi", 100, -3.7, 3.7)
hgen_mu_t_phi.Sumw2()

hgen_mu_vxy = TH1F("gen_mu_vxy", "gen_mu_vxy", 100, 0, 4)
hgen_mu_vxy.Sumw2()

hgen_mu_t_vxy = TH1F("gen_mu_trig_vxy", "gen_mu_trig_vxy", 100, 0, 4)
hgen_mu_t_vxy.Sumw2()

################# histos for leading particle among all gen particles 

hgen_pt = TH1F("gen_pt", "gen_pt", 100, 0, 1200) # pt generation level
hgen_pt.Sumw2()

hgen_t_pt = TH1F("gen_pt", "gen_pt & trigger", 100, 0, 1200) # pt generation level & firing the trigger . 
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

hgen_jet_pt = TH1F("gen_jet_pt", "gen_jet_pt", 100, 0, 1200) # pt generation level
hgen_jet_pt.Sumw2()

hgen_jet_t_pt = TH1F("gen_jet_pt", "gen_jet_pt & trigger", 100, 0, 1200) # pt generation level & firing the trigger . 
hgen_jet_t_pt.Sumw2()


hgen_jet_eta = TH1F("gen_jet_eta", "gen_jet_eta", 100, -6, 6)
hgen_jet_eta.Sumw2()

hgen_jet_t_eta = TH1F("gen_jet_trig_eta", "gen_jet_trig_eta", 100, -6, 6)
hgen_jet_t_eta.Sumw2()

hgen_jet_phi = TH1F("gen_jet_phi", "gen_jet_phi", 100, -3.7, 3.7)
hgen_jet_phi.Sumw2()

hgen_jet_t_phi = TH1F("gen_jet_trig_phi", "gen_jet_trig_phi", 100, -3.7, 3.7)
hgen_jet_t_phi.Sumw2()


hgen_met_pt = TH1F("gen_met_pt", "gen_met_pt", 100, 0, 1200) # pt generation level
hgen_met_pt.Sumw2()

hgen_met_t_pt = TH1F("gen_met_pt", "gen_met_pt & trigger", 100, 0, 1200) # pt generation level & firing the trigger . 
hgen_met_t_pt.Sumw2()

hgen_met_phi = TH1F("gen_met_phi", "gen_met_phi", 100, -3.7, 3.7) # pt generation level
hgen_met_phi.Sumw2()

hgen_met_t_phi = TH1F("gen_met_phi", "gen_met_phi & trigger", 100, -3.7, 3.7) # pt generation level & firing the trigger . 
hgen_met_t_phi.Sumw2()

##################
ngen =0 # number of generated events
ngent = 0 # number of gen + trig fired

nmugen=0   # number of events generated with muons
nmugent=0  # number of events generated with muons AND passing the trigger 

npargen = 0 
npartgent = 0

for event in mytree:
    trig_bitpos=19
    evl=len(event.gen_ID)
    ngen+=1
    genID = []
    genpt = []
    geneta = []
    genphi = []
    genvxy = []
    genjetpt =[]
    genjeteta = []
    genjetphi = []

    for id in event.gen_ID : genID.append(id)
    for pt in event.gen_pt : genpt.append(pt)
    for eta in event.gen_eta : geneta.append(eta)
    for phi in event.gen_phi : genphi.append(phi)
    for vxy in event.gen_vxy : genvxy.append(vxy)
    for jetpt in event.gen_jet_pt : genjetpt.append(jetpt) # gen jet pt is sorted by default so leading jet is jet_pt[0]. 
    for jeteta in event.gen_jet_eta : genjeteta.append(jeteta)
    for jetphi in event.gen_jet_phi : genjetphi.append(jetphi)

    ##### leading particle in the event

    idx= genpt.index(max(genpt)) # leading particle index in genpt list
    
    #print('-------')
    #print(event.gen_MET_pt)
    #print(genjeteta)
    
    hgen_jet_pt.Fill(genjetpt[0])
    hgen_jet_eta.Fill(genjeteta[0])
    hgen_jet_phi.Fill(genjetphi[0])

    hgen_pt.Fill(genpt[idx])
    hgen_eta.Fill(geneta[idx])
    hgen_phi.Fill(genphi[idx])

    hgen_met_pt.Fill(event.gen_MET_pt)
    hgen_met_phi.Fill(event.gen_MET_phi)


    if ((event.trig_fired >> trig_bitpos) & 1) == 1:
    #if ((event.trig_fired >> 3) & 1) == 1 or ((event.trig_fired >> 4) & 1) == 1 or ((event.trig_fired >> 5) & 1) == 1  or ((event.trig_fired >> 7) & 1) == 1:

        ngent+=1
        hgen_t_pt.Fill(genpt[idx])
        hgen_t_eta.Fill(geneta[idx])
        hgen_t_phi.Fill(genphi[idx])


        hgen_jet_t_pt.Fill(genjetpt[0])
        hgen_jet_t_eta.Fill(genjeteta[0])
        hgen_jet_t_phi.Fill(genjetphi[0])


        hgen_met_t_pt.Fill(event.gen_MET_pt)
        hgen_met_t_phi.Fill(event.gen_MET_phi)
        

    ######## select muons and find the leading one; filling histos for leading mouns     
    
    if -13 in event.gen_ID and 13 in event.gen_ID:
        nmugen+=1  # count events, denominator for trigger effeciency

        if event.gen_pt[evl-2] > event.gen_pt[evl-1]: 
            hgen_mu_pt.Fill(mytree.gen_pt[evl-2])
            hgen_mu_eta.Fill(mytree.gen_eta[evl-2])
            hgen_mu_phi.Fill(mytree.gen_phi[evl-2])
            hgen_mu_vxy.Fill(mytree.gen_vxy[evl-2])

            #print('leading pt (-13): ',event.gen_pt[evl-2] ,' compared to: ', event.gen_pt[evl-1])
        else:
            hgen_mu_pt.Fill(mytree.gen_pt[evl-1])
            hgen_mu_eta.Fill(mytree.gen_eta[evl-1])
            hgen_mu_phi.Fill(mytree.gen_phi[evl-1])
            hgen_mu_vxy.Fill(mytree.gen_vxy[evl-1])
    
            #print('leading pt (13): ',event.gen_pt[evl-1],' comp', event.gen_pt[evl-2])

        if ((event.trig_fired >> trig_bitpos) & 1) == 1:
        #if ((event.trig_fired >> 3) & 1) == 1 or ((event.trig_fired >> 4) & 1) == 1 or ((event.trig_fired >> 5) & 1) == 1  or ((event.trig_fired >> 7) & 1) == 1:
    
            nmugent +=1 # count events, numerator for trigger effeciency

            if event.gen_pt[evl-2] > event.gen_pt[evl-1]: 

                hgen_mu_t_pt.Fill(mytree.gen_pt[evl-2])
                hgen_mu_t_eta.Fill(mytree.gen_eta[evl-2])
                hgen_mu_t_phi.Fill(mytree.gen_phi[evl-2])
                hgen_mu_t_vxy.Fill(mytree.gen_vxy[evl-2])

                #print('leading pt (-13): ',event.gen_pt[evl-2] ,' compared to: ', event.gen_pt[evl-1])
            else:

                hgen_mu_t_pt.Fill(mytree.gen_pt[evl-1])
                hgen_mu_t_eta.Fill(mytree.gen_eta[evl-1])
                hgen_mu_t_phi.Fill(mytree.gen_phi[evl-1])
                hgen_mu_t_vxy.Fill(mytree.gen_vxy[evl-1])
                #print('leading pt (13): ',event.gen_pt[evl-1],' comp', event.gen_pt[evl-2])
    
    # end of gen muons

#print(ngen, '-', ngent)

print("\n", "efficiency for events selecting muons: N_trig = ",nmugent,"; N_total=", nmugen, ";\n eff =", (nmugent/nmugen)*100 ,"% \n" )
print("\n", "efficiency for all events: N_trig = ",ngent,"; N_total=", ngen, ";\n eff =", (ngent/ngen)*100 ,"% \n" )

Eff_gen_mu_pt = TEfficiency(hgen_mu_t_pt,hgen_mu_pt)
Eff_gen_mu_eta = TEfficiency(hgen_mu_t_eta,hgen_mu_eta)
Eff_gen_mu_phi = TEfficiency(hgen_mu_t_phi,hgen_mu_phi)
Eff_gen_mu_vxy = TEfficiency(hgen_mu_t_vxy,hgen_mu_vxy)

Eff_gen_pt = TEfficiency(hgen_t_pt,hgen_pt)
Eff_gen_eta = TEfficiency(hgen_t_eta,hgen_eta)
Eff_gen_phi = TEfficiency(hgen_t_phi,hgen_phi)

Eff_gen_jet_pt = TEfficiency(hgen_jet_t_pt,hgen_jet_pt)
Eff_gen_jet_eta = TEfficiency(hgen_jet_t_eta,hgen_jet_eta)
Eff_gen_jet_phi = TEfficiency(hgen_jet_t_phi,hgen_jet_phi)

Eff_gen_met_pt = TEfficiency(hgen_met_t_pt,hgen_met_pt)
Eff_gen_met_phi = TEfficiency(hgen_met_t_phi,hgen_met_phi)

hgen_mu_pt.GetYaxis().SetTitle("Number of events")
hgen_mu_pt.GetXaxis().SetTitle("leading muon_pt (gen)")
hgen_mu_t_pt.GetYaxis().SetTitle("Number of events")
hgen_mu_t_pt.GetXaxis().SetTitle("leading muon_pt (gen)")
hgen_mu_eta.GetYaxis().SetTitle("Number of events")
hgen_mu_eta.GetXaxis().SetTitle("leading muon_eta (gen)")
hgen_mu_t_eta.GetYaxis().SetTitle("Number of events")
hgen_mu_t_eta.GetXaxis().SetTitle("leading muon_eta (gen)")
hgen_mu_phi.GetYaxis().SetTitle("Number of events")
hgen_mu_phi.GetXaxis().SetTitle("leading muon_phi (gen)")
hgen_mu_t_phi.GetYaxis().SetTitle("Number of events")
hgen_mu_t_phi.GetXaxis().SetTitle("leading moun_phi (gen)")
hgen_mu_vxy.GetYaxis().SetTitle("Number of events")
hgen_mu_vxy.GetXaxis().SetTitle("leadig moun_vxy (gen)")
hgen_mu_t_vxy.GetYaxis().SetTitle("Number of events")
hgen_mu_t_vxy.GetXaxis().SetTitle("Leading moun_vxy (gen)")

Eff_gen_mu_pt.SetTitle("Efficiency;leading muon_pt (gen);#epsilon", )
Eff_gen_mu_eta.SetTitle("Efficiency;leading muon_eta (gen);#epsilon", )
Eff_gen_mu_phi.SetTitle("Efficiency;leading muon_phi (gen);#epsilon", )
Eff_gen_mu_vxy.SetTitle("Efficiency;leading muon_vxy (gen);#epsilon", )

############### plots for gen all 

hgen_pt.GetYaxis().SetTitle("Number of events")
hgen_pt.GetXaxis().SetTitle("leading part_pt (gen)")
hgen_t_pt.GetYaxis().SetTitle("Number of events")
hgen_t_pt.GetXaxis().SetTitle("leading part_pt (gen)")
hgen_eta.GetYaxis().SetTitle("Number of events")
hgen_eta.GetXaxis().SetTitle("leading part_eta (gen)")
hgen_t_eta.GetYaxis().SetTitle("Number of events")
hgen_t_eta.GetXaxis().SetTitle("leading part_eta (gen)")
hgen_phi.GetYaxis().SetTitle("Number of events")
hgen_phi.GetXaxis().SetTitle("leading part_phi (gen)")
hgen_t_phi.GetYaxis().SetTitle("Number of events")
hgen_t_phi.GetXaxis().SetTitle("leading part_phi (gen)")

hgen_jet_pt.GetYaxis().SetTitle("Number of events")
hgen_jet_pt.GetXaxis().SetTitle("leading jet_pt (gen)")
hgen_jet_t_pt.GetYaxis().SetTitle("Number of events")
hgen_jet_t_pt.GetXaxis().SetTitle("leading jet_pt (gen)")
hgen_jet_eta.GetYaxis().SetTitle("Number of events")
hgen_jet_eta.GetXaxis().SetTitle("leading jet_eta (gen)")
hgen_jet_t_eta.GetYaxis().SetTitle("Number of events")
hgen_jet_t_eta.GetXaxis().SetTitle("leading jet_eta (gen)")
hgen_jet_phi.GetYaxis().SetTitle("Number of events")
hgen_jet_phi.GetXaxis().SetTitle("leading jet_phi (gen)")
hgen_jet_t_phi.GetYaxis().SetTitle("Number of events")
hgen_jet_t_phi.GetXaxis().SetTitle("leading jet_phi (gen)")

hgen_met_pt.GetYaxis().SetTitle("Number of events")
hgen_met_pt.GetXaxis().SetTitle("met_pt (gen)")
hgen_met_t_pt.GetYaxis().SetTitle("Number of events")
hgen_met_t_pt.GetXaxis().SetTitle("met_pt (gen)")
hgen_met_phi.GetYaxis().SetTitle("Number of events")
hgen_met_phi.GetXaxis().SetTitle("met_phi (gen)")
hgen_met_t_phi.GetYaxis().SetTitle("Number of events")
hgen_met_t_phi.GetXaxis().SetTitle("met_phi (gen)")

Eff_gen_pt.SetTitle("Efficiency;leading part_pt (gen);#epsilon", )
Eff_gen_eta.SetTitle("Efficiency;leading part_eta (gen);#epsilon", )
Eff_gen_phi.SetTitle("Efficiency;leading part_phi (gen);#epsilon", )

Eff_gen_jet_pt.SetTitle("Efficiency;leading jet_pt (gen);#epsilon", )
Eff_gen_jet_eta.SetTitle("Efficiency;leading jet_eta (gen);#epsilon", )
Eff_gen_jet_phi.SetTitle("Efficiency;leading jet_phi (gen);#epsilon", )

Eff_gen_met_pt.SetTitle("Efficiency;met_pt (gen);#epsilon", )
Eff_gen_met_phi.SetTitle("Efficiency;met_phi (gen);#epsilon", )

###########

c1.cd()
c1. SetLogy(True)

c1.Print(plotFileName+"[")

#hgen_mu_pt.Draw("h")
#c1.Print(plotFileName)

#hgen_mu_t_pt.Draw("h")
#c1.Print(plotFileName)

c1.SetLogy(False)
Eff_gen_mu_pt.Draw()
c1.Print(plotFileName)

#hgen_mu_eta.Draw("h")
#c1.Print(plotFileName)

#hgen_mu_t_eta.Draw("h")
#c1.Print(plotFileName)

c1.SetLogy(False)
Eff_gen_mu_eta.Draw()
c1.Print(plotFileName)

#hgen_mu_phi.Draw("h")
#c1.Print(plotFileName)

#hgen_mu_t_phi.Draw("h")
#c1.Print(plotFileName)

c1.SetLogy(False)
Eff_gen_mu_phi.Draw()
c1.Print(plotFileName)

#c1.SetLogy(True)
#hgen_mu_vxy.Draw("h")
#c1.Print(plotFileName)

#hgen_mu_t_vxy.Draw("h")
#c1.Print(plotFileName)

c1.SetLogy(False)
Eff_gen_mu_vxy.Draw()
c1.Print(plotFileName)


#hgen_pt.Draw("h")
#c1.Print(plotFileName)

#hgen_t_pt.Draw("h")
#c1.Print(plotFileName)

c1.SetLogy(False)
Eff_gen_pt.Draw()
c1.Print(plotFileName)

#hgen_eta.Draw("h")
#c1.Print(plotFileName)

#hgen_t_eta.Draw("h")
#c1.Print(plotFileName)

c1.SetLogy(False)
Eff_gen_eta.Draw()
c1.Print(plotFileName)

#hgen_phi.Draw("h")
#c1.Print(plotFileName)

#hgen_t_phi.Draw("h")
#c1.Print(plotFileName)


c1.SetLogy(False)
Eff_gen_phi.Draw()
c1.Print(plotFileName)

#### jets

#hgen_jet_pt.Draw("h")
#c1.Print(plotFileName)

#hgen_jet_t_pt.Draw("h")
#c1.Print(plotFileName)

c1.SetLogy(False)
Eff_gen_jet_pt.Draw()
c1.Print(plotFileName)

#hgen_jet_eta.Draw("h")
#c1.Print(plotFileName)

#hgen_jet_t_eta.Draw("h")
#c1.Print(plotFileName)

c1.SetLogy(False)
Eff_gen_jet_eta.Draw()
c1.Print(plotFileName)

#hgen_jet_phi.Draw("h")
#c1.Print(plotFileName)

#hgen_jet_t_phi.Draw("h")
#c1.Print(plotFileName)

c1.SetLogy(False)
Eff_gen_jet_phi.Draw()
c1.Print(plotFileName)

#### MET

#hgen_met_pt.Draw("h")
#c1.Print(plotFileName)

#hgen_met_t_pt.Draw("h")
#c1.Print(plotFileName)

c1.SetLogy(False)
Eff_gen_met_pt.Draw()
c1.Print(plotFileName)

#hgen_met_phi.Draw("h")
#c1.Print(plotFileName)

#hgen_met_t_phi.Draw("h")
#c1.Print(plotFileName)

c1.SetLogy(False)
Eff_gen_met_phi.Draw()
c1.Print(plotFileName)

c1.Print(plotFileName+"]")