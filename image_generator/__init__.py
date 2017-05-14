import cStringIO
from PIL import Image

DEFAULT_MODE = 'RGB'


def generate_text_image(fmt, fg, bg, size, text):
    """Generate a single background color image with text in it."""
    if fmt.lower() == 'jpg':
        fmt = 'jpeg'

    img = Image.new(DEFAULT_MODE, size, color=bg)

    buffer = cStringIO.StringIO()
    img.save(buffer, format=fmt)
    return buffer.getvalue()
