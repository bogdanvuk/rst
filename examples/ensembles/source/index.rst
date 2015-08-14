.. |algo| replace:: *EFTI*
.. |task| replace:: Task
.. |cop| replace:: *EFTIP*
.. |acep| replace:: *ACEP*
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

==========================================================
Co-Processor for Evolutionary Full Decision Tree Induction
==========================================================

Introduction
============

Machine learning :cite:`flach2012machine,murphy2012machine` is a branch of artificial intelligence field of study that researches algorithms that "learn" from input data and construct systems that make predictions on the data. One of the main features of machine learning systems is the power of generalization, allowing them to perform well on new, unseen data instances after having experienced a learning data set.

Different machine learning systems have been proposed in the open literature, including decision trees (DTs) :cite:`rokach2007data,rokach2005top`, artificial neural networks (ANNs) :cite:`haykin2009neural` and support vector machines (SVMs) :cite:`abe2005support`. They have been especially widely used in the field of data mining (see e,g. :cite:`witten2005data`), with DTs, ANNs and SVMs being the most popular (e.g. :cite:`rokach2007data,wu2009top,wang2006data`).

The learning process, i.e. induction of machine learning systems can either be supervised or unsupervised. When the desired output is supplied together with the input data to the machine learning induction algorithm, the learning is called supervised. On the other hand, when only the input data is available to the inducer, the learning is called unsupervised. In this case the inducer needs to discover the structure and patterns in the input data on its own, which can be a goal in itself. The input data used for learning usually consists of the set of instances (called a training set) of the problem being solved by the machine learning system. The lifetime of a machine learning system usually consists of two phases: training (induction or learning) and deployment. The system is built in the training phase using the training set. During the deployment phase, the constructed system will be faced with new, previously unseen instances and it will provide the output using the knowledge extracted from the training set instances.

Machine learning systems are often employed to perform classification of the input data instances into the set of classes. For this task, the DT is widely used classifier. The DT classifier operation can be represented by a flowchart with the tree structure. This flowchart resembles human reasoning and is thus easily understood, which makes DT a popular choice for classification model representations. Additional advantages of DTs over other machine learning algorithms comprise: robustness to noise, ability to deal with redundant or missing attributes, ability to handle both numerical and categorical data, etc.

Oblique binary classification DTs will be the focus of this paper. The classes of the problem are represented by the DT leaves. The instance is classified by traversing the DT, starting from the root, until it reaches one of the leaves. The traversal path is determined by the tests performed over the instance in each non-leaf (also called a node in the paper) which it encounters during the traversal. Given that the instance is defined by its attribute vector - **A**, the tests performed by the oblique DT in each node are of the following form:

.. math:: \mathbf{a}\cdot \mathbf{A} = \sum_{i=1}^{n}a_{i}\cdot A_{i} < thr, 
    :label: oblique_test

where **a** represents the test coefficient vector and *thr* (abbreviated from threshold) models the afine part of the test. An example of an oblique binary DT traversal is showed in :num:`Figure #fig-oblique-dt`.

.. _fig-oblique-dt:

.. bdp:: images/dt_traversal.py
    
    An example of the oblique binary DT with one possible traversal path shown in red. 

The DT traversal for each instance begins at DT root node and continues until a leaf is reached, when the instance is assigned the class associated with the leaf. Whenever a node is reached during the traversal the test associated with the node (given by equation :eq:`oblique_test`) is evaluated. If the test yields the value **true**, the DT traversal is continued via nodes left child, otherwise it is continued via nodes right child. In :num:`Figure #fig-oblique-dt`, one possible traversal path is shown with red line. In this example, the instance is classified into the class :math:`C_{4}` after the traversal.

In general, DT can be induced in two ways: incrementally (node-by-node) and whole tree at once. Most of DT induction algorithms use some kind of heuristic for optimization process, which is often some sort of evolutionary algorithm (EA), since the finding of the optimal oblique DT is a hard algorithmic problem :cite:`struharik2014inducing`. The greedy top-down recursive partitioning strategy is a computationally least demanding approach for DT induction, hence most DT induction algorithms use this approach. Naturally, this approach suffers from inability of escaping local optima. Better results, especially if DT size is considered, are obtained by the inducers that work in full DT, with cost of higher computational complexity :cite:`struharik2014inducing`.

