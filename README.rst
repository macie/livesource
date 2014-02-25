LiveSource is a Python library and command-line tool for monitoring values in
source code, based on ideas from Bret Victor “Inventing on Principle” lecture.


Typical usage::

    #!/usr/bin/env python
    from livesource import LiveSource

    print((LiveSource('a = max([1, 2, 3])').get_values()))
