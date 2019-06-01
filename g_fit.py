import os
import math
import pandas as pd
def arvuta(tabel):
    andmed = pd.Series([tabel['Keskmine kiirus (m/s)'].mean()*3.6, tabel['Sammuloend'].sum()]).tolist()
    #loon uue järjendi, kuhu arvutatakse vastavalt esimesele ja teisele kohale keskmiste kiiruste keskmine (km/h) ja sammude summa
    if math.isnan(float(andmed[0])): #juhul, kui tabli veerg on vähese aktiivsuse tõttu tühi
        andmed[0] = 0
    if math.isnan(float(andmed[1])):
        andmed[1] = 0
    return andmed #tagastan arvutatud andmed

def analyys(fail):
    andmed = [0,0] #järjend, kuhu kõikide failide andmed kokku summeeritakse
    p = 0 #peab meeles, mille järgi hiljem keskmist arvutada
    for i in range(1,32): #kuus on kuni 31 päeva
        if i < 10:
            fail = fail[:-6]+str(0)+str(i)+".csv" #kohandan failinime vaadeldavale failile kohaseks; tagab olenemata sisestatud failinimest kuu kõigi failide töötlemise
        else:
            fail = fail[:-6]+str(i)+".csv" #alates 10. kuupäevast ei ole enam vaja failinimes 0-ga kuupäevas arvestada
        if os.path.isfile(fail): #kontrollin, kas fail eksisteerib - vajalik, et eristada 29, 30 ja 31 päevaseid võimalikke analüüsitavaid kuid või poolikuid kuid
            tabel = pd.read_csv(fail, delimiter=',') #loen failist andmed eraldusmärgiga ","
            tabeli_andmed = arvuta(tabel) #töötlen tabelit teises funktsioonis
            andmed[0] += tabeli_andmed[0] #summeerin töötlemisel saadud kesmised kiirused
            andmed[1] += tabeli_andmed[1] #summeerin töötlemisel saadud sammud
            p = i
    tulemus = "Keskmine keskmiste kiiruste kiirus " + fail[-14:-10]+". aasta " + fail[-8:-7] + ". kuul oli " + str(round(andmed[0]/p,2)) + " km/h ja kokku astuti " + str(int(andmed[1])) + " sammu, mis teeb päeva keskmiseks " + str(round(andmed[1]/p,2)) + " sammu."
    #koostan tulemuslause, ümardan keskmised kaks kohta peale koma ja teen sammude summa täisarvuks; aasta ja kuu võetakse failinime lõpust lugema hakates vastavatelt kohtadelt,
    #et tagada funktsionaalsus ka juhul, kui programm ja analüüsitavad failid ei asu samas kaustas
    return tulemus #tagastan tulemuslause

fail = input("Sisestage üks analüüsitava kuu kuupäeva failinimi (vajadusel koos kohaviidetega). Näiteks: ./2018-03/2018-03-01.csv: ") #küsin kasutajalt ühte kuu failinime
tulemus = analyys(fail) #edastan töötlemiseks funktsiooni
print(tulemus) #väljastan tulemuse

eraldi = input("Kas kirjutan tulemuse ka eraldi tekstifaili ("+fail[-14:-7] + "_tulemused.txt)? \nJah/Ei: ") #küsin kasutajalt, kas kirjutada tulemuslause eraldi faili
if eraldi.upper() == "JAH":
    file = open(fail[-14:-7] + "_tulemused.txt","w") #kirjutan faili nimega aasta-kuu_tulemused.txt
    file.write(tulemus) 
    file.close()