DT induction phase can be very computationally demanding and can last for hours or even days **[ref]** for practical problems.This is certainly true for full DT inference algorithms. By accelerating this task, machine learning systems could be trained faster allowing for shorter design cycles, or could process large amount of data, which is of particular interest if DTs are used in the data mining applications :cite:`witten2005data`. This might also allow DT learning systems to be rebuilt
in real-time for applications that require such rapid adapting, such as machine vision :cite:`prince2012computer,challa2011fundamentals`, bioinformatics :cite:`lesk2013introduction,baldi2001bioinformatics`, web mining :cite:`liu2007web,russell2013mining`, text mining :cite:`weiss2010fundamentals,aggarwal2012mining`, etc.

In order to accelerate DT induction phase, two general approaches can be used. First approach focuses on developing new algorithmic frameworks or new software tools and is the dominant way of meeting this requirement :cite:`bekkerman2011scaling,choudhary2011accelerating`. Second approach focuses on hardware acceleration of machine learning algorithms, by developing new hardware architectures optimized for accelerating selected machine learning systems.

The proposed co-processor is used for acceleration of a new DT induction algorithm, called |algo|. |algo| (Evolutionary Full Tree Induction) is an algorithm for full oblique classification DT induction using EA. In the remaining of the paper, the proposed co-processor will be called |cop| (Evolutionary Full Tree Induction co-Processor).

Hardware acceleration of machine learning algorithms receives significant attention in scientific community. Wide range of solutions have been suggested in the open literature for various predictive models. Authors are aware of the work that has been done on accelerating SVMs and ANNs, where hardware architectures for acceleration of both learning and deployment phases have been proposed. Architectures for hardware acceleration of SVM learning algorithms have been proposed in :cite:`anguita2003digital`, while architectures for acceleration of previously created SMVs have been proposed in :cite:`papadonikolakis2012novel,anguita2011fpga,mahmoodi2011fpga,vranjkovic2011new`. Research in the hardware acceleration of ANNs has been particularly intensive. Numerous hardware architectures for the acceleration of already learned ANNs have been proposed :cite:`savich2012scalable,vainbrand2011scalable,echanobe2014fpga`. Also, a large number of hardware architectures capable of implementing ANN learning algorithms in hardware have been proposed :cite:`misra2010artificial,omondi2006fpga,madokoro2013hardware`. However in the field of hardware acceleration of DTs majority of papers focus on acceleration of already created DTs :cite:`struharik2009intellectual,li2011low,saqib2015pipelined`. Hardware acceleration of DT induction is scarcely covered. Authors are currently aware of only two papers on the topic of hardware acceleration of DT induction using :cite:`struharik2009evolving,chrysos2013hc`. However, these results focus on accelerating greedy top-down DT induction approaches. In :cite:`struharik2009evolving` incremental DT induction algorithm, where EA is used to calculate optimal coefficient vector one node at a time, is completely accelerated in hardware. In :cite:`chrysos2013hc` authors use a HW/SW approach to accelerate the computationally most demanding part of the well known CART incremental DT induction algorithm. Authors are not aware of any previous work on hardware acceleration of full DT inductions algorithms.

This paper is concerned with the hardware acceleration of a novel full DT evolutionary induction algorithm, called |algo|. |algo| (Evolutionary Full Tree Induction) is an algorithm for full oblique classification DT induction using EA **[nasa referenca]**. As mentioned earlier, full DT induction algorithms typically build better DTs (smaller and more accurate) when compared with incremental DT induction algorithms. However, full DT induction algorithms are more computationally demanding, requiring much more time to build a DT. This is one of the reasons why incremental DT induction algorithms are currently dominating the DT field. Developing a hardware accelerator for full DT induction algorithm should significantly decrease the DT inference time, and therefore make it more attractive. As far as the 
authors are aware, this is the first paper concerning with the hardware acceleration of some full DT induction algorithm.

