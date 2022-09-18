from dataclasses import dataclass
import os
import pathlib
import log

TF_CACHE_DIR = os.getenv("TF_CACHE_DIR", pathlib.Path.home() / ".cache/nvim/tfutils")

@dataclass
class TfCache():
    """ ExampleCache data class: Build, store and retrieve data
    """
    def __init__(self, provider: str, document: str):
        self.cache_dir = TF_CACHE_DIR
        if not pathlib.Path(self.cache_dir).exists():
            os.makedirs(self.cache_dir)

        provider_path = self.cache_dir / provider
        if not pathlib.Path(provider_path).exists():
            os.makedirs(provider_path)

        self.document = pathlib.Path(provider_path / document)

    def set(self, data):
        with self.document.open("w") as f:
            f.writelines(data)

    def get(self):
        data = []
        with self.document.open() as f:
            data = f.readlines()
        return data

    def clean(self):
        self.document.unlink()

    def exists(self):
        return self.document.exists()
