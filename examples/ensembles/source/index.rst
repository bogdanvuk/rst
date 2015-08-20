.. |algo| replace:: *EEFTI*
.. |efti| replace:: *EFTI*
.. |eftis| replace:: *EFTIs*
.. |cop| replace:: *EEFTIP*
.. |smae| replace:: *SMAE*
.. |SM| replace:: :math:`S^M`
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
.. |ne| replace:: :math:`n_e`
.. |Ths| replace:: :math:`T_{hs}`
.. |Tsw| replace:: :math:`T_{sw}`
.. |Tswmut| replace:: :math:`T_{sw\_mut}`
.. |Tswacc| replace:: :math:`T_{sw\_acc}`
.. |Thsmut| replace:: :math:`T_{hs\_mut}`
.. |Thsacc| replace:: :math:`T_{hs\_acc}`

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

In general, DT can be induced in two ways: incrementally (node-by-node) and whole tree at once. Most of DT induction algorithms use some kind of heuristic for optimization process, which is often some sort of evolutionary algorithm (EA), since the finding of the optimal oblique DT is a hard algorithmic problem :cite:`barros2012survey`. The greedy top-down recursive partitioning strategy is a computationally least demanding approach for DT induction, hence most DT induction algorithms use this approach. Naturally, this approach suffers from inability of escaping local optima. Better results, especially if DT size is considered, are obtained by the inducers that work in full DT, with cost of higher computational complexity :cite:`struharik2014inducing`.

DT induction phase can be very computationally demanding and can last for hours or even days **[ref]** for practical problems.This is certainly true for full DT inference algorithms. By accelerating this task, machine learning systems could be trained faster allowing for shorter design cycles, or could process large amount of data, which is of particular interest if DTs are used in the data mining applications :cite:`witten2005data`. This might also allow DT learning systems to be rebuilt
in real-time for applications that require such rapid adapting, such as machine vision :cite:`prince2012computer,challa2011fundamentals`, bioinformatics :cite:`lesk2013introduction,baldi2001bioinformatics`, web mining :cite:`liu2007web,russell2013mining`, text mining :cite:`weiss2010fundamentals,aggarwal2012mining`, etc.

In order to accelerate DT induction phase, two general approaches can be used. First approach focuses on developing new algorithmic frameworks or new software tools and is the dominant way of meeting this requirement :cite:`bekkerman2011scaling,choudhary2011accelerating`. Second approach focuses on hardware acceleration of machine learning algorithms, by developing new hardware architectures optimized for accelerating selected machine learning systems.

The proposed co-processor is used for acceleration of a new DT induction algorithm, called |algo|. |algo| (Evolutionary Full Tree Induction) is an algorithm for full oblique classification DT induction using EA. In the remaining of the paper, the proposed co-processor will be called |cop| (Evolutionary Full Tree Induction co-Processor).

Hardware acceleration of machine learning algorithms receives significant attention in scientific community. Wide range of solutions have been suggested in the open literature for various predictive models. Authors are aware of the work that has been done on accelerating SVMs and ANNs, where hardware architectures for acceleration of both learning and deployment phases have been proposed. Architectures for hardware acceleration of SVM learning algorithms have been proposed in :cite:`anguita2003digital`, while architectures for acceleration of previously created SVMs have been proposed in :cite:`papadonikolakis2012novel,anguita2011fpga,mahmoodi2011fpga,vranjkovic2011new`. Research in the hardware acceleration of ANNs has been particularly intensive. Numerous hardware architectures for the acceleration of already learned ANNs have been proposed :cite:`savich2012scalable,vainbrand2011scalable,echanobe2014fpga`. Also, a large number of hardware architectures capable of implementing ANN learning algorithms in hardware have been proposed :cite:`misra2010artificial,omondi2006fpga,madokoro2013hardware`. However, in the field of hardware acceleration of DTs majority of papers focus on acceleration of already created DTs :cite:`struharik2009intellectual,li2011low,saqib2015pipelined`. Hardware acceleration of DT induction is scarcely covered. Authors are currently aware of only two papers on the topic of hardware acceleration of DT induction algorithms :cite:`struharik2009evolving,chrysos2013hc`. But these results focus on accelerating greedy top-down DT induction approaches. In :cite:`struharik2009evolving` incremental DT induction algorithm, where EA is used to calculate optimal coefficient vector one node at a time, is completely accelerated in hardware. In :cite:`chrysos2013hc` a HW/SW approach was used to accelerate the computationally most demanding part of the well known CART incremental DT induction algorithm.

