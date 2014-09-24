#-*- coding:utf-8 -*-

import re

from tilebox import TileCoord
from tilebox.layout.template import TemplateTileLayout


class TDTTileLayout(TemplateTileLayout):
    """TianDiTu tile layout"""

    def __init__(self, template, layer='dlg'):
        TemplateTileLayout.__init__(self, template)
        self.layer = layer

        # init url
        self.layers = {'dlg':[], 'img':[], 'dem':[], 'dlgAnno':[], 'imgAnno':[]}

        # dlg
        for it in range(10):      # 0-9 map 1-10
            self.layers['dlg'].append('A0512_EMap')
        for it in range(2):   # 10-11 map 11-12
            self.layers['dlg'].append('B0627_EMap1112')
        for it in range(6):        # 12-17 map 13-18
            self.layers['dlg'].append('siwei0608')

        # img
        for it in range(10):        # 0-9 map 1-10
            self.layers['img'].append('sbsm0210')
        self.layers['img'].append('e11')    # 10
        self.layers['img'].append('e12')    # 11
        self.layers['img'].append('e13')    # 12
        self.layers['img'].append('eastdawnall')    # 13
        for it in  range(4):        # 14-17 map 15-18
            self.layers['img'].append('sbsm1518')

        # dem
        for it in range(12):        # 0-11
            self.layers['dem'].append('DemYuXun')
        self.layers['dem'].append('DemYunXun_E13')   # 12
        self.layers['dem'].append('DemYunXun_E14')   # 13

        # dlgAnno
        for it in range(10): # 0-9 map 1-10
            self.layers['dlgAnno'].append('AB0512_Anno')

        # imgAnno
        for it in range(10): # 0-9 map 1-10
            self.layers['imgAnno'].append('A0104_ImgAnnoE')
        for it in range(4):  # 10-13 map 11-14
            self.layers['imgAnno'].append('B0530_eImgAnno')
        for it in range(4):  # 14-17 map 15-18
            self.layers['imgAnno'].append('siweiAnno68')

    def filename(self, tilecoord):
        if tilecoord.z < len(self.layers[self.layer]):
            temp = self.layers[self.layer][tilecoord.z]
            temp = self.template + "&T=" + temp
            return temp % \
                dict(z=tilecoord.z + 1, x=tilecoord.x, y=tilecoord.y)
        return None

    def _tilecoord(self, match):
        tc = TileCoord(*(int(match.group(s)) for s in 'zxy'))
        tc.z = tc.z-1
        return tc
