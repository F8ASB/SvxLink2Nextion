#!/usr/bin/env python
# -*- coding: utf-8 -*-
#F8ASB V1.10

#import serial
import configparser, os
import time # used by follow function
import sys

def follow(thefile):
    thefile.seek(0,2)      # Go to the end of the file
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)    # Sleep briefly
            continue
        yield line

#Fonction ecriture texte sur Nextion ex: ecrire(t0.txt,"hello word")
#def ecrire(champ,valeur):
#        eof = "\xff\xff\xff"
#        stringw = champ+'="'+valeur+'"' +eof
#        port.write(stringw)

#Fonction appel de page
#def page(nompage):
#        eof = "\xff\xff\xff"
#        appelpage = 'page '+nompage +eof
#        port.write(appelpage)
#        print appelpage

#Chemin log a suivre
svxlogfile = "/tmp/svxlink.log"   #SVXLink log file 
version="Version 1.00"
#LOGICS NAMES
StrSimplex = "SimplexLogic"                 # Identification of a Simplex Logic in Svxlink, by default = "SimplexLogic"
StrRepeater = "RepeaterLogic"               # Identification of a Repeater Logic in Svxlink, by default = "RepeaterLogic"
StrReflector = "ReflectorLogic"
#MODULES NAMES
StrHelp = "Help"                      # Identification of a Help Module in Svxlink, by default = "Help"
StrParrot = "Parrot"                  # Identification of a Parrot Module in Svxlink, by default = "Parrot"
StrEcholink = "EchoLink"              # Identification of a Echolink Module in Svxlink, by default = "EchoLink"
StrVoicemail = "TclVoiceMail"         # Identification of a Voicemail Module in Svxlink, by default = "TclVoiceMail"
StrMetarinfo = "MetarInfo"            # Identification of a Metar informations Module in Svxlink, by default = "MetarInfo"
StrDtmfrepeater = "DtmfRepeater"      # Identification of a DTMF Repeater Module in Svxlink, by default = "DtmfRepeater"
StrSelcallenc = "SelCallEnc"          # Identification of a Selective Call Encoder Module in Svxlink, by default = "SelCallEnc"
StrPropagation = "PropagationMonitor" # Identification of a Propagation information Module in Svxlink, by default = "PropagationMonitor"
timeinfo=""
trameecho=""
listecho =[]
decodeecho=False

i=0
logfile = open(svxlogfile)
loglines = follow(logfile)
print("++++++++++++++++++++++++++++++++++++")
print("+ SvxStatus by F8ASB: "+version+" +")
print("++++++++++++++++++++++++++++++++++++")