In this paper, a hardware acceleration of a novel full DT ensemble evolutionary induction algorithm based on Bagging [**ref**], called |algo| is presented. The Bagging approach was chosen for the |algo| since it makes the induction of the ensemble members completely decoupled from each other, making it very well suited for the parallelization and hence hardware acceleration. The |algo| uses |efti| :cite:`efti` (Evolutionary Full Tree Induction) algorithm that performs the induction of the full oblique classification DTs. The |efti| algorithm was chosen as the ensemble member inducer since it provides smaller DTs with similar or better classification accuracy than other well-known DT inference algorithms, both incremental and full DT :cite:`efti`. However, |efti| is more computationally demanding than the incremental inducers, hence |algo| could merit greatly from a hardware accelerator, making it more attractive. In this paper, |cop| co-processor is proposed to accelerate parts of the |algo| that are most computationally intensive, with remaining parts of the algorithm run on CPU. The |cop| co-processor architecture benefits also from the fact that |efti| algorithm evolves the DT using only one individual, in contrast to many other algorithms based on EA that require populations :cite:`bot2000application,krketowski2005global,llora2004mixed,papagelis2000ga`. The architecture can thus be simplified with hardware resources allocated only for a single individual per ensemble member. Furthermore, by using HW/SW co-design approach, the proposed |cop| co-processor can be used to accelerate DT ensemble inducers based on Bagging which rely on a variety of other EA-based DT inductino algorithms :cite:`barros2012survey,bot2000application,krketowski2005global,llora2004mixed,papagelis2000ga`. As far as the authors are aware, this is the first paper concerned with the hardware acceleration of full DT ensemble induction algorithm based on bagging.

|algo| algorithm
================

In this section, the |algo| algorithm for induction of DT ensembles using full DT induction approach based on EA is described. Only one individual per ensemble member is required for the induction by the |algo| algorithm. Each individual represents the best DT evolved up to the current iteration for it's corresponding ensemble member. Since |algo| uses supervised learning, the training set used to induce the ensemble consists of the problem instances together with their corresponding class memberships. Since |algo| uses the Bagging algorithm, one subset of the training set is generated for each ensemble member which will be used to induce it. The subsets can be generated in many ways: **Koji nacini, nisam bas nasao na netu?** Each ensemble member starts off as a randomly generated one-node DT and the algorithm iteratively tries to improve on it. DTs are slightly changed, i.e. mutated, in each iteration, and let to perform classification of their corresponding subset of the training set. The known training set classification is then used to calculate the quality of the classification results. When the newly mutated DT performs better at the classification than its predecessor, it is promoted to the new current best individual for its ensemble member and will become the base for the mutations in the following iterations, until a better one is found. After the desired number of iterations, the algorithm exits and returns the set of best DT individuals, one for each ensemble member. 

.. _fig-algorithm-pca:
.. literalinclude:: code/algorithm.py
    :caption: Overview of the |algo| algorithm

The :num:`Algorithm #fig-algorithm-pca` shows the |algo| algorithm entry point. Please note that all algorithms in this paper are described in Python language style and that many details have been omitted for the sake of clarity. As it was discussed in the `Introduction`_, the |efti| algorithm is used for the induction of each ensemble member since it is suitable for hardware acceleration (it uses only one individual for the induction and creates smaller DTs with no loss of accuracy compared to many other well-known algorithms :cite:`efti`). The |algo| was chosen to be based on Bagging, since the induction process of one ensemble member is then uninfluenced by the induction processes of other ensemble members in any way, hence they can be performed in separate tasks. These tasks implement the |efti| algorithm and their pseudo-code is shown in :num:`Algorithm #fig-task-pca`. The |algo| first divides the training set in subsets using *divide_train_set()* function and stores them in the array *task_train_sets*. Then the result array is created using *initialize_result_array()* function and stored in the *res* array. The *res* array contains one item for each ensemble member, to which the corresponding |efti| will output the induced DTs and various miscellaneous corresponding statistical data. Next, the |efti| tasks are created, assigned their corresponding *task_train_sets* item and *res* item, and run. The |algo| waits for a completion of all |efti| tasks and returns the *res* array populated by them.

.. _fig-task-pca:
.. literalinclude:: code/task.py
    :caption: Overview of the |efti| algorithm

The :num:`Algorithm #fig-task-pca` shows the algorithmic framework for the each of the |efti| tasks, which is similar for all EAs. The current best DT individual is called *dt* in the pseudo-code. Initially, each individual starts of as a single node DT. In order to generate the node test coefficients, two instances with different class associations are selected at random from the training set. Each instance with its attribute vector forms a point and each node test with its node coefficients forms a plane in |NA|-dimensional space, where |NA| equals the size of the instance attribute vector (|A|) and node test coefficient vector (|a|). The node test coefficients of the root node are then calculated in such a way to form a plane perpendicular to the line connecting the points representing the two selected training set instances. The consequence of the way the node test is devised is that when the DT is let to classify the training set, the two selected instances (selected to have different classes) will be split by the node test, i.e. they will take different paths. This splitting of the instances is fundamental for building a classifier. Furthermore, it is expected that the instances of the same class are grouped in same regions of the attribute vector space, thus it is likely that the node test will also split many other instances that share classes with two selected ones. All this is implemented in the *initialize()* function. Additionally, this function will be called each time a new node is added to the DT.

