class BaseManager:  # pylint: disable=too-few-public-methods
    """Provides common JSON file load / save / next-id logic."""

    def __init__(self, file_path, default_file):
        self.file_path = file_path or default_file
