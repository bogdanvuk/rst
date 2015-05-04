def efti(train_set):
    # Create initial 3-node DT and randomize root condition
    initialize(dt)
    best_fit = fitness_eval(dt, train_set)
    
    for iter in range(max_iter):
        
        dt_mut = mutate(dt)
        cur_fit = fitness_eval(dt_mut, train_set)
        
        if cur_fit > best_fit:
            best_fit = cur_fit
            dt = dt_mut
            
    return dt