Once the DT individual is initialized, the |efti| iteratively performs three main operation:

- **DT Mutation** - implemented by *mutate()* function
- **Fitness Evaluation** - implemented by *fitness_eval()* function
- **Individual Selection** - given by the last **if** statement of the :num:`Algorithm #fig-algorithm-pca`.

|efti| performs two types of mutations on DT individual: Node test coefficients mutation and DT topology mutation. Node test coefficient is mutated by switching the value of one of its bit at random position. Only small fraction (|alpha|) of node test coefficients are mutated each iteration in order not to generate large shifts in the search space. The node tests determine the paths the instances will take during the classification, i.e. determine their classification, hence these mutation are done with hope of obtaining better classification results. Parameter |alpha| changes dynamically between the iterations. At the end of the iteration, if there was an improvement to the DT fitness, i.e. new best individual is found, |alpha| is reset to some initial value. However, in each iteration there was no improvement |alpha| is gradually increased in order to allow for bigger steps in search space.

Topology mutations represent even larger steps in the search space and are thus employed even less often, only every few iterations. Parameter |rho| defines the probability a single node will be either removed from the DT individual or added to it. First, one leaf node is selected at random to be replaced by the new non-leaf node. Next, the test coefficients for the new node are calculated using *initialize()* function described above and two leaf nodes are generated as its children. This way, a new test is introduced into the DT where instances of different classes might separate, take different paths through the DT and eventually finish classified as different, thus increasing the DT accuracy and its fitness. 

On the other hand, when node is to be removed, it is selected at random from all non-leaf DT nodes. The selected non-leaf node is deleted along with the whole sub-tree of nodes rooted at it. The removal of the node is done in hope of removing an unnecessary test and make the DT smaller, since the size of the DT, besides the accuracy, influences the DT fitness as well.

.. _fig-fitness-eval-pca:
.. literalinclude:: code/fitness_eval.py
    :caption: The pseudo-code of the fitness evaluation task.

After the DT individual is mutated, its fitness is obtained using the algorithm given in :num:`Algorithm #fig-fitness-eval-pca` as weighted sum of two values: DT accuracy and DT oversize. The input parameter *dt* is the current DT individual and *train_set* is the training set. DT oversize negatively influences the fitness and is calculated as the relative difference between the number of leaves in DT (|Nl|) and total number of classes in training set (|Nc|). This means that once |Nl| becomes bigger than |Nc|, the DT individual starts to suffer penalties to its fitness. The threshold is set to |Nc| since DT needs to have at least one leaf for each of the training set classes in order to have a chance of classifying correctly the instances belonging to each of the training set classes. DT accuracy influences positively the fitness and is calculated by letting DT individual classify all the training set instances and is described in more details in next paragraphs. The fitness evaluation task performs the following:

- It finds the distribution of the classes over the leaves of the DT - implemented by the first **for** loop
- It finds the dominant class for each leaf - implemented by the second **for** loop
- It calculates the fitness as a weighted sum of the DT accuracy and DT oversize.

The class distribution is obtained from the classification results of the training set, calculated by the DT individual. The :math:`d_{i,j}` element of the distribution matrix contains the number of instances of class *j* that finished in the leaf node with ID *i* after DT traversal. In order to populate the matrix, the *find_dt_leaf_for_inst()* function is called (whose pseudo-code is given in :num:`Algorithm #fig-find-dt-leaf-for-inst-pca`) for each training set instance, to perform the DT traversal in the manner depicted in the :num:`Figure #fig-oblique-dt` where the red line shows one possible traversal path. During the traversal, the *evaluate_node_test()* function is iteratively used to perform the node test evaluation given by the equation :eq:`oblique_test`, to determine in which direction the traversal should continue. The function returns the ID of a leaf (variable *leaf_id* in the :num:`Algorithm #fig-fitness-eval-pca`) in which the instance finished the traversal. Using the leaf ID and being that the class of the instance is known from the training set (variable *instance_class* in the :num:`Algorithm #fig-fitness-eval-pca`), the corresponding element *distribution[leaf_id][instance_class]* of the distribution matrix is incremented for each instance. After all the instances from training set traverse the DT, this matrix contains the distribution of classes among the leaf nodes.

.. _fig-find-dt-leaf-for-inst-pca:
.. literalinclude:: code/find_dt_leaf_for_inst.py
    :caption: The pseudo-code of the procedure for determining the end-leaf for an instance.

Second, dominant class is calculated by the next loop of the *fitness_eval()* function. Dominant class for a leaf node is the class having the largest percentage of instances finishing the traversal in that leaf node. Formally, the dominant class *k* of the leaf node with ID *i* is:

.. math:: k | (d_{i,k} = \max_{j}(d_{i,j}))
    :label: dominant_class

