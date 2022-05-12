# Baigiamasis projektas
# Rūta Monkevičiūtė
# 2022-05-16

## Projekto aprašymas

Projekto tikslas - atlikti bibliografinių duomenų statistinę analizę

Projekto uždaviniai:
1. Išnagrinėti iš išvalyti turimus bibliogafinius duomenis;
2. Atlikti duomenų bibliometrinę analizę;
3. Sukurti autorių bendraautorystės tinklą, grafiškai jį pavaizduoti ir įvertinti gauto grafo rodiklius;
4. Sukurti žurnalų klasterizavimo modelį;
5. Perkelti sukurtą modelį į Flask aplikaciją.

Šiems uždaviniams įgyvendinti sukurti 4 Jupyter notebook failai ir viena Flask aplikacija. Toliau aprašomi juose atlikti veiksmai ir gauti rezultatai.

## Bibliografinių duomenų failo valymas ir galutinio duomenų rinkinio sudarymas.

*Naudojamas notebook failas: Duomenu_paruosimas.ipynb*

### Duomenų valymas

Pradiniame duomenų rinkinyje, viename iš stulpelių (projection_apa), kartu ir be konkrečių ir vieningų skirtukų pateikta ši informacija:
- Autoriaus (-ių) pavardė(s) ir inicialai;
- Išleidimo metai;
- Antraštė;
- Leidinio, kuriame išspausdintas straipsnis, antraštė;
- Leidinio tomas ir numeris;
- Straipsnio puslapiai leidinyje;
- DOI (skaitmeninis objekto identifikatorius)

Kitas iššūkis susijęs su autorių pavardėmis ir inicialais – pavardės gali būti rašomos keliais būdais:
1. Pavardė, V.
2. Pavardė, V.V.
3. Pavardė, V.V.V.
4. Pavardė, V.V.V.V.
5. Pavardė, V.V.V.V.V.
6. Pavardė Pavardė, V.
7. Pavardė-Pavardė, V.
8. Pavardė Pavardė Pavardė, V.

Įvertinus šias duomenų savybes, duomenų valymas (stulpelio išskaidymas į dalis) buvo daromas šiais etapais:
1. Išskirtos autorių pavardės (naudota *re* biblioteka).
2. Pašalinti internetiniai adresai (jie atskirti naudojant vieną iš skirtukų: „doi“, „Retrieved“ arba „Žiūrėta“).
3. Sukuriamas naujas stulpelis: 0, jei doi adreso nėra, 1 – jei jis yra.
4. Atskirti publikacijų puslapiai leidiniuose (naudota *re* biblioteka).
5. Pašalinti publikavimo metai, nes jie yra pateikti atskirame stulpelyje (naudota *re* biblioteka).
6. Atskirti publikacijos pavadinimai bei leidinio numeriai.
7. Atskirti leidinių pavadinimai įvairiomis kalbomis.

*scopus_info*,  *if_info* ir *res_fields* stulpeliai pateikti standartizuotai, todėl buvo nesudėtinga juos išskaidyti į sudedamąsias dalis.
*dbases* stulpelis taip pat išskaidytas į sudedamąsias dalis. Atrinkta 10 daugiausiai naudotų duomenų bazių ir joms sukurti atskiri stulpeliai, o likusios reikšmės priskirtos kategorijai „other_dbases“.

Atlikus duomenų valymą, iš pirminių 8 stulpelių buvo gauti 37 nauji stulpeliai.

### Leidinių pavadinimų sutvarkymas

Buvo pastebėta, kad dalis žurnalų pavadinimų kartojasi, ir jie nebūtinai turi identiškus pavadinimus. Vienas iš leidinių pavadinimų nevienodumo pavyzdžių gali būti žurnalas Acta Physica Polonica A:
1. Acta physica Polonica A;
2. Acta physica Polonica. A;
3. Acta physica polonica. A.

Siekiant suvienodinti pavadinimus, buvo pasirinktas būdas leidinius priskirti grupėms, kur viena grupė apjungtų tą patį leidinį užrašytą skirtingais būdais.

