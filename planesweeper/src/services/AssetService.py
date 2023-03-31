import os
from primitives.asset import Asset

class AssetService:

    @staticmethod
    def get_assets_path() -> str:
        dirname = os.path.dirname(__file__)
        return os.path.join(dirname, "..", "assets")
    
    @staticmethod
    def get_asset(asset: str) -> Asset:
        path = os.path.join(AssetService.get_assets_path(), asset)

        if os.path.exists(path):
            return Asset(asset, os.path.join(AssetService.get_assets_path(), asset))
        
        return Asset(asset, None)
    
    