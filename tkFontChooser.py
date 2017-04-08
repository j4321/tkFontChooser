#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""
tkFontChooser - Font chooser for Tkinter
Copyright 2016-2017 Juliette Monsel <j_4321@protonmail.com>

tkFontChooser is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

tkFontChooser is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


try:
    from tkinter import Toplevel, Listbox, StringVar, BooleanVar, TclError
    from tkinter.ttk import Checkbutton, Frame, Label, Button, Scrollbar, Style, Entry
    from tkinter.font import families, Font
except ImportError:
    from Tkinter import Toplevel, Listbox, StringVar, BooleanVar
    from ttk import Checkbutton, Frame, Label, Button, Scrollbar, Style, Entry
    from tkFont import families, Font

from locale import getdefaultlocale

lang = getdefaultlocale()[0][:2]

EN = {"Cancel": "Cancel", "Bold": "Bold", "Italic": "Italic",
      "Underline": "Underline", "Overstrike": "Strikethrough"}
FR = {"Cancel": "Annuler", "Bold": "Gras", "Italic": "Italique",
      "Underline": "Souligné", "Overstrike": "Barré"}
LANGUAGES = {"fr": FR, "en": EN}
if lang == "fr":
    TR = LANGUAGES["fr"]
else:
    TR = LANGUAGES["en"]


