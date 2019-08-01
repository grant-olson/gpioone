# UNSCII

[Unscii](https://www.google.com/search?client=firefox-b-1-d&q=unscii) is a public domain set
of fonts that have hex dumps for direct rasterization. This makes it easy to use on embedded
devices without having to deal with the, although nice, complex and large Pillow library and
.ttf font files to generate text on small devices such as OLEDs.

The files in this directory are autogenerated by running `python generate_unscii.py` and the
resulting files are not meant to be read by humans. However the module can be imported, and
a program can spit individual characters in to the exposed dictionaries `unscii_bytes` and
`unscii_transposed_bytes` to send to a matrix display.

The `unscii_transposed_bytes` flips the bytes on their side so that a device that loads data
top to bottom, then left to right, instead of the normal left-to-right, top-to-bottom, can
quickly shoot out the appropriate bits. One such device is the ubiquitious SSD1306 OLED
controller.