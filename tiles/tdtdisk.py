from tilebox.layout.template import TemplateTileLayout
from tilebox.layout.wrapped import WrappedTileLayout
from tilebox.store.filesystem import FilesystemTileStore

tilestore = FilesystemTileStore(
        WrappedTileLayout(TemplateTileLayout('L%(z)d/R%(x)d/C%(y)d'), 'tianditu_data/tdtdisk/image/4326/', '.jpg'),
        attribution='&copy; tdt disk', content_type='image/jpeg')
