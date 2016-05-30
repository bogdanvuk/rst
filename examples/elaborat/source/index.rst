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

Oblast istraživanja - mašinsko učenje
=====================================

Mašinsko učenje :cite:`flach2012machine,murphy2012machine` je grana istraživačke oblasti veštačke inteligencije. Ona se bavi razvojem algoritama koji "uče" izvlačeći obrazce iz ulaznih podataka i kao svoj izlaz daju sisteme konstruisane da prave predikcije nad novim podacima. Jedna od glavnih snaga sistema mašinksog učenja je moć generalizacije, koja im omogućava da ostvare dobre rezultate na novim, do sada neviđenim podacima, nakon što su bili izloženi skupu podataka za treniranje.

Razni sistemi mašinskog učenja su do sada predloženi u literaturi uključujući: stabla odluke (DT od eng. *decision trees*) :cite:`rokach2007data,rokach2005top`, neuronske mreže (ANN od eng. "artificial neural networks") :cite:`haykin2009neural` i "support vector" mašine (SVM) :cite:`abe2005support`. Ovi sistemi se posebno široko primenjuju u oblasti vađenja podataka (eng. "data mining") (see e,g. :cite:`witten2005data`), sa DT, ANN i SVM-ovima kao najpopularnijima (e.g. :cite:`rokach2007data,wu2009top,wang2006data`).

Proces učenja, tzv. indukcija sistema mašinskog učenja, može biti kako nadlgedano tako i nenadgledano. Nadgledano učenje podrazumeva da je uz svaki ulazni podatak iz trening skupa dat i željeni odziv sistema na taj podatak. Sa druge strane, u slučaju kada se algoritmu za indukciju pruži samo trening skup podataka bez željenog odziva, reč je o nenadgledanom učenju. U tom slučaju, algoritam za indukciju mora sam da otkrije strukturu i obrasce u skupu ulaznih podataka, što samo po sebi može biti i cilj u rešavanja nekog problema. Ulazni podaci koji se koriste za učenje se obično sastoje od skupa instanci problema koji se rešava sistemom mašinskog učenja i naziva se trening skup. Životni vek sistema mašinskog učenja obično ima dve faze: trening fazu (takože i indukciju ili učenje) i fazu korišćenja. Konstrukcija sistema se vrši u trening fazi uz pomoć trening skupa, dok se u fazi korišćenja indukovani sistem suočava sa novim, do sada neviđenim instancama i pokušava da da što bolji odziv koristeći znanje izvučeno iz trening skupa.

Stabla odluke
=====================

Sistemi mašinskog učenja se često koriste za klasifikaciju ulaznih instanci u neki skup klasa. Instance problema se najčešće modeluju vektorom atributa **A**, na osnovu kojih se vrši klasifikacija. Za ovaj problem se često koriste stabla odluke. Proces klasifikacije uz pomoć stabla odluke se može predstaviti dijagramom koji ima strukturu stabla, kao što se vidi na :num:`Slici #fig-oblique-dt`. Ovaj diagram predstavlja tok blizak toku ljudskog razmišljanja, te ga je lako razumeti, što čini stabla odluke popularnim izborom za rešavanja problema klasifikacije. Stabla odluke imaju i brojne druge prednosti u odnosu na ostale sisteme mašinskog učenja, između ostalog: visok stepen imunosti na šum, mogućnost klasifikacije instanci sa redudantnim ili atributima koji nedostaju, mogućnost klasifikovanja instanci kako sa kategoričkim, tako i sa numeričkim atributima itd.

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
======================

Kod kosih stabla odluke, testovi u čvorovima generišu kose hiperravni kojima dele prostor atributa. Kosa hiperravan je jednoznačno određena sledećom jednačinom:

.. math:: \mathbf{a}\cdot \mathbf{A} = \sum_{i=1}^{n}a_{i}\cdot A_{i} < thr,
    :label: oblique_test

gde **a** predstavlja vektor koeficijenata testa a *thr* (skraćeno od eng. *threshold*) modeluje afini deo testa.