The maximum classification accuracy over the training set is attained when all leaf nodes are assigned their corresponding dominant classes. Therefore, when an instance finishes in the leaf node whose dominant class is the same as the class of the instance, the instance classification is qualified as a hit, otherwise it is qualified as a miss. The *hits* variable of the :num:`Algorithm #fig-fitness-eval-pca` counts the instance classification hits. The DT accuracy is then calculated as a percentage of the classification hits over the total number of instances in the training set.

Finally, upon acquiring the fitness of the newly mutated DT the :num:`Algorithm #fig-algorithm-pca` performs the individual selection. The most basic individual selection is presented here for the sake of the brevity. However, the more complex procedure is implemented in |efti| algorithm which allows, with some probability, for an individual with worse fitness to be selected. In that case, the algorithm continues as if the worse fitness individual were a current best. Nevertheless, the best overall individual is always memorized and there is an increasing chance that it will be selected again if the algorithm makes no progress in fitness. 

Profiling results
-----------------

In order to decide which part of the |algo| algorithm should be accelerated in hardware, the profiling was performed on the algorithm software implementation. The software implementation was realized in C programming language, with many optimization techniques employed:

- node test evaluation loop (within *evaluate_node_test()* function in :num:`Algorithm #fig-find-dt-leaf-for-inst-pca`) has been unfold
- all arithmetic operation were performed using 64-bit operands (optimized for 64-bit CPU which was used for profiling),
- compiler optimization settings were set to maximum for speed, etc.

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
    * - Steel Plates Faults
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

GCC 4.8.2 compiler was used to compile the software implementation of |algo| algorithm and GProf to profile it on each of of the tests listed in :num:`Table #tbl-uci-datasets`. It was run on AMD Phenom(tm) II X4 965 (3.4 GHz) computer and the results obtained by profiling are shown in :num:`Figure #fig-profiling-plot`. All tests were performed by inducing a single member ensemble, since the results obtained in this way are then convenient for conducting the calculation of the arbitrary size ensemble induction performance as discussed in the `Theoretical estimation of acheivable speedup with the proposed HW/SW system`_. The figure shows percentage of time spent in the *fitness_eval()* function and its subfuctions for each dataset. On average, |algo| spent 99.4% of time calculating the fitness of the individual.

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
    
    Profiling results of the |algo| algorithm's C implementation.

The execution times shown for the functions represent only the self time, i.e. the execution times of its subfunctions are subtracted from their total execution time. Following functions from table in :num:`Figure #fig-profiling` (which was sorted by the execution times) belong to the fitness evaluation task: *evaluate node test()*, *find_dt_leaf_for_inst()*, *find_node_distribution()* and *fitness_eval()*. By summing the execution times of these four functions we obtain that the fitness evaluation task takes about 99.84% of total time for this particular test. 

The results show that the obvious computational bottleneck of the |algo| algorithm lays in the fitness evaluation operation, taking 99.4% of computational time on average. This makes it an undoubtful candidate for hardware acceleration. All other operations including the initialization routines within :num:`Algorithm #fig-algorithm-pca`, DT mutation and individual selection operations were decided to be left in software, since they require an insignificant amount of time to perform. On the other hand, by leaving these operations in software the design remains flexible for experimenting with the algorithms for DT mutation, Bagging and individual selection. Furthermore, many other algorithms based on the EA like: Simulated Annealing (SA), Genetic Algorithms (GA), Genetic Programming (GP) etc., can be employed to perform DT induction instead of |efti| and benefit from the co-processor performing the fitness evaluation operation, which significantly expands the scope of use of the proposed |cop| co-processor.

Co-processor for DT ensemble induction - |cop|
==============================================

.. _fig-system-bd:
.. bdp:: images/system_bd.py
    :width: 70%
    
    The |cop| co-processor structure and integration with the host CPU

Proposed |cop| co-processor performs the task of determining the accuracies of the DT individuals for the fitness evaluation tasks of the DT ensemble induction. The |cop| can calculate the DT accuracies, i.e. the number of hits accumulated in the *hits* variable of the :num:`Algorithm #fig-fitness-eval-pca`, for all ensemble members in parallel. The co-processor is connected to the CPU via AXI4 AMBA bus, which can be used by software to completely control the |cop| operation:

- Download of the training set parts for each ensemble member
- Download of the DT descriptions, including structural organization and coefficient values for all node tests present in the DTs
- Start of the accuracy evaluation process for each of the ensemble members individually
- Read-out of the vector of combined statuses of the accuracy evaluation processes for all ensemble members 
- Read-out of the classification performance results for each of the ensemble members

The |cop| consists of an array of DT accuracy evaluators: :math:`SMAE_1` (Single Member Accuracy Evaluator) to :math:`SMAE_{S^M}`, each of which can be used to evaluate the accuracy of the DT for a single ensemble member inducer. Parameter |SM| represents the total number of |smae| units in the |cop| and thus the maximal number of ensemble member accuracies evaluation that can be performed in parallel. Furthermore, the co-processor features the IRQ Status block that allows the user to read-out the operation status of all |smae|. The |cop| co-processor structure and integration with the host CPU is depicted in the :num:`Figure #fig-system-bd`.

