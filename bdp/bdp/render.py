import importlib.machinery
import sys
import os
import argparse

import bdp.node

def render_tikz(file_name, bdp_gen_path, search_paths=[]):
    found = False
    importlib.reload(bdp.node)
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
                    loader = importlib.machinery.SourceFileLoader("tmp", bdp_file_name)
                    bdp_mod = loader.load_module("tmp")
                    found = True
                    break
                except FileNotFoundError as e:
                    print(e)
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
    \begin{tikzpicture}[yscale=-1, every node/.style={inner sep=0,outer sep=0, anchor=center}]
    
    """
    
    tikz_epilog = r"""
    \end{tikzpicture}
    
    
    \end{document}
    """ 
    
#     os.chdir(bdp_gen_path)
    tex_file = os.path.join(bdp_gen_path, tex_name)
    with open(tex_file, 'w') as f:
        f.write(tikz_prolog)
    
        for obj in bdp_mod.obj_list:
            f.write(obj)
    #         f.write(obj.render_tikz())    
    
        f.write(tikz_epilog)
        
    return tex_file
        
def convert_pdf(tex_file):
    from subprocess import call, STDOUT
    call(["pdflatex", 
          "-interaction=nonstopmode", 
          "-file-line-error",
          '-output-directory', os.path.dirname(tex_file),
          "-halt-on-error", tex_file], stderr=STDOUT)

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(
        description='Block Diagram in Python renderer.'
    )

    parser.add_argument('input', metavar='input',
                        help="Input BDP file")
    parser.add_argument('output', metavar='output',
                        help="Input BDP file")

    opts = parser.parse_args(sys.argv[1:])
    
    tex_file = render_tikz(opts.input, opts.output)
    
    convert_pdf(tex_file)