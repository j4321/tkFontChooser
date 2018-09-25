.. tkfontchooser documentation master file, created by
   sphinx-quickstart on Tue Sep 25 12:51:34 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

tkfontchooser
=============

|Release| |Travis| |Appveyor| |Codecov| |Windows| |Linux| |Mac| |License|

A simple font chooser for Tkinter that allow the user to select the font
family among the fonts available on his/her system. The size and style
(bold, italic, underline, strikethrough) of the text can be set too.

This module contains a ``FontChooser`` class which implements the font
chooser and an ``askfont`` function that displays the font chooser and
returns the chosen font when the user closes the font chooser. The font
is returned as a dictionary like the one returned by the function
``tkFont.Font.actual``.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   example
   documentation
   changelog


.. |Release| image:: https://badge.fury.io/py/tkfontchooser.svg
    :alt: Latest Release
.. _Release:  https://pypi.org/project/tkfontchooser/
.. |Linux| image:: https://img.shields.io/badge/platform-Linux-blue.svg
    :alt: Platform
.. |Windows| image:: https://img.shields.io/badge/platform-Windows-blue.svg
    :alt: Platform
.. |Mac| image:: https://img.shields.io/badge/platform-Mac-blue.svg
    :alt: Platform
.. |Travis| image:: https://travis-ci.org/j4321/tkFontChooser.svg?branch=master
    :target: https://travis-ci.org/j4321/tkFontChooser
    :alt: Travis CI Build Status
.. |Appveyor| image:: https://ci.appveyor.com/api/projects/status/ydgaxicd3at93gx6/branch/master?svg=true
    :target: https://ci.appveyor.com/project/j4321/tkfontchooser/branch/master
    :alt: Appveyor Build Status
.. |Codecov| image:: https://codecov.io/gh/j4321/tkFontChooser/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/j4321/tkFontChooser
    :alt: Code coverage
.. |License| image:: https://img.shields.io/github/license/j4321/tkFontChooser.svg
    :target: https://www.gnu.org/licenses/gpl-3.0.en.html
    :alt: License
