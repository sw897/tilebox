
from pymongo import MongoClient

from tilebox import Bounds, BoundingPyramid, Tile, TileCoord, TileStore, TileFormat

class MongoDbTileStore(TileStore):
    """A Mongodb tile store"""

    def __init__(self, connection, database, collection, **kwargs):
        self.client = MongoClient("mongodb://"+connection)
        self.db = self.client[database]
        self.collection = self.db[collection]
        TileStore.__init__(self, **kwargs)

    def get_all(self):
        for tile in self.list():
            with open(tile.path, 'rb') as file:
                tile.data = file.read()
            yield tile

    # def delete_one(self, tile):
    #     raise NotImplementedError

    def get_one(self, tile):
        mongo_tilecoord = {
                "zoom_level":tile.tilecoord.z,
                "tile_column":tile.tilecoord.x,
                "tile_row":tile.tilecoord.y
                }
        mongo_tile = self.collection.find_one(mongo_tilecoord)
        if mongo_tile is None:
            return None
        tile.data = mongo_tile["tile_data"]
        tileformat = TileFormat.from_type_index(mongo_tile["tile_format"])
        tile.content_type = tileformat.content_type
        return tile

    def list(self):
        for mongo_tile in self.collection.find({}):
            tile = Tile(TileCoord(mongo_tile["zoom_level"], mongo_tile["tile_column"], mongo_tile["tile_row"]))
            yield tile
            
    def put_one(self, tile):
        assert tile.data is not None
        if tile.content_type:
            tileformat = TileFormat.from_content_type(tile.content_type)
        elif self.content_type:
            tileformat = TileFormat.from_content_type(self.content_type)
        else:
            tileformat = TileFormat()
        mongo_tile = {
                "zoom_level":tile.tilecoord.z,
                "tile_column":tile.tilecoord.x,
                "tile_row":tile.tilecoord.y,
                "tile_format":tileformat.typeindex,
                "tile_data":tile.data
                }
        tile_id = self.collection.insert(mongo_tile)
        return tile
