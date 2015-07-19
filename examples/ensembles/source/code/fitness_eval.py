def fitness_eval(dt, train_set):
    
    for (instance, instance_class) in train_set:
        leaf_id = find_dt_leaf_for_inst(dt, instance)
        distribution[leaf_id][instance_class] += 1

    hits = 0

    for leaf in leaves:
        dominant_class_cnt = max(distribution[leaf])
        hits += dominant_class_cnt

    accuracy = hits / len(train_set)
    oversize = leaves_cnt(dt) / class_cnt(train_set) - 1
    fitness = w_a * accuracy - w_s * oversize
    
    return fitness