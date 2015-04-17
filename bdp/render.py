import importlib.machinery
import sys
import os

bdp_gen_path = "/home/personal/doktorat/prj/eclipse_wspace/bdp_test/"
bdp_file_name = "/home/personal/doktorat/prj/eclipse_wspace/bdp_test/test.py"

loader = importlib.machinery.SourceFileLoader("", bdp_file_name)

# bdp_file_name = "/home/personal/doktorat/prj/eclipse_wspace/bdp_test/test"

# bdp_file_name = "dt_memory_arch"

# bdp_mod = importlib.import_module(bdp_file_name)
bdp_mod = loader.load_module()

tikz_prolog = r"""
\documentclass{standalone}

\usepackage{tikz}
\usetikzlibrary{shapes,arrows}

\begin{document}
\pagestyle{empty}
\begin{tikzpicture}[yscale=-1]

"""

tikz_epilog = r"""
\end{tikzpicture}


\end{document}
""" 

os.chdir(bdp_gen_path)

with open("test.tex", 'w') as f:
    f.write(tikz_prolog)

    for obj in bdp_mod.obj_list:
        f.write(obj.render_tikz())    

    f.write(tikz_epilog)
    
from subprocess import call, STDOUT
call(["pdflatex", 
      "-interaction=nonstopmode", 
      "-file-line-error",
      "-halt-on-error", "test.tex"], stderr=STDOUT)