The |algo| algorithm was chosen to be accelerated by hardware, since it does not use the population of individuals as most of EA-based DT algorithms do. As a result, less memory is needed for individual storage and induction time is shorter **[kao na primer neka referenca iz surveya]**. Nevertheless, it proved to provide smaller DTs with similar or better classification accuracy than other well-known DT inference algorithms, both incremental and full DT **[nasa referenca]**. Being that the EAs are iterative by nature and extensively perform simple computations on the data, |algo| algorithm should benefit from hardware acceleration, as would any other DT induction algorithm based on the EAs. This paper proposes to design |cop| (Evolutionary Full Tree Induction co-Processor) co-processor to accelerate only the most computationally intensive part of the |algo| algorithm, leaving the remaining parts of the algorithm in software. In the paper it is shown that the most critical part of the |algo| algorithm is the training set classification step from the fitness evaluation phase, so |cop| has been designed to accelerate this step in hardware. Another advantage of this HW/SW co-design approach is that the proposed |cop| co-processor can be used with wide variety of other EA-based DT induction algorithms **[referenca ka nekom survey-u, ili ovog sto imam ili iz njegovih referenci]**, to accelerate the training set classification step that is always present during the fitness evaluation phase.

|algo| algorithm
================

In this section, the |algo| algorithm for induction of DT ensembles using full DT induction approach based on EA is described. Only one individual per ensemble member is required for the induction by the |algo| algorithm. Each individual represents the best DT evolved up to the current iteration for it's corresponding ensemble member. Since |algo| uses supervised learning, the training set used to induce the ensemble consists of the problem instances together with their corresponding class memberships. The training set is divided in as many equally large parts as there are members in the ensemble and each member is induced by using its own part of the training set, i.e. its own set of instances. Each ensemble member starts off as a randomly generated one-node DT and the algorithm iteratively tries to improve on it. DTs are slightly changed, i.e. mutated, in each iteration, and let to perform classification of their corresponding training set part. The known training set classification is then used to calculate the quality of the classification results. When the newly mutated DT performs better at the classification than its predecessor, it is promoted to the new current best individual for its ensemble member and will become the base for the mutation in the next iterations, until a better one is found. After the desired number of iterations, the algorithm exits and returns the set of best DT individuals, one per ensemble members. 

The :num:`Algorithm #fig-algorithm-pca` shows the |algo| algorithm entry point. Please note that all algorithms in this paper are described in Python language style and that many details have been omitted for the sake of clarity. The inductions of individual ensemble members are completely decoupled from each another, and can be processed in separate tasks called |task| shown in :num:`Algorithm #fig-task-pca`. The |algo| first divides the training set in the parts using *divide_train_set()* function and stores them in the array *task_train_sets*. Then the result array is created using *initialize_result_array()* function and stored in the *res* array. The *res* array contains one item for each ensemble member, to which the corresponding |task| will output the induced DTs and various miscellaneous corresponding statistical data. 

.. _fig-algorithm-pca:

.. literalinclude:: code/algorithm.py
    :caption: Overview of the |algo| algorithm

Next, the |task| s are created, assigned their corresponding *task_train_sets* item and *res* item, and run. The |algo| waits for a completion of all |task|s and returns the *res* array populated by them.

The :num:`Algorithm #fig-task-pca` shows the algorithmic framework for the each of the |task|s, which is similar for all EAs. The current best DT individual is called *dt* in the pseudo-code. 

.. _fig-task-pca:

.. literalinclude:: code/task.py
    :caption: Overview of the |algo| algorithm

The initial DT contains only one non-leaf node (root) and two leaves. The root test coefficients are obtained by selecting two instances with different classes from the training set at random, and adjusting the coefficients in such a way that these two instances take different paths after the root test. This is performed by the *initialize()* function.

There are three main tasks performed by the |algo| algorithm:

