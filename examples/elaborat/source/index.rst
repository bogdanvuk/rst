.. role:: raw(raw)
   :format: latex

.. |algo| replace:: *EEFTI*
.. |efti| replace:: *EFTI*
.. |eftis| replace:: *EFTIs*
.. |cop| replace:: *DTEEP*
.. |smae| replace:: *SMAE*
.. |SM| replace:: :math:`S_m`
.. |A| replace:: :math:`\mathbf{A}`
.. |a| replace:: :math:`\mathbf{a}`
.. |NA| replace:: :math:`N_{A}`
.. |NIass| replace:: :math:`N_{Iass}`
.. |AM| replace:: :math:`A_{m}`
.. |IM| replace:: :math:`I_m`
.. |na| replace:: :math:`\bar{n}`
.. |NI| replace:: :math:`N_{I}`
.. |Da| replace:: :math:`\bar{D}`
.. |Nl| replace:: :math:`N_l`
.. |ACEM| replace:: :math:`ACE_m`
.. |NM| replace:: :math:`N_{M}`
.. |LM| replace:: :math:`L_{m}`
.. |Nc| replace:: :math:`N_{c}`
.. |NP| replace:: :math:`N_{P}`
.. |RA| replace:: :math:`R_{A}`
.. |alpha| replace:: :math:`{\alpha}`
.. |rho| replace:: :math:`{\rho}`
.. |WDTD| replace:: :math:`W_{DTD}`
.. |ne| replace:: :math:`n_e`
.. |Ths| replace:: :math:`T_{hs}`
.. |Tsw| replace:: :math:`T_{sw}`
.. |Tswmut| replace:: :math:`T_{sw\_mut}`
.. |Tswacc| replace:: :math:`T_{sw\_acc}`
.. |Thsmut| replace:: :math:`T_{hs\_mut}`
.. |Thsacc| replace:: :math:`T_{hs\_acc}`

====================
Elaborat za doktorat
====================

Motivacija
==========

.. _hdr-key-contributions:

Ključni očekivani doprinos
--------------------------

U ovoj sekciji su nabrojani ključni očekivani doprinosi u okviru rada na doktorskoj disertaciji. Uvod, motivacija i pregled stanja u oblasti je detaljnije izložen u narednim sekcijama. Predlaže se:

1. **Razvoj novog evolutivnog algoritma za indukciju celih kosih stabala odluke, koji ne zahteva populaciju, tj. vrši indukciju na samo jednoj jedinki**. Algoritmi za indukciju celih stabala odluke su manje zastupljeni od inkrementalnih zbog svoje veće vremenske kompleksnosti, ali bi se hardverskom akceleracijom mogli učiniti atraktivnijima. Hardverska akceleracija predloženog algoritma je takođe u planu rada na doktorskoj disertacijiji i opisana je u stavci 2. Algoritmi za indukciju stabala odluke bazirani na EA često koriste populaciju jedinki :cite:`bot2000application,krketowski2005global,llora2004mixed,papagelis2000ga`, što nije zgodno za hardversku akceleraciju, jer zahteva značajne hardverske resurse. Nama nije poznat ni jedan algoritam iz naučne literature koji indukuje celo stablo odluke uz pomoć samo jedne jedinke, odakle i motivacija za razvoj novog algoritma. Detaljnije u :num:`Sekciji #hdr-algo-single-induction`.

2. **Razvoj nove hardverske arhitekture za akceleraciju algoritma iz stavke 1.** Većina naučnih radova se fokusira na ubrzavanje već indukovanih stabala :cite:`struharik2009intellectual,li2011low,saqib2015pipelined`, dok se mali broj onih koji se bave treniranjem stabala odluke bazira na inkrementalnom pristupu indukcije :cite:`struharik2009evolving,chrysos2013hc`. Koliko je nama poznato, ne postoji ni jedan rad na temu hardverske akceleracije algoritama za indukciju celih stabala odluke, pa odatle i motivacija za rad na ovakvom akceleratoru u okviru doktorske disertacije. Detaljnije u :num:`Sekciji #hdr-accel-single-induction`

