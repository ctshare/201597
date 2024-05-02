"""
For homeworks autograding@A201+A202
"""

from io import StringIO
from IPython import get_ipython
from IPython.core.magic import Magics, cell_magic, magics_class, register_cell_magic

@magics_class
class A201_autograde_magic(Magics):
    @cell_magic
    def A201_autograde_stdin(self, line, cell):
        """
        Transform a cell into a function with user inputs packed into a list as the function parameter.
        """
        self.shell.run_cell(cell)
        i = 0
        new_codeblock = ""
        new_codeblock += f"def {line}(in_list):\n"
        new_codeblock += "\tresult=''\n"
        for codeline in StringIO(cell):
            new_codeblock += "\t"
            if "input(" in codeline:
                start = codeline.find("input(")
                end = codeline.find(")", start)
                new_codeblock += codeline[:start] + f"in_list[{i}]" + codeline[end+1:] 
                i += 1
            else:
                new_codeblock += codeline
        self.shell.run_cell(new_codeblock)
    
    @cell_magic
    def A201_autograde_stdout(self, variable, cell):
        """
        Capture the output of a code cell without stdin and suppresing the display.
        """
        get_ipython().magics_manager.magics['cell']['capture'](variable, cell)
        globals()["os"] = __import__("os")
        globals()[variable].show()
        
ipy = get_ipython()
ipy.register_magics(A201_autograde_magic)