class FontChooser(Toplevel):
    """ Font chooser toplevel """

    def __init__(self, master, font_dict={}, text="Abcd", **kwargs):
        """
            Create a new FontChooser instance.

            font: dictionnary, like the one returned by the .actual
                  method of a Font object

                    {'family': 'DejaVu Sans',
                     'overstrike':False,
                     'size': 12,
                     'slant': 'italic' or 'roman',
                     'underline': False,
                     'weight': 'bold' or 'normal'}

            text: text to be displayed in the preview label

            **kwargs: additional keyword arguments to be passed to
                      Toplevel.__init__
        """
        Toplevel.__init__(self, master, **kwargs)
        self.title("Font Chooser")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.quit)
        self._validate_family = self.register(self.validate_font_family)
        self._validate_size = self.register(self.validate_font_size)

        # variable storing the chosen font
        self.res = ""

        style = Style(self)
        style.configure("prev.TLabel", background="white")
        bg = style.lookup("TLabel", "background")
        self.configure(bg=bg)

        # family list
        self.fonts = list(set(families()))
        self.fonts.append("TkDefaultFont")
        self.fonts.sort()
        for i in range(len(self.fonts)):
            self.fonts[i] = self.fonts[i].replace(" ", "\ ")
        max_length = int(2.5*max([len(font) for font in self.fonts]))//3
        self.sizes = ["%i" % i for i in (list(range(6, 17)) + list(range(18, 32, 2)))]
        # font default
        font_dict["weight"] = font_dict.get("weight", "normal")
        font_dict["slant"] = font_dict.get("slant", "roman")
        font_dict["underline"] = font_dict.get("underline", False)
        font_dict["overstrike"] = font_dict.get("overstrike", False)
        font_dict["family"] = font_dict.get("family",
                                            self.fonts[0].replace('\ ', ' '))
        font_dict["size"] = font_dict.get("size", 10)

        # Widgets creation
        options_frame = Frame(self, relief='groove', borderwidth=2)
        self.font_family = StringVar(self, " ".join(self.fonts))
        self.font_size = StringVar(self, " ".join(self.sizes))
        self.var_bold = BooleanVar(self, font_dict["weight"] == "bold")
        b_bold = Checkbutton(options_frame, text=TR["Bold"],
                             command=self.toggle_bold,
                             variable=self.var_bold)
        b_bold.grid(row=0, sticky="w", padx=4, pady=(4, 2))
        self.var_italic = BooleanVar(self, font_dict["slant"] == "italic")
        b_italic = Checkbutton(options_frame, text=TR["Italic"],
                               command=self.toggle_italic,
                               variable=self.var_italic)
        b_italic.grid(row=1, sticky="w", padx=4, pady=2)
        self.var_underline = BooleanVar(self, font_dict["underline"])
        b_underline = Checkbutton(options_frame, text=TR["Underline"],
                                  command=self.toggle_underline,
                                  variable=self.var_underline)
        b_underline.grid(row=2, sticky="w", padx=4, pady=2)
        self.var_overstrike = BooleanVar(self, font_dict["overstrike"])
        b_overstrike = Checkbutton(options_frame, text=TR["Overstrike"],
                                   variable=self.var_overstrike,
                                   command=self.toggle_overstrike)
        b_overstrike.grid(row=3, sticky="w", padx=4, pady=(2, 4))
        self.var_size = StringVar(self)
        self.entry_family = Entry(self, width=max_length, validate="key",
                                  validatecommand=(self._validate_family, "%d", "%S",
                                                   "%i", "%s", "%V"))
        entry_size = Entry(self, width=4, validate="key",
                           textvariable=self.var_size,
                           validatecommand=(self._validate_size, "%d", "%P", "%V"))
        self.list_family = Listbox(self, selectmode="browse",
                                   listvariable=self.font_family,
                                   highlightthickness=0,
                                   exportselection=False,
                                   width=max_length)
        self.list_size = Listbox(self, selectmode="browse",
                                 listvariable=self.font_size,
                                 highlightthickness=0,
                                 exportselection=False,
                                 width=4)
        scroll_family = Scrollbar(self, orient='vertical',
                                  command=self.list_family.yview)
        scroll_size = Scrollbar(self, orient='vertical',
                                command=self.list_size.yview)
        self.preview_font = Font(self, **font_dict)
        if len(text) > 30:
            text = text[:30]
        self.preview = Label(self, relief="groove", style="prev.TLabel",
                             text=text, font=self.preview_font,
                             anchor="center")

        # Widget configuration
        self.list_family.configure(yscrollcommand=scroll_family.set)
        self.list_size.configure(yscrollcommand=scroll_size.set)

        self.entry_family.insert(0, font_dict["family"])
        self.entry_family.selection_clear()
        self.entry_family.icursor("end")
        entry_size.insert(0, font_dict["size"])

        i = self.fonts.index(self.entry_family.get().replace(" ", "\ "))
        self.list_family.selection_clear(0, "end")
        self.list_family.selection_set(i)
        self.list_family.see(i)
        i = self.sizes.index(entry_size.get())
        self.list_size.selection_clear(0, "end")
        self.list_size.selection_set(i)
        self.list_size.see(i)

        self.entry_family.grid(row=0, column=0, sticky="ew",
                               pady=(10, 1), padx=(10, 0))
        entry_size.grid(row=0, column=2, sticky="ew",
                        pady=(10, 1), padx=(10, 0))
        self.list_family.grid(row=1, column=0, sticky="nsew",
                              pady=(1, 10), padx=(10, 0))
        self.list_size.grid(row=1, column=2, sticky="nsew",
                            pady=(1, 10), padx=(10, 0))
        scroll_family.grid(row=1, column=1, sticky='ns', pady=(1, 10))
        scroll_size.grid(row=1, column=3, sticky='ns', pady=(1, 10))
        options_frame.grid(row=0, column=4, rowspan=2,
                           padx=10, pady=10, ipadx=10)

        self.preview.grid(row=2, column=0, columnspan=5, sticky="eswn",
                          padx=10, pady=(0, 10), ipadx=4, ipady=4)

        button_frame = Frame(self)
        button_frame.grid(row=3, column=0, columnspan=5, pady=(0, 10), padx=10)

        Button(button_frame, text="Ok",
               command=self.ok).grid(row=0, column=0, padx=4, sticky='ew')
        Button(button_frame, text=TR["Cancel"],
               command=self.quit).grid(row=0, column=1, padx=4, sticky='ew')
        self.list_family.bind('<<ListboxSelect>>', self.update_entry_family)
        self.list_size.bind('<<ListboxSelect>>', self.update_entry_size,
                            add=True)
        self.list_family.bind("<KeyPress>", self.keypress)
        self.entry_family.bind("<Return>", self.change_font_family)
        self.entry_family.bind("<Tab>", self.tab)
        entry_size.bind("<Return>", self.change_font_size)

        self.entry_family.bind("<Down>", self.down_family)
        entry_size.bind("<Down>", self.down_size)

        self.entry_family.bind("<Up>", self.up_family)
        entry_size.bind("<Up>", self.up_size)

        # bind Ctrl+A to select all instead of go to beginning
        self.bind_class("TEntry", "<Control-a>", self.select_all)

        self.update_idletasks()
        self.grab_set()
        self.entry_family.focus_set()
        self.lift()


    def select_all(self, event):
        event.widget.selection_range(0, "end")

    def keypress(self, event):
        key = event.char.lower()
        l = [i for i in self.fonts if i[0].lower() == key]
        if l:
            i = self.fonts.index(l[0])
            self.list_family.selection_clear(0, "end")
            self.list_family.selection_set(i)
            self.list_family.see(i)
            self.update_entry_family()

    def up_family(self, event):
        try:
            txt = self.entry_family.get().replace(" ", "\ ")
            l = [i for i in self.fonts if i[:len(txt)] == txt]
            if l:
                self.list_family.selection_clear(0, "end")
                i = self.fonts.index(l[0])
                if i > 0:
                    self.list_family.selection_set(i - 1)
                    self.list_family.see(i - 1)
                else:
                    i = len(self.fonts)
                    self.list_family.see(i - 1)
                    self.list_family.select_set(i - 1)

        except TclError:
            i = len(self.fonts)
            self.list_family.see(i - 1)
            self.list_family.select_set(i - 1)
        self.list_family.event_generate('<<ListboxSelect>>')

    def up_size(self, event):
        try:
            s = self.var_size.get()
            i = self.sizes.index(s)
            self.list_size.selection_clear(0, "end")
            if i > 0:
                self.list_size.selection_set(i - 1)
                self.list_size.see(i - 1)
            else:
                i = len(self.sizes)
                self.list_size.see(i - 1)
                self.list_size.select_set(i - 1)
        except TclError:
            i  = len(self.sizes)
            self.list_size.see(i - 1)
            self.list_size.select_set(i - 1)
        self.list_size.event_generate('<<ListboxSelect>>')

    def down_family(self, event):
        try:
            txt = self.entry_family.get().replace(" ", "\ ")
            l = [i for i in self.fonts if i[:len(txt)] == txt]
            if l:
                self.list_family.selection_clear(0, "end")
                i = self.fonts.index(l[0])
                if i < len(self.fonts) - 1:
                    self.list_family.selection_set(i + 1)
                    self.list_family.see(i + 1)
                else:
                    self.list_family.see(0)
                    self.list_family.select_set(0)

        except TclError:
            self.list_family.selection_set(0)
        self.list_family.event_generate('<<ListboxSelect>>')

    def down_size(self, event):
        try:
            s = self.var_size.get()
            i = self.sizes.index(s)
            self.list_size.selection_clear(0, "end")
            if i < len(self.sizes) - 1:
                self.list_size.selection_set(i + 1)
                self.list_size.see(i + 1)
            else:
                self.list_size.see(0)
                self.list_size.select_set(0)
        except TclError:
            self.list_size.selection_set(0)
        self.list_size.event_generate('<<ListboxSelect>>')

    def toggle_bold(self):
        b = self.var_bold.get()
        self.preview_font.configure(weight=["normal", "bold"][b])

    def toggle_italic(self):
        b = self.var_italic.get()
        self.preview_font.configure(slant=["roman", "italic"][b])

    def toggle_underline(self):
        b = self.var_underline.get()
        self.preview_font.configure(underline=b)

    def toggle_overstrike(self):
        b = self.var_overstrike.get()
        self.preview_font.configure(overstrike=b)

    def change_font_family(self, event=None):
