# def make_wallpapers_flowbox_item(self, wp_path):
#         pixbuf_fake_list=[]
#         pixbuf_thread = ThreadingHelper.do_async(
#             self.make_wallpaper_pixbuf,
#             (wp_path, pixbuf_fake_list)
#         )
#         ThreadingHelper.wait_for_thread(pixbuf_thread)
#         if len(pixbuf_fake_list) == 1:
#             wp_pixbuf = pixbuf_fake_list[0]
#             box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
#             image = Gtk.Image.new_from_pixbuf(wp_pixbuf)
#             box.pack_start(image, False, False, 0)
#             box.set_margin_left(12)
#             box.set_margin_right(12)
#             box.wallpaper_path = wp_path
#             return box

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio, GdkPixbuf
from . import threading_helper as ThreadingHelper

class WallpaperBox(Gtk.FlowBoxChild):

    def __init__(self, wp_path, *args, **kwds):
        super().__init__(*args, **kwds)

        self.set_halign(Gtk.Align.CENTER)
        self.set_valign(Gtk.Align.CENTER)

        self.wallpaper_path = wp_path
        self.is_fav = False
        self.container_box = Gtk.Overlay()
        self.container_box.set_halign(Gtk.Align.CENTER)
        self.container_box.set_valign(Gtk.Align.CENTER)
        self.wp_image = Gtk.Image.new_from_icon_name('image-x-generic', Gtk.IconSize.DIALOG)
        self.heart_icon = Gtk.Image.new_from_icon_name('emblem-favorite', Gtk.IconSize.DIALOG)
        self.heart_icon.set_no_show_all(True)
        self.heart_icon.set_halign(Gtk.Align.END)
        self.heart_icon.set_valign(Gtk.Align.END)
        self.heart_icon.set_margin_bottom(6)
        self.heart_icon.set_margin_right(6)
        self.container_box.add(self.wp_image)
        self.container_box.set_margin_left(12)
        self.container_box.set_margin_right(12)
        self.container_box.wallpaper_path = wp_path

        self.container_box.add_overlay(self.heart_icon)
        self.heart_icon.hide()

        self.add(self.container_box)

    def set_wallpaper_thumb(self):
        pixbuf_fake_list=[]
        pixbuf_thread = ThreadingHelper.do_async(
            self.make_wallpaper_pixbuf,
            (self.wallpaper_path, pixbuf_fake_list)
        )
        ThreadingHelper.wait_for_thread(pixbuf_thread)
        self.wp_image.set_from_pixbuf(pixbuf_fake_list[0])
        self.wp_image.show()

    def set_fav(self, fav):
        self.is_fav = fav
        if self.is_fav:
            self.heart_icon.show()
        else:
            self.heart_icon.hide()

    def make_wallpaper_pixbuf(self, wp_path, return_pixbuf_pointer=-1):
        wp_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(wp_path, 250, 250, True)
        if type(return_pixbuf_pointer) == list:
            return_pixbuf_pointer.append(wp_pixbuf)
        return wp_pixbuf