Buvo nuspręsta pritaikyti du metodus, esančius *FuzzyWuzzy* bibliotekoje: *Token Sort Ratio* ir *Token Set Ratio* ir patikrinti, kuris iš jų grąžins geresnius rezultatus.

Jei įrašai visiškai sutampa, grąžinama reikšmė 100. Siekiant kuo didesnio tikslumo, buvo pasirinktas panašumo indeksas lygus 95 kaip žemiausia panašumo riba. 

Apskaičiavus abiejų modelių rezultatus, gautos išvados: 
- *Token Sort Ratio* metodu, gaunamas 202 leidinių poros; 
- *Token Set Ratio* metodu – 505 poros. 

Dėl to nuspręsta toliau dirbti su Token Set Ratio metodu.

Kitu žingsniu visiems leidiniams suteikiamas indeksas. Buvo pastebėta, kad leidiniai rezultatų lentelėje kartojasi: vienu atveju jie yra kaip pirmasis įrašas, su kuriuo lyginami visi likę, kitu atveju – jis yra priskiriamas bendrai grupei. Dėl to vienas leidinys gali turėti kelis skirtingus indeksus. Šiam neatitikimui pašalinti, lyginami vieno leidinio indeksai ir jam priskiriamas tik pirmasis, kitus panaikinant. Atlikus šiuos veiksmus, unikalūs indeksai priskiriami ir tiems leidinių pavadinimams, kurie nebuvo identifikuoti, kaip turintys panašumų su kitais įrašais. 

Galutiniai rezultatai:
- Prieš pradedant leidinių grupavimą, duomenų rinkinyje buvo 1 713 unikalių leidinių pavadinimų;
- Atlikus jų grupavimą ir priskyrus grupės indeksą, liko 1 254 unikalios reikšmės;
- Žurnalų pavadinimų grupavimas pagerino leidinių pavadinimų kokybę 27 %. 

### Autorių bendraautorystės sąrašo sudarymas

Įkeliamas autorių failas, kuriame autorių vardai pakeisti į indeksus. Šis procesas buvo atliktas Excel programoje. 

Proceso eiga:

- Autoriai sugrupuojami į sąrašus pagal bendraautorystės ryšius;
- Gautos visos unikalios autorių poros (naudota *itertools* biblioteka);
- Kiekvienai porai priskiriamas svoris - kiek kartų ji pasikartojo duomenų rinkinyje.

Sukurti 2 bendraautorių sąrašai: viename yra visi autoriai, kitame pašalinamos išskirtys (publikacijos, kuriose yra >20 bendraautorių).

Gauti duomenys išsaugomi duomenų failuose.

## Duomenų bibliometrinė analizė

*Naudojamas notebook failas: Aprasomoji_statistika.ipynb*

Bibliometrijos sąvoka gali būti formuluojama kaip matematinių ir statistinių metodų visuma dokumentų srautams ir jų bibliografinėms charakteristikoms tirti.

Atliekant bibliometrinę analizę, nagrinėtos šios temos:

- Publikacijų skaičius 2010 – 2019 periode;
- Vidutinis publikacijų skaičius;
- Mokslo ir meno sričių klasifikatoriai;
- Technologijos mokslų mokslo sritis;
- Technologijos mokslų sričių pokytis per 2010 – 2019 metus;
- Dokumentu tipai;
- Autorių analizė;
- 10 produktyviausių autorių;
- Duomenų bazių analizė;
- Pagrindinių duomenų bazių publikacijų skaičiaus pokytis.

## Autorių bendraautorystės tinklas

*Naudojamas notebook failas: Grafai.ipynb*

Autorių sąryšių tinklui sudaryti buvo naudojamos dvi sistemos:

- Vizualizavimo įrankis Gephi;
- Python.

Kad bibliografinių duomenų tinklas būtų sėkmingai atvaizduotas Gephi sistemoje, sukuriami 2 nauji duomenų rinkiniai: viršūnės ir briaunos.

