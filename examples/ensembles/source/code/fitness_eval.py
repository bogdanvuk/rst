def fitness_eval(dt, train_set):
    
    for (instance, instance_class) in train_set:
        leaf_id = find_dt_leaf_for_inst(dt, instance)
        distribution[leaf_id][instance_class] += 1

    hits = 0
    classes = set()
    impurity = []
    
    for leaf in leaves:
        dominant_class_cnt = max(distribution[leaf])
        classes.add(distribution[leaf].index(dominant_class_cnt))
        impurity.append(dominant_class_cnt/sum(distribution[leaf]))
        hits += dominant_class_cnt

    Nc = class_cnt(train_set)
    accuracy = hits / len(train_set)
    oversize = (1 + w_s*(Nc - leaves_cnt(dt))/Nc)
    missing  = (1 + w_m*(Nc - len(classes)  )/Nc)
    
    fitness = accuracy * oversize * missing
    
    return fitness, impurity