tkFontChooser
=============

|Release| |Travis| |Appveyor| |Codecov| |Windows| |Linux| |Mac| |License|

A simple font chooser for Tkinter that allow the user to select the font
family among the fonts available on his/her system. The size and style
(bold, italic, underline, strikethrough) of the text can be set too.

This module contains a `FontChooser` class which implements the font
chooser and an `askfont` function that displays the font chooser and
returns the chosen font when the user closes the font chooser. The font
is returned as a dictionary like the one returned by the function
`tkFont.Font.actual`.

Requirements
------------

- Linux, Windows, Mac
- Python 2 or 3 with tkinter + ttk (default for Windows but not for Linux)


Installation
------------

- Ubuntu: use the PPA `ppa:j-4321-i/ppa`

    ::

        $ sudo add-apt-repository ppa:j-4321-i/ppa
        $ sudo apt-get update
        $ sudo apt-get install python(3)-tkfontchooser


- Archlinux: 

    the package is available on `AUR <https://aur.archlinux.org/packages/python-tkfontchooser>`__


- With pip:

    ::

        $ pip install tkfontchooser


Example
=======

.. code:: python

    try:
        from tkinter import Tk
        from tkinter.ttk import Style, Button, Label
    except ImportError:
        from Tkinter import Tk
        from ttk import Style, Button, Label
    from sys import platform
    from tkfontchooser import askfont

    # create main window
    root = Tk()
    style = Style(root)
    if "win" == platform[:3]:
        style.theme_use('vista')
    elif "darwin" in platform:
        style.theme_use('clam')
    else:
        style.theme_use('clam')
    bg = style.lookup("TLabel", "background")
    root.configure(bg=bg)
    label = Label(root, text='Chosen font: ')
    label.pack(padx=10, pady=(10,4))

    def callback():
        # open the font chooser and get the font selected by the user
        font = askfont(root)
        # font is "" if the user has cancelled
        if font:
            # spaces in the family name need to be escaped
            font['family'] = font['family'].replace(' ', '\ ')
            font_str = "%(family)s %(size)i %(weight)s %(slant)s" % font
            if font['underline']:
                font_str += ' underline'
            if font['overstrike']:
                font_str += ' overstrike'
            label.configure(font=font_str, text='Chosen font: ' + font_str.replace('\ ', ' '))

    Button(root, text='Font Chooser', command=callback).pack(padx=10, pady=(4,10))
    root.mainloop()


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
.. |Appveyor|:: https://ci.appveyor.com/api/projects/status/ydgaxicd3at93gx6?svg=true
    :target: https://ci.appveyor.com/project/j4321/tkFontChooser/branch/master
    :alt: Appveyor Build Status
.. |Codecov| image:: https://codecov.io/gh/j4321/tkFontChooser/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/j4321/tkFontChooser
    :alt: Code coverage
.. |License| image:: https://img.shields.io/github/license/j4321/tkFontChooser.svg
    :target: https://www.gnu.org/licenses/gpl-3.0.en.html
    :alt: License
