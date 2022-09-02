import pathlib
import re
import pynvim
import webbrowser
import requests


@pynvim.plugin
class TfUtils:
    def __init__(self, nvim):
        self.nvim = nvim

    @pynvim.function("TfCreateVar", sync=False)
    def create_var(self, args):
        """Create terraform variable"""
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

    def get_provider_url(self, resource_name: str):
        """Get provider url bases on resource name"""
        supported_providers = {
            "aws": {
                "url": f"https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/",
                "regex": "^aws_(.*)",
            }
        }
        for provider in supported_providers:
            result = re.findall(supported_providers[provider]["regex"], resource_name)
            if result:
                return supported_providers[provider]["url"] + result[0]
        return None

    @pynvim.function("TfViewDoc", sync=True)
    def view_doc(self, args):
        """Browse doc base on the resource name"""
        resource_name = args[0]
        url = self.get_provider_url(resource_name)
        self.nvim.out_write("url")
        webbrowser.open(url)

    @pynvim.function("TfExample", sync=True)
    def view_example_doc(self, args):
        resource_name = args[0]
        resource_url = self._get_resource_url(resource_name)

        registry_url = "https://registry.terraform.io"
        res = requests.get(registry_url + resource_url)
        #TODO: Filter response data to get example string

    def _get_resource_url(self, resource_name: str):
        provider_url = "https://registry.terraform.io/v2/provider-docs"
        params = {
            "filter[provider-version]": 27638, # hard code provide-version
            "filter[category]": "resources", # hard ccode provide resource
            "filter[slug]": resource_name,
        }

        res = requests.get(provider_url, params = params)

        resource_url = res.json()['data'][0]['links']['self']

        return resource_url
