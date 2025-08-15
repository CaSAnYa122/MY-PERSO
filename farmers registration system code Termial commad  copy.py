import sqlite3
import hashlib
import csv
import os
import re

#Fungua au tengeneza database
def fungua_uhifadhi():
    return sqlite3.connect('godauni.db')

#Kutengeneza jedwali la watumiaji
def tengeneza_jedwali_watumiaji():
    conn=fungua_uhifadhi()
    cursor=conn.cursor()
    cursor.execute('''
     CREATE TABLE IF NOT EXISTS watumiaji(
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         jina TEXT NOT NULL,
         nywila TEXT NOT NULL
        )
         ''')
    conn.commit()
    conn.close
     
#Hatua ya 1: kutengeneza jedwali la wakulima kama halipo
def tengeneza_jedwali():
    conn=fungua_uhifadhi()
    cursor=conn.cursor()
    cursor.execute('''
     CREATE TABLE IF NOT EXISTS wakulima(
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         jina TEXT NOT NULL,umri INTEGER,
         jinsia TEXT,
         zao TEXT,
         idadi_weka INTEGER,
         tarehe_kuweka TEXT,
         tarehe_kutoa TEXT,
         idadi_baki INTEGER
         )
        ''')
                   
    conn.commit()
    conn.close()


#Validation ya jina
def validate_jina(jina):
    return len(jina)>=3

#Validation ya nywila(iwe nambari 4 tu)
def validate_nywila(nywila):
    return nywila.isdigit() and len(nywila)==4
#Validation ya tarehe
def validate_tarehe(tarehe):
    return re.match(r"\d{4}-\d{2}-\d{2}",tarehe)


#Kusajili watumiaji kwa validation
def sajili_mtumiaji():
    jina=input("Ingiza jina la mtumiaji(kuanzia herufi 3):")
    if not validate_jina(jina):
        print("jina la mtumiaji lazima liwe na angalau herufi 3!")
        return
    nywila=input("Ingiza nywila(nambari 4 pekee):")
    if not validate_nywila(nywila):
        print("nywila lazima iwe na nambari 4 pekee!")
        return

    hashed_nywila=hashlib.sha256(nywila.encode()).hexdigest()
    
    conn=fungua_uhifadhi()
    cursor=conn.cursor()
    cursor.execute('''INSERT INTO watumiaji(jina,nywila)
                       VALUES(?,?)''',(jina,hashed_nywila))

    conn.commit()
    conn.close()
    print("\nMtumiaji amesajiliwa kikamilifu!\n")


#Kuingia kwenye mfumo
def ingia():
    jina=input("Ingiza jina la mtumiaji:")
    nywila=input("Ingiza nywila:")

    hashed_nywila=hashlib.sha256(nywila.encode()).hexdigest()

    conn=fungua_uhifadhi()
    cursor=conn.cursor()
    cursor.execute('''SELECT*FROM
                 watumiaji WHERE jina=? AND nywila=?''',(jina,hashed_nywila))
    mtumiaji=cursor.fetchone()
    conn.close()

    if mtumiaji:
        print(f"\nKaribu {jina} umefanikiwa kuingia.\n")
        menyu_kuu()
    else:
        print("\nJina la mtumiaji au nywila si sahihi!\n")

#Hatua ya 2:kusajili mkulima mpya kwa validation
def sajili_mkulima():
    jina=input("Ingiza jina la mkulima(angalau herufi 3):")
    if not validate_jina(jina):
        print("Jina la mkulima lazima liwe na angalau herufi 3!")
        return
    
    umri=int(input("ingiza umri wa mkulima:"))
    jinsia=input("Ingiza jinsia (mwanaume/mwanamke):")
    zao=input("ingiza aina ya zao:")
    idadi_weka=int(input("ingiza idadi iliyowekwa(GUNIA):")) 
    tarehe_kuweka=input("ingiza tarehe ya kuweka(YYYY-MM-DD):")
    if not validate_tarehe(tarehe_kuweka):
        print("Tarehe lazima iwe katika muundo(YYYY-MM-DD)!")
        return
    tarehe_kutoa=input("ingiza tarehe ya kutoa(YYYY-MM-DD):")
    if not validate_tarehe(tarehe_kutoa):
        print("Tarehe lazima iwe katika muundo(YYYY-MM-DD):")
    idadi_baki=int(input("ingiza idadi iliyobaki(GUNIA):"))

    conn=fungua_uhifadhi()
    cursor=conn.cursor()
    cursor.execute('''
      INSERT INTO wakulima(jina,umri,jinsia,zao,
    idadi_weka,tarehe_kuweka,tarehe_kutoa,
    idadi_baki)
        VALUES(?,?,?,?,?,?,?,?)
      ''',(jina,umri,jinsia,zao,idadi_weka,tarehe_kuweka,
           tarehe_kutoa,idadi_baki))

    conn.commit()
    conn.close()
    print("\nMKULIMA AMESAJILWA KIKAMILIFU!\n")

