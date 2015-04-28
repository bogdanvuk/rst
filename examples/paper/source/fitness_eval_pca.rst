
.. _fig-fitness-eval-pca:

.. code-block:: python
    
    def fitness_eval(dt):
    
        for instance, instance_class in training_set:
            leaf_id = find_dt_leaf_for_inst(dt, instance)
        
            distribution[leaf_id][instance_class] += 1
    
        hits = 0
    
        for leaf in leaves:
            dominant_class_cnt = max(distribution[leaf])
        
            hits += dominant_class_cnt
    
        fitness = hits / len(train_set)
    
        return fitness

.. raw:: latex
    
    \begin{figure}[htbp]
    \caption{The pseudo-code of the fitness evaluation task.}\label{index:fig-fitness-eval-pca}\end{figure}
        