- **DT Mutation** - implemented by *mutate()* function
- **Fitness Evaluation** - implemented by *fitness_eval()* function
- **Individual Selection** - given by the last **if** statement of the :num:`Algorithm #fig-algorithm-pca`, which represents the elemental way of selecting individuals by performing the comparison of the fitness of the currently best individual (*dt*) with the fitness of the newly mutated individual (*dt_mut*) and takes *dt_mut* as new current best if it has better fitness. |algo| algorithm implements a more complex procedure for individual selection which allows, with some probability, for an individual with worse fitness to be selected. However, this was omitted for the sake of brevity. 

Next, the details on DT mutation and fitness evaluation tasks will be provided. |algo| performs two types of mutations on DT individual:

- Node test coefficients mutation
- DT topology mutation

During each iteration of |algo|, a small portion (|alpha|) of DT nodes' test coefficients is mutated at random. Coefficient is mutated by flipping one of its bits at random position. Every change in node test influences the classification, as the instances take different paths through the DT, hence being classified differently. Usually one coefficient per several nodes (dictated by parameter |alpha|) is mutated each iteration, in order for classification result to change in small steps. Parameter |alpha| is adapted dynamically from one iteration to other depending on the speed at which the DT fitness is improving in a manner that |alpha| is increased each iteration when there is no improvement, and reset to default minimal value when new individual is selected as current best.

On the other hand, topology mutations represent very large moves in the search space, so they are performed even less often. In every iteration, there is a small chance (|rho|) that a node will either be added to the DT or removed from it. This change either adds an additional test for the classification, or removes one or whole subtree of tests. The node is always added in place of an existing leaf, i.e. never in place of an internal non-leaf node.  The test coefficients of the newly added non-leaf node are calculated in the same way as are the root test coefficients during initialization. On the other hand, if node is to be removed, it is always one of the non-leaf nodes. By adding a test, a new point is created where during classification, instances from different classes might separate and take different paths through the DT and eventually be classified as different. This increases the accuracy of the DT. On the other hand, by removing the unnecessary test the DT is made smaller. Size of the DT is also an important factor in fitness calculation in |algo| algorithm.

.. _fig-fitness-eval-pca:

.. literalinclude:: code/fitness_eval.py
    :caption: The pseudo-code of the fitness evaluation task.

The fitness of a mutated individual (DT) is evaluated using the training set. The DT is let to classify all the problem instances and the classification results are then compared to the desired classifications specified in the training set. The pseudo-code for this task is given in :num:`Algorithm #fig-fitness-eval-pca`. The input parameter *dt* is the current DT individual and *train_set* is the training set.

The fitness evaluation task performs the following:

- Finding the distribution of the classes over the leaves of the DT - implemented by the first **for** loop
- Finding the dominant class for each leaf - implemented by the second **for** loop
- Calculating the fitness as a weighted sum of two values: DT accuracy and DT oversize (calculated as the relative difference between the number of leaves in DT and total number of classes in training set) - implemented by the last four statements.

First, the class distribution is determined by letting all instances from the training set traverse the DT, i.e. by calling the *find_dt_leaf_for_inst()* function whose pseudo-code is given in :num:`Algorithm #fig-find-dt-leaf-for-inst-pca`. This function uses *evaluate_node_test()* function in each iteration to determine the traversal path and returns the ID of a leaf node in which the instance finished the traversal. The *evaluate_node_test()* function performs the node test evaluation given by equation :eq:`oblique_test`. The traversal is performed in the manner depicted in the :num:`Figure #fig-oblique-dt` where one possible path is given by the red line.

.. _fig-find-dt-leaf-for-inst-pca:

.. literalinclude:: code/find_dt_leaf_for_inst.py
    :caption: The pseudo-code of the procedure for determining the end-leaf for an instance.

Next step in the fitness evaluation process (:num:`Algorithm #fig-fitness-eval-pca`) is to calculate the class distribution matrix. The classes of all the instances from the training set are known and read for each instance into the *instance_class* variable (from the *fitness_eval()* function). Based on the leaf nodes' IDs returned by *find_dt_leaf_for_inst()* and the *instance_class* variable value, the distribution matrix is updated. The :math:`d_{i,j}` element of the distribution matrix contains the number of instances of class *j* that finished in the leaf node with ID *i* after DT traversal. After all the instances from training set traverse the DT, this matrix contains the distribution of classes among the leaf nodes.

