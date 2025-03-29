#!/usr/bin/python3
import sys

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, cairo

import render_text
import constants
from get_fonts import get_system_fonts, get_font_metadata


class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title='MintFonts')
        self.set_default_size(constants.WIDTH, constants.HEIGHT)
        self.set_default_icon_name('preferences-desktop-font')

        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.connect('draw', self.on_draw_font)
        self.add(self.drawing_area)

        self.hb = Gtk.HeaderBar()
        self.hb.set_show_close_button(True)
        self.hb.set_title('All fonts')

        self.set_titlebar(self.hb)

        self.load_font(sys.argv[1])
        self.fonts = get_system_fonts()
    
    def load_font(self, path):
        self.face = render_text.load_font(path)

        fontmeta = get_font_metadata(path)
        self.hb.set_title(fontmeta['family'])
        self.hb.set_subtitle(fontmeta['style'])

        button = Gtk.Button(label='Install')
        button.get_style_context().add_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)

        if path in get_system_fonts():
            button.set_label('Installed')
            button.set_sensitive(False)
        
        self.hb.pack_end(button)

    def on_draw_font(self, widget, cr):
        cr.set_source_rgb(1, 1, 1)
        cr.paint()

        self.show_font(cr)

    def show_font(self, cr: cairo.Context):
        y = render_text.get_line_sep(self.face, constants.FONTSIZE)

        render_text.render_text(cr, constants.ALPHABET, constants.PADDING, y, self.face, constants.FONTSIZE)
        y = y*2  # Сдвигаемся на одну строку вниз
        render_text.render_text(cr, constants.ALPHABET.upper(), constants.PADDING, y, self.face, constants.FONTSIZE)
        y = y*1.5  # Сдвигаемся на одну строку вниз
        render_text.render_text(cr, constants.NUMBERS, constants.PADDING, y, self.face, constants.FONTSIZE)

        for i in range(10, 120, 15):
            y += render_text.get_line_sep(self.face, i)
            render_text.render_text(cr, constants.PHRASE, constants.PADDING, y, self.face, i)


if __name__ == '__main__':
    w = MainWindow()
    w.connect('destroy', Gtk.main_quit)
    w.show_all()
    Gtk.main()