.. _fig-oblique-dt:

.. bdp:: images/oblique_dt_traversal.py

    Primer kosog binarnog stabla odluke i jedne moguće putanje pri klasifikaciji instance prikazane crvenom linijom.

Svaka instanca počinje svoj prolazak kroz stablo na mestu korena i nastavlja sve dok ne stigne u neki od listova, gde joj se dodeljuje klasa asocirana tom listu. Kod svakog novog čvora do koga instanca stigne, računa se test definisan funkcijom :eq:`oblique_test`, na osnovu koeficijenata :math:`\mathbf{a}_{i}` i vektora atributa **A** koji definiše instancu (gde je *i* redni broj čvora u stablu). Ako test vrati vrednost *tačno* (T), prolazak kroz stablo se nastavlja preko levog potomka *i*-tog čvora, dok se u suprotnom nastavlja preko njegovog desnog potomka. Na :num:`Slici #fig-oblique-dt`, jedna moguća putanja je prikazana crvenom linijom. U primeru sa slike, instanca je nakon prolaska kroz stablo klasifikovana u klasu :math:`C_{4}`.

Načelno, stabla odluke se mogu indukovati na dva načina: inkrementalno (čvor po čvor) ili globalno indukujući celo stablo od jednom. Većina algoritama za indukciju kosih stabala odluke koriste neku vrstu heuristike u procesu optimizacije indukovanog stabla, koja je često neki tip evolutivnog algoritma (EA), jer je pronalaženje optimalnog stabla odluke NP-težak algoritamski problem :cite:`barros2012survey` **Ima i drugih referenci u google scholaru kad se ukuca NP-hard i DT, pa ubaci**. The greedy top-down recursive partitioning strategy is the computationally least demanding approach for the DT induction, hence most DT induction algorithms use this approach. Naturally, this approach suffers from inability of escaping local optima. Better results, especially if the DT size is considered, can be obtained by the inducers that work on full DT, with the cost of higher computational complexity :cite:`struharik2014inducing`.

The DT induction phase of full DT inference algorithms can be very computationally demanding and can last for hours or even days for practical problems. By accelerating the DT induction phase larger training sets could be used, which is of particular interest in the data mining applications :cite:`witten2005data`. Furthermore, faster DT training allows for shorter design cycles and opens the possibility of DT induction in real-time for the applications that require such rapid adapting, such as web mining :cite:`liu2007web,yu2013depth`, bioinformatics :cite:`lesk2013introduction,baldi2001bioinformatics`, machine vision :cite:`prince2012computer,ali2010hardware,tomasi2010fine`, text mining :cite:`weiss2010fundamentals,aggarwal2012mining`, etc.

Two approaches can be used to achieve DT induction phase acceleration:

- Development new algorithmic frameworks or new software tools, which is the dominant approach :cite:`bekkerman2011scaling,choudhary2011accelerating`.
- Development new hardware architectures optimized for accelerating selected machine learning systems

In the open literature a significant number of different architectures for the hardware acceleration of machine learning algorithms have been also proposed. Architectures for the hardware acceleration of SVM learning algorithms have been proposed in :cite:`anguita2003digital`, while architectures for the acceleration of previously created SVMs have been proposed in :cite:`papadonikolakis2012novel,anguita2011fpga,mahmoodi2011fpga,vranjkovic2011new`. Research in the hardware acceleration of ANNs has been particularly intensive. Numerous hardware architectures for the acceleration of already learned ANNs have been proposed :cite:`savich2012scalable,vainbrand2011scalable,echanobe2014fpga`. Also, a large number of hardware architectures capable of implementing ANN learning algorithms in hardware have been proposed :cite:`misra2010artificial,omondi2006fpga,madokoro2013hardware`. On the other hand, in the field of hardware acceleration of DTs majority of papers focus on the acceleration of already created DTs :cite:`struharik2009intellectual,li2011low,saqib2015pipelined`, while hardware acceleration of DT inference is scarcely covered. Reconfigurale hardware accelerator, proposed in :cite:`vranjkovic2015reconfigurable`, is particularly interesting since it is capable of accelerating DTs, SVMs and ANNs. This is the only architecture, known to the authors, that is capable of accelerating different types of machine learning classifiers. As far as authors are currently aware, there are only two papers on the topic of hardware acceleration of DT induction algorithms :cite:`struharik2009evolving,chrysos2013hc`. However, in these papers the algorithms using greedy top-down DT induction approach have been accelerated. In :cite:`struharik2009evolving` incremental DT induction algorithm is completely accelerated in hardware, and EA is used to calculate the optimal coefficient vector one node at a time. In :cite:`chrysos2013hc` a HW/SW approach was used to accelerate the computationally most demanding part of the well known CART incremental DT induction algorithm.

