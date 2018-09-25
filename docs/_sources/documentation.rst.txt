Documentation
=============

::

    askfont(master=None, text="Abcd", title="Font Chooser", **font_args)

Open the font chooser and return a dictionary of the font properties. This
dictionary is similar to the one returned by the ``actual`` method of a tkinter
``Font`` object.

::

    {'family': str,
     'size': int,
     'weight': 'bold'/'normal',
     'slant': 'italic'/'roman',
     'underline': bool,
     'overstrike': bool}

General arguments
~~~~~~~~~~~~~~~~~

    master : Tk or Toplevel instance
        parent window

    text : str
        sample text to be displayed in the font chooser

    title : str
        dialog title

Font arguments
~~~~~~~~~~~~~~

    family : str
        font family

    size : int
        font size

    slant : str
        "roman" or "italic"

    weight : str
        "normal" or "bold"

    underline : bool
        whether the text is underlined

    overstrike : bool
        whether the text is overstriked