Autoriaus straipsnių skaičius nurodo, kiek kartų konkretus autorius pasikartojo duomenų rinkinyje. Bendraautorystės ryšys pasirinktas kaip nekryptinis (*Undirected*), nes autorių bendradarbiavimo ryšys laikomas vienodas abejomis kryptimis. Bendraautorystės pasikartojimų skaičius nurodo autorių tarpusavio bendradarbiavimo pasikartojimų skaičių duomenų rinkinyje. Sudarant bibliometrinį tinklą Gephi sistemoje, autoriaus straipsnių skaičius lemia viršūnės dydį (kuo didesnė viršūnė, tuo daugiau autoriaus darbų nagrinėta), o bendraautorystės pasikartojimų skaičius – dviejų autorių bendradarbiavimo stiprumą arba dvi viršūnes jungiančios briaunos storį (kuo storesnė briauna, tuo dažniau pasikartojantis bendradarbiavimas).

Kaip jau minėta anksčiau, buvo sudaryti 2 bendraautorystės tinklai, nes išskirtys smarkiai paveikė viso tinklo parametrus.

**Visų autorių bendraautorystės tinklas**

https://github.com/monkeviciute/code_academy_projektas/blob/main/visi%20autoriai.png

**Autorių bendraautorystės tinklas, pašalinus išskirtis**

https://github.com/monkeviciute/code_academy_projektas/blob/main/be_isskirciu.png

Naudojantis Gephi ir Python (*networkx* biblioteka), rasti įvairūs tinklų rodikliai:

- Viršūnių laipsniai ir jų pasikartojimo dažnis;
- Laipsnių vidurkis;
- Grafo vidutiniai jungumo matai;
- Grafo tankumas;
- Laipsnių koreliacijos koeficientas;
- Grafo skersmuo;
- Vidutinis atstumas tarp grafo viršūnių;
- Klasterizacijos koeficientas;
- Laipsnių centriškumas;
- Artumo centriškumas;
- Tarpusavio centriškumas.

## Žurnalų klasterizavimo modelis

*Naudojamas notebook failas: Klasterizacija.ipynb*

Pagal bibliografinius rodiklius, leidiniai yra vertinami, jiems yra skaičiuojami prestižiškumo rodikliai ir jie pagal tai yra reitinguojami. Atlikus klasterizavimą, bus siekiama įvertinti, į kiek klasterių pasiskirsto nagrinėjami žurnalai, kokios yra šių klasterių savybės ir galiausiai, kurie iš jų yra dažniausiai pasirenkami. 

Duomenų rinkinyje iš viso yra paminėtas 1 301 žurnalas ir 50,3 % iš jų (655 žurnalai) neturi priskirtų nagrinėjamų bibliografinių rodiklių. Tokių žurnalų įtraukti į klasterizacijos modeliui perduodamą duomenų rinkinį nėra prasmės, nes jie būtų priskirti vienam klasteriui, kuris neturėtų nieko bendro su likusiais. Dėl to šie įrašai pašalinami iš duomenų rinkinio. Likę 646 žurnalai taip pat turi ne visus išvardintus rodiklius arba jie priskirti leidiniams ne visais nagrinėjamais metais (duomenų rinkinyje Scopus ir WoS rodikliai pateikti 2009 – 2018 metų periode), todėl trūkstamos reikšmės pakeičiamos į 0. 

Prieš sukuriant modelį, atliekamas duomenų normalizavimas. Proceso etapai:
1. Duomenys išskaidomi į 3 mažesnius rinkinius priklausomai nuo mokslo srities (SCIE, SSCI, NA);
2. Duomenų normalizavimas pritaikomas kiekvienam mažesniam duomenų rinkiniui atskirai;
3. Gauti normalizuoti duomenys sujungiami į vieną galutinį duomenų rinkinį.

Duomenų normalizavimui nuspręsta taikyti *min – max* metodą, kuris pagrįstas duomenų parametrų diapazono keitimu iš originalių verčių į [0, 1] intervalą. 

### Kmeans klasterizavimo modelis

Sukuriamas Kmeans modelis naudojantis *sklearn* biblioteka.

