from io import StringIO
from IPython import get_ipython
from IPython.core.magic import Magics, cell_magic, magics_class, register_cell_magic

@magics_class
class MyMagic(Magics):
    @cell_magic
    def A201_autograde(self, line, cell):
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
        
ipy = get_ipython()
ipy.register_magics(MyMagic)
