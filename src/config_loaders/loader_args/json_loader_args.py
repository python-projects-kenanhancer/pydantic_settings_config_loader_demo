from .loader_args import LoaderArgs


class JsonLoaderArgs(LoaderArgs):
    def __init__(self, file_path: str):
        self.file_path = file_path
