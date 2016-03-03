def fitness_eval(dt, train_set):
    
    for (instance, instance_class) in train_set:
        leaf_id = find_dt_leaf_for_inst(dt, instance)
        distribution[leaf_id][instance_class] += 1

    hits = 0
    dt_classes = set()
    dt_impurity = []
    
    for leaf in leaves:
        dominant_class_cnt = max(distribution[leaf])
        dominant_class = distribution[leaf].index(dominant_class_cnt)
        impurity = dominant_class_cnt/sum(distribution[leaf])
        
        dt_classes.add(dominant_class)
        dt_impurity.append(impurity)
        hits += dominant_class_cnt

    Nc = class_cnt(train_set)
    
    accuracy = hits / len(train_set)
    oversize = w_s*(leaves_cnt(dt) - Nc)/Nc
    missing  = w_m*(Nc - len(dt_classes))/Nc
    
    fitness = accuracy * (1 - oversize) * (1 + missing)
    
    return fitness, dt_impurity