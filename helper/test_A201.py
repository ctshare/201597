"""
For homeworks autograding@A201+A202
@author: chentao@iu
"""

from io import StringIO
from IPython import get_ipython
from IPython.core.magic import Magics, cell_magic, magics_class, register_cell_magic
from IPython.utils.capture import capture_output

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
    def A201_autograde_stdout(self, line, cell):
        """
        Capture the output of a code cell without stdin and suppresing the display.
        If output has multiple lines, "\n" is replaced by "#"
        """
        with capture_output(stdout=True, stderr=False, display=False) as result:
            self.shell.run_cell(cell)
            message = result.stdout
        modified_message = message.replace("\n", "#")
        new_code = fr"{line }= '{modified_message }' "
        self.shell.run_cell(new_code)
        print(message)

    @cell_magic
    def A201_autograde_stdin_gen(self, line, cell):
        """
        Transform a cell into a function with user inputs packed into a list as the function parameter.
        """
        self.shell.run_cell(cell)
        i = 0
        new_codeblock = ""
        new_codeblock += f"def {line}(in_list):\n"
        new_codeblock += "\tresult=''\n"
        new_codeblock += "\tgen = iter(in_list)\n"
        for codeline in StringIO(cell):
            new_codeblock += "\t"
            if "input(" in codeline:
                start = codeline.find("input(")
                end = codeline.find(")", start)
                new_codeblock += codeline[:start] + f"next(gen)" + codeline[end+1:] 
                i += 1
            else:
                new_codeblock += codeline
        self.shell.run_cell(new_codeblock)

ipy = get_ipython()
ipy.register_magics(A201_autograde_magic)

def A201_autograder_message(output_str, ans, input_str=None, message_str=None):
    if input_str is not None:
        print(f"Input:{input_str}")
    print(f"Expected output: {ans}")
    print(f"Your answer: {output_str}")
    if message_str is not None:
        print(f"message:{message_str}")
    return ans in output_str
    