3. **Razvoj novog evolutivnog algoritma za indukciju ansambala kosih celih stabala odluke na bazi algoritma predloženog u stavki 1.**. Ansambli klasifikatora imaju veću preciznost predikcija i veću robustnost na šum u odnosu na pojedinačne klasifikatore, odakle i motivacija za razvoj algoritma za njihovu indukciju. Isti argumenti u vezi pogodnosti za hardversku akceleraciju navedeni u vezi algoritma predloženog u stavci 1. za važe i za ovde predloženi algoritam za indukciju ansambala. Detaljnije u :num:`Sekciji #hdr-algo-ensemble-induction`

4. **Razvoj hardverske arhitekture koja bi akcelerirala evolutivni algoritam za indukciju ansambala kosih celih stabala odluke koji zahteva samo jednu jedinku po članu ansambla, predloženog u stavki 3.** Nama je poznat samo jedan rad na ovu temu, ali u njemu se sekvencijalno indukuju stabla odluke. Detaljnije u :num:`Sekciji #hdr-accel-ensemble-induction`

Uvod u mašinsko učenje
----------------------

Mašinsko učenje :cite:`flach2012machine,murphy2012machine` je grana istraživačke oblasti veštačke inteligencije. Ona se bavi razvojem algoritama koji "uče" izvlačeći obrazce iz ulaznih podataka i kao svoj izlaz daju sisteme konstruisane da prave predikcije nad novim podacima. Jedna od glavnih snaga sistema mašinksog učenja je moć generalizacije, koja im omogućava da ostvare dobre rezultate na novim, do sada neviđenim podacima, nakon što su bili izloženi skupu podataka za treniranje.

Razni sistemi mašinskog učenja su do sada predloženi u literaturi uključujući: stabla odluke (DT od eng. *decision trees*) :cite:`rokach2007data,rokach2005top`, neuronske mreže (ANN od eng. "artificial neural networks") :cite:`haykin2009neural` i "support vector" mašine (SVM) :cite:`abe2005support`. Ovi sistemi se posebno široko primenjuju u oblasti vađenja podataka (eng. "data mining") (see e,g. :cite:`witten2005data`), sa DT, ANN i SVM-ovima kao najpopularnijima (e.g. :cite:`rokach2007data,wu2009top,wang2006data`).

Proces učenja, tzv. indukcija sistema mašinskog učenja, može biti kako nadlgedano tako i nenadgledano. Nadgledano učenje podrazumeva da je uz svaki ulazni podatak iz trening skupa dat i željeni odziv sistema na taj podatak. Sa druge strane, u slučaju kada se algoritmu za indukciju pruži samo trening skup podataka bez željenog odziva, reč je o nenadgledanom učenju. U tom slučaju, algoritam za indukciju mora sam da otkrije strukturu i obrasce u skupu ulaznih podataka, što samo po sebi može biti i cilj u rešavanja nekog problema. Ulazni podaci koji se koriste za učenje se obično sastoje od skupa instanci problema koji se rešava sistemom mašinskog učenja i naziva se trening skup. Životni vek sistema mašinskog učenja obično ima dve faze: trening fazu (takože i indukciju ili učenje) i fazu korišćenja. Konstrukcija sistema se vrši u trening fazi uz pomoć trening skupa, dok se u fazi korišćenja indukovani sistem suočava sa novim, do sada neviđenim instancama i pokušava da da što bolji odziv koristeći znanje izvučeno iz trening skupa.

Stabla odluke
-------------

Sistemi mašinskog učenja mogu rešavati razne probleme, kao što su klasifikacija, regresija, klasterisanje, itd. Za rešavanje problema klasifikacije, za koji se često koriste stabla odluke, potrebno je rasporediti ulazne instance problema u neki skup klasa. Instance problema se najčešće modeluju vektorom atributa **A**, na osnovu kojih se vrši klasifikacija. Za ovaj problem se često koriste stabla odluke. Proces klasifikacije uz pomoć stabla odluke se može predstaviti dijagramom koji ima strukturu stabla, kao što se vidi na :num:`Slici #fig-oblique-dt`. Ovaj diagram predstavlja tok blizak toku ljudskog razmišljanja, te ga je lako razumeti, što čini stabla odluke popularnim izborom za rešavanja problema klasifikacije. Stabla odluke imaju i brojne druge prednosti u odnosu na ostale sisteme mašinskog učenja, između ostalog: visok stepen imunosti na šum, mogućnost klasifikacije instanci sa redudantnim ili atributima koji nedostaju, mogućnost klasifikovanja instanci kako sa kategoričkim, tako i sa numeričkim atributima itd.

