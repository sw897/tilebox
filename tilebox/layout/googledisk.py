#-*- coding:utf-8 -*-

import re

from tilebox import TileCoord
from tilebox.layout.re_ import RETileLayout


class GoogleDiskTileLayout(RETileLayout):
    """google disk tile layout"""

    PATTERN = r'([0-9]+)/([0-9]+)/([0-9]+)/([0-9]+)/([0-9]+)/([0-9]+)/([0-9]+)'
    RE = re.compile(PATTERN + r'\Z')

    def __init__(self):
        RETileLayout.__init__(self, self.PATTERN, self.RE)

    def filename(self, tilecoord):
        return '/' + GoogleDiskTileLayout.zerocode_from_tilecoord(tilecoord)

    def _tilecoord(self, match):
        z, x1, x2, x3, y1, y2, y3 = map(int, match.groups())
        x = x1 * 1000000 + x2 * 1000 + x3
        y = y1 * 1000000 + y2 * 1000 + y3
        return TileCoord(z, x, y)

    @staticmethod
    def zerocode_from_tilecoord(tilecoord):
        x, y , z= tilecoord.x, tilecoord.y, tilecoord.z
        components = [
                GoogleDiskTileLayout.zero_pad(z, 2),
                GoogleDiskTileLayout.zero_pad(x / 1000000, 3),
                GoogleDiskTileLayout.zero_pad(x / 1000 % 1000, 3),
                GoogleDiskTileLayout.zero_pad(x % 1000, 3),
                GoogleDiskTileLayout.zero_pad(y / 1000000, 3),
                GoogleDiskTileLayout.zero_pad(y / 1000 % 1000, 3),
                GoogleDiskTileLayout.zero_pad(y % 1000, 3)
        ]
        return '/'.join("%s" % k for k in components)

    @staticmethod
    def zero_pad(number, length):
        number = str(number)
        assert(length >= len(number))
        return ''.join("%d" % 0 for it in range(length-len(number))) + number
