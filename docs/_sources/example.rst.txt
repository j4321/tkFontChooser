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
