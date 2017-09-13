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

Tests
"""

import unittest
from tkfontchooser import FontChooser
try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk


class BaseWidgetTest(unittest.TestCase):
    def setUp(self):
        self.window = tk.Toplevel()
        self.window.update()

    def tearDown(self):
        self.window.update()
        self.window.destroy()


class TestEvent:
    """Fake event for testing."""
    def __init__(self, **kwargs):
        self._prop = kwargs

    def __getattr__(self, attr):
        if attr not in self._prop:
            raise AttributeError("TestEvent has no attribute %s." % attr)
        else:
            return self._prop[attr]


class TestFontChooser(BaseWidgetTest):
    def test_fontchooser_init(self):
        FontChooser(self.window,
                    {'family': 'Arial', 'weight': 'bold', 'slant': 'italic'},
                    text='Abcd', title='Test')
        self.window.update()
