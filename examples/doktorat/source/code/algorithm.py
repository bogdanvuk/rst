def efti(train_set):
    initialize(dt)
    best_fit, impurity = fitness_eval(dt, train_set)
    
    for iter in range(max_iter):
        
        dt_mut = mutate(dt, impurity)
        cur_fit, impurity = fitness_eval(dt_mut, train_set)
        
        if cur_fit > best_fit:
            best_fit = cur_fit
            dt = dt_mut
            
    return dt