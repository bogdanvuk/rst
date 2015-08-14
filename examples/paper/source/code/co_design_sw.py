def efti():
    initialize(dt)
    hw_load_training_set()
    best_fit = fitness_eval(dt, train_set)
    
    for iter in range(max_iter):
        
        dt_mut = mutate(dt)
        cur_fit = fitness_eval(dt_mut, train_set)
        
        if cur_fit > best_fit:
            best_fit = cur_fit
            dt = dt_mut
            
    return dt

def fitness_eval(dt):
    hw_load_dt_diff(dt)
    
    hw_start_accuracy_eval()

    while (not hw_finished_accuracy_eval()):
        pass
    
    accuracy = hw_get_hits() / len(train_set)
    oversize = len(dt.leaves) / class_cnt(train_set) - 1
    fitness = w_a * accuracy - w_s * oversize
    
    return fitness