Teoretski stabla odluke mogu biti različitog stepena, ali se najčešće koriste binarna stabla, odnosno stabla u kojima svaki čvor ima dva potomka. :num:`Slika #fig-oblique-dt`, prikazuje proces klasifikacije na binarnom stablu odluke. Stablo se sastoji od 4 čvora označenih krugovima numerisanim od 1 do 4. Stablo takođe ima 5 listova označenih kvadratima, pri čemu je svakom listu dodeljena jedna od klasa problema (:math:`C_{1}` do :math:`C_{5}` u ovom primeru). Klasifikacija se vrši tako što se pusti da se instanca kreće kroz stablo, počevši od korena (numerisanog brojem 1), sve dok ne stigne do nekog od listova. U zavisnosti od lista u kome instanca završi svoj put kroz stablo, njoj se pridružuje klasa dodeljena tom listu.

.. _fig-dt-traversal:

.. bdp:: images/dt_traversal.py

    Proces klasifikacije na binarnom stablu odluke.

Svakom čvoru stabla odluke pridružen je po jedan test (:math:`T_{1}` do :math:`T_{4}` u ovom primeru), koji na osnovu atributa instance odlučuje kroz koji potomak će se nastaviti put kroz stablo. U slučaju binarnih stabala, od testova se očekuje binarni odgovor. Konačna putanja instance kroz stablo će zavisiti od rezultata testova u svakom čvoru stabla na koji instanca naiđe u toku svog puta. Puštajući jednu po jednu instancu trening skupa, može se dobiti njegova potpuna klasifikacija.

Svaki problem čija se klasifikacija rešava pomoću stabala odluke, definisan je skupom svojih instanci. Pri definisanju problema, potrebno je izabrati koji atributi će činiti vektor atributa (**A**) instanci i jednoznačno ih predstavljati. Takođe je potrebno definisati domen svakog atributa, gde se najčešće javlja dva slučaja:

 - Kategorički atributi imaju diskretan i često konačan domen
 - Numerički atributi za domen imaju podskup skupa realnih brojeva

Skup svih mogućih vektora atributa predstavlja *n*-dimenzionalni prostor atributa, gde je *n* broj atributa kojima su instance opisane i ujedno i veličina vektor **A**. U kontekstu prostora atributa, svaki test binarnog stabla odluke deli ovaj prostor na dva regiona, čineći da je svakom čvoru i listu stabla asocirana jedan pod-region prostora. Svaki čvor stabla na osnovu svog testa deli sebi asocirani pod-region na dva i dodeljuje svaki od njih po jednom svom potomku. Konačan rezultat ovog procesa je jasna particija prostora atributa na disjunktne regione asocirane klasama problema.

Na osnovu karakteristika funkcija kojima su implementirani testovi, stabla odluke se mogu podeliti na: ortogonalna, kosa i nelinearna. Svoje nazive, ovi tipovi stabala odluka su dobila na osnovu izgleda površi kojom njihovi testovi dele prostor atributa. Tako ortogonalna stabla odluke dele prostor ortogonalnim hiperravnima, kosa - kosim hiperravnima, a nelinearna - nelinearnih hiperpovršima.

U ovom radu, fokus će biti na kosim stablima odluke jer se željena preciznost sa njima može postići sa drastično manje čvorova u odnosu na ortogonalna stabla. **ZAŠTO JE OVO BITNO?** Što se tiče nelinearnih stabala odluke, ona se retko koriste zbog kompleksnosti njihove indukcije, ali i samog procesa klasifikacije.

Kosa stabla odluke
------------------

Kod kosih stabla odluke, testovi u čvorovima generišu kose hiperravni kojima dele prostor atributa. Kosa hiperravan je jednoznačno određena sledećom jednačinom:

.. math:: \mathbf{a}\cdot \mathbf{A} = \sum_{i=1}^{n}a_{i}\cdot A_{i} < thr,
    :label: oblique_test

gde **a** predstavlja vektor koeficijenata testa a *thr* (skraćeno od eng. *threshold*) modeluje afini deo testa.

.. _fig-oblique-dt:

.. bdp:: images/oblique_dt_traversal.py

    Primer kosog binarnog stabla odluke i jedne moguće putanje pri klasifikaciji instance prikazane crvenom linijom.

Svaka instanca počinje svoj prolazak kroz stablo na mestu korena i nastavlja sve dok ne stigne u neki od listova, gde joj se dodeljuje klasa asocirana tom listu. Kod svakog novog čvora do koga instanca stigne, računa se test definisan funkcijom :eq:`oblique_test`, na osnovu koeficijenata :math:`\mathbf{a}_{i}` i vektora atributa **A** koji definiše instancu (gde je *i* redni broj čvora u stablu). Ako test vrati vrednost *tačno* (T), prolazak kroz stablo se nastavlja preko levog potomka *i*-tog čvora, dok se u suprotnom nastavlja preko njegovog desnog potomka. Na :num:`Slici #fig-oblique-dt`, jedna moguća putanja je prikazana crvenom linijom. U primeru sa slike, instanca je nakon prolaska kroz stablo klasifikovana u klasu :math:`C_{4}`.

.. _hdr-algo-single-induction:

Indukcija stabala odluke
------------------------

Načelno, stabla odluke se mogu indukovati na dva načina: inkrementalno (čvor po čvor) ili globalno indukujući celo stablo od jednom. Većina algoritama za indukciju kosih stabala odluke koriste neku vrstu heuristike u procesu optimizacije indukovanog stabla, koja je često neki tip evolutivnog algoritma (EA), jer je pronalaženje optimalnog stabla odluke NP-težak algoritamski problem :cite:`barros2012survey` **Ima i drugih referenci u google scholaru kad se ukuca NP-hard i DT, pa ubaci**. 

Inkrementalni pristup gradi stablo odluke počevši od korena i dodajući mu iterativno po jedan čvor. Ovo je "greedy" pristup, u kome se parametri testa pridruženog čvoru, tj. vrednosti vektora koeficijenata **a** i vrednost prag *thr*, optimizuju na osnovu informacija of performansama stabla dostupnih u momentu kreiranja trenutnog čvora, tj. na osnovu "lokalnih" informacija. Nakon što je čvor dodat u stablo i algoritam nastavlja da kreira druge čvorove, situacija se promenila i dostupne su nove informacije, ali one neće biti iskorišćene za dodatnu optimizaciju čvora koji je već dodat u stablo, te se kaže da je optimizacioni proces ostao zarobljen u lokalnom optimumu. Algoritam obično optimizuje parametre testa u procesu maksimizacije neke ciljne funkcije koja meri kvalitet podele instanci iz trening skupa koje u procesu klasifikacije uspevaju da stignu do čvora kome je pridružen test. Ovom podelom se dobija dva podskupa instanci, od kojih se svaki prosleđuje na obradu po jednom potomku čvora. Za svaki od ova dva podskupa se dalje proverava da li se sastoje od instanci koje pripadaju različitim klasa ili je pak podskup "čist" u smislu da sadrži instance samo jedne klase. U slučaju da je podskup čist, kao potomak se dodaje list i njemu se asocira klasa instanci iz podskupa. U suprotnom, proces indukcije stabla se nastavlja iterativno i kao potomak se dodaje novi čvor u cilju dalje deobe podskupa instanci na čiste podskupove. Prednost inkrementalnog pristupa je brzina, ali indukovana stabla su suboptimalna po veličini i kasnijim klasifikacionim rezultatima na novim instancama. Razni algoritmi za inkrementalnu indukciju stabala odluke su predloženi u literaturi :cite:`quinlan1986induction,islam2010explore,mahmood2010novel,yildiz2012univariate,lopez2013fisher,breiman1984classification,murthy1994system,cantu2003inducing,liu2011improved,manwani2012geometric,barros2014framework,struharik2014inducing`.

