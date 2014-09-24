from tilebox.layout.template import TemplateTileLayout
from tilebox.layout.wrapped import WrappedTileLayout
from tilebox.store.filesystem import FilesystemTileStore

tilestore = FilesystemTileStore(
        WrappedTileLayout(TemplateTileLayout('%(z)d/%(x)d/%(y)d'), 'tianditu_data/tmsdisk/', '.png'),
        attribution='&copy; tms', content_type='image/png')