Second, the next loop of the *fitness_eval()* finds the dominant class for each leaf node. Dominant class for a leaf node is the class having the largest percentage of instances finishing the traversal in that leaf node. Formally, the dominant class *k* of the leaf node with ID *i* is:

.. math:: k | (d_{i,k} = \max_{j}(d_{i,j}))
    :label: dominant_class

If we were to do a classification run with the current DT individual over the training set, the maximum accuracy would be attained if all leaf nodes were assigned their corresponding dominant classes. Thus, each instance which finishes in a certain leaf node, that corresponds to the node's dominant class is added to the number of classification hits (the *hits* variable of the :num:`Algorithm #fig-fitness-eval-pca`), otherwise it is qualified as a miss.

Fitness is calculated as a weighted sum of two values: DT accuracy and DT oversize. DT accuracy is calculated as the percentage of classification hits. DT oversize is calculated as the relative difference between the number of leaves in DT (obtained via *leaves_cnt()* function) and total number of classes in training set (obtained via *class_cnt()* function). In order to be able to classify correctly all training set instances, after the induction, DT needs to have at least one leaf for each class occuring in the training set. Therefore, DT starts to suffer penalties to the fitness only when the number of DT leaves exceeds the total number of classes in the training set.

Profiling results
-----------------

To confirm the results obtained by the computational complexity analysis, software profiling was performed on the |algo| algorithm's C implementation. Software implementation was developed using many optimization techniques:

- arithmetic operation on 64-bit operands only (optimized for 64-bit CPU), 
- loop unfolding for node test evaluation loop, 
- maximum compiler optimization settings, etc.

To perform the experiments 21 datasets, presented in :num:`Table #tbl-uci-datasets`, were selected from the UCI benchmark datasets database :cite:`newman1998uci`. UCI database is commonly used in the machine learning community to estimate and compare performance of different machine learning algorithms.

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

- **Name** - The name of the function
- **Time** - Total amount of time spent in the function  
- **Calls** - Total number of calls to the function
- **% Time** - Percentage of time spent in the function relative to the total execution time.

.. _fig-profiling:

.. figure:: images/profiling.png
    
    Profiling results of the |algo| algorithm C implementation.

The execution times shown for the functions represent only the self time, i.e. the execution times of its subfunctions are subtracted from the total execution time. The functions from the top of the table in :num:`Figure #fig-profiling` (which was sorted by the execution times), all belong to the fitness evaluation task: *evaluate node test()*, *find_dt_leaf_for_inst()*, *find_node_distribution()* and *fitness_eval()*. By summing the execution times of these four functions we obtain that the fitness evaluation tasks takes about 99.84% of total time for this particular test. 

Hence, the |algo| algorithm has obvious computational bottleneck in the fitness evaluation task, which takes 99.4% of computational time on average, which makes it an undoubtful candidate for hardware acceleration. Since the DT mutation task takes insignificant amount of time to perform, it was decided for it to be left in software. Further advantage of leaving the mutation in software is the ease of changing and experimenting with this task. Many other algorithms can then be implemented in software and make use of the hardware accelerated fitness evaluation task like: Genetic Algorithms (GA), Genetic Programming (GP), Simulated Annealing (SA), etc.

Co-processor for DT ensemble induction - |cop|
==============================================

Proposed |cop| co-processor performs the task of determining the accuracies of the DT individuals for the fitness evaluation tasks of the DT ensemble induction. The |cop| can calculate the DT accuracies, i.e. the number of hits contained in the *hits* variable of the :num:`Algorithm #fig-fitness-eval-pca`, for all ensemble members in parallel. The co-processor is connected to the CPU via AXI4 AMBA bus, which can be used by software to completely control the |cop| operation:

- Download of the training set
- Download of the DT descriptions, including structural organization and coefficient values for all node tests present in the DTs
- Start of the accuracy evaluation process for each of the ensemble members individually
- Read-out of the vector of combined statuses of the accuracy evaluation processes for all ensemble members 
- Read-out of the classification performance results for each of the ensemble members

.. _fig-system-bd:

.. bdp:: images/system_bd.py
    :width: 100%
    
    The |cop| co-processor structure and integration with the host CPU

The |cop| consists of an array of DT accuracy evaluators (|acep|), each of which can be used to evaluate the accuracy of the DT for a single ensemble member inducer. Furthermore, the co-processor features the Status block that allows the user to read-out the operation status of all |acep|. The |cop| co-processor structure and integration with the host CPU is depicted in the :num:`Figure #fig-system-bd`.

|acep|
------

.. _fig-eftip:

.. bdp:: images/eftip.py
    
    The |acep| module structure

The major components of the |acep| co-processor and their connections are depicted in the :num:`Figure #fig-eftip`:

- **Classifier**: Performs the DT traversal for each training set instance, i.e. implements the *find_dt_leaf_for_inst()* function in :num:`Algorithm #fig-find-dt-leaf-for-inst-pca`. The classification process is pipelined, with each stage performing DT node test calculations for one DT level. |DM| is the number of pipeline stages and thus the maximum supported depth of the induced DT. For each instance in the training set, the Classifier outputs the ID assigned to the leaf in which the instance finished the traversal (please refer to *fitness_eval()* function :num:`Algorithm #fig-fitness-eval-pca`).
- **Training Set Memory**: The memory for storing all training set instances that should be processed by the |cop| co-processor.
- **DT Memory Array**: The array of memories used to store the DT description with elements :math:`L_{1}` through :math:`L_{D^{M}}`. The Classifier calculates node tests for each DT level in parallel. Each Classifier pipeline stage requires its own memory that holds description of all nodes at DT level it is associated with.
- **Accuracy Calculator**: Calculates the accuracy of the DT based on the classification data received from the Classifier. For each instance of the training set, the Classifier supplies the ID of the leaf in which the instance finished. Based on this information, the Accuracy Calculator updates the distribution matrix and calculates the number of hits which is sent to the Control Unit and stored in the memory-maped Classification Performance Register, ready to be read by the user.
- **Control Unit**: Acts as a bridge between the AXI4 interface and internal protocols and controls the accuracy evaluation process.

Required Hardware Resources and Performance
-------------------------------------------

The |cop| co-processor is implemented as an IP core with many customization parameters that can be configured at the design phase and are given in :num:`Table #tbl-cop-params`. These parameters mainly impose constraints on the maximum size of the DT that can be induced and the maximum size of the training set that can be used. 

.. role:: raw(raw)
   :format: latex

.. tabularcolumns:: c p{0.4\linewidth} p{0.4\linewidth}

.. _tbl-cop-params:

.. list-table:: Customization parameters that can be configured at design phase of the |cop| co-processor
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

The amount of resources required to implement |cop| co-processor is a function of the customization parameters given in the :num:`Table #tbl-cop-params` and is given in the :num:`Table #tbl-req-res` for various hardware resources.

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

Second, the number of clock cycles required to determine the DT accuracy will be discussed. The Classifier has a throughput of one instance per clock cycle, hence all instances are classified in :math:`N_I` cycles. However, there is an initial latency equal to the length of the pipeline :math:`N_{P}`. Furthermore, the Accuracy Calculator needs extra time after the classification has finished in order to determine the dominant class which is equal to the total number of classes in the training set :math:`N_{C}`, plus the time to sum all dominant class hits, which is equal to the number of active leaves :math:`N_{l}`. Finally, the time required to calculate DT accuracy, expressed in clock cycles, for a given training set can be calculated as follows:

.. math:: accuracy\_evaluation\_time = N_{I} + N_{P} + N_{C} + N_{l} \ clock\ cycles,

and is thus dependent on the training set size.

Software for |cop| assisted DT ensemble induction
=================================================

