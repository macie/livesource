.. image:: https://travis-ci.org/macie/livesource.svg?branch=master
  :target: https://travis-ci.org/macie/livesource
.. image:: https://coveralls.io/repos/macie/livesource/badge.png?branch=master
  :target: https://coveralls.io/r/macie/livesource

LiveSource is a Python library and command-line tool for monitoring values in
source code, based on ideas from Bret Victor “Inventing on Principle” lecture.


Typical usage::

    #!/usr/bin/env python
    from livesource import LiveSource

    print((LiveSource('a = max([1, 2, 3])').get_values()))
