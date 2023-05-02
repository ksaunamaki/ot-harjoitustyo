class Asset:
    """Image asset filesystem path and keying information.
    """
    def __init__(self, key: str, path: str):
        self.key: str = key
        self.path: str = path
