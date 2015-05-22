.. |algo| replace:: *EFTI*
.. |cop| replace:: *EFTIP*
.. |A| replace:: :math:`\mathbf{A}`
.. |a| replace:: :math:`\mathbf{a}`
.. |NA| replace:: :math:`N_{A}`
.. |NAM| replace:: :math:`N^{M}_{A}`
.. |NIM| replace:: :math:`N^{M}_{I}`
.. |na| replace:: :math:`\bar{n}`
.. |NI| replace:: :math:`N_{I}`
.. |Da| replace:: :math:`\bar{D}`
.. |Nl| replace:: :math:`N_l`
.. |NlM| replace:: :math:`N^{M}_{l}`
.. |NM| replace:: :math:`N_{M}`
.. |DM| replace:: :math:`D^{M}`
.. |Nc| replace:: :math:`N_{c}`
.. |NP| replace:: :math:`N_{P}`
.. |RA| replace:: :math:`R_{A}`
.. |alpha| replace:: :math:`{\alpha}`
.. |rho| replace:: :math:`{\rho}`
.. |WDTM| replace:: :math:`W_{DTM}`

=========================================================================
A Co-Processor for Evolutionary Full Tree Oblique Decision Tree Induction
=========================================================================

Introduction
============

As a branch of artificial intelligence, machine learning :cite:`flach2012machine,murphy2012machine` comprises set of procedures/algorithms for construction of systems that adapt their behavior to the input data i.e. by "learning" from the data. Important feature of machine learning systems is that they can be built with little knowledge of input data and can perform well on previously unseen data instances (generalization property).

In the open literature, a range of machine learning predictive models have been introduced, including decision trees (DTs) :cite:`rokach2007data,rokach2005top`, support vector machines (SVMs) :cite:`abe2005support` and artificial neural networks (ANNs) :cite:`haykin2009neural`. Data mining is a field where machine learning predictive models have been widely used (see e,g. :cite:`witten2005data`), among which DTs, ANNs and SVMs are most popular (e.g. :cite:`rokach2007data,wu2009top,wang2006data`).

Machine learning systems can be constructed using supervised learning, unsupervised learning or any combination of the two techniques. Supervised learning implies using the desired responses to various input data to construct the system, while unsupervised learning implies constructing the system based on input data only. When the supervised learning is used, **the lifetime of a machine learning system** usually comprises two phases: training (induction or learning) and deployment. During the training phase a training set is used to build the system. Training set comprises input data and the desired system responses to that data. Once constructed, the system is ready for deployment, where new, previously unseen data will arrive and the system must provide the responses using the knowledge extracted from the training set.

Machine learning systems can perform various tasks, such as classification, regression, clustering, etc. Classification implies categorizing objects given the list of their attributes. Widely used to represent classification models is a DT classifier, which can be depicted in a flowchart-like tree structure. Due to their comprehensible nature that resembles the human reasoning, DTs have been widely used to represent classification models. Amongst other learning algorithms DTs have several advantages, such as robustness to noise, ability to deal with redundant or missing attributes, ability to handle both numerical and categorical data and **facility of understanding the computation process.**

This paper focuses on oblique binary DTs. The leaves of the DT represent the classes of the problem. The non-leaves (also called nodes in the paper) contain the tests which are performed on the problem instances in order to determine their path through the DT until they reach DT leaves. Each instance of the problem is defined by its attribute vector - **A**. The tests performed by the oblique DT in each node are of the following form:

.. math:: \mathbf{a}\cdot \mathbf{A} = \sum_{i=1}^{n}a_{i}\cdot A_{i} < threshold, 
    :label: oblique_test

where **a** represents the coefficient vector and *threshold* models the afine part of the test. The :num:`Figure #fig-oblique-dt` shows an example of the oblique binary DT.

.. _fig-oblique-dt:

.. figure:: images/dt_traversal.py
    
    An example of the oblique binary DT with one possible traversal path shown in red. 

Each instance starts from the DT root and traverses the DT in order to be assigned a class. If the test condition given by equation :eq:`oblique_test` is **true** in certain node, the DT traversal is continued via left child, otherwise it is continued via right child. Depending on the leaf in which the instance finished after traversal, it is classified into class assigned to that leaf. One possible traversal path is shown in :num:`Figure #fig-oblique-dt` in red. After the traversal the instance was classified into the class :math:`C_{4}`.

There are two general approaches to DT induction: incremental (node-by-node) and full tree induction. Furthermore, the process of finding the optimal oblique DT is a hard algorithmic problem **[ref]**, therefore most of DT induction algorithms use some kind of heuristic for optimization process, which is often some sort of evolutionary algorithm (EA). The :num:`Figure #fig-evolutionary-dt-algorithm-tree` shows the taxonomy of EA for DT induction given in :cite:`RCB12`. Computationally least demanding approach for DT induction is a greedy top-down recursive partitioning strategy for the tree growth, hence most DT induction algorithms use this approach. Naturally, this approach suffers from inability of escaping local optima. Better results are obtained by the inducers that work on full DT, with cost of higher computational complexity.

The training phase is more demanding of the two and can last for hours or even days **[ref]** for practical problems. By accelerating this task, machine learning systems could be trained faster, allowing for shorter design cycles. This might also allow machine learning systems to be rebuilt in real-time for applications that require such rapid adapting **[ref]**.

**da li staviti odakle je uzeta slika. Da li ukloniti? Da li je bitno za dalji rad?**

.. _fig-evolutionary-dt-algorithm-tree:

.. graphviz::
    :caption: Taxonomy of evolutionary algorithms for DT induction.
    
    digraph foo {
        node [ shape=box ]
        nodesep=0.5
        margin = 0.3
        ranksep = "0.3 equally"
        fontsize = 10
        "Evolutionary\n DT" -> "Full DT"
        "Evolutionary\n DT" -> "Components"
        "Full DT" -> "Classification"
        "Full DT" -> "Regression"
        "Classification" -> "Axis-\n Parallel"
        "Classification" -> "Oblique"
        "Regression" -> "Regression\n DT"
        "Regression" -> "Model\n DT"
        "Components" -> "Hyperplanes"
        "Components" -> "Pruning"
        "Components" -> "Other"
    }

**Odakle algoritam? Koju referncu na njega? Da li slati na konferenciju**

The proposed co-processor is used for acceleration of a new DT induction algorithm, called |algo|. |algo| (Evolutionary Full Tree Induction) is an algorithm for full oblique classification DT induction using EA. In the remaining of the paper, the proposed co-processor will be called |cop| (Evolutionary Full Tree Induction co-Processor).