#Hatua ya 3 :Kuonyesha wakulima wote
def onyesha_wakulima():
    conn=fungua_uhifadhi()
    cursor=conn.cursor()
    cursor.execute('SELECT*FROM wakulima')
    wakulima=cursor.fetchall()
    if not wakulima:
        print("Hakuna mkulima aliyesajiliwa bado.\n")
    else:
        for m in wakulima:
            print(f"\nID:{m[0]}\njina:{m[1]}\numri:{m[2]}\njinsia:{m[3]}\nzao:{m[4]}\n"
                  f"idadi_weka:{m[5]}\ntarehe_weka:{m[6]}\ntarehe_kutoa:{m[7]}\nidadi_baki:{m[8]}")
    conn.close

#Htua ya 4:Kusasisha taarifa za mkulima
def sasisha_mkulima():
    id=int(input("Weka ID ya mkulima unayetaka kusasisha:"))
    jina=input("Ingiza jina jipya la mkulima:")
    umri=int(input("ingiza umri mpya wa mkulima:"))
    jinsia=input("Ingiza jinsia mpya (mwanaume/mwanamke):")
    zao=input("ingiza aina mpya ya zao:")
    idadi_weka=int(input("ingiza idadi mpya iliyowekwa:")) 
    tarehe_kuweka=input("ingiza tarehe mpya ya kuweka(YYYY-MM-DD):")
    tarehe_kutoa=input("ingiza tarehe mpya ya kutoa(YYYY-MM-DD):")
    idadi_baki=int(input("ingiza idadi mpya iliyobaki:"))

    conn=fungua_uhifadhi()
    cursor=conn.cursor()
    cursor.execute('''
      UPDATE wakulima SET jina=?,umri=?,jinsia=?,zao=?,
      idadi_weka=?,tarehe_kuweka=?,tarehe_kutoa=?,idadi_baki=?,
      WHERE id=?
      ''',(jina,umri,jinsia,zao,idadi_weka,tarehe_kuweka,tarehe_kutoa,idadi_baki,id))

    conn.commit()
    conn.close()
    print("Taarifa zimesasishwa vizuri!\n")
#Hatua ya 5:Kufuta mkulima
def futa_mkulima():
    id=int(input("Weka ID ya mkulima unayetaka kufuta:"))
    conn=fungua_uhifadhi()
    cursor=conn.cursor()
    cursor.execute('DELETE FROM wakulima WHERE id=?',(id))
    conn.commit()
    conn.close()
    print("Mkulima amefutwa!\n")


#Hatua ya 6:Kutafuta mkulima kwa jina
def tafuta_mkulima():
    jina=input("Ingiza jina la mkulima kutafuta:")
    conn=fungua_uhifadhi()
    cursor=conn.cursor()
    cursor.execute("SELECT*FROM wakulima WHERE jina=?",(jina,))
    mkulima=cursor.fetchone()
    if mkulima:
        print(f"\nID: {mkulima[0]}")
        print(f"\njina: {mkulima[1]}")
        print(f"\numri: {mkulima[2]}")
        print(f"\njinsia: {mkulima[3]}")
        print(f"\nzao: {mkulima[4]}")
        print(f"\nidadi iliyoletwa: {mkulima[5]}")
        print(f"\ntarehe ya kuweka: {mkulima[6]}")
        print(f"\ntarehe ya kutoa: {mkulima[7]}")
        print(f"\nidadi iliyobaki: {mkulima[8]}\n")
    else:
        print("Hakuna mkulima mwenye jina hilo.")

    conn.close()