|smae|
------

.. _fig-eftip:
.. bdp:: images/eftip.py
    
    The |smae| module structure

The major components of the |smae| co-processor and their connections are depicted in the :num:`Figure #fig-eftip`:

- **Control Unit**: Provides AXI4 interface for the user to access the |smae| block. It acts as a gateway and demultiplexes and relays the read and write operations to components of the |smae| block. Furthermore, it implements the control logic of the accuracy evaluation flow and contains control registers for starting, stopping and restarting the process, as well as reading out the current evaluation status. When instructed by user via AXI4 interface to initiate the accuracy evaluation process, it signals the Training Set Memory to start the output of the instances to the Classifier, waits for the classification to finish and the accuracy to be calculated by Accuracy Calculator block, then generates the pulse on the *IRQ* output and stores the accuracy result in the Classification Performance Register for user to read it.
- **Classifier**: Implements the *find_dt_leaf_for_inst()* function in :num:`Algorithm #fig-find-dt-leaf-for-inst-pca`, i.e. performs the DT traversal for each training set instance. Classifier comprises an array of *TLE* (Tree Level Evaluator), which calculate instance traversal paths in parallel by pipelining the process. Each pipeline stage calculates the node test given by :eq:`oblique_test` for one level of the DT, since the instance can only visit one node per level during traversal. Based on the calculation result it then passes the instance to the next *TLE* stage, i.e. next DT level, and informs the stage whether the traversal is to be continued via right or left child. The block for node test calculation is once again pipelined using parallel multipliers and the tree of adders. Maximum supported depth of the induced DT is depends on the number of pipeline stages (|DM|). At the end of the pipeline Classifier outputs for each instance the ID assigned to the leaf (variable *leaf_id*) in which the instance finished the traversal (please refer to *fitness_eval()* function :num:`Algorithm #fig-fitness-eval-pca`).
- **Training Set Memory**: The memory for storing all training set instances that participate in the classification. The memory is accessible via AXI4 bus for the user to upload the training set to the |smae|.
- **DT Memory Array**: Comprises the array of memories :math:`DTD_{1}` (DT Description) through :math:`DTD_{D^{M}}`, one per each DT level, i.e. one per each Classifier pipeline stage, to hold the description of the DT. Each Classifier pipeline stage requires its own *DTD* memory that holds description of all nodes at DT level the stage is associated with, since all calculations are performed in parallel.
- **Accuracy Calculator**: Implements the class distribution matrix, dominant class and accuracy calculations described by the :num:`Algorithm #fig-fitness-eval-pca`. The *leaf_id* is received from the Classifier together with the known class (variable *instance_class*) for each instance in the training set. Distribution matrix is updated accordingly and once all the instances have been clasified, the number of hits is calculated and sent to the Control Unit.

IRQ Status block
----------------

IRQ Status block has been implemented in order to provide user the means of reading the statuses of all |smae| units with one AXI4 read operation and thus optimize the traffic. Each |smae| unit comprises an *IRQ* (interrupt request) signal used to inform the IRQ Status block that the |smae| unit has finished the accuracy evaluation. The IRQ Status block comprises an array of IRQ Status Word Registers which can all be read in a single burst via AXI bus. Each IRQ Status Word is a 32-bit register (since |cop| was optimized for 32-bit AXI) packed from the bits representing the statuses of up to 32 |smae| units. Each bit is called :math:`SMAE_i` Status Bit, where *i* denotes the ID of the |smae| unit whose status the bit is tracking as shown in figure :num:`Figure #fig-irq-status`. The figure is presented for one specific |SM| value, but there are no limitations on the actual parameter value imposed by the IRQ Status block. The bits of the IRQ Status Word Register are sticky, i.e. set each time the *IRQ* is signaled from the corresponding |smae| and cleared when the register is read by the user.

.. _fig-irq-status:
.. bdp:: images/irq_status.py
    
    IRQ Status

Required Hardware Resources and Performance
-------------------------------------------

The |cop| co-processor is implemented as an IP core with many customization parameters that can be configured at the design phase and are given in :num:`Table #tbl-cop-params`. These parameters mainly impose constraints on the maximum size of the DT that can be induced and the maximum size of the training set that can be used. 

.. role:: raw(raw)
   :format: latex

**Promeniti oznake**

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

Theoretical estimation of acheivable speedup with the proposed HW/SW system
---------------------------------------------------------------------------

In this section the shape of the speedup of the HW/SW implementation over the pure software implementation of the |algo| algorithm will be calculated as function of the number of ensemble members |ne|:

.. math:: speedup(n_e) = \frac{\Tsw(n_e)}{\Ths(n_e)}
    :label: m-speedup-function
    