Hardware acceleration of machine learning algorithms receives significant attention in scientific community. Wide range of solutions have been suggested in open literature for various predictive models. Authors are aware of the work that has been done on accelerating SVMs (**where?**) and ANNs (**where?**). However in the field of hardware acceleration of DTs majority of papers focus on acceleration of already formed DTs, i.e. the hardware acceleration of DT induction is **scarcely covered**. The only work on the topic of hardware acceleration of DT induction using EAs that the authors are currently aware of is :cite:`struharik2009evolving`. However, this work focuses on greedy top-down approach where EA is used to calculate optimal coefficient vector one node at a time. Moreover, to our knowledge there are no suggested solutions based on HW/SW co-design.

The |algo| algorithm was chosen to be accelerated by hardware, since it does not use the population of individuals as most of EA-based algorithms do. As a result, less memory is needed for individual storage and induction time is shorter **[kao na primer neka referenca iz surveya]**. Nevertheless, in our experiments it proved to provide smaller DTs with similar or better classification accuracy than other well-known DT inference algorithms.

Being that the EAs are iterative by nature and extensively perform simple computations on the data, |algo| algorithm should benefit from hardware acceleration. It was decided to design |cop| co-processor to accelerate the most computationally intensive part of the algorithm. Advantage of the HW/SW co-design approach is that the proposed co-processor can be used with wide variety of EA-based DT induction algorithms, besides the one described here. **[referenca ka nekom survey-u, ili ovog sto imam ili iz njegovih referenci]**

|algo| algorithm
================

This section describes the |algo| iterative algorithm for full DT induction based on EA. It requires only one individual for the induction, which presents the best DT evolved up to the current iteration. The DT is induced from the training set. Since the algorithm is performing supervised learning, the training set consists of the problem instances which have the known class. |algo| algorithm starts from the randomized one-node DT and iteratively tries to improve on it. In each iteration DT is slightly changed, i.e. mutated, and let to perform classification of the training set instances. The classification results are then compared with the known classification given in the training set. If the newly mutated DT provides better classification results than its predecessor, it is taken as the new current best individual, i.e. in the next iteration it will become the base for the mutation. This process is repeated for the desired number of iterations, after which the algorithm exits and the best DT individual is returned. Once the DT is formed this way, it will be used to classify new instances of the problem.

The :num:`Algorithm #fig-algorithm-pca` shows the algorithmic framework for the |algo| algorithm, which is similar for all EAs. The current best DT individual is called *dt* in the pseudo-code. Please note that all algorithms in this paper are described in Python language style and that many details have been omitted for the sake of clarity.

.. _fig-algorithm-pca:

.. literalinclude:: code/algorithm.py
    :caption: Overview of the |algo| algorithm

The initial DT contains only one non-leaf node (root) and two leaves. The  root test coefficients are obtained by selecting two instances with different class from the training set at random, and adjusting the coefficients in such a way that these two instances take different paths after the root test. This is performed by the *initialize()* function.

There are three main tasks performed by the |algo| algorithm:

- **DT Mutation** - implemented by *mutate()* function
- **Fitness Evaluation** - implemented by *fitness_eval()* function
- **Individual Selection** - trivial step implemented by the last **if** statement. Performs comparison of the fitness of the currently best individual (*dt*) with the fitness of the newly mutated individual (*dt_mut*) and takes *dt_mut* as new current best if it has better fitness.

Next, the details on DT mutation and fitness evaluation tasks will be provided, as well as on their computational complexities. EFTI performs two types of mutations on DT individual:

- Node test coefficients mutation
- DT topology mutation

During each iteration of |algo|, a small portion (|alpha|) of DT nodes' test coefficients is mutated at random. Coefficient is mutated by flipping one of its bits at random position. Every change in node test influences the classification, as the instances take different paths through the DT, hence finishing classified differently. Usually one coefficient per several nodes (dictated by parameter |alpha|) is mutated each iteration, in order for classification result to change in small steps. Parameter |alpha| is adapted dynamically from one iteration to other depending on the speed at which the DT fitness is improving in a manner that |alpha| is increased each iteration there is no improvement, and reset to default minimal value when new individual is selected as current best.

On the other hand, topology mutations represent very large moves in the search space, so they are performed even less often. In every iteration, there is a small chance (|rho|) that a node will either be added to the DT or removed from it. This change either adds an additional test for the classification, or removes one or whole subtree of tests. The node is always added in place of an existing leaf, i.e. never in place of an internal non-leaf node.  The test coefficients of the newly added non-leaf node are calculated in the same way as are the root test coefficients during initialization. On the other hand, if node is to be removed, it is always one of the non-leaf nodes. By adding a test, a new point is created where during classification, instances from different classes might separate and take different paths through the DT and eventually be classified as different. This increases the accuracy of the DT. On the other hand, by removing the unnecessary test the DT is made smaller. Size of the DT is also an important factor in its fitness.

.. _fig-fitness-eval-pca:

.. literalinclude:: code/fitness_eval.py
    :caption: The pseudo-code of the fitness evaluation task.

The fitness of a mutated individual (DT) is evaluated using the training set. The DT is let to classify all the problem instances and the classification results are then compared to the desired classifications specified in the training set. The pseudo-code for this task is given in :num:`Algorithm #fig-fitness-eval-pca`. The input parameter *dt* is the current DT individual and *train_set* is the training set.

The fitness evaluation task performs the following:

- It finds the distribution of the classes over the leaves of the DT - implemented by the first **for** loop
- It finds the dominant class for each leaf - implemented by the second **for** loop
- It calculates the fitness as a weighted sum of two values: DT accuracy and DT oversize (calculated as the relative difference between the number of leaves in DT and total number of classes in training set) - implemented by the last four statements.

First, the class distribution is determined by letting all the instances from the training set traverse the DT, i.e. by calling the *find_dt_leaf_for_inst()* function whose pseudo-code is given in :num:`Algorithm #fig-find-dt-leaf-for-inst-pca`. This function uses *evaluate_node_test()* function in each iteration to determine the traversal path and returns the ID of a leaf node into which the instance finished. The traversal is performed in the manner depicted in the :num:`Figure #fig-oblique-dt` where one possible path is given by the red line.

.. _fig-find-dt-leaf-for-inst-pca:

.. literalinclude:: code/find_dt_leaf_for_inst.py
    :caption: The pseudo-code of the procedure for determining the end-leaf for an instance.

The *evaluate_node_test()* function performs the node test evaluation given by equation :eq:`oblique_test`. The pseudo-code of this function is given in :num:`Algorithm #fig-evaluate-node-test-pca`.

.. _fig-evaluate-node-test-pca:

