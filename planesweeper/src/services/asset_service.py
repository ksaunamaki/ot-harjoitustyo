import os
from primitives.asset import Asset


class AssetService:
    """Handles resolving and returning fully-qualified filesystem path for
        image assets requested by the game. This service assumes that all asset images
        will be places under "assets" subdirectory under main game root directory.
    """

    @staticmethod
    def get_assets_path() -> str:
        """Get filesystem path for the assets -subdirectory.

        Returns:
            str: Path to the assets directory.
        """
        dirname = os.path.dirname(__file__)
        return os.path.join(dirname, "..", "assets")

    @staticmethod
    def get_asset(asset: str) -> Asset:
        """Gets asset data object for requested asset name (image file name).

        Args:
            asset (str): Asset's name (e.g. "image1.png").

        Returns:
            Asset: Asset data.
        """
        path = os.path.join(AssetService.get_assets_path(), asset)

        if os.path.exists(path):
            return Asset(asset, os.path.join(AssetService.get_assets_path(), asset))

        return Asset(asset, None)