Gauto modelio rezultatai nebūtinai yra geriausi iš pirmojo karto ir svarbu įsitikinti ar klasterių skaičius parinktas teisingai. Šiai užduočiai atlikti buvo naudojami 3 metodai: 
1.	Sudarant klasterių kvadratinės paklaidos sumos mažėjimo ir klasterių tarpusavio ryšio grafiką;
2.	Naudojant Python sistemoje jau paruoštą metodą kelbow_visualizer iš yellowbrick.cluster.elbow bibliotekos;
3.	Apskaičiuojant silueto koeficientą.

Taikant pirmąjį metodą, sukurtam K-vidurkių modeliui nurodoma, kokį klasterių skaičių taikyti, ir šis procesas pritaikomas klasterių skaičiui nuo 2 iki 20. Tokiu būdu gaunama kvadratinės paklaidos suma kiekvieno klasterių skaičiaus atveju. Gautos reikšmės vizualizuojamos grafike ir tikimasi, kad optimaliausias klasterių skaičius bus matomas kaip „alkūnės“ forma, kurios lūžio taškas atitiks susistabilizavisį klasterių skaičių. Nubrėžus šį grafiką turimam duomenų rinkiniui, „alkūnės“ forma nėra pakankamai aiški, dėl to optimalų klasterių skaičių rasti nėra paprasta. 

Antrasis taikytas optimalių klasterių skaičiaus radimo metodas remiasi metodu *kelbow_visualizer* iš *yellowbrick.cluster.elbow* bibliotekos. 
*kelbow_visualizer* modelyje nurodomas modelių klasterių skaičius. Jis parenkamas toks pat kaip ir pirmuoju atveju: nuo 2 iki 20. Modelis grąžina grafiką, kuriame informatyviai pateikiamas optimalus klasterių skaičius, kuris yra 7.

Taikant trečiąjį metodą buvo naudota *Yellowbrick* biblioteka. Šioje bibliotekoje yra sukurtas silueto koeficiento apskaičiavimo modelis (*silhouette_score*), kuriam perduodamas paruoštas K-vidurkių modelis ir gaunamos silueto koeficiento reikšmės klasteriams nuo 2 iki 20. Iš gautų rezultatų matoma, kad didžiausia silueto koeficiento reikšmė gaunama, kuomet klasterių skaičius lygus 7.

Nustačius optimalų klasterių skaičių, jis nurodomas K-vidurkių modelyje ir atnaujintas modelis pakartotinai pritaikomas duomenų rinkiniui. Modelio rezultatas – klasterių numeriai, kurie prijungiami prie pradinio duomenų rinkinio. Norint grafiškai pavaizduoti gautus klasterius, reikia pritaikyti matmenų mažinimo metodą ir daugiamačius duomenis pateikti mažesnio skaičiaus matmenų erdvėje. Šiam tikslui pasiekti taikomas tiesinės projekcijos metodas – pagrindinių komponenčių analizė.


###Rezultatų analizė

1.	Į klasterį numeris 1 pakliūna žurnalai, kurių vidutinės rodiklių reikšmės yra mažiausios. Kadangi IF ir SJR vidutinės rodiklių reikšmės yra mažiausios iš visų klasterių, galima teigti, kad į jį patenka **mažiausiai prestižiniai žurnalai**.
2.	Klasteris numeris 2 pasižymi didžiausia SJR rodiklio reikšme. Visų kitų rodiklių vidutinės reikšmės taip pat yra vienos didžiausių, dėl to daroma išvada, kad į šį klasterį pakliūna **prestižiškiausi žurnalai**.  
3.	Klasteris numeris 3 išsiskiria vidutine rodiklio AIF reikšme, kuri yra didžiausia iš visų klasterių. Tai reiškia, kad žurnalai, patenkantys į šį klasterį, **išsiskiria citavimų skaičiumi**, tačiau negali būti priskiriami prie prestižinių leidinių, nes kitų rodiklių vidutinės reikšmės nėra didelės.
4.	Daugiausia žurnalų priskirta klasteriui numeris 4 (177), tačiau vidutinės žurnalų rodiklių reikšmės yra vienos mažiausių. Šiame klasteryje yra žurnalai, kurių vidutinės SNIP, CiteScore ir AIF rodiklių reikšmės yra mažiausios, o tai reiškia, kad į jį patenka **mažiausiai cituojami žurnalai**. 
5.	Klasteris 6 pagal žurnalų skaičių yra antras pagal dydį (147 žurnalai). Jam priskirtų žurnalų WoS rodikliai IF ir AIF turi vienas didžiausių vidutinių reikšmių. Galima teigti, kad šiame klasteryje yra **labiausiai cituojami žurnalai** pagal WoS duomenų bazės rodiklius.
6.	Klasteriai 0 ir 5 yra pakankamai panašūs: visų rodiklių vidutinės reikšmės yra gana panašios ir neišsiskiria iš kitų klasterių. Galima daryti išvadą, kad žurnalai, esantys šiuose klasteriuose, yra **vidutinės svarbos**.

