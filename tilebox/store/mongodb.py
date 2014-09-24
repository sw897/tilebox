
import pymongo

from tilebox import Bounds, BoundingPyramid, Tile, TileCoord, TileStore

class MongoTileStore(TileStore):
    """A Mongodb tile store"""

    def __init__(self, connection, database, collection, **kwargs):
        self.connection = pymongo.Connection(connection)
        self.db = self.connection[database]
        self.collection = self.db[collection]
        TileStore.__init__(self, **kwargs)

    def __contains__(self, tile):
        return tile and tile.tilecoord in self.tiles

    def __len__(self):
        return len(self.tiles)

    def delete_one(self, tile):
        del self.tiles[tile.tilecoord]
        return tile

    def get_all(self):
        for tilecoord, data in self.tiles.iteritems():
            tile = Tile(tilecoord, data=data)
            if self.content_type is not None:
                tile.content_type = self.content_type
            yield tile

    def get_one(self, tile):
        try:
            tile.data = self.tiles[tile.tilecoord]
        except KeyError:
            return None
        if self.content_type is not None:
            tile.content_type = self.content_type
        return tile

    def list(self):
        return (Tile(tilecoord) for tilecoord in self.tiles)

    def put_one(self, tile):
        self.tiles[tile.tilecoord] = getattr(tile, 'data', None)
        return tile