where |Tsw| and |Ths| denote the run times of the pure software and HW/SW implementations respectively. As discussed in the previous section, the good candidate for hardware acceleration of |efti| algorithm is the accuracy calculation task, while leaving the mutation to be implemented in software. Hence, we will observe separately the contributions of the two parts to the total algorithm runtime. Furthermore, the hardware accelerator for the accuracy calculation task can be easily made to calculate the accuracy for each ensemble member in parallel, since there is no coupling between different members' the induction processes. For the software implementation we obtain:

.. math:: \Tsw(n_e) = \Tswmut + \Tswacc
    :label: m-tsw-breakdown

where |Tswmut| and |Tswacc| denote the amount of time pure software implementation spends on the mutation and accuracy calculation tasks respectively. |Tswmut| is a linear function of |ne|, since the mutation is performed once per iteration per ensemble member. Hence, if the number of iteration is kept constant, we obtain:

.. math:: \Tswmut(n_e) = \Tswmut(1) \cdot n_e
    :label: m-tswmut-func
    
On the contrary, |Tswacc| is a constant with respect to |ne|, since the training set is divided amongst ensemble members, making the number of instances being classified and thus the amount of computation constant. For the HW/SW implementation we obtain:

.. math:: \Ths(n_e) = \Thsmut(1) \cdot n_e + \Thsacc
    :label: m-ths-breakdown

where |Thsmut| and |Thsacc| denote the amount of time HW/SW implementation spends on the mutation and accuracy calculation tasks respectively. |Thsmut| is implemented in software and is a linear function of |ne| for the same reasons given for |Tswmut|. Furthermore, |Thsmut| is somewhat greater than |Tswmut| (:math:`\Thsmut = \Tswmut + \Delta_t`) since it also comprises the latency of hardware accelerator interface operations, which is not present in the pure software implementation. 

Because HW/SW accuracy calculation is performed in parallel for all ensemble members, the calculation time is proportional to the size of the training set allocated for each ensemble member. Since the training set is divided equally among the ensemble members, |Thsacc| is inversely proportional to the |ne|:

.. math:: \Thsacc(n_e) = \frac{\Thsacc(1)}{n_e}
    :label: m-thsacc-func
    
By substituting equations :eq:`m-tsw-breakdown`, :eq:`m-tswmut-func`, :eq:`m-ths-breakdown` and :eq:`m-thsacc-func` into the :eq:`m-speedup-function`, we obtain:

.. math:: speedup(n_e) = \frac{\Tswmut(1) \cdot n_e + \Tswacc}{\Thsmut(1) \cdot n_e + \frac{\Thsacc(1)}{n_e}} = \frac{\Tswmut(1) \cdot n_e^{2} + \Tswacc \cdot n_e}{\Thsmut(1) \cdot n_e^{2} + \Thsacc(1)}
    :label: m-speedup-func-subst

|Tswacc| was shown in the `Profiling results`_ section to take almost all of the computational time. This parameter is heavily influenced by the amount of computation needed to calculate the instance traversal (:num:`Algorithm #fig-find-dt-leaf-for-inst-pca`). Time needed to perform the traversal for all instances is proportional to the number of instances in the training set (|NI|), number of attributes |A| (equation :eq:`oblique_test`) and the depth of the DT. Depth of the DT is determined by the complexity of the training set data, but the larger training sets with higher |Nc| and |A| tend to require larger trees to meet the classification accuracy. The datasets that can be of interest to run induction on using the |cop| are the ones that require significant time to execute in software on the CPU. For these datasets :math:`\Tswacc \gg \Tswmut` and thus :math:`\Tswacc \gg \Thsmut`. By using hardware acceleration and massive parallelism, :math:`\Tswacc \gg \Thsacc` is accomplished as well. By taking these parameter relationships into the account, :math:`speedup(n_e)` function given by equation :eq:`m-speedup-func-subst` takes shape depicted in :num:`Figure #fig-speedup-func-plot`.

**Staviti za jedan konkretan slucaj iz eksperimenata**

.. _fig-speedup-func-plot:
.. plot:: images/speedup_func_plot.py
    :width: 100%
    
    The shape of the :math:`speedup(n_e)` function given by equation :eq:`m-speedup-func-subst`.

The plot on :num:`Figure #fig-speedup-func-plot` suggests that accelerating the |algo| by a co-processor that performs the DT accuracy calculation in parallel for all ensemble members, will in the beginning provide increase in speedup as the number of ensemble members increase. Then, after some speedup maximum, it will slowly degrade, but continue to offer substantial speedup for all reasonable ensemble sizes. The maximum of the speedup can be found by seeking the maximum of the function in equation :eq:`m-speedup-func-subst`. By taking into the account parameter relationships, the point of maximum of the :math:`speedup(n_e)` function can be expressed as follows:

.. math:: max(speedup(n_e))\approx\frac{\Tswacc}{2\sqrt{\Thsacc(1)\Thsmut(1)}}\ at\ n_e \approx \sqrt{\frac{\Thsacc(1)}{\Thsmut(1)}}
	:label: m-speedup-maximum
	
Furthermore, the :num:`Figure #fig-speedup-func-plot` shows that even though the speedup starts declining after reaching its maximum for certain |ne|, the downslope is slowly flattening, and the significant speedup is achieved even for large ensemble inference.

Software for |cop| assisted DT ensemble induction
=================================================

**Nagojiti sto vise**

As it was described, |cop| co-processor can perform accuracy evaluation task in parallel for as many ensemble members as there are |smae| units. Hence, in HW/SW implementation of the |algo| algorithm, each of the |efti| tasks is assigned one |smae| unit to use exclusively for acceleration of accuracy evaluation for its DT individual. Since there is a single AXI bus connecting the CPU to |cop| co-processor, no two |efti| tasks can access it in the same time. Hence, a scheduler task is needed to manage the granting of access rights to the tasks by using semaphores of the underlying operating system to signal that the access to the |cop| has been granted to the task. The |algo| top level pseudo-code with added instantiation of the synchronization mechanism in form of the scheduler task and the semaphores is presented in :num:`Algorithm #fig-co-design-sw-pca`. Furthermore, each of the tasks is assigned a unique ID (variable *smae_id* in the pseudo-code), which serves as a handle to the semaphore and the |smae| unit of the |cop| co-processor assigned to the task.

.. _fig-co-design-sw-pca:
.. literalinclude:: code/co_design_sw.py
    :caption: The pseudo-code of the |algo| algorithm using |cop| co-processor 

First let us show how each |efti| task(:num:`Algorithm #fig-algorithm-pca`) needs to be changed in order to support the co-processor. New |efti| pseudo-code for HW/SW co-design is given by :num:`Algorithm #fig-co-design-sw-pca`. The *smae_id* is used by all hardware interface functions to calculate the hardware addresses belonging to the assigned |smae| unit. First the training set needs to be loaded into the |smae|, since it will be needed to perform the accuracy calculation. Because |cop|'s memory space is mapped to the main CPU's memory space via AXI bus, the *hw_load_training_set()* function simply copies all instances of the training set to the Training Set Memory address space of the assigned |smae| unit.

.. _fig-co-design-efti-pca:
.. literalinclude:: code/co_design_efti.py
    :caption: The pseudo-code of the |efti| task algorithm used in the HW/SW co-design implementation

Each time DT individual is mutated its description needs to be reloaded into the DT Memory Array of the assigned |smae| unit. Since only small parts of the DT individuals are mutated each iteration, only the changed parts can be loaded to the co-processor in order to optimize the traffic. Hence, the *mutate()* function is slightly changed to return the list of all changes it made to the DT individual into the *dt_diff* variable. The function *hw_load_dt_diff()* is then called to copy all these changes to appropriate DT Memory Array locations of the assigned |smae| unit. Furthermore, if new DT individual does not get selected for a new current best, the mutations need to be discarded. This is executed by the *hw_revert_dt_diff()* function, which undoes all the changes applied by the *hw_load_dt_diff()* function.

.. _fig-co-design-fitness-eval-pca:
.. literalinclude:: code/co_design_fitness_eval.py
    :caption: The pseudo-code of the fitness evaluation function used in the HW/SW co-design implementation

The pseudo-code for the *fitness_eval()* function used in the HW/SW co-design implementation is shown in the figure :num:`Figure #fig-co-design-fitness-eval-pca`. With training set and DT description readily loaded into the co-processor, signal is sent to the the assigned |smae| to start the accuracy evaluation. After that the task waits for the semaphore signal form the Scheduler task to indicate that the accuracy has been calculated and the access to the |cop| has been granted it. The task switch performed by the underlying operating system and the processor is freed to serve other |efti| tasks.

The pseudo-code of the Scheduler task is given in :num:`Algorithm #fig-co-design-scheduler-pca`. The main function of the scheduler task is to monitor the IRQ Status Registers of the |cop| and based on its value signal the semaphores assigned to the corresponding |efti| tasks. The Scheduler task reads the |cop| status via *hw_get_status()* function into the variable *status*. It then iterates over all bits of the variable *status* that correspond to the SMAE Status Bits, and checks which of them have the value of 1, meaning the corresponding |smae| unit has reported the end of the accuracy evaluation process. The corresponding |efti| task is then woken by signaling the appropriate semaphore.

.. _fig-co-design-scheduler-pca:
.. literalinclude:: code/co_design_scheduler.py
    :caption: The pseudo-code of the |algo| algorithm using |cop| co-processor 

The hardware interface function pseudo-codes were omitted for brevity.

Experiments
===========

** Probali smo RTOS, veliki latency. U nedostatku besplatnih RTOSa za Cortex-A9, napisali smo nas jednostavan cooperative scheduler.**

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

