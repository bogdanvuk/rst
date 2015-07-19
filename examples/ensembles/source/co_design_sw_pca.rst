
.. _fig-co-design-sw-pca:

.. code-block:: python
    
    def fitness_eval(dt):
	    load_dt_diff(dt) #Replace only the part of DT that has changed
	    
	    hw_start_fitness_eval()
	
	    while (not hw_finished_fitness_eval()):
	        pass
	    
	    fitness = hw_get_hits() / len(train_set)
	
	    return fitness
	
	def efti():
	    # Create initial 3-node DT and randomize root condition
	    initialize(dt)
	    
	    hw_load_training_set()
	    
	    best_fit = fitness_eval(dt)
	    
	    for iter in range(max_iter):
	        dt_mut = mutate(dt)
	        cur_fit = fitness_eval(dt_mut)
	        if cur_fit >  best_fit:
	            best_fit = cur_fit
	            dt = dt_mut
        
        return dt
