from tilebox.layout.wwdisk import WWDiskTileLayout
from tilebox.layout.wrapped import WrappedTileLayout
from tilebox.store.filesystem import FilesystemTileStore


tilestore = FilesystemTileStore(
        WrappedTileLayout(WWDiskTileLayout(), 'tianditu_data/wwdisk/', '.jpg'),
        attribution='&copy; worldwind', content_type='image/jpeg')
