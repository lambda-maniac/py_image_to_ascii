from PIL import Image

def cprint(string, r, g, b, foreground = True, end = "\n"):
    print(f'\x1b[{38 if foreground else 48};2;{r};{g};{b}m{string}', end = end)

def to_ascii_art(file_path, size = (64, 32), colored = False, out = "STDOUT$", dense = False):
    img = Image.open(file_path)
    img = img.resize(size, Image.ANTIALIAS)

    chars = ' .\'`^",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$' \
            if dense else                                                              \
            " .:-=+*#%@"

    total_chars        = len(chars)
    max_grey_variation = 256 # RGB Byte
    bias               = total_chars / max_grey_variation

    img_width, img_height = img.size
    img_pixels            = img.load()

    file = None
    if out != "STDOUT$": file = open(out, 'w+')

    for pixel_y in range(img_height):
        for pixel_x in range(img_width):
            r, g, b, *_ = img_pixels[pixel_x, pixel_y]

            pixel_grey_scale = (r + g + b) / 3
            pixel_weight     = int( pixel_grey_scale * bias )

            char_representation = chars[ pixel_weight    ] if pixel_weight < total_chars \
                           else   chars[ total_chars - 1 ]

            if    file : file.write (char_representation)
            if colored : cprint     (char_representation, r, g, b, end = "")
            else       : print      (char_representation, end = "")

        if file: file.write('\n')
        print("")

    if file: file.close()