.. literalinclude:: code/evaluate_node_test.py
    :caption: The pseudo-code of the function for node test evaluation.

Next step in the fitness evaluation process (:num:`Algorithm #fig-fitness-eval-pca`) is to calculate the class distribution matrix. The classes of all the instances from the training set are known and read for each instance into the *instance_class* variable (from the *fitness_eval()* function). Based on the leaf nodes' IDs returned by *find_dt_leaf_for_inst()* and the *instance_class* variable value, the distribution matrix is updated. The :math:`d_{i,j}` element of the distribution matrix contains the number of instances of class *j* that finished into the leaf node with ID *i* after DT traversal. After all the instances from training set traverse the DT, this matrix contains the distribution of classes among the leaf nodes.

Second, the next loop of the *fitness_eval()* finds the dominant class for each leaf node. Dominant class for a leaf node is the class having the largest percentage of instances finishing the traversal in that leaf node. Formally, the dominant class *k* of the leaf node with ID *i* is:

.. math:: k | (d_{i,k} = \max_{j}(d_{i,j}))
    :label: dominant_class

If we were to do a classification run with the current DT individual over the training set, the maximum accuracy would be attained if all leaf nodes were assigned their corresponding dominant classes. Thus, each instance which finishes in a certain leaf node, that is of the node's dominant class is added to the number of hits (the *hits* variable of the :num:`Algorithm #fig-fitness-eval-pca`), otherwise it is qualified as a miss.

Fitness is calculated as a weighted sum of two values: DT accuracy and DT oversize. The accuracy is calculated as the percentage of classification hits, i.e. the number of instances that are of the dominant class of a node they finished in after the traversal. DT oversize is calculated as the relative difference between the number of leaves in DT (obtained via *leaves_cnt()* function) and total number of classes in training set (obtained via *class_cnt()* function). In order to be able to classify correctly all training set instances, after the induction DT needs to have at least one leaf for each class which occurs in the training set. Therefore, DTs start to suffer penalties to the fitness only when the number of DT leaves exceeds the total number of classes in the training set.

Complexity of |algo| algorithm
------------------------------

The computational complexity of the |algo| algorithm can be calculated using the algorithm pseudo-code. Since individual selection is performed in constant time it can be omitted, and the total complexity can be computed as:

.. math:: max\_iter\cdot(O(mutate) + O(fitness\_eval))
    :label: cplx_algo_tot_components

Let *n* be the number of non-leaf nodes in DT. In the worst case, the depth of the DT equals the number of non-leaf nodes:

.. math:: D=n
	:label: depth

Let |NA| equal the size of attribute (|A|) and coefficient (|a|) vectors. Each non-leaf node in DT has |NA| + 1 (*threshold*) coefficients, and the portion |alpha| is mutated each iteration, so the complexity of mutating coefficients is:

.. math:: O(\alpha \cdot n \cdot \NA)
	:label: cplx_mut_coef

The topology can be mutated by either adding or removing the node from the DT. When the node is removed, only a pointer to the removed child is altered so the complexity is:

.. math:: O(1)
	:label: cplx_rem_node

When the node is added, the new set of node test coefficients needs to be calculated, hence the complexity of:

.. math:: O(\NA)
	:label: cplx_add_node

Since :math:`\rho\ll\alpha\cdot n` the complexity of the whole DT Mutation task sums to:

.. math:: O(\alpha \cdot n \cdot \NA + \rho (O(1)+O(\NA))) = O(\alpha \cdot n \cdot \NA)
    :label: cplx_mutation

Let |NI| be the number of instances in the training set, |Nl| the number of leaves and |Nc| the total number of classes in the classification problem. The number of leaves in binary DT is:

.. math:: N_l = n + 1
    :label: leaves_cnt

Once the number of hits is determined, fitness can be calculated in constant time :math:`O(1)`, hence the complexity of whole *fitness_eval()* function is:

.. math:: N_I\cdot O(find\_dt\_leaf\_for\_inst) + O(N_l\cdot N_c) + O(1)
    :label: fitness_eval

As for the *find_dt_leaf_for_inst()* function, the complexity can be calculated as:

.. math:: D\cdot O(evaluate\_node\_test),
    :label: find_dt_leaf

and the complexity of the node test evaluation is:

.. math:: O(\NA)
    :label: node_test_eval

By inserting equation :eq:`node_test_eval` into the equation :eq:`find_dt_leaf`, and then both of them into the equation :eq:`fitness_eval`, we obtain the complexity for the *fitness_eval()* function:

.. math:: N_{I}\cdot D\cdot\NA + \Nl\cdot N_c
    :label: fitness_eval_tot

By inserting equations :eq:`fitness_eval_tot`, :eq:`cplx_mutation`, :eq:`leaves_cnt` and :eq:`depth` into the equation :eq:`cplx_algo_tot_components`, we obtain the total complexity of |algo| algorithm:

.. math:: max\_iter\cdot(N_I\cdot n\cdot\NA + n\cdot N_c + \alpha \cdot n \cdot \NA)
    :label: cplx_all_together    

Since :math:`\alpha\cdot n \ll N_I\cdot n` the mutation insignificantly influences the complexity and can be disregarded. We finally obtain that |algo| algorithm complexity is dominated by the fitness evaluation complexity, and sums up to:

.. math:: O(max\_iter\cdot(N_I\cdot n\cdot\NA + n\cdot N_c))
    :label: cplx_final

It is clear from equation :eq:`cplx_final` that *fitness_eval()* function is a good candidate for hardware acceleration, while the mutation tasks can be left in software since they insignificantly influence the complexity of the |algo| algorithm.

Profiling results
-----------------

To confirm the results obtained by the computational complexity analysis the software profiling was performed on the |algo| algorithm's C implementation. Software implementation was developed using many optimization techniques:

- arithmetic operation on 64-bit operands only (optimized for 64-bit CPU), 
- loop unfolding for node test evaluation loop :num:`Figure #fig-evaluate-node-test-pca`, 
- maximum compiler optimization settings, etc.

To perform the experiments 21 datasets, presented in :num:`Table #tbl-uci-datasets`, were selected from the UCI benchmark datasets database :cite:`newman1998uci`. UCI database is commonly used in the machine learning community to estimate and compare performance.

.. tabularcolumns:: l p{30pt} p{40pt} p{40pt} p{40pt}

.. _tbl-uci-datasets:

.. list-table:: Characteristics of the UCI datasets used in the experiments
    :header-rows: 1 
    
    * - Dataset Name
      - Short Name
      - No. of attributes
      - No. of instances
      - No. of classes
    * - Australian Credit Approval
      - ausc
      - 14
      - 690
      - 2
    * - Credit Approval
      - ca
      - 15
      - 699
      - 2
    * - Car Evaluation
      - car
      - 6
      - 1728
      - 4
    * - Contraceptive Method Choice
      - cmc
      - 9
      - 1473
      - 3
    * - Cardiotocography
      - ctg
      - 21
      - 2126
      - 10
    * - German Credit Data
      - ger
      - 24
      - 1000
      - 2
    * - Japanese Vowels
      - jvow
      - 14
      - 4274
      - 9
    * - Page Block Classification
      - page
      - 10
      - 5473
      - 5
    * - Pima Indians Diabetes
      - pid
      - 8
      - 768
      - 2
    * - Parkinson Speech
      - psd
      - 27
      - 1040
      - 2
    * - Seismic Bumps
      - sb
      - 18
      - 2584
      - 2
    * - Image Segmentation
      - seg
      - 18
      - 2310
      - 7
    * - Sick
      - sick
      - 29
      - 3722
      - 2
    * - SPECT Heart
      - spect
      - 22
      - 267
      - 2
    * - Stell Plates Faults
      - spf
      - 21
      - 1941
      - 7
    * - Thyroid Disease
      - thy
      - 29
      - 3722
      - 4
    * - Vehicle Silhouettes
      - veh
      - 18
      - 846
      - 4
    * - Congressional Voting Records
      - vote
      - 16
      - 435
      - 2
    * - Vowel Recognition
      - vow
      - 10
      - 990
      - 11
    * - Waveform Database Generator
      - w21
      - 21
      - 5000
      - 3
    * - Wall Following Robot Navigation
      - wfr
      - 24
      - 5456
      - 4

Software implementation of |algo| algorithm was compiled using GCC 4.8.2 compiler, run on AMD Phenom(tm) II X4 965 (3.4 GHz) computer and profiled using GProf for each of the tests listed in :num:`Table #tbl-uci-datasets`. The results obtained by profiling were consistent with the algorithm complexity analysis performed in the previous chapter and are shown in :num:`Figure #fig-profiling-plot`. The figure shows percentage of time spent in the *fitness_eval()* function and its subfuctions for each dataset. In average, |algo| spent 99.4% of time calculating the fitness of the individual. 

.. _fig-profiling-plot:

.. plot:: images/profiling_plot.py
    :width: 100%
    
    Percentage of time spent in the *fitness_eval()* function and its subfuctions for each dataset listed in :num:`Table #tbl-uci-datasets`

The results of one example profiling experiment on the *veh* dataset are shown in :num:`Figure #fig-profiling`. The results are given in tabular fashion with each row providing the profiling data for one function. Following data are given for each function:

- **Time** - Total amount of time spent in the function  
- **Calls** - Total number of calls to the function
- **% Time** - Percentage of time spent in the function relative to the total execution time.

.. _fig-profiling:

.. figure:: images/profiling.png
    
    Profiling results of the |algo| algorithm C implementation.

The |algo| algorithm has obvious computational bottleneck in the fitness evaluation task, which takes 99.4% of computational time on average. So the fitness evaluation is an undoubtful candidate for hardware acceleration. Since the DT mutation task takes insignificant amount of time to perform, it was decided for it to be left in software. Further advantage of leaving the mutation in software is the ease of changing and experimenting with this task. Many other algorithms can then be implemented in software and make use of the hardware accelerated fitness evaluation task like: Genetic Algorithms (GA), Genetic Programming (GP), Simulated Annealing (SA), etc.

Co-processor for DT induction - |cop|
=====================================

The proposed |cop| co-processor performs the task of determining the accuracy of the DT individual for the fitness evaluation task of the DT induction, i.e. it calculates the number of hits contained in the *hits* variable of the :num:`Algorithm #fig-fitness-eval-pca`. The co-processor is connected to the CPU via AXI4 AMBA bus, which can be used by software to completely control the |cop| operation:

- Download the training set
- Download the DT description
- Start the accuracy evaluation
- Read the results

.. _fig-system-bd:

.. figure:: images/system_bd.py
    :width: 100%
    
    The |cop| co-processor structure and integration with host CPU

The major components of the |cop| co-processor and their connections are depicted in the :num:`Figure #fig-system-bd`:

- **Classifier**: Performs the DT traversal for each instance, i.e. implements the *find_dt_leaf_for_inst()* function in :num:`Algorithm #fig-find-dt-leaf-for-inst-pca`. The classification process is pipelined, with each stage performing node test calculations for one DT level. |DM| is the number of pipeline stages and thus the maximum supported depth of the induced DT. For each instance in training set, the Classifier outputs the ID assigned to the leaf in which the instance finished the traversal (please refer to *fitness_eval()* function :num:`Algorithm #fig-fitness-eval-pca`).
- **Training Set Memory**: The memory for storing all training set instances that should be processed by the |cop| co-processor.
- **DT Memory Array**: The array of memories used to store the DT description with elements :math:`L_{1}` through :math:`L_{D^{M}}`. The Classifier calculates node tests for each DT level in parallel. Each Classifier pipeline stage requires its own memory that holds description of all nodes on the DT level it is associated with.
- **Accuracy Calculator**: Calculates the accuracy of the DT based on the classification data received from the Classifier. For each instance of the training set, the Classifier supplies the ID of the leaf in which the instance finished. Based on this information, the Accuracy Calculator updates the distribution matrix and calculates the number of hits which is sent to the Control Unit and stored in the memory-maped register, ready to be read by the user.
- **Control Unit**: Acts as a bridge between the AXI4 and internal protocols and controls the accuracy evaluation process.

Classifier
----------

Classifier module performs the classification of an arbitrary set of instances on an arbitrary binary oblique DT. The Classifier was implemented using modified design described in :cite:`struharik2009intellectual`. The original architecture from :cite:`struharik2009intellectual` was designed to perform the classification using already induced DTs, hence was adapted so that it could be used in |algo| algorithm for DT induction as well, and is shown in :num:`Figure #fig-dt-classifier-bd`.

.. _fig-dt-classifier-bd:

.. figure:: images/classifier.py
    
    Classifier architecture.

The Classifier performs the DT traversal for each instance (example traversal is shown by red line in :num:`Figure #fig-oblique-dt`), i.e. implements the *find_dt_leaf_for_inst()* function from the :num:`Algorithm #fig-find-dt-leaf-for-inst-pca`. The traversal of an instance starts at the root node of the DT and continues until a leaf is reached and the path it takes is determined by the outcome of node tests (given by the equation :eq:`oblique_test`). For each traversal, only one node per DT level is visited, so there is only one node test performed per DT level. Hence, this process is suitable for pipelining with one stage per DT level. The Classifier module therefore consists of a chain of NTE (Node Test Evaluators) whose number |DM|, determines the maximum depth of the DT that can be induced by the current hardware instance of |cop| co-processor. |DM| value can be specified by the user during the design phase of |cop|.

