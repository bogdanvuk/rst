
.. _fig-evaluate-node-test-pca:

.. code-block:: python
    
    def evaluate_node_test(cur_node, instance):
    
        sum = 0
        
        for coef, attr in zip(cur_node.coefficients, instance):
            sum += coef*attr
            
            
        sum += cur_node.threshold
        
        return sum < 0 
        

.. raw:: latex
    
    \begin{figure}[htbp]
    \caption{The pseudo-code of the fitness evaluation task.}\label{hereboy:fig-evaluate-node-test-pca}\end{figure}
