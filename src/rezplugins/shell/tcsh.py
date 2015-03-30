"""
TCSH shell
"""
from rez.shells import UnixShell
from rezplugins.shell.csh import CSH
from rez import module_root_path
from rez.rex import EscapedString
import os.path
import pipes


class TCSH(CSH):
    executable = UnixShell.find_executable('tcsh')

    @classmethod
    def name(cls):
        return 'tcsh'

    def escape_string(self, value):
        value = EscapedString.promote(value)
        value = value.expanduser()
        result = ''

        for is_literal, txt in value.strings:
            if is_literal:
                txt = pipes.quote(txt)
                if not txt.startswith("'"):
                    txt = "'%s'" % txt
            else:
                txt = txt.replace('\\', '\\\\')
                txt = txt.replace('"', '"\\""')
                txt = txt.replace('!', '\\!')
                txt = '"%s"' % txt
            result += txt
        return result

    def _bind_interactive_rez(self):
        super(TCSH, self)._bind_interactive_rez()
        completion = os.path.join(module_root_path, "completion", "complete.csh")
        self.source(completion)


def register_plugin():
    return TCSH