Each NTE can perform node test calculation for any DT node of the corresponding DT level. :math:`NTE_1` always processes the root DT node, however, which nodes are processed by other stages, depends on the path of traversal for each individual instance. Every stage has one sub-module of DT Memory Array associated to it that holds the descriptions of all the nodes on that DT level.

Inter-NTE interface comprises the following buses: 

- **Instance bus** - passes the instance description to the next NTE as the instance traverses the DT.
- **Leaf ID bus** - if the instance has already been classified into a DT leaf, passes the ID of that leaf to the next NTE. Otherwise, it passes a zero. Based on this information, next NTE will know whether the instance has already been classified, meaning that no further tests need to be performed.
- **Child ID bus** - passes to the next NTE the ID of the non-leaf node through which the traversal is to be continued. Based on this information, the next NTE will know which node's test (out of all non-leaf nodes on NTE's corresponding DT level) should be performed on the instance. 

For each instance received at the Classifier input, the first NTE block processes the calculation given by equation :eq:`oblique_test` for the attributes of received instance |A| and root node coefficients |a|. It then decides on how to proceed with DT traversal: via left or via right child. The selected child can be either a leaf or non-leaf node. If the child is a non-leaf node, its ID is output using *Leaf ID Output* port to the next pipeline stage where the traversal is continued. On the other hand, if the child is a leaf, the classification is done and the ID of a leaf node is output to next pipeline stage informing it that no further calculation needs to be done for this instance. Each NTE calculation described above corresponds to one iteration of the *find_dt_leaf_for_inst()* function loop (:num:`Figure #fig-find-dt-leaf-for-inst-pca`), and NTE outputs correspond to the *cur_node_id* variable. The instance is also passed to the next stage using *Instance Output* port along with the child node ID using *Child ID Output* port, since next stage will perform the calculation on it as well, i.e. the instance traverses to the next DT level.

All subsequent stages operate in similar manner, except that in addition they also receive the calculation results from their predecessor. Somewhere along the NTE chain all the instances will be classified into some leaf. This information is output from the Classifier module via *Leaf ID Output* port to the Accuracy Calculator (together with the corresponding instance description via *Instance Output* port) in order to update the distribution matrix and calculate the final number of hits.

If NTE receives the non-zero value at the *Leaf ID Input* port, meaning that the instance is already classified, it simply passes this information onward and disregards internal computations. On the other hand, if zero is received at the *Leaf ID Input*, then the *Child ID Input* contains a valid non-leaf node ID of the corresponding DT level, and the following is performed:

1. the node coefficients |a| are fetched from the DT Memory Array sub-module using *Child ID Input* value as the index,
2. node test calculation is performed according to equation :eq:`oblique_test`, and
3. the leaf ID and the child ID values are calculated based on the outcome of the node test and output to the next NTE via *Leaf ID Output* and *Child ID Output*, along with the training set instance.

The NTE operation is again pipelined internally for maximal throughput. Block diagram in the :num:`Figure #fig-dt-test-eval-bd` shows the architecture of the NTE module.

.. _fig-dt-test-eval-bd:

.. figure:: images/evaluator.py
    
    NTE (Node Test Evaluator) block architecture

The NTE module's main task is the calculation of sum of products given by the equation :eq:`oblique_test`. The maximum supported number of attributes per instance - |NAM|, is the value which can be specified by the user during the design phase of |cop|. If the instances have less than |NAM| number of attributes, the surplus inputs should be supplied with zeros in order not to affect the sum. 

By using only two input multipliers and adders, the computation is parallelized and pipelined as much as possible. The multiplications are performed in parallel for all |NAM| coefficient and attribute pairs. Since there are only two input adders at disposal and the |NAM|-rnary sum is needed, the tree of two input adders is necessary, that is :math:`\left \lceil log_{2}(\NAM)  \right \rceil` deep. The total number of pipeline stages |NP| needed equals the depth of the adder tree, plus a DT Memory fetch and the multiplication stage:

.. math:: N_{P}=\left \lceil log_{2}(\NAM) + 2 \right \rceil
	:label: np

The Instance Queue and Node Queue are necessary due to the pipelining. Instance Queue delays the output of the instance to the next NTE module until its corresponding node test calculation is done, i.e. all the NTE internal pipeline stages are passed and the *Leaf ID Output* and *Child ID Output* are determined. Node Queue is necessary since the *Leaf ID Input* and *Child ID Input* are received at the first pipeline stage, but are not needed until the last pipeline stage. Additionally, in order not to use separate memory for the information about the node's children, it is kept together with the node test coefficients in DT Memory and read at first pipeline stage. Hence, Node Queue is also used to memorize information about node's children together with the *Leaf ID Input* and *Child ID Input* and make it available at the last stage of the pipeline, where it is needed for making a traversal choice. 

At the last pipeline stage, the result of the calculation is compared with the node test *threshold* to determine if the traversal will continue to the left or right child. Along with node test coefficients |a| in the DT Memory, the following data about child nodes is stored: *Child Left ID*, *Child Right ID*, *Leaf Left ID* and *Leaf Right ID*. If the left child is a non-leaf node, the *Child Left ID* contains the ID of the child node in the next DT level, i.e. index of the child node in the next node's DT Memory sub-module, and the *Leaf Left ID*  equals 0. On the other hand, if left child is a leaf node, *Leaf Left ID* has non-zero value representing the leaf node ID, while *Child Left ID* is disregarded. The right child IDs are interpreted analogously. Depending on the decision to continue with the traversal to the left or to the right, *Child Left ID* or *Child Right ID* is output to the *Child ID Output* and *Leaf Left ID* or *Leaf Right ID* is output to the *Leaf ID Output* for the next NTE module. 

However, when NTE receives the non-zero value for the *Leaf ID Input*, the calculation result is disregarded (it is performed nevertheless in order to simplify the design) and the *Leaf ID Input* is simply forwarded to the *Leaf ID Output*.

Training Set Memory
-------------------

This is the memory that holds all training set instances that should be processed by the |cop| co-processor. It is a two-port memory with ports of different widths and is shown in :num:`Figure #fig-inst-mem-org`. It is comprised of 32-bit wide stripes in order to be accessed by the CPU via 32-bit AXI. Each instance description, spanning multiple stripes, comprises the following fields:

- Array of instance attribute values: :math:`\mathbf{A}_{1}` to :math:`\mathbf{A}_{\NAM}`, each :math:`R_A` (parameter specified by the user at design time) bits wide, 
- Instance class: *C*, which is :math:`R_C` (parameter specified by the user at design time) bits wide

