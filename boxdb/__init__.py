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
