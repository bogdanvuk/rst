def find_dt_leaf_for_inst(dt, instance):
    
    cur_node_id = dt.root
    classified = False
    
    while (not classified):
        
        if evaluate_node_test(cur_node_id, instance):
            cur_node_id = cur_node.left
        else:
            cur_node_id = cur_node.right                

        if is_leaf(cur_node_id):
            classified = True          
        
    return cur_node_id