Training set memory can be accessed via two ports:

- Port A: Read/Write port accessed by the CPU via AXI interface, 32-bit wide
- Port B: Read port for parallel read-out of the whole instance, :math:`R_{A}\cdot\NAM + R_{C}` bits wide

Width of the Port B is determined at design phase of |cop| and corresponds to the instance of the maximal size supported, i.e. the instance with the |NAM| number of attributes. When co-processor is used for solving a problem with less attributes, the Training Set Memory fields of unused attributes need to be filled with zeros in order to obtain correct calculation.

.. _fig-inst-mem-org:

.. figure:: images/inst_mem.py
    
    Training set memory organization

Instance attributes are encoded using arbitrary fixed point number format, specified by user. However, the same number format has to be used for all instances' attribute encodings. The total maximum number of instances (|NIM|), i.e. the depth of the Training Set Memory is selected by the user at design phase of |cop| and determines the maximum possible training set size that can be stored inside the |cop| co-processor.

DT Memory Array
---------------

.. todo::
	**Da li neki epitet dodatni uz DT Memory Array(structural memory?). DT description - da li dodatni epitet DT structural description, information**

This memory holds the DT description. For each NTE of the Classifier module there is one DT Memory Array sub-module (:math:`L_1 - L_{D^M}` blocks in :num:`Figure #fig-system-bd`), that holds the description of all nodes at the corresponding DT level. Each sub-module of the DT Memory Array is a two-port memory with ports of different widths and is shown in :num:`Figure #fig-dt-mem-array-org`. Each element is comprised of 32-bit wide stripes in order to be accessed by the CPU via 32-bit AXI. 

.. _fig-dt-mem-array-org:

.. figure:: images/dt_mem.py
    
    DT memory organization

Each DT Memory Array sub-module contains a list of node descriptions as shown in :num:`Figure #fig-dt-mem-array-org`, comprising the following fields:

- Array of node test coefficients: :math:`\mathbf{a}_{1}` to :math:`\mathbf{a}_{\NAM}`, each :math:`R_A` bits wide
- The node test threshold: *threshold*, which is :math:`R_A` bits wide
- ID of the left child if it is leaf: *Leaf Left ID*, which is :math:`R_{Leaf\ ID}` (parameter specified by the user at design time) bits wide
- ID of the left child if it is non-leaf: *Child Left ID*, which is :math:`R_{Child\ ID}` (parameter specified by the user at design time) bits wide
- ID of the right child if it is leaf: *Leaf Right ID*, which is :math:`R_{Leaf\ ID}` bits wide
- ID of the right child if it is non-leaf: *Child Right ID*, which is :math:`R_{Child\ ID}` bits wide 

The total maximum number of nodes storable in the DT Memory Array sub-module - :math:`N^{M}_{nl}`, is a parameter specified by the user at design phase of |cop|. This value imposes a constraint on the maximum number of nodes that the induced DT can have per level.

The parameter :math:`R_{Leaf\ ID}` imposes a constraint on the maximal number of leaves induced DT can have, since the field of that width can encode :math:`2^{R_{Leaf\ ID}} - 1` number of different IDs. Similarly, the parameter :math:`R_{Child\ ID}` has to be selected large enough so that child ID fields can encode all :math:`N^{M}_{nl}` possible nodes on single DT level.

As it was already described in the sub-section `Classifier`_, for both left and right child IDs, if the leaf ID field has non-zero value, the child is interpreted as a leaf and the child ID field value is ignored. On the other hand, if the leaf ID field value is zero, the child ID field value represents the index in the next DT Memory Array sub-module at which the child description is located.

DT Memory Array sub-module can be accessed via two ports:

- Port A: Read/Write port accessed by the CPU via AXI interface, 32-bit wide
- Port B: Read port for parallel read-out of the whole node description, |WDTM| (given by :eq:`w-dt`) bit wide.

.. math:: \WDTM = R_{A}\cdot\NAM + R_{threshold} + 2\cdot R_{Leaf\ ID} + 2\cdot R_{Child\ ID}
    :label: w-dt

Width of the Port B is determined at design phase of |cop| and corresponds to the instance of the maximal size supported, i.e. the instance with the |NAM| number of attributes.

Accuracy Calculator
-------------------

This module calculates the accuracy of the DT via *distribution* matrix as described by :num:`Algorithm #fig-fitness-eval-pca`. It monitors the output of the Classifier module, i.e the training set classification, and for each instance in the training set, based on its class (*C*) and the leaf in which it finished the traversal (*Leaf ID*), appropriate element of the *distribution* matrix is incremented. Accuracy Calculator block is shown in :num:`Figure #fig-fit-calc-bd`.

.. _fig-fit-calc-bd:

.. figure:: images/fitness_calc_bd.py
    
    Accuracy Calculator block diagram

In order to speed up the dominant class calculation (second loop of the *fitness_eval()* function in :num:`Algorithm #fig-fitness-eval-pca`), the Accuracy Calculator is implemented as an array of calculators, whose each element keeps track of the distribution for the single leaf node. Hence, the dominant class calculation (*dominant_class_cnt*) can be done in parallel for each leaf node. The number of elements in the array equals maximum number of leaf nodes parameter - |NlM| which can be specified by the user during the design phase of |cop|. This value imposes a constraints on the maximum number of leaves in DT. Each calculator comprises:

- **Class Distribution Memory**: for keeping track of the class distribution of the corresponding leaf node
- **Incrementer**: Updates the memory based on the Classifier output
- **The dominant class calculator**: For each training set class, calculates how many instances of that class were classified in the corresponding leaf node. It then finds class that has the largest number of instances in the corresponding leaf node (dominant class), and outputs that number (*dominant_class_cnt*). If the instance's class equals the dominant class of the leaf node it finished the traversal in, it is considered a hit, otherwise it is considered a miss. Hence, *dominant_class_cnt* represents the number of hits for the corresponding leaf node.

Accuracy Calculator then sums the hits for all leaf node calculators and outputs the sum as number of hits for whole DT. The number is then stored in the register of the Control Unit from where it can be read-out by the CPU.

Control Unit
------------

The module provides AXI4 interface access to the configuration and status registers as well as DT Memory Array and Training Set Memory. The following registers are provided:

- **Operation Control** - allows user to start, stop and reset the |cop| co-processor.
- **Instance Number** - allows user to tell |cop| the number of instances in the training set.
- **Status Register** - informs the user when the fitness evaluation task is done and allows the user to read the calculated number of hits. 

