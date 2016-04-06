# -*- coding: utf-8 -*-

import inspect

from shaibos.util.unicode_mixin import UnicodeMixin


class Iterable(UnicodeMixin):
    # Jinja2 wants to iterate over all properties; __dict__ doesn't return the @property ones
    def __iter__(self):
        for attr, value in inspect.getmembers(self):
            if not attr.startswith('_'):
                yield attr, value
