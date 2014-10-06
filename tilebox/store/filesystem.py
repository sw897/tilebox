import errno
import os
import os.path

from tilebox import Tile, TileStore, TileFormat


class FilesystemTileStore(TileStore):
    """Tiles stored in a filesystem"""

    def __init__(self, tilelayout, **kwargs):
        TileStore.__init__(self, **kwargs)
        self.tilelayout = tilelayout

    def delete_one(self, tile):
        filename = self.tilelayout.filename(tile.tilecoord)
        if os.path.exists(filename):
            os.remove(filename)
        return tile

    def get_all(self):
        for tile in self.list():
            with open(tile.path, 'rb') as file:
                tile.data = file.read()
            yield tile

    def get_one(self, tile):
        filename = self.tilelayout.filename(tile.tilecoord)
        if os.path.isfile(filename):
            return self._get_one(tile, filename)
        else:
            if tile.content_type:
                tileformat = TileFormat.from_content_type(tile.content_type)
            elif self.content_type:
                tileformat = TileFormat.from_content_type(self.content_type)
            else:
                tileformat = TileFormat()
            filename = filename + tileformat.ext
            if os.path.isfile(filename):
                tile.content_type = tileformat.content_type
                return self._get_one(tile, filename)
            else:
                # filenames = map(lambda ext: filename + ext, tileformat.extentions)
                # for filename in filenames:
                for ext in tileformat.extentions:
                    filename2 = filename + ext
                    if os.path.isfile(filename2):
                        tileformat = TileFormat.from_extention(ext)
                        tile.content_type = tileformat.content_type
                        tile = self._get_one(tile, filename2)
                        if tile is not None:
                            return tile
                return None

    def _get_one(self, tile, filename):
        try:
            with open(filename, 'rb') as file:
                tile.data = file.read()
            if tile.content_type is None and self.content_type is not None:
                tile.content_type = self.content_type
            return tile
        except IOError as e:
            if e.errno == errno.ENOENT:
                return None
            else:
                raise

    def list(self):
        top = getattr(self.tilelayout, 'prefix', '.')
        for dirpath, dirnames, filenames in os.walk(top):
            for filename in filenames:
                path = os.path.join(dirpath, filename)
                tilecoord = self.tilelayout.tilecoord(path)
                if tilecoord:
                    yield Tile(tilecoord, path=path)

    def put_one(self, tile):
        assert tile.data is not None
        filename = self.tilelayout.filename(tile.tilecoord)
        if tile.content_type:
            tileformat = TileFormat.from_content_type(tile.content_type)
        elif self.content_type:
            tileformat = TileFormat.from_content_type(self.content_type)
        else:
            tileformat = TileFormat()
        filename = filename + tileformat.ext
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(filename, 'wb') as file:
            file.write(tile.data)
        return tile