The |cop| co-processor has been modeled in VHDL hardware description language and implemented using the Xilinx Vivado Design Suite 2014.4 software for logic synthesis and implementation with default synthesis and P&R options. From the implementation report files, device utilization data has been analyzed and information about the number of used slices, BRAMs and DSP blocks has been extracted, and is presented in :num:`Table #tbl-utilization`. The maximum operating frequency of 133 MHz of system clock frequency for the implemented |cop| co-processor was attained.

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

For the PC implementation, AMD Phenom(tm) II X4 965 (3.4 GHz) platform was used and the software was built using GCC 4.8.2 compiler. For the SW-ARM and HW/SW implementations, ARM Cortex-A9 667MHz (Xilinx **XC7Z020-1CLG484C Ovo necemo reci** Zynq-7000) platform has been used. The software was built using Sourcery CodeBench Lite ARM EABI 4.8.3 compiler (from within Xilinx SDK 2014.4) and the |cop| co-processor was built using Xilinx Vivado Design Suite 2014.4. 

Care was taken when writing the software and many optimization techniques were employed as described in chapter `Profiling results`_ in order to create the fastest possible software implementation and have a fair comparison with the HW/SW solution.

For each of the datasets from :num:`Table #tbl-uci-datasets`, an experiment consisting of five 5-fold cross-validations has been performed for all three |algo| algorithm implementations, and for each cross-validation run DT induction time has been measured. Software timing was obtained by different means for two target platforms:

- For PC platform, the <time.h> C library was used and timing was output to the console
- For ARM platform, TTC hardware timer was used and timing was output via UART

All datasets from :num:`Table #tbl-uci-datasets` were compiled together with the source code and were readily available in the memory, thus there was no training set loading overhead on the DT induction timings for both pure software experiments. On the other hand, in the HW/SW co-design experiment, datasets needed to be loaded from the CPU memory via AXI bus (via *hw_load_training_set()*), so this operation was excluded from timing analysis in order to make a fair comparison.

The results of the experiments are presented in :num:`Table #tbl-results`. For each implementation and dataset, the average induction times of the five 5-fold cross-validation runs are given together with their 95% confidence intervals. The last row of the table provides the average speedup of the HW/SW implementation over both SW-ARM and SW-PC implementations, together with the 95% confidence intervals.

**1. Opcija: U tabeli da stavljamo speedup-e, bez apsolutnih vrednosti**

.. tabularcolumns:: l R{0.15\linewidth} R{0.15\linewidth} R{0.15\linewidth}
.. _tbl-results:
.. csv-table:: DT induction times for various |algo| implementations and average speedup of HW/SW implementation over pure software implementations
    :header-rows: 1
    :file: scripts/results.csv

:num:`Table #tbl-results` indicates that the average speedup of the HW/SW implementation is 42 times over the SW-ARM and 3.2 times over SW-PC implementation. Computational complexity increases as |NI|, |NA|, *n* and |Nc| increase. The number of nodes in DT *n* is dependant on the training set instance attribute values, but can be expected to increase also with |NI|, |NA| and |Nc|. By observing the speedup of the HW/SW implementation over pure software implementations shown in :num:`Figure #fig-speedup` for each dataset and the datasets' characteristics given in :num:`Table #tbl-uci-datasets`, it can be seen that indeed more speedup is gained for datasets with larger |NI|, |NA| and |Nc|.

** Svaki histogram pocepati na 5 (koliko ima razlicitih velicina ansambla), mozda podeliti na dva grafika da se sve vidi **

.. _fig-speedup:
.. plot:: images/speedup_plot.py
    :width: 100%
    
    Speedup of the HW/SW implementation over a) SW-ARM implementation and b) SW-PC implementation, given for each dataset listed in :num:`Table #tbl-uci-datasets`

:num:`Figure #fig-speedup` and :num:`Table #tbl-results` suggest that HW/SW implementation using |cop| co-processor offers a substantial speedup in comparison to pure software implementations for both PC and ARM. Furthermore, |cop| implementation used in the experiments operates at much lower frequency (133MHz) than both ARM (667MHz) and PC(3.4GHz) platforms. If |cop| co-processor were implemented in ASIC, the operating frequency would be increased by an order of magnitude, and the DT induction speedup would increase accordingly.

Conclusion
==========

In this paper a parameterizable co-processor for hardware aided decision tree (DT) induction using evolutionary approach is proposed. |cop| co-processor is used for hardware acceleration of the DT accuracy evaluation task since this task is proven in the paper to be the execution time bottleneck. The algorithm for full DT induction using evolutionary approach (|algo|) has been implemented in software to use the |cop| co-processor implemented in FPGA as a co-processor. Comparison of HW/SW |algo| algorithm implementation with pure software implementations suggests that proposed HW/SW architecture offers substantial speedups for all tests performed on UCI datasets.

.. bibliography:: hereboy.bib
	:style: unsrt
