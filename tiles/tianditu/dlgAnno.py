from tilebox.store.url import URLTileStore
from tilebox.layout.tdt import TDTTileLayout


tilestore = URLTileStore(
        (TDTTileLayout('http://tile%d.tianditu.com/DataServer?L=%%(z)d&X=%%(x)d&Y=%%(y)d' % server, 'dlgAnno') for server in range(8)),
        attribution='&copy; tianditu contributors', content_type='image/png')