## Flask aplikacijos kūrimas

*Naudojamas failas: app.py*

Aprašytas klasterizacijos modelis sukurtas naudojant duomenų failą, kuris turi 67 stulpelius, nes jame pateikiamos rodiklių reikšmės 10 metų periode.

Siekiant sukurti optimalesnę aplikaciją, sudarytas naujas duomenų rinkinys: parenkamos visų rodiklių paskutinių metų reikšmės ir mokslo šaka – SCIE.

Naudojant šiuos duomenis, sukuriamas naujas Kmeans modelis, patikrinamas optimalus klasterių skaičius, jis atnaujinamas modelyje ir gaunami klasteriai.

Klasterių reikšmės, kurios bus naudojamos Flask app:

- 0 – Gerą reitingą turintys žurnalai;
- 1 – Mažiausiai prestižiniai žurnalai;
- 2 – Vidutinės svarbos žurnalai;
- 3 – Labiausiai cituojami žurnalai;
- 4 – Prestižiškiausi žurnalai.

Paleidus aplikaciją, galima įvesti savo duomenis (rekomenduojami rėžiai pateikiami prie įvesties langelio) ir gauti žurnalo klasterio reikšmę.

## Išvados

1. Bibliografinių duomenų rinkinys pasižymi keletu savybių:
   1. Nereikšmingi, neaiškūs, trūkstami, netvarkingi duomenys;
   2. Ne visada laikomasi duomenų standartinio užrašymo;
   3. Kadangi duomenų rinkinyje yra daug tekstinių duomenų, matoma, kad yra rašybos klaidų. Ne visada naudojamos lietuviškos raidės.
   4. Duomenys yra atskirti ne nuosekliais skirtukais.
2. Prieš pradedant bet kokį darbą, būtinas detalus duomenų rinkinio valymo ir tvarkymo procesas.
3. Bibliometrinės analizės išvados:
   1. Vidutinis publikacijų skaičius per nagrinėjamus metus yra 695 publikacijos;
   2. Publikacijos skirstomos į 7 mokslo sritis;
   3. Vidutiniškai, 3 autoriai dalinasi vienos publikacijos bendraautoryste;
   4. Išskirti produktyviausi autoriai;
   5. Daugiausia publikacijų talpinama Scopus duomenų bazėje.
4. Iš autorių bendradarbiavimo tinklo analizės, daromos kelios išvados:
   1. Išskirtys daro didelę įtaką visam tinklui;
   2. Kelios viršūnės išsiskiria pagal svarbą visam tinklui;
   3. Vidutinis viršūnės laipsnis (visų autorių tinklo) yra 10;
   4. Grafo tankumas yra labai mažas: (0,002), dėl to visos viršūnės nėra stipriai sujungtos.
5. Žurnalų klasterizavimo modelis padėjo apibendrinti nagrinėjamų žurnalų savybes:
   1. Žurnalai skirstomi į 7 grupes;
   2. Kelios iš jų persidengia ir turi panašių savybių;
   3. Klasterių pasiskirstymas nėra tolygus;
   4. Klasterių sudarymas padėjo įvertinti, kaip leidiniai gali būti grupuojami ir kokios yra šių grupių savybės.