With |cop| co-processor performing DT accuracy evaluation task, remaining functionality of the |task| algorithm (:num:`Algorithm #fig-algorithm-pca`) is implemented in software. Furthermore, software needs to implement procedures for interfacing the |cop| co-processor as well. 

The further major difference to the pure software solution that arises from the use of the |cop| is the 

The pseudo-code for software used in the co-design is given by :num:`Algorithm #fig-co-design-sw-pca`.

.. _fig-co-design-sw-pca:

.. literalinclude:: code/co_design_sw.py
    :caption: The pseudo-code of the |algo| algorithm using |cop| co-processor 

The only difference to the pure software solution of the main *efti()* function, is that the training set needs to be transfered to the |cop| co-processor, which is performed by the *hw_load_training_set()* function. Since |cop|'s memory space is mapped to the main CPU's memory space via AXI bus, this function simply copies the instances to the memory region corresponding to the Training Set Memory of the |cop|.

The *fitness_eval()* function performs the following:

- uploads the new (mutated) DT description to the |cop|, by changing only the mutated parts in the memory that is mapped to the DT Memory Array of the |cop| via *hw_load_dt_diff()* function,
- initiates the DT accuracy evaluation by writing to the Operation Control register of the |cop| via *hw_start_fitness_eval()* function,
- waits for the DT accuracy evaluation results to become available, by polling the |cop| Classification Performance Register via *hw_finished_fitness_eval()* function,
- fetches the number of classification hits from the |cop| Classification Performance Register via *hw_get_hits()* and calculates the fitness in the same manner as in :num:`Algorithm #fig-fitness-eval-pca`. 

The hardware interface function pseudo-codes were omitted for brevity.

Experiments
===========

In this section the results of the experiments designed to estimate DT induction speedup of the software implementation of the |algo| algorithm using |cop| co-processor over pure software implementation of the |algo| algorithm are given.

Required Hardware Resources
---------------------------

The customization parameters of the |cop| co-processor, whose description is given in :num:`Table #tbl-cop-params`, have been set for the experiments to support all training sets from :num:`Table #tbl-uci-datasets`. The values of the customization parameters are given in :num:`Table #tbl-exp-params`.

.. tabularcolumns:: p{0.5\linewidth} p{0.07\linewidth} 

.. _tbl-exp-params:

.. list-table:: Values of customization parameters of |cop| co-processor instance used in DT induction speedup experiments
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

The |cop| co-processor has been implemented using the Xilinx Vivado Design Suite 2014.4 software for logic synthesis and implementation with default synthesis and P&R options. From the implementation report files, device utilization data has been analyzed and information about the number of used slices, BRAMs and DSP blocks has been extracted, and is presented in :num:`Table #tbl-utilization`. The maximum operating frequency of 133 MHz of system clock frequency for the implemented |cop| co-processor was attained.

.. tabularcolumns:: l l l l

.. _tbl-utilization:

.. list-table:: FPGA resources required to implement |cop| co-processor for DT induction with selected UCI datasets
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

Given in brackets along with each resource utilization number is a percentage of used resources from the total resources available on the corresponding FPGA devices. :num:`Table #tbl-utilization` shows that implemented |cop| co-processor fits even into the entry level XC7Z020 Xilinx FPGA device of the Zynq series, and requires even smaller percentage of resources on entry- to mid-level Kintex7 and Virtex7 Xilinx FPGA devices (XC7K325 and XC7VX690).

Estimation of Induction Speedup
-------------------------------

Three implementations of |algo| algorithm have been developed for experiments, all of them written in C language:

- **SW-PC**: Pure software implementation for PC
- **SW-ARM**: Pure software implementation for ARM Cortex-A9 processor
- **HW/SW**: HW/SW co-design solution, where |cop| co-processor implemented in FPGA was used for the time critical fitness evaluation task. Remaining functionality of the |algo| algorithm (shown in :num:`Algorithm #fig-co-design-sw-pca`) was left in software and implemented for ARM Cortex-A9 processor.

