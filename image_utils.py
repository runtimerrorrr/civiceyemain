from PIL import Image, UnidentifiedImageError
import uuid
import os


ALLOWED_FORMATS = {
    "JPEG": ".jpg",
    "PNG": ".png"
}


def validate_image(file):

    if not file or not file.filename:
        return False, "No image provided."

    try:
        file.stream.seek(0)

        image = Image.open(file.stream)

        image_format = image.format

        if image_format not in ALLOWED_FORMATS:
            return False, "Only JPG, JPEG and PNG images are allowed."

        image.verify()

        file.stream.seek(0)

        return True, image_format

    except (UnidentifiedImageError, OSError, ValueError):
        return False, "Invalid or corrupted image."

    finally:
        file.stream.seek(0)


def generate_image_filename(image_format):

    extension = ALLOWED_FORMATS[image_format]

    return str(uuid.uuid4()) + extension