#Hatua ya 7:Kutoa ripoti
def toa_ripoti_CSV():
    conn=sqlite3.connect("godauni.db")
    cursor=conn.cursor()
    cursor.execute("SELECT*FROM wakulima")
    data=cursor.fetchall()
    jina_faili="Wakulima_report.CSV"
    with open(jina_faili,mode="w",newline='',encoding="utf-8") as file:
        writer=csv.writer(file)
        writer.writerow(["ID","jina","umri","jinsia","zao","idadi iliyowekwa",
                         "tarehe ya kuweka","tarehe ya kutoa","idadi iliyobaki"])
        for mkulima in data:
            writer.writerow(mkulima)
            
    conn.close()
    
    print(f"\nRipoti imetolewa kwenye faili:{jina_faili}")


#Hatua ya 8:Kutoa ripoti ya jumla ya gunia na idadi
def ripoti_ya_jumla():
    conn=sqlite3.connect("godauni.db")
    cursor=conn.cursor()
    cursor.execute("SELECT COUNT(*)FROM wakulima")
    jumla_wakulima=cursor.fetchone()[0]
    cursor.execute("SELECT SUM(idadi_weka)FROM wakulima")
    jumla_weka=cursor.fetchone()[0]or 0
    cursor.execute("SELECT SUM(idadi_baki)FROM wakulima")
    jumla_baki=cursor.fetchone()[0]or 0
    jumla_chukuliwa=jumla_weka-jumla_baki
    cursor.execute("SELECT DISTINCT zao FROM wakulima")
    mazao_tofauti=cursor.fetchall()
    orodha_mazao=[zao[0] for zao in mazao_tofauti]

    conn.close()

    print("\n=====RIPOTI YA JUMLA YA GODAUNI=====")
    print(f"idadi ya wakulima:{jumla_wakulima}")
    print(f"jumla ya gunia zilizowekwa:{jumla_weka}")
    print(f"jumla ya gunia zilizochukuliwa:{jumla_chukuliwa}")
    print(f"gunia zilizobaki:{jumla_baki}")
    print(f"aina za mazao:{','.join(orodha_mazao)}")
        
         
        
#Menyu kuu ya kuchagua
def menyu_kuu():
    tengeneza_jedwali()
    while True:
        print("\n=========MFUMO WA USAJILI WA WAKULIMA=========")
        print("1.Sajili mkulima mpya")
        print("2.0nyesha wakulima wote")
        print("3.Sasisha taarifa za mkulima")
        print("4.Futa mkulima")
        print("5.Toka")
        print("6.Tafuta mkulima kwa jina")
        print("7.Toa ripoti ya wakulima (csv)")
        print("8.Ripoti ya jumla ya godauni\n")
        chaguo=input("chagua(1-8):")

        if chaguo=="1":
            sajili_mkulima()
        elif chaguo=="2":
            onyesha_wakulima()
        elif chaguo=="3":
            sasisha_mkulima()
        elif chaguo=="4":
            futa_mkulima()
        elif chaguo=="5":
            print("<<<ASANTE KWA KUTUMIA MFUMO HUU!>>>")
            break
        elif chaguo=="6":
            tafuta_mkulima()
        elif chaguo=="7":
            toa_ripoti_CSV()
        elif chaguo=="8":
            ripoti_ya_jumla()
        else:
            print("Tafadhali chagua namba sahihi(1-8).")

#Menyu ya uthibitisho wa watumiaji
def menyu_uthibitisho():
    tengeneza_jedwali_watumiaji()
    while True:
        print("\n========MFUMO WA UTHIBITISHO=========")
        print("1.JISajili(mtumiaji mpya)")
        print("2.ingia kwenye mfumo")
        print("3.Toka")

        chaguo=input("\nChagua(1-3):")

        if chaguo=="1":
            sajili_mtumiaji()
        elif chaguo=="2":
            ingia()
        elif chaguo=="3":
            print("Asante kwa kutumia mfumo huu!")
            break
        else:
            print("Tafadhali chagua namba sahihi(1-3).")


#Anzisha program
menyu_uthibitisho()
            
         
        
    
    
    
    
    
     
    
    
    
                    
             
                   
                   
