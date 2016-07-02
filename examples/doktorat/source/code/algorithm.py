def efti(train_set, max_iter):
    initialize(dt)
    best_fit = fitness_eval(dt, train_set)

    for iter in range(max_iter):

        dt_mut  = mutate(dt)
        cur_fit = fitness_eval(dt_mut, train_set)

        dt = select(dt, dt_mut)

    return dt
