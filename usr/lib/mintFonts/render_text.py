import freetype as ft
import cairo

import constants


def load_font(fontpath: str):
    # Загружаем шрифт
    face = ft.Face(fontpath)

    return face


def render_text(cr: cairo.Context,
                text: str,
                x: int, y: int,
                face, fontsize: int):
    cr.set_source_rgb(0, 0, 0)
    
    # Инициализируем позицию
    pen_x, pen_y = x, y

    face.set_char_size(64*fontsize)
    
    for char in text:
        # Загружаем глиф
        face.load_char(char, ft.FT_LOAD_RENDER)
        
        bitmap = face.glyph.bitmap
        left = face.glyph.bitmap_left
        top = face.glyph.bitmap_top
        
        # Получаем данные битмапа как bytes
        buf = bytes(bitmap.buffer)
        
        # Рассчитываем правильный stride
        stride = cairo.ImageSurface.format_stride_for_width(cairo.FORMAT_A8, bitmap.width)
        
        # Создаем буфер нужного размера
        surface_data = bytearray(stride * bitmap.rows)
        
        # Копируем данные построчно с учетом pitch (реального stride битмапа)
        for y in range(bitmap.rows):
            src_start = y * bitmap.pitch
            dst_start = y * stride
            surface_data[dst_start:dst_start+bitmap.width] = buf[src_start:src_start+bitmap.width]

        if bitmap.width > 0:  # Если печатаемый символ
            surface = cairo.ImageSurface.create_for_data(
                surface_data,
                cairo.FORMAT_A8,
                bitmap.width,
                bitmap.rows,
                stride
            )
            
            # Устанавливаем позицию для глифа
            cr.save()
            cr.translate(pen_x + left, pen_y - top)
            cr.set_source_surface(surface)
            cr.paint()
            cr.restore()
        
        # Перемещаем перо
        pen_x += face.glyph.advance.x >> 6


def get_line_sep(face,
                 fontsize: int,
                 padding: int = 5):
    face.set_char_size(64*fontsize)

    # Загрузка глифа
    face.load_char('A', ft.FT_LOAD_RENDER)

    return (face.glyph.advance.x >> 6) + constants.PADDING
