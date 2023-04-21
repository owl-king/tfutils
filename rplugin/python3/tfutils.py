import os
import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).parent))

import re
import pynvim
import webbrowser
import requests
import math
#import cache
import log
import timeit
from functools import reduce


@pynvim.plugin
class TfUtils:
    def __init__(self, nvim):
        self.nvim = nvim

    @pynvim.function("TfCreateVar", sync=False)
    def create_var(self, args):
        """Create terraform variable"""
        current_dir = self.nvim.eval('expand("%:p:h")')
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
                    template = """variable "{variable}" {{
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
                "provider_version": 27638,
            },
            "google": {
                "url": f"https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/",
                "regex": "^google_(.*)",
                "provider_version": 27977,
            },
        }
        for provider in supported_providers:
            result = re.findall(supported_providers[provider]["regex"], resource_name)
            if result:
                return (
                    result[0],
                    supported_providers[provider]["url"] + result[0],
                    supported_providers[provider]["provider_version"],
                    provider,
                )
        return None

    @pynvim.function("TfViewDoc", sync=True)
    def view_doc(self, args):
        """Browse doc base on the resource name"""
        resource_name = args[0]
        _, url = self.get_provider_url(resource_name)
        self.nvim.out_write("url")
        webbrowser.open(url)

    #@pynvim.function("TfExample", sync=True)
    #def view_example_doc(self, args):
    #    resource_name = args[0]
    #    resource_short_name, url, provider_version, provider = self.get_provider_url(
    #        resource_name
    #    )
    #    resource_url = self._get_resource_url(resource_short_name, provider_version)

    #    resource_cache = cache.TfCache(provider, resource_short_name)
    #    example_data = None

    #    if not resource_cache.exists():
    #        r = requests.get(resource_url)
    #        content = r.json()["data"]["attributes"]["content"]
    #        example_data = []
    #        regex_tf_condtions = ["```terraform(.*?)```", "```hcl(.*?)```"]
    #        for regex_tf in regex_tf_condtions:
    #            example_data = re.findall(regex_tf, content, re.DOTALL)
    #            if example_data:
    #                break
    #        resource_cache.set(example_data)
    #    example_data = resource_cache.get()

    #    buf = self._show_example_windows()
    #    self._update_example_windows(buf, resource_name, example_data)

    def _normalize_data_for_buf(self, data):
        # Because nvim set lines does not accept line with newline
        return [line.replace("\n", "") for line in data]

    def _update_example_windows(self, buf, resource, data):
        api = self.nvim.api
        api.buf_set_option(buf, "modifiable", True)
        api.buf_set_lines(buf, 0, -1, False, [f"Examples from {resource} offcial docs"])
        api.buf_set_lines(buf, -1, -1, False, self._normalize_data_for_buf(data))
        api.buf_set_option(buf, "modifiable", False)

    def _show_example_windows(self):
        api = self.nvim.api
        buf = api.create_buf(False, True)
        api.buf_set_option(buf, "bufhidden", "wipe")
        width = api.get_option("columns")
        height = api.get_option("lines")
        win_height = math.ceil(height * 0.8 - 4)
        win_width = math.ceil(width * 0.8)
        row = math.ceil((height - win_height) / 2 - 1)
        col = math.ceil((width - win_width) / 2)
        opts = {
            "style": "minimal",
            "relative": "editor",
            "width": win_width,
            "height": win_height,
            "row": row,
            "col": col,
        }
        win = api.open_win(buf, True, opts)
        return buf

    def _get_resource_url(self, resource_name: str, provider_version: int):
        provider_url = "https://registry.terraform.io/v2/provider-docs"
        params = {
            "filter[provider-version]": provider_version,  # hard code provide-version
            "filter[category]": "resources",  # hard ccode provide resource
            "filter[slug]": resource_name,
        }

        res = requests.get(provider_url, params=params)

        resource_url = res.json()["data"][0]["links"]["self"]
        registry_url = "https://registry.terraform.io"
        return registry_url + resource_url
