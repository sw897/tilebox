from tilebox.layout.googledisk import GoogleDiskTileLayout
from tilebox.layout.wrapped import WrappedTileLayout
from tilebox.store.filesystem import FilesystemTileStore


tilestore = FilesystemTileStore(
        WrappedTileLayout(GoogleDiskTileLayout(), 'tianditu_data/googledisk/', '.png'),
        attribution='&copy; google', content_type='image/png')