#        family = self.var_family.get()
        family = self.entry_family.get()
        if family.replace(" ", "\ ") in self.fonts:
            self.preview_font.configure(family=family)

    def change_font_size(self, event=None):
        size = int(self.var_size.get())
        self.preview_font.configure(size=size)

    def validate_font_size(self, d, ch, V):
        ''' Validation of the size entry content '''
        l = [i for i in self.sizes if i[:len(ch)] == ch]
        if l:
            i = self.sizes.index(l[0])
            self.list_size.selection_clear(0, "end")
            self.list_size.selection_set(i)
            deb = self.list_size.nearest(0)
            fin = self.list_size.nearest(self.list_size.winfo_height())
            if V != "forced":
                if i < deb or i > fin:
                    self.list_size.see(i)
                return True
        if d == '1':
            return ch.isdigit()
        else:
            return True

#    def validate_font_family(self, ch, V):
#        ''' Validation of the family entry content '''
#        ch = ch.replace(" ", "\ ")
#        l = [i for i in self.fonts if i[:len(ch)] == ch]
#        if not l:
#            return False
#        else:
#            i = self.fonts.index(l[0])
#            self.list_family.selection_clear(0, "end")
#            self.list_family.selection_set(i)
#            deb = self.list_family.nearest(0)
#            fin = self.list_family.nearest(self.list_family.winfo_height())
#            index = self.entry_family.index("insert")
#            self.entry_family.delete(0, "end")
#            self.entry_family.insert(0, l[0].replace("\ ", " "))
#            self.entry_family.icursor(index)
#            if V != "forced":
#                if i < deb or i > fin:
#                    self.list_family.see(i)
#                return True
#

    def tab(self, event):
        self.entry_family = event.widget
        self.entry_family.selection_clear()
        self.entry_family.icursor("end")
        return "break"

    def validate_font_family(self, action, modif, pos, prev_txt, V):
        """ completion of the text in the path entry with existing
            folder/file names """
        if self.entry_family.selection_present():
            sel = self.entry_family.selection_get()
            txt = prev_txt.replace(sel, '')
        else:
            txt = prev_txt
        if action == "0":
            txt = txt[:int(pos)] + txt[int(pos)+1:]
            return True
        else:
            txt = txt[:int(pos)] + modif + txt[int(pos):]
            ch = txt.replace(" ", "\ ")
            l = [i for i in self.fonts if i[:len(ch)] == ch]
            if l:
                i = self.fonts.index(l[0])
                self.list_family.selection_clear(0, "end")
                self.list_family.selection_set(i)
                deb = self.list_family.nearest(0)
                fin = self.list_family.nearest(self.list_family.winfo_height())
                index = self.entry_family.index("insert")
                self.entry_family.delete(0, "end")
                self.entry_family.insert(0, l[0].replace("\ ", " "))
                self.entry_family.selection_range(index + 1, "end")
                self.entry_family.icursor(index + 1)
                if V != "forced":
                    if i < deb or i > fin:
                        self.list_family.see(i)
                return True
            else:
                return False

    def update_entry_family(self, event=None):
        #  family = self.list_family.get("@%i,%i" % (event.x , event.y))
        family = self.list_family.get(self.list_family.curselection()[0])
        self.entry_family.delete(0, "end")
        self.entry_family.insert(0, family)
        self.entry_family.selection_clear()
        self.entry_family.icursor("end")
        self.change_font_family()

    def update_entry_size(self, event):
        #  size = self.list_size.get("@%i,%i" % (event.x , event.y))
        size = self.list_size.get(self.list_size.curselection()[0])
        self.var_size.set(size)
        self.change_font_size()

    def ok(self):
        self.res = self.preview_font.actual()
        self.quit()

    def get_res(self):
        return self.res

    def quit(self):
        self.destroy()


def askfont(master=None, text="Abcd", **font_args):
    """ Open the font chooser and return the chosen font.
        text: sample text to be displayed in the font chooser
        font_args: family, size, slant (=roman/italic),
                   weight (=normal/bold), underline (bool), overstrike (bool)
    """
    chooser = FontChooser(master, font_args, text)
    chooser.wait_window(chooser)
    return chooser.get_res()


if __name__ == "__main__":
    ''' Minimal example '''
    try:
        from tkinter import Tk
    except ImportError:
        from Tkinter import Tk
    from sys import platform

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
    label.pack(padx=10, pady=(10, 4))

    def callback():
        font = askfont(root)
        if font:
            # spaces in the family name need to be escaped
            font['family'] = font['family'].replace(' ', '\ ')
            font_str = "%(family)s %(size)i %(weight)s %(slant)s" % font
            if font['underline']:
                font_str += ' underline'
            if font['overstrike']:
                font_str += ' overstrike'
            label.configure(font=font_str,
                            text='Chosen font: ' + font_str.replace('\ ', ' '))

    Button(root, text='Font Chooser',
           command=callback).pack(padx=10, pady=(4, 10))
    root.mainloop()
