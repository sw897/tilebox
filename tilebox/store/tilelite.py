# http://mbtiles.org/

import mimetypes
import sqlite3

from tilebox import Bounds, BoundingPyramid, Tile, TileCoord, TileStore, TileFormat
from tilebox.lib.sqlite3_ import SQLiteDict, query


class Tiles(SQLiteDict):
    """A dict facade for the tiles table"""

    CREATE_TABLE_SQL = 'CREATE TABLE IF NOT EXISTS tiles (zoom_level integer, tile_column integer, tile_row integer, tile_format integer, tile_data blob, PRIMARY KEY (zoom_level, tile_column, tile_row))'
    CONTAINS_SQL = 'SELECT COUNT(*) FROM tiles WHERE zoom_level = ? AND tile_column = ? AND tile_row = ?'
    DELITEM_SQL = 'DELETE FROM tiles WHERE zoom_level = ? AND tile_column = ? AND tile_row = ?'
    GETITEM_SQL = 'SELECT tile_format, tile_data FROM tiles WHERE zoom_level = ? AND tile_column = ? AND tile_row = ?'
    ITER_SQL = 'SELECT zoom_level, tile_column, tile_row FROM tiles'
    ITERITEMS_SQL = 'SELECT zoom_level, tile_column, tile_row, tile_format, tile_data FROM tiles'
    ITERVALUES_SQL = 'SELECT tile_format, tile_data FROM tiles'
    LEN_SQL = 'SELECT COUNT(*) FROM tiles'
    SETITEM_SQL = 'INSERT OR REPLACE INTO tiles (zoom_level, tile_column, tile_row, tile_format, tile_data) VALUES (?, ?, ?, ?, ?)'

    def __init__(self, tilecoord_in_topleft, *args, **kwargs):
        self.tilecoord_in_topleft = tilecoord_in_topleft
        SQLiteDict.__init__(self, *args, **kwargs)

    def _packitem(self, key, value):
        typeindex, data = value
        y = key.y if self.tilecoord_in_topleft else (1 << key.z) - key.y - 1
        return (key.z, key.x, y, typeindex, sqlite3.Binary(data) if value is not None else None)

    def _packkey(self, key):
        y = key.y if self.tilecoord_in_topleft else (1 << key.z) - key.y - 1
        return (key.z, key.x, y)

    def _unpackitem(self, row):
        z, x, y, typeindex, data = row
        y = y if self.tilecoord_in_topleft else (1 << z) - y - 1
        return (TileCoord(z, x, y), typeindex, data)

    def _unpackkey(self, row):
        z, x, y = row
        y = y if self.tilecoord_in_topleft else (1 << z) - y - 1
        return TileCoord(z, x, y)


class TileliteTileStore(TileStore):
    """A sqlite3 tile store"""

    BOUNDING_PYRAMID_SQL = 'SELECT zoom_level, MIN(tile_column), MAX(tile_column) + 1, MIN((1 << zoom_level) - tile_row - 1), MAX((1 << zoom_level) - tile_row - 1) + 1 FROM tiles GROUP BY zoom_level ORDER BY zoom_level'

    def __init__(self, connection, commit=True, tilecoord_in_topleft=False, **kwargs):
        self.connection = connection
        self.tiles = Tiles(tilecoord_in_topleft, self.connection, commit)
        TileStore.__init__(self, **kwargs)

    def __contains__(self, tile):
        return tile and tile.tilecoord in self.tiles

    def __len__(self):
        return len(self.tiles)

    def delete_one(self, tile):
        del self.tiles[tile.tilecoord]
        return tile

    def get_all(self):
        for tilecoord, typeindex, data in self.tiles.iteritems():
            tile = Tile(tilecoord, data=data)
            tileformat = TileFormat.from_type_index(typeindex)
            tile.content_type = tileformat.content_type
            yield tile

    def get_cheap_bounding_pyramid(self):
        bounds = {}
        for z, xstart, xstop, ystart, ystop in query(self.connection, self.BOUNDING_PYRAMID_SQL):
            bounds[z] = (Bounds(xstart, xstop), Bounds(ystart, ystop))
        return BoundingPyramid(bounds)

    def get_one(self, tile):
        try:
            typeindex, tile.data = self.tiles[tile.tilecoord]
            tileformat = TileFormat.from_type_index(typeindex)
            tile.content_type = tileformat.content_type
        except KeyError:
            return None
        return tile

    def list(self):
        return (Tile(tilecoord) for tilecoord in self.tiles)

    def put_one(self, tile):
        content_type = getattr(tile, 'content_type', None)
        tileformat = TileFormat.from_content_type(content_type)
        self.tiles[tile.tilecoord] = [tileformat.typeindex, getattr(tile, 'data', None)]
        return tile