Required Hardware Resources and Performance
-------------------------------------------

The |cop| co-processor is implemented as an IP core with many customization parameters that can be configured at design phase and are given in :num:`Table #tbl-cop-params`. These parameters mainly impose constraints on the maximum size of the DT that can be induced and the maximum size of the training set that can be used. 

.. role:: raw(raw)
   :format: latex

.. tabularcolumns:: c p{0.4\linewidth} p{0.4\linewidth}

.. _tbl-cop-params:

.. list-table:: Parameters that can be configured at design phase of the |cop| co-processor
    :header-rows: 1 
    :widths: 15 30 30
    
    * - Parameter
      - Description
      - Constraint
    * - |DM|
      - The number of NTEs in the Classifier
      - The maximum depth of the induced DT 
    * - |NAM|
      - Determines: Training Set Memory width, :raw:`\newline` 
        DT Memory Array sub-module width, :raw:`\newline` 
        NTE adder tree size.
      - The maximum number of attributes training set can have
    * - :math:`R_A`
      - Determines: Training Set Memory width, :raw:`\newline` 
        DT Memory Array sub-module width, :raw:`\newline` 
        NTE adder tree size.
      - Resolution of induced DT coefficients
    * - :math:`C^M`
      - Accuracy Calculator memory depth
      - The maximum number of training set and induced DT classes
    * - :math:`R_C`
      - Parameter must be at least :math:`log_{2}(C^M)`
      - --
    * - |NlM|
      - Number of Accuracy Calculator Elements
      - The maximum number of leaves of the induced DT 
    * - |NIM|
      - Training Set Memory depth
      - The number of training set instances that can be stored in |cop| co-processor
    * - :math:`N^{M}_{nl}`
      - DT Memory Array sub-module depth
      - The maximum number of nodes per level of the induced DT 

The amount of resources required to implement |cop| co-processor is a function of the parameters given in the :num:`Table #tbl-cop-params` and is given in the :num:`Table #tbl-req-res` for various resource types.

.. tabularcolumns:: p{0.2\linewidth} p{0.2\linewidth} p{0.5\linewidth}

.. _tbl-req-res:

.. list-table:: Required hardware resources for the |cop| architecture implementation
    :header-rows: 1 
    
    * - Resource Type
      - Module
      - Quantity
    * - RAMs
      - Training Set Memory
      - :math:`\NIM\cdot (R_A*\NAM + R_C)`
    * - (total number of bits)
      - DT Memory Array
      - |WDTM|
    * - 
      - Accuracy Calculator
      - :math:`\NlM\cdot C^{M}\cdot \left \lceil log_{2}(N^{M}_{I})  \right \rceil`
    * - 
      - NTE
      - :math:`N_P\cdot (R_{A}\cdot\NA + R_{C}) +` :raw:`\newline`
        :math:`N_P\cdot (R_{threshold} + 2*R_{Leaf\ ID} + 2*R_{Child\ ID})`
    * - Multipliers
      - NTE
      - :math:`\DM\cdot \NA`
    * - Adders
      - NTE
      - :math:`\DM \left \lceil log_{2}(\NA)  \right \rceil`
    * - Incrementers
      - Accuracy Calculator
      - :math:`\NlM`

Second, the number of clock cycles required to determine the DT accuracy will be discussed. The Classifier has a throughput of one instance per clock cycle, hence all instances are classified in :math:`N_I` cycles. However, there is an initial latency equal to the length of the pipeline :math:`N_{P}`. Furthermore, the Accuracy Calculator needs extra time after the classification has finished in order to determine the dominant class which is equal to the total number of classes in the training set :math:`N_{C}`, plus the time to sum all dominant class hits, which is equal to the number of active leaves :math:`N_{l}`. Finally, the time required to calculate DT accuracy, expressed in clock cycles, is given by:

.. math:: fitness\_evaluation\_time = N_{I} + N_{P} + N_{C} + N_{l} \ clock\ cycles,

and is thus dependent on the training set size.

.. todo::
    
    **Fali prica o skalabilnosti predlozenog resenja... Kako resavamo problem ako nam je trening set veci od kapaciteta Training Set memorije?**

Software for |cop| assisted DT induction
========================================

With |cop| co-processor performing fitness evaluation task, remaining functionality of the |algo| algorithm (:num:`Algorithm #fig-algorithm-pca`) is implemented in software. Furthermore, software needs to implement procedures for interfacing the |cop| co-processor as well. The pseudo-code for software used in the co-design is given by :num:`Algorithm #fig-co-design-sw-pca`.

.. _fig-co-design-sw-pca:

.. literalinclude:: code/co_design_sw.py
    :caption: The pseudo-code of the |algo| algorithm using |cop| co-processor 

The only difference to the pure software solution of the main *efti()* function, is that the training set needs to be transfered to the |cop| co-processor, which is performed by the *hw_load_training_set()* function. Since |cop|'s memory space is mapped to the main CPU's memory space via AXI bus, this function simply copies the instances to the memory region corresponding to the Training Set Memory of the |cop|.

The *fitness_eval()* function performs the following:

- uploads the new (mutated) DT description to the |cop|, by changing only the mutated parts in the memory that is mapped to the DT Memory Array of the |cop| via *hw_load_dt_diff()* function,
- initiates the fitness evaluation by writing to the Operation Control register of the |cop| via *hw_start_fitness_eval()* function,
- waits for the fitness evaluation results to become available, by polling the |cop| status register via *hw_finished_fitness_eval()* function,
- fetches the number of hits from the |cop| Status Register via *hw_get_hits()* and calculates the fitness in the same manner as in :num:`Algorithm #fig-fitness-eval-pca`. 

The hardware interface function pseudo-codes were omitted for brevity.

Experiments
===========

In this section the results of the experiments designed to estimate DT induction speedup of the software implementation of the |algo| algorithm using |cop| co-processor over pure software implementation of the |algo| algorithm are given.

Required Hardware Resources
---------------------------

The parameters of the |cop| architecture, whose description is given in :num:`Table #tbl-cop-params`, have been set for the experiments to support all training sets from :num:`Table #tbl-uci-datasets`. The values of the parameters are given in :num:`Table #tbl-exp-params`.

.. tabularcolumns:: p{0.5\linewidth} p{0.07\linewidth} 

.. _tbl-exp-params:

.. list-table:: Characteristics of the UCI datasets used in the experiments
    :header-rows: 1 
    
    * - Parameter
      - Value
    * - DT Max. depth (|DM|)
      - 6
    * - Max. attributes num. (|NAM|)
      - 32
    * - Attribute encoding resolution (:math:`R_{A}`)
      - 16
    * - Class encoding resolution (:math:`R_{C}`)
      - 8
    * - Max. training set classes (:math:`C^{M}`)
      - 16
    * - Max. number of leaves (|NlM|)
      - 16
    * - Max. number of training set instances (|NIM|)
      - 4096
    * - Max. number of nodes per level (:math:`N^{M}_{nl}`)
      - 16  

