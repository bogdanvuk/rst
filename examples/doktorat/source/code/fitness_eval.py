def fitness_eval(dt, train_set):

    accuracy = accuracy_calc(dt, train_set)

    Nc = train_set.cls_num()
    oversize = (len(dt.leaves) - Nc)/Nc

    fitness = accuracy * (1 - Ko*oversize)
    return fitness
