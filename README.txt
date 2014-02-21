==========
LiveSource
==========

LiveSource provides both: commandline application and library for live coding
and rapid development. It provides both: library and commandline application.


Applications
------------

* software development 

* education

* art (real-time audio-visual performance)

Typical usage often looks like this::

    #!/usr/bin/env python

    from livesource import SourceCode

    print((SourceCode('a = max([1, 2, 3])').code()))

(Note the double-colon and 4-space indent formatting above.)

Paragraphs are separated by blank lines. *Italics*, **bold**,
and ``monospace`` look like this.


A Section
=========

Lists look like this:

* First

* Second. Can be multiple lines
  but must be indented properly.

A Sub-Section
-------------

Numbered lists look like you'd expect:

1. hi there

2. must be going

Urls are http://like.this and links can be
written `like this <http://www.example.com/foo/bar>`_.


TODO
====

* plugins for text editors

* full test coverage

* optimization (if possible?)

Source: http://github.com/LiveSource