Drugi pristup za kreiranje stabala odluke je indukcija celog stabla. Ovde se u svakoj iteraciji algoritma manipuliše celim stablom, tako da su uvek na raspolaganju kompletne (globalne) informacije o performansama indukovanog stabla odluke. U procesu indukcije, prema nekom algoritmu, čvorovi se dodaju ili brišu i parametri njihovih testova se menjaju u cilju optimizacije stabla. Pošto se optimizacija vrši na osnovu globalnih informacija o performansama, ovaj postupaku načelno proizvodi kompaktnija, a često i tačnija stabla odluke u odnosu na inkrementalne algoritme. Sa druge strane, ovi algoritmi imaju veću vremensku kompleksnost od inkrementalnih, što rezultuje u dužim vremenima potrebnim za indukciju. Značajan broj algoritama za indukciju celih stabala je takođe predložen u literaturi :cite:`papagelis2000ga,bot2000application,llora2004mixed,krketowski2005global,otero2012inducing,boryczka2015enhancing`.

Kao što je rečeno, pronalaženje optimalnog stabla odluke je NP težak problem, ali čak i ako se koristi inkrementalni pristup indukciji, kada je reč o kosim stablima odluke, nalaženje optimalnog položaja jedne neortogonalne hiperravni :eq:`oblique_test` je NP-težak algoritamski problem :cite:`heath1993induction`. Iz ovog razloga, većina algoritama za indukciju kosih stabala odluke koriste neku vrstu heuristike u procesu optimizacije, koja je često neka vrsta evolutivnog algoritma (EA). :num:`Slika #fig-evolutionary-dt-algorithm-tree` prikazuje taksonomiju evolutivnih algoritama za indukciju stabala odluke prikazanu u :cite:`barros2012survey`. 

.. _fig-evolutionary-dt-algorithm-tree:

.. figure:: images/taxonomy.pdf

    Taksonomija evolutivnih algoritama za indukciju stabala odluke.

Kao što je opisano u stavki 1. unutar :num:`Sekcije #hdr-key-contributions`, u okviru rada na doktorskoj disertaciji, predlaže se razvoj novog algoritma za indukciju celih kosih stabala odluke na bazi EA. Zbog svoje manje vremenske kompleksnosti, inkrementalni algoritmi trenutno dominiraju u istraživačkom polju indukcije stabala odluke. Kada bi bio razvijen hardverski akcelerator za indukciju celih stabala odluke koji bi drastično skratilo vreme potrebno za indukciju, ovaj pristup bi takođe dobio na atraktivnosti. Algoritmi za indukciju stabala odluke bazirani na EA često koriste populaciju jedinki :cite:`bot2000application,krketowski2005global,llora2004mixed,papagelis2000ga`, što nije zgodno za hardversku akceleraciju, jer zahteva značajne hardverske resurse. Iz ovog razloga se predlaže akceleracija algoritma baziranog na EA, koji za indukciju koristi samo jednu jedinku. Ovo bi otvorilo vrata svetu "embedded" sistema, gde ne postoji obilje resursa, kao što su memorija i procesorsko vreme. Nama nije poznat ni jedan algoritam iz naučne literature koji ispunjava ovaj uslov, te je plan da se takav algoritam razvije u okviru rada na doktorskoj disertaciji.

.. _hdr-accel-single-induction:

Algoritmi za formiranje celog stabla u hardveru
-----------------------------------------------

Faza indukcije u slučaju da se koristi algoritam za formiranje celog stabla odluke, može trajati satima ili čak danima za praktiče probleme. Ako bi se faza indukcije uspela akcelerirati, moguće bi bilo koristiti veće trening skupove, što bi bilo od posebnog značaja u aplikacijama "vađenja podataka" :cite:`witten2005data`. Dalje, brži trening stabala odluke bi omogućio kraće dizajn cikluse i otvara mogućnost indukcije stabala odluke u realnom vremenu za primene koje zahtevaju tako brzo prilagođavanje, kao što su "web mining" :cite:`liu2007web,yu2013depth`, bioinformatika :cite:`lesk2013introduction,baldi2001bioinformatics`, mašinski vid :cite:`prince2012computer,ali2010hardware,tomasi2010fine`, "text mining" :cite:`weiss2010fundamentals,aggarwal2012mining`, itd.

