import re

from tilebox import TileCoord
from tilebox.layout.re_ import RETileLayout


class TileCacheDiskLayout(RETileLayout):
    """TileCache disk layout"""

    PATTERN = r'[0-9]{2}(?:/[0-9]{3}){6}'
    RE = re.compile(r'([0-9]{2})/([0-9]{3})/([0-9]{3})/([0-9]{3})/([0-9]{3})/([0-9]{3})/([0-9]{3})')

    def __init__(self):
        RETileLayout.__init__(self, self.PATTERN, self.RE)

    def filename(self, tilecoord):
        zs = '%02d' % (tilecoord.z,)
        xs = '%09d' % (tilecoord.x,)
        ys = '%09d' % (tilecoord.y,)
        return '/'.join((zs, xs[0:3], xs[3:6], xs[6:9], ys[0:3], ys[3:6], ys[6:9]))

    def _tilecoord(self, _match):
        ints = map(int, _match.groups())
        z = ints[0]
        x = 1000000 * ints[1] + 1000 * ints[2] + ints[3]
        y = 1000000 * ints[4] + 1000 * ints[5] + ints[6]
        return TileCoord(z, x, y)
