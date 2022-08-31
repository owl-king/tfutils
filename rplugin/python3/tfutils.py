import pathlib
import pynvim

@pynvim.plugin
class TfUtils:
    def __init__(self, nvim):
        self.nvim = nvim

    @pynvim.function("TfCreateVar", sync=False)
    def create_var(self, args):
        """Create terraform variable
        """
        current_dir = self.nvim.command_output("pwd")
        tfvars_file_loc = current_dir + "/variables.tf"
        if not pathlib.Path(tfvars_file_loc).exists():
            open(tfvars_file_loc, mode="w", encoding="utf-8").close()

        variable = ""
        description = ""
        if len(args) >= 1:
            variable = args[0]
        if len(args) >= 2:
            description = args[1]
        with open(tfvars_file_loc, mode="r+", encoding="utf-8") as f:
            content = f.read()
            var_conditions = ['variable "{variable}"', variable]
            if not any(map(lambda x: x in content, var_conditions)):
                template = 'variable "{variable}" {{}}\n'.format(variable=variable)
                if description:
                    template = """
variable "{variable}" {{
    description = "{description}"
}}
""".format(
                        variable=variable, description=description
                    )
                f.write(template)
