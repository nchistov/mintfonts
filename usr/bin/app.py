import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import render_text
import constants


class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title='MintFonts')
        self.set_default_size(constants.WIDTH, constants.HEIGHT)

        self.fontpath = "/mnt/home/nick/Python/BeeWare/mintfonts/Bytesized-Regular.ttf"

        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.connect('draw', self.on_draw_font)
        self.add(self.drawing_area)
    
    def on_draw_font(self, widget, cr):
        cr.set_source_rgb(1, 1, 1)
        cr.paint()

        self.show_font(cr)
    
    def show_font(self, cr):
        print(self.get_size())

        face = render_text.load_font(self.fontpath)
        y = render_text.get_line_sep(face, constants.FONTSIZE)

        render_text.render_text(cr, constants.ALPHABET, constants.PADDING, y, face, constants.FONTSIZE)
        y = y*2  # Сдвигаемся на одну строку вниз
        render_text.render_text(cr, constants.ALPHABET.upper(), constants.PADDING, y, face, constants.FONTSIZE)
        y = y*1.5  # Сдвигаемся на одну строку вниз
        render_text.render_text(cr, constants.NUMBERS, constants.PADDING, y, face, constants.FONTSIZE)

        for i in range(10, 120, 10):
            y += render_text.get_line_sep(face, i)
            render_text.render_text(cr, constants.PHRASE, constants.PADDING, y, face, i)
