import sys


class UnicodeMixin(object):
    """Mixin class to handle defining the proper __str__/__unicode__ methods in Python 2 or 3."""

    def __unicode__(self):
        # Override this
        pass

    if sys.version_info[0] >= 3:  # Python 3
        def __str__(self):
            return self.__unicode__()
    else:  # Python 2
        def __str__(self):
            return self.__unicode__().encode('utf-8')
