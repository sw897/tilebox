from tilebox.layout.tilecache import TileCacheDiskLayout
from tilebox.layout.wrapped import WrappedTileLayout
from tilebox.store.filesystem import FilesystemTileStore


class TileCacheDiskTileStore(FilesystemTileStore):

    def __init__(self, prefix='', suffix='', **kwargs):
        tilelayout = WrappedTileLayout(TileCacheDiskLayout(), prefix=prefix, suffix=suffix)
        FilesystemTileStore.__init__(self, tilelayout, **kwargs)
