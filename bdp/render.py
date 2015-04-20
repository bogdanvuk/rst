import importlib.machinery
import sys
import os

import node

def render_tikz(file_name, bdp_gen_path, search_paths=[]):
    found = False
    importlib.reload(node)
    try:
        bdp_file_name = file_name
        print(bdp_file_name)
        loader = importlib.machinery.SourceFileLoader("", bdp_file_name)
        bdp_mod = loader.load_module()
        found = True
    except FileNotFoundError:
        
        print(search_paths)
        
        if isinstance(search_paths, str):
            bdp_file_name = os.path.join(search_paths, file_name)
            loader = importlib.machinery.SourceFileLoader("", bdp_file_name)
            bdp_mod = loader.load_module()
        else:
            for s in search_paths:
                try:
                    bdp_file_name = os.path.join(s, file_name)
                    print(bdp_file_name)
                    loader = importlib.machinery.SourceFileLoader("", bdp_file_name)
                    bdp_mod = loader.load_module()
                    found = True
                    break
                except FileNotFoundError:
                    pass
            
    if not found:
        return

    tex_name = os.path.splitext(os.path.basename(bdp_file_name))[0] + '.tex'

    # bdp_file_name = "/home/personal/doktorat/prj/eclipse_wspace/bdp_test/test"
    
    # bdp_file_name = "dt_memory_arch"
    
    # bdp_mod = importlib.import_module(bdp_file_name)
    
    
    tikz_prolog = r"""
    \documentclass{standalone}
    
    \usepackage{tikz}
    \usetikzlibrary{shapes,arrows}
    
    \begin{document}
    \pagestyle{empty}
    \begin{tikzpicture}[yscale=-1, every node/.style={inner sep=0,outer sep=0}]
    
    """
    
    tikz_epilog = r"""
    \end{tikzpicture}
    
    
    \end{document}
    """ 
    
#     os.chdir(bdp_gen_path)
    print(os.path.join(bdp_gen_path, tex_name))
    with open(os.path.join(bdp_gen_path, tex_name), 'w') as f:
        f.write(tikz_prolog)
    
        for obj in bdp_mod.obj_list:
            f.write(obj)
    #         f.write(obj.render_tikz())    
    
        f.write(tikz_epilog)
        
#     from subprocess import call, STDOUT
#     call(["pdflatex", 
#           "-interaction=nonstopmode", 
#           "-file-line-error",
#           "-halt-on-error", "test.tex"], stderr=STDOUT)

if __name__ == '__main__':
    bdp_gen_path = "/home/projects/workspace/runtime-Runtime_Eclipse/bdp_test/"
    bdp_file_name = "/home/projects/workspace/runtime-Runtime_Eclipse/bdp_test/test.py"
    
    render_tikz(bdp_file_name, bdp_gen_path)