for line in loglines:
 #       print line
        if "transmitter ON" in line:
            print ("TX ON")
                
        elif "transmitter OFF" in line:
            print ("TX OFF")                                                               
        
        elif "Shutting down application" in line:
            print ("SHUTTING DOWN SVX")
                
        elif "tone call detected" in line:
            print ("TONE DETECTED")
                
        elif "Sending long identification" in line:
            print ("LONG BEACON")
                
        elif "Sending short identification." in line:
            print ("SHORT BEACON")
                
        elif "The squelch is OPEN (" in line:
            print ("SQUELCH OPEN")
                
        elif "The squelch is CLOSED (" in line:
            print ("SQUELCH CLOSED") 

        elif "EchoLink directory status changed to ON" in line:
            print ("Echolink ON")

        elif "server message:" in line:
            print ("CONNEXION ECHOLINK OK")

        elif "Activating module EchoLink" in line:
            print ("Module Echolink Actif")
            listecho =[]

        elif ": SvxLink 1.6.99.16" in line and len(line) < 60:
            print ("Incomming list detected")
            timeinfo= line.split(":")
            timeinfo= timeinfo[0]+":"+timeinfo[1]+":"+timeinfo[2]
            decodeecho=True
            
            
        elif timeinfo in line and len(line) > 30:
            trameecho=line.split(":")  
            filtre=trameecho[3].split(" ")
            callecho=((filtre)[1])
            #print(callecho)
            if callecho!=">"and decodeecho==True:
                listecho.append(callecho)
                #print(",".join(listecho))
        
        elif timeinfo in line and len(line) < 30 and decodeecho==True:
            if len(listecho) >1:
                print("Connected List: "+(",".join(listecho)))
                #print(",".join(listecho))
                decodeecho=False

        elif ">" in line:
            print ("info station")
            call= line.split(" ")
            #callseul=call.split(" ")
            print (call[6])

        # LOG LINES
        
        # Sun Mar 29 11:07:30 2020: Tx1: Turning the transmitter ON
        # Sun Mar 29 11:07:30 2020: --- EchoLink info message received from F1ZHH-R ---
        # Sun Mar 29 11:07:30 2020: SvxLink 1.6.99.16 - F1ZHH-R (8)
        # Sun Mar 29 11:07:30 2020:
        # Sun Mar 29 11:07:30 2020: F1ZHH-R         [FON Center + Reflector - Connectez vous ici pour le FON]
        # Sun Mar 29 11:07:30 2020: F4EVC-L         [430.950MHz Tone 233.6Hz] Metz (57)
        # Sun Mar 29 11:07:30 2020: F6GUZ-L         FON_Dept37/145.3375 Mhz Tcs 123 Hz
        # Sun Mar 29 11:07:30 2020: F5PBG-L         (29)145.3375MHz-71.9Hz Brest
        # Sun Mar 29 11:07:30 2020: F0EOC-L         Martial
        # Sun Mar 29 11:07:30 2020: F4VTG-L         145.2875-T88.5
        # Sun Mar 29 11:07:30 2020: F4ENC-L         [Svx]Centre Montaigu (85) 144.3375 (betatest) Mhz CTCSS 67Hz ^_^ f4enc[at]gmx[dot]fr
        # Sun Mar 29 11:07:30 2020: F4HXP         Michel
        # Sun Mar 29 11:07:30 2020: F5SWB-L         MyName
        # Sun Mar 29 11:07:30 2020:
        # Sun Mar 29 11:07:33 2020: Tx1: Turning the transmitter OFF
        #Sun Mar 29 15:13:57 2020: SvxLink 1.6.99.16 - LZ0BOT-R
        #ReflectorLogic: Connected nodes: BAVARDAGE, (51) F5ZRI V, (88) F8ASB H


        elif StrReflector+": Talker stop: " in line:
            callsign= line.split(":")
            print ("talker stop:"+callsign[5])

        elif StrReflector+": Talker start: " in line:
            callsign= line.split(":")
            print ("talker start:"+callsign[5])
        
        elif StrReflector+": Node joined: " in line:
            callsign= line.split(":")
            print ("Out station :"+callsign[5])

        elif StrReflector+": Node left: " in line:
            callsign= line.split(":")
            print ("Incomming station :"+callsign[5])
        
        elif StrReflector+": Connected nodes: " in line:
            callsign= line.split(":")
            print ("List station :"+callsign[5])

        

        elif StrRepeater+": Activating module " + StrParrot  in line:
            print (StrParrot+ " module activated on "+StrRepeater)
                    

        elif StrRepeater+": Deactivating module " + StrParrot  in line:
            print (StrParrot+" module desactivated on "+StrRepeater)


        elif StrRepeater+": Activating module " + StrHelp  in line:
            print (StrHelp+" module activated on "+StrRepeater)
                    

        elif StrRepeater+": Deactivating module " + StrHelp  in line:
            print (StrHelp+" module desactivated on "+StrRepeater)
                

        elif StrRepeater+": Activating module " + StrEcholink  in line:
            print (StrEcholink+" module activated on "+StrRepeater)
                   

        elif StrRepeater+": Deactivating module " + StrEcholink in line:
            print (StrEcholink+" module desactivated on "+StrRepeater)
                                

        elif StrRepeater+": Activating module " + StrMetarinfo  in line:
            print (StrMetarinfo+" module activated on "+StrRepeater)                    

        elif StrRepeater+": Deactivating module " + StrMetarinfo in line:
            print (StrMetarinfo+" module desactivated on "+StrRepeater)

        elif StrRepeater+": Activating module " + StrVoicemail  in line:
            print (StrVoicemail+" module activated on "+StrRepeater)

        elif StrRepeater+": Deactivating module " + StrVoicemail in line:
            print (StrVoicemail+" module desactivated on "+StrRepeater)
            rep_mod_voicemail = 0         

        elif StrRepeater+": Activating module " + StrDtmfrepeater  in line:
            print (StrDtmfrepeater+" module activated on "+StrRepeater)
            rep_mod_dtmf = 1    

        elif StrRepeater+": Deactivating module " + StrDtmfrepeater in line:
            print (StrDtmfrepeater+" module desactivated on "+StrRepeater)
            rep_mod_dtmf = 0    

        elif StrRepeater+": Activating module " + StrSelcallenc in line:
            print (StrSelcallenc+" module activated on "+StrRepeater)
            rep_mod_selcall= 1    

        elif StrRepeater+": Deactivating module " + StrSelcallenc in line:
            print (StrSelcallenc+" module desactivated on "+StrRepeater)
            rep_mod_selcall = 0    

        elif StrRepeater+": Activating module " + StrPropagation in line:
            print (StrPropagation+" module activated on "+StrRepeater)
            rep_mod_propag= 1    

        elif StrRepeater+": Deactivating module " + StrPropagation in line:
            print (StrPropagation+" module desactivated on "+StrRepeater)
            rep_recoder = 0    

        elif StrRepeater+": Activating QSO recorder" in line:
            print ("QSO recorder activated on "+StrRepeater)
            rep_recoder= 1    

        elif StrRepeater+": Deactivating QSO recorder" in line:
            print ("QSO recorder module desactivated on "+StrRepeater)
            rep_mod_propag = 0    

        elif StrSimplex+": Activating module " + StrParrot  in line:
            print (StrParrot+ " module activated on "+StrSimplex)
            sim_mod_parrot = 1    

        elif StrSimplex+": Deactivating module " + StrParrot  in line:
            print (StrParrot+" module desactivated on "+StrSimplex)
            sim_mod_parrot = 0

        elif StrSimplex+": Activating module " + StrHelp  in line:
            print (StrHelp+" module activated on "+StrSimplex)
            sim_mod_help = 1    

        elif StrSimplex+": Deactivating module " + StrHelp  in line:
            print (StrHelp+" module desactivated on "+StrSimplex)
            sim_mod_help = 0

        elif StrSimplex+": Activating module " + StrEcholink  in line:
            print (StrEcholink+" module activated on "+StrSimplex)
            sim_mod_echolink = 1    

        elif StrSimplex+": Deactivating module " + StrEcholink in line:
            print (StrEcholink+" module desactivated on "+StrSimplex)
            sim_mod_echolink = 0                

        elif StrSimplex+": Activating module " + StrMetarinfo  in line:
            print (StrMetarinfo+" module activated on "+StrSimplex)
            sim_mod_metar = 1    

        elif StrSimplex+": Deactivating module " + StrMetarinfo in line:
            print (StrMetarinfo+" module desactivated on "+StrSimplex)
            sim_mod_metar = 0     

        elif StrSimplex+": Activating module " + StrVoicemail  in line:
            print (StrVoicemail+" module activated on "+StrSimplex)
            sim_mod_voicemail = 1    

        elif StrSimplex+": Deactivating module " + StrVoicemail in line:
            print (StrVoicemail+" module desactivated on "+StrSimplex)
            sim_mod_voicemail = 0         

        elif StrSimplex+": Activating module " + StrDtmfrepeater  in line:
            print (StrDtmfrepeater+" module activated on "+StrSimplex)
            sim_mod_dtmf = 1    

        elif StrSimplex+": Deactivating module " + StrDtmfrepeater in line:
            print (StrDtmfrepeater+" module desactivated on "+StrSimplex)
            sim_mod_dtmf = 0    

        elif StrSimplex+": Activating module " + StrSelcallenc in line:
            print (StrSelcallenc+" module activated on "+StrSimplex)
            sim_mod_selcall= 1    

        elif StrSimplex+": Deactivating module " + StrSelcallenc in line:
            print (StrSelcallenc+" module desactivated on "+StrSimplex)
            sim_mod_selcall = 0    

        elif StrSimplex+": Activating module " + StrPropagation in line:
            print (StrPropagation+" module activated on "+StrSimplex)
            sim_mod_propag= 1    

        elif StrSimplex+": Deactivating module " + StrPropagation in line:
            print (StrPropagation+" module desactivated on "+StrSimplex)
            sim_mod_propag = 0    

        elif StrSimplex+": Activating QSO recorder" in line:
            print ("QSO recorder activated on "+StrSimplex)
            sim_recoder= 1    

        elif StrSimplex+": Deactivating QSO recorder" in line:
            print ("QSO recorder module desactivated on "+StrSimplex)
            sim_recoder = 0                 

        elif "EchoLink QSO state changed to CONNECTED" in line:
           #voir pour *ECHOTEST*
            ch =  line.split(':')
            Last_Echolink_station = ch[3]
           # Echok_Station_conn = 1
            print ("STATION ECHOLINK CONNECTED: "+Last_Echolink_station[1:])
            
    
        elif "EchoLink QSO state changed to DISCONNECTED" in line:
           # Echok_Station_conn = 0
            print ("STATION DECONNECTEE")
              
        # Check if process svxlink is running
        #if check_svxlink() == 1 :
        #    svxrun = 1
        #else :
        #    svxrun = 0