Problemu akceleracije faze indukcije se može pristupiti na dva načina:

- Razvojem novih algoritamskih okvira ili novih softverskih alata, pri čemu je ovaj postupak dominantan u literaturi :cite:`bekkerman2011scaling,choudhary2011accelerating`.
- Razvojem novih hardverskih arhitektura, optimizovanih za ubrzano izvršavanje postojećih algoritama za indukciju.

U literaturi je predložen znatan broj različitih arhitektura za hardversku akceleraciju algoritama za mašinsko učenje. Arhitekture za hardversku akceleraciju algoritama za treniranje SVM-ova :cite:`anguita2003digital` i algoritama za izvršenje SVM-ova :cite:`papadonikolakis2012novel,anguita2011fpga,mahmoodi2011fpga,vranjkovic2011new`. Istraživanje na polju hardverske akceleracije ANN-ova je bilo prilično intenzivno, te su mnoge hardverske arhitekture za ubrzanje izvršenja istreniranih ANN-ova već predložene :cite:`savich2012scalable,vainbrand2011scalable,echanobe2014fpga`. Takođe, predložene su mnoge hardverske arhitekture na kojima je moguće implementirati algoritme za treniranje ANN-ova :cite:`misra2010artificial,omondi2006fpga,madokoro2013hardware`. 

