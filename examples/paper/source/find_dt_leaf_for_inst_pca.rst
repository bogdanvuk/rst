
.. _fig-find-dt-leaf-for-inst-pca:

.. code-block:: python
   
    def find_dt_leaf_for_inst(dt, instance):
    
        cur_node = dt.root
        classified = False
        
        while (not classified):
            
            if evaluate_node_test(cur_node, instance):
                cur_node = cur_node.left
            else:
                cur_node = cur_node.right                
    
            if is_leaf(cur_node):
                classified = True                
            
        return cur_node 
            
.. raw:: latex
    
    \begin{figure}[htbp]
    \caption{The pseudo-code of the procedure for determining the end-leaf for an instance.}\label{hereboy:fig-find-dt-leaf-for-inst-pca}\end{figure}
        
