def find_dt_leaf_for_inst(dt, instance):
    
    cur_node = dt.root
    classified = False
    
    path_diverged = False
    while (not classified):
        if not path_diverged:
            if cur_node.is_mutated:
                sum = instance.update_node_test_sum(cur_node)
                next_cur_node = cur_node.left if sum < thr else cur_node.right
                
                if next_cur_node != instance.get_next_node_from_stored_path(cur_node):
                    instance.update_instance_path(next_cur_node)
                    path_diverged = True
                    
                cur_node = next_cur_node
            else:
                cur_node = instance.get_next_node_from_stored_path(cur_node)
        else:
            sum = instance.calculate_node_test_sum(cur_node)
            cur_node = cur_node.left if sum < thr else cur_node.right
            
            instance.update_instance_path(cur_node)
            
        if cur_node.is_leaf:
            classified = True          
        
    return cur_node.id