The |cop| has been implemented using the Xilinx Vivado Design Suite 2014.4 software for logic synthesis and implementation with default synthesis and P&R options. From the implementation report files, device utilization data has been analyzed and information about the number of used slices, BRAMs and DSP blocks has been extracted, and is presented in :num:`Table #tbl-utilization`. The maximum operating frequency of 133 MHz of system clock frequency for the implemented |cop| architecture was attained.

.. tabularcolumns:: l l l l

.. _tbl-utilization:

.. list-table:: FPGA resources required to implement |cop| architecture for DT induction with selected UCI datasets
    :header-rows: 1 
    
    * - FPGA Device
      - Slices
      - BRAMs
      - DSPs
    * - XC7Z020
      - 6587 (55%)
      - 65 (47%)
      - 192 (87%)
    * - XC7Z100
      - 6556 (9%)
      - 65 (9%)
      - 192 (10%)
    * - XC7K325
      - 6750 (13%)
      - 65 (15%)
      - 192 (23%)
    * - XC7VX690
      - 6708 (6%)
      - 65 (4%)
      - 192 (5%)

Given in brackets along with each resource utilization number is a percentage of total resources available on the corresponding FPGA devices that the number represents. :num:`Table #tbl-utilization` shows that implemented |cop| co-processor fits even into the entry level XC7Z020 Xilinx FPGA device of the Zynq series, and takes even smaller percentage of resources on entry- to mid-level Kintex7 and Virtex7 Xilinx FPGA devices (XC7K325 and XC7VX690).

Estimation of Induction Speedup
-------------------------------

Three implementations of |algo| algorithm have been developed for experiments, all of them written in C language:

- **SW-PC**: Pure software implementation for PC
- **SW-ARM**: Pure software implementation for ARM Cortex-A9 processor
- **HW/SW**: Part of the algorithm shown in :num:`Algorithm #fig-co-design-sw-pca` was implemented for ARM Cortex-A9 processor to use the |cop| co-processor implemented in FPGA

For PC implementation the AMD Phenom(tm) II X4 965 (3.4 GHz) platform was used and the software was built using GCC 4.8.2 compiler. For SW-ARM and HW/SW implementations the ARM Cortex-A9 667MHz (Xilinx XC7Z020-1CLG484C Zynq-7000) platform has been used. The software was built using Sourcery CodeBench Lite ARM EABI 4.8.3 compiler (from within Xilinx SDK 2014.4) and the |cop| co-processor was built using Xilinx Vivado Design Suite 2014.4. 

Care was taken in writing the software and many optimization techniques were employed as described in chapter `Profiling results`_.

For each of the datasets from :num:`Table #tbl-uci-datasets`, an experiment consisting of five 5-fold cross-validations has been performed for all three |algo| algorithm implementations and for each cross-validation run the DT induction time has been measured. Software timing was obtained by different means for two platforms:

- For PC platform, the <time.h> C library was used and timing was output to the console
- For ARM platform, TTC hardware timer was used and timing was output via UART

All datasets from :num:`Table #tbl-uci-datasets` were compiled together with the source code and were readily available in the memory, thus there was no loading overhead on the DT induction timings for both pure software experiments. On the other hand, in the HW/SW co-design experiment, datasets needed to be loaded from the CPU memory via AXI bus (via *hw_load_training_set()*), so this operation was excluded from timing analysis in order to make a fair comparison.

The results of the experiments are given in :num:`Table #tbl-results`. For each implementation and dataset, the average induction times of the five 5-fold cross-validation runs are given together with their 95% confidence intervals. The last row of the table provides the average speedup of the HW/SW implementation over both SW-ARM and SW-PC implementations, together with the 95% confidence intervals.

.. tabularcolumns:: l R{0.15\linewidth} R{0.15\linewidth} R{0.15\linewidth}

.. _tbl-results:

.. csv-table:: DT induction times for various |algo| implementations and average speedup of HW/SW implementation over pure software implementations
    :header-rows: 1
    :file: scripts/results.csv

:num:`Table #tbl-results` shows that the average speedup of the HW/SW implementation is 41.9 over the SW-ARM and 3.2 over SW-PC implementation. Speedup varies with different datasets, which is expected since the |algo| algorithm computational complexity is dependent on the dataset as the equation :eq:`cplx_final` suggests. Computational complexity increases as |NI|, |NA|, *n* and |Nc| increase. The number of nodes in DT *n* is dependant on the training set instance attribute values, but can be expected to increase also with |NI|, |NA| and |Nc|. By observing the speedup of the HW/SW implementation over pure software implementations shown in :num:`Figure #fig-speedup` for each dataset and the datasets' characteristics given in :num:`Table #tbl-uci-datasets`, it can be seen that indeed more speedup is gained for datasets with larger |NI|, |NA| and |Nc|.

.. _fig-speedup:

.. plot:: images/speedup_plot.py
    :width: 100%
    
    Speedup of the HW/SW implementation over a) SW-ARM implementation and b) SW-PC implementation, given for each dataset listed in :num:`Table #tbl-uci-datasets`

.. todo::
    
    **Da li je ovaj grafik OK? Nisam znao od kakvih podataka da crtam candlestick...**

:num:`Figure #fig-speedup` and :num:`Table #tbl-results` suggest that HW/SW implementation using |cop| co-processor offers a substantial speedup in comparison to pure software implementations for both PC and ARM. Furthermore, |cop| implementation used in the experiments operates at much lower frequency (133MHz) than both ARM (667MHz) and PC(3.4GHz) platforms, meaning that it is accordingly more energy efficient. Also, if |cop| co-processor were implemented in ASIC, the operating frequency would be increased by a factor of 10-30, and the speedup would increase accordingly.

Conclusion
==========

In this paper a universal reconfigurable co-processor for hardware aided decision tree (DT) induction using evoulutionary approach is proposed. |cop| co-processor is used for hardware acceleration of the fitness evaluation task since this task is proven in the paper to be the execution time bottleneck. The algorithm for full DT induction using evolutionary approach (EFTI) has been implemented in software to use |cop| co-processor implemented in FPGA as a co-processor. Comparison of HW/SW |algo| algorithm implementation with pure software implementations suggests that proposed HW/SW architecture offers substantial speedups for all tests performed on UCI datasets.

.. bibliography:: hereboy.bib
	:style: unsrt
