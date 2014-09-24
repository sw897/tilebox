#!/usr/bin/env python

import collections
from itertools import ifilter, imap, islice
import logging
from operator import attrgetter
import os.path
import re


logger = logging.getLogger(__name__)


class BoxDB(object):
    """A meta box db """

    def __init__(self, **kwargs):
        """
        Construct a :class:`BoxStore`.

        :param kwargs: Extra attributes

        """
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def delete(self, tilestores):
        """
        Delete ``tilestores`` from the boxdb.

        :param tilestores: Input tilestore stream
        :type tilestores: iterable

        :rtype: iterator

        """
        return imap(self.delete_one, ifilter(None, tilestores))

    def delete_one(self, tilestore):
        """
        Delete ``tilestore`` and return ``tilestore``.

        :param tilestore: TileStore
        :type tilestore: :class:`TileStore` or ``None``

        :rtype: :class:`TileStore` or ``None``

        """
        raise NotImplementedError

    def get(self, tilestores):
        """
        Add data to each of ``tiles``.

        :param tiles: Tilestream
        :type tiles: iterator

        :rtype: iterator

        """
        return imap(self.get_one, ifilter(None, tiles))

    def get_all(self):
        """
        Generate all the tiles in the store with their data.

        :rtype: iterator

        """
        return imap(self.get_one, ifilter(None, self.list()))

    def get_bounding_pyramid(self):
        """
        Returns the bounding pyramid that encloses all tiles in the store.

        :rtype: :class:`BoundingPyramid`

        """
        return reduce(BoundingPyramid.add,
                      imap(attrgetter('tilecoord'),
                           ifilter(None, self.list())),
                      BoundingPyramid())

    def get_cheap_bounding_pyramid(self):
        """
        Returns a bounding pyramid that is cheap to calculate, or ``None`` if
        it is not possible to calculate a bounding pyramid cheaply.

        :rtype: :class:`BoundingPyramid` or ``None``

        """
        return None

    def get_one(self, tile):
        """
        Add data to ``tile``, or return ``None`` if ``tile`` is not in the store.

        :param tile: Tile
        :type tile: :class:`Tile` or ``None``

        :rtype: :class:`Tile` or ``None``

        """
        raise NotImplementedError

    def list(self):
        """
        Generate all the tiles in the store, but without their data.

        :rtype: iterator

        """
        if self.bounding_pyramid:
            for tilecoord in self.bounding_pyramid:
                yield Tile(tilecoord)

    def put(self, tiles):
        """
        Store ``tiles`` in the store.

        :param tiles: Tilestream
        :type tiles: iterator

        :rtype: iterator

        """
        return imap(self.put_one, ifilter(None, tiles))

    def put_one(self, tile):
        """
        Store ``tile`` in the store.

        :param tile: Tile
        :type tile: :class:`Tile` or ``None``

        :rtype: :class:`Tile` or ``None``

        """
        raise NotImplementedError

    @classmethod
    def load(cls, name):  # pragma: no cover
        """
        Construct a :class:`TileStore` from a name.

        :param name: Name
        :type name: string

        :rtype: :class:`TileStore`

        The following shortcuts are available:

        bounds://<bounding-pyramid>

        file://<template>

        http://<template> and https://<template>

        memcached://<server>:<port>/<template>

        s3://<bucket>/<template>

        sqs://<region>/<queue>

        <filename>.bsddb

        <filename>.mbtiles

        <filename>.zip

        <module>

        """
        if name == 'null://':
            from tilebox.store.null import NullTileStore
            return NullTileStore()
        if name.startswith('bounds://'):
            from tilebox.store.boundingpyramid import BoundingPyramidTileStore
            return BoundingPyramidTileStore(BoundingPyramid.from_string(name[9:]))
        if name.startswith('file://'):
            from tilebox.layout.template import TemplateTileLayout
            from tilebox.store.filesystem import FilesystemTileStore
            return FilesystemTileStore(TemplateTileLayout(name[7:]),)
        if name.startswith('http://') or name.startswith('https://'):
            from tilebox.layout.template import TemplateTileLayout
            from tilebox.store.url import URLTileStore
            return URLTileStore((TemplateTileLayout(name),))
        if name.startswith('memcached://'):
            from tilebox.layout.template import TemplateTileLayout
            from tilebox.store.memcached import MemcachedTileStore
            from tilebox.lib.memcached import MemcachedClient
            server, template = name[12:].split('/', 1)
            host, port = server.split(':', 1)
            client = MemcachedClient(host, int(port))
            return MemcachedTileStore(client, TemplateTileLayout(template))
        if name.startswith('s3://'):
            from tilebox.layout.template import TemplateTileLayout
            from tilebox.store.s3 import S3TileStore
            bucket, template = name[5:].split('/', 1)
            return S3TileStore(bucket, TemplateTileLayout(template))
        if name.startswith('sqs://'):
            from tilebox.store.sqs import SQSTileStore
            import boto.sqs
            from boto.sqs.jsonmessage import JSONMessage
            region_name, queue_name = name[6:].split('/', 1)
            connection = boto.sqs.connect_to_region(region_name)
            queue = connection.create_queue(queue_name)
            queue.set_message_class(JSONMessage)
            return SQSTileStore(queue)
        root, ext = os.path.splitext(name)
        if ext == '.bsddb':
            import bsddb
            from tilebox.store.bsddb import BSDDBTileStore
            return BSDDBTileStore(bsddb.hashopen(name))
        if ext == '.mbtiles':
            import sqlite3
            from tilebox.store.mbtiles import MBTilesTileStore
            return MBTilesTileStore(sqlite3.connect(name))
        if ext == '.zip':
            import zipfile
            from tilebox.store.zip import ZipTileStore
            return ZipTileStore(zipfile.ZipFile(name, 'a'))
        module = __import__(name)
        components = name.split('.')
        module = reduce(lambda module, attr: getattr(module, attr),
                        components[1:],
                        module)
        return getattr(module, 'tilestore')