Kao što je opisano u stavki 2. unutar :num:`Sekcije #hdr-key-contributions`, u okviru rada na doktorskoj disertaciji, predlaže se razvoj hardverske arhitekture koja bi akcelerirala evolutivni algoritam za indukciju celih kosih stabala odluke, koji ne zahteva populaciju, predložen u stavki 1. unutar :num:`Sekcije #hdr-key-contributions`. Na planu hardverske akceleracije stabala odluka, većina naučnih radova se fokusira na ubrzavanje već indukovanih stabala :cite:`struharik2009intellectual,li2011low,saqib2015pipelined`, dok je hardverska akceleracija indukcije stabala odluke slabo prisutna. Rekonfigurabilni hardverski akcelerator, predložen u :cite:`vranjkovic2015reconfigurable` je naročito zanimljiv, jer je u stanju da akcelerira sva tri pomenuta tipa prediktora: stabla odluke, SVM-ove i ANN-ove. Koliko nam je poznato, postoje samo dva rada na temu hardverske akceleracije algoritama za indukciju stabala odluke :cite:`struharik2009evolving,chrysos2013hc`, ali oba koriste "greedy", "top-down", inkrementalni pristup. U :cite:`struharik2009evolving`, inkrementalni algoritam za indukciju stabala odluke je potpuno akceleriran u hardveru i EA je korišćen za izračunavanje optimalnih vektora koeficijenata testova čvor po čvor. U :cite:`chrysos2013hc`, HW/SW (skraćeno od eng. *HardWare/SoftWare* kodizajn tehnika je korišćena za akceleraciju računski najzahtevnijih delova poznatog CART inkrementalnog algoritma za indukciju stabala odluke. Koliko je nama poznato, ne postoji ni jedan rad na temu hardverske akceleracije algoritama za indukciju celih stabala odluke, pa odatle i motivacija za rad na ovakvom akceleratoru u okviru doktorske disertacije.

.. _hdr-algo-ensemble-induction:

Algoritmi za formiranje ansambala
---------------------------------

Da bi se unapredile performanse klasifikatora, predloženo je korišćenje ansambala sistema za klasifikaciju :cite:`rokach2010ensemble` umesto jednog klasifikatora. Ansambl klasifikatora kombinuje predikcije nekoliko individualnih klasifikatora u cilju dobijanja boljih performansi. Treniranje ansambala zahteva indukciju skupa pojedinačnih klasifikatora, uglavnom stabala odluke ili ANN-ova, čije predikcije se onda kombinuju u fazi kroišćenja ansambla u procesu klasifikacije novih instanci. Iako jednostavna, ova ideja se pokazala kao veoma efektivna, proizvodeći sisteme koji su precizniji od pojedinačnog klasifikatora.

Prilikom indukcije ansambla klasifikatora, potrebno je rešiti dva problema: 

- Kako obezbediti raznovrsnost članova ansambla, tj. raznovrsnost njihovih predikcija
- Koju proceduru upotrebiti za kombinovanje pojedinačnih predikcija svakog klasifikatora, tako da se pojača uticaj dobrih odluka a potisne uticaj loših.

Među najpopularnijim metodama koje obezbeđuju raznovrsnost članova ansambla su Brajmanov "bagging" algoritam :cite:`buhlmann2012bagging`, Šapirov "boosting" algoritam :cite:`buhlmann2012bagging`, AdaBoost :cite:`buhlmann2012bagging`, Wolpertov "stacked generalization" algoritam :cite:`ozay2008performance`, i mešavina eksperata :cite:`jacobs1991adaptive`. Najčešće korišćene procedura za kombinaciju predikcija su između ostalog: većinsko glasanje, ponderisano većinsko glasanje i "behavior knowledge spaces" :cite:`huang1993behavior`.

Glavna prednost ansambala klasifikatora u odnosu na pojedinačne klasifikatore je veću preciznost predikcija i veća robustnost na šum. Sa druge strane, u odnosu na pojedinane klasifikatore, potrebne su velike količine memorije da bi se smestile definicije članova ansambla, a veliko računarska moć potrebna da bi se izračunao odgovor ansambla, što sve vodi ka dužim i u pogledu resursa zahtevnijim fazama indukcije. Ovo je stoga što se ansamble obično sastoje od 30 i više pojedinačnih klasifikatora :cite:`buhlmann2012bagging`, te ako bi želeli iste performanse klasifikacije što se tiče brzine, bilo bi potrebno 30+ puta više memorije i računarske moći. 

Kao što je opisano u stavki 3. unutar :num:`Sekcije #hdr-key-contributions`, u okviru rada na doktorskoj disertaciji, predlaže se razvoj novog evolutivnog algoritma za indukciju ansambala kosih celih stabala odluke koji zahteva samo jednu jedinku po članu ansambla, na bazi algoritma predloženog u stavki 1. unutar :num:`Sekcije #hdr-key-contributions`. Isti argumenti u vezi pogodnosti za hardversku akceleraciju navedeni u vezi predloženog algoritma za indukciju pojedinačnih celih kosih stabala odluke, važe i za algoritam za indukciju ansambala. Dodatna motivacija za razvoj algoritma za indukciju ansambala je činjenica da ansambli imaju bolje performanse od pojedinačnih klasifikatora, kao što je već rečeno.

.. _hdr-accel-ensemble-induction:

Algoritmi za formiranje ansambala u hardveru
--------------------------------------------

Kao što je već rečeno u prethodnoj sekciji, algoritmi za formiranje ansambala imaju drastično veće potrebe za resursima u odnosu na algoritme za indukciju pojedinačnih klasifikatora. Još jednom, hardverska akceleracija ansambala klasifikatora pruža način da se omogući da trajanje indukcije ansambala bude uporedivo sa trajanjem indukcije pojedinačnog klasifikatora.

Što se tiče hardverske akceleracije ansambala sistema za klasifikaciju, prema našem znanju, većina se predloženih rešenja bavi hardverskom implementacijom ansambala klasifikatora koji su prethodno formirani u softveru :cite:`bermak2003compact,osman2009random,van2012accelerating,hussain2012adaptive,struharik2013hardware`. Poznat nam je samo jedan rad :cite:`struharik2009evolving` u kome je predložena arhitektura za hardversku evoluciju homogenih ansambala klasifikatora baziranih na stablima odluke. Ovaj rad implementira algoritam koji sekvencijalno indukuje stabla odluke koji postaju članovu ansambla klasifikatora.

Kao što je opisano u stavki 4. unutar :num:`Sekcije #hdr-key-contributions`, u okviru rada na doktorskoj disertaciji, predlaže se razvoj hardverske arhitekture koja bi akcelerirala evolutivni algoritam za indukciju ansambala kosih celih stabala odluke koji zahteva samo jednu jedinku po članu ansambla, predložen takođe u stavki 3. unutar :num:`Sekcije #hdr-key-contributions`.

.. bibliography:: hereboy.bib
	:style: unsrt