To further improve the classification performance, ensemble classifier systems :cite:`rokach2010ensemble` have been proposed instead of the single classifier systems. Ensemble classifier combines predictions from several individual classifiers in order to obtain a classifier that outperforms every one of them. Ensemble learning requires creation of a set of individually trained classifiers, typically DTs or ANNs, whose predictions are then combined during the process of classification of previously unseen instances. Although simple, this idea has proved to be effective, producing systems that are more accurate than a single classifier.

In the process of creation of ensemble classifiers, two problems have to be solved: ensuring the diversity of ensemble members and devising a procedure for combining individual member predictions in order to amplify correct decisions and suppress the wrong ones. Some of the most popular methods for ensuring ensemble's diversity are Breiman's bagging :cite:`buhlmann2012bagging`, Shapire's boosting :cite:`buhlmann2012bagging`, AdaBoost :cite:`buhlmann2012bagging`, Wolpert's stacked generalization :cite:`ozay2008performance`, and mixture of experts :cite:`jacobs1991adaptive`. Most commonly used combination rules include : majority voting, weighted majority voting and behavior knowledge spaces :cite:`huang1993behavior`.

The main advantage of ensemble classifier over single classifier systems is the higher accuracy and greater robustness of ensemble classifier systems. However, large amounts of memory are needed to store the ensemble classifier and high computing power is required to calculate the ensemble's output, when compared with the single classifier solutions, leading to much longer ensemble inference and instance classification times. This is because ensemble classifiers typically combine 30 or more individual classifiers :cite:`buhlmann2012bagging` so, if we want to get the same performance as with the single classifier system, 30+ times more memory and computing power would be required. Once more, hardware acceleration of ensemble classifier offers a way of achieving this goal.

Concerning the hardware acceleration of ensemble classifier systems, according to our best knowledge, most of the proposed solutions are related to the hardware implementation of ensemble classifiers that were previously inferred in the software. Most of the proposed solutions are concerned with the hardware acceleration of homogeneous ensemble classifiers :cite:`bermak2003compact,osman2009random,van2012accelerating,hussain2012adaptive,struharik2013hardware`. As far as the authors are aware, there is only one proposed solution to the hardware implementation of heterogeneous ensemble classifiers :cite:`shi2008committee`. Please notice, that all these solutions are only capable of implementing ensemble classifiers systems that were previously inferred in software, running on some general purpose processor. Authors are aware of only one paper :cite:`struharik2009evolving`, that proposes an architecture for the hardware evolution of homogeneous ensemble classifier systems based on the DTs. This solution uses the DT inference algorithm that incrementally creates DTs that are members of the ensemble classifier system.

However, in the hardware implementation the main concern is the number of required hardware resources, mainly memory, necessary to implement a DT ensemble classifier. Smaller DTs are preferred because they require less hardware resources for the implementation and lead to ensembles with the smaller hardware footprint. Therefore, algorithms for DT ensemble classifier induction that generate small, but still accurate, DTs are of great interest when the hardware implementation of DT ensemble classifiers is considered. This requirement puts the full DT induction algorithms into focus.

.. bibliography:: hereboy.bib
	:style: unsrt