For the PC implementation, AMD Phenom(tm) II X4 965 (3.4 GHz) platform was used and the software was built using GCC 4.8.2 compiler. For the SW-ARM and HW/SW implementations, ARM Cortex-A9 667MHz (Xilinx XC7Z020-1CLG484C Zynq-7000) platform has been used. The software was built using Sourcery CodeBench Lite ARM EABI 4.8.3 compiler (from within Xilinx SDK 2014.4) and the |cop| co-processor was built using Xilinx Vivado Design Suite 2014.4. 

Care was taken when writing the software and many optimization techniques were employed as described in chapter `Profiling results`_ in order to create the fastest possible software implementation and have a fair comparison with the HW/SW solution.

For each of the datasets from :num:`Table #tbl-uci-datasets`, an experiment consisting of five 5-fold cross-validations has been performed for all three |algo| algorithm implementations, and for each cross-validation run DT induction time has been measured. Software timing was obtained by different means for two target platforms:

- For PC platform, the <time.h> C library was used and timing was output to the console
- For ARM platform, TTC hardware timer was used and timing was output via UART

All datasets from :num:`Table #tbl-uci-datasets` were compiled together with the source code and were readily available in the memory, thus there was no training set loading overhead on the DT induction timings for both pure software experiments. On the other hand, in the HW/SW co-design experiment, datasets needed to be loaded from the CPU memory via AXI bus (via *hw_load_training_set()*), so this operation was excluded from timing analysis in order to make a fair comparison.

The results of the experiments are presented in :num:`Table #tbl-results`. For each implementation and dataset, the average induction times of the five 5-fold cross-validation runs are given together with their 95% confidence intervals. The last row of the table provides the average speedup of the HW/SW implementation over both SW-ARM and SW-PC implementations, together with the 95% confidence intervals.

.. tabularcolumns:: l R{0.15\linewidth} R{0.15\linewidth} R{0.15\linewidth}

.. _tbl-results:

.. csv-table:: DT induction times for various |algo| implementations and average speedup of HW/SW implementation over pure software implementations
    :header-rows: 1
    :file: scripts/results.csv

:num:`Table #tbl-results` indicates that the average speedup of the HW/SW implementation is 42 times over the SW-ARM and 3.2 times over SW-PC implementation. Speedup varies with different datasets. Computational complexity increases as |NI|, |NA|, *n* and |Nc| increase. The number of nodes in DT *n* is dependant on the training set instance attribute values, but can be expected to increase also with |NI|, |NA| and |Nc|. By observing the speedup of the HW/SW implementation over pure software implementations shown in :num:`Figure #fig-speedup` for each dataset and the datasets' characteristics given in :num:`Table #tbl-uci-datasets`, it can be seen that indeed more speedup is gained for datasets with larger |NI|, |NA| and |Nc|.

.. _fig-speedup:

.. plot:: images/speedup_plot.py
    :width: 100%
    
    Speedup of the HW/SW implementation over a) SW-ARM implementation and b) SW-PC implementation, given for each dataset listed in :num:`Table #tbl-uci-datasets`

:num:`Figure #fig-speedup` and :num:`Table #tbl-results` suggest that HW/SW implementation using |cop| co-processor offers a substantial speedup in comparison to pure software implementations for both PC and ARM. Furthermore, |cop| implementation used in the experiments operates at much lower frequency (133MHz) than both ARM (667MHz) and PC(3.4GHz) platforms. If |cop| co-processor were implemented in ASIC, the operating frequency would be increased by a factor of 10-30, and the DT induction speedup would increase accordingly.

Conclusion
==========

In this paper a parameterizable co-processor for hardware aided decision tree (DT) induction using evoulutionary approach is proposed. |cop| co-processor is used for hardware acceleration of the DT accuracy evaluation task since this task is proven in the paper to be the execution time bottleneck. The algorithm for full DT induction using evolutionary approach (|algo|) has been implemented in software to use |cop| co-processor implemented in FPGA as a co-processor. Comparison of HW/SW |algo| algorithm implementation with pure software implementations suggests that proposed HW/SW architecture offers substantial speedups for all tests performed on UCI datasets.

.. bibliography:: hereboy.bib
	:style: unsrt
