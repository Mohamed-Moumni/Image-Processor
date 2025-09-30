from .minio_service import MinioService
from .image_service import ImageService
from PIL import Image, ExifTags, ImageOps, ImageEnhance, ImageFilter
import io


class TransformationService:
    def __init__(self):
        self.img_serv = ImageService()
        self.minio_serv = MinioService()

    def resize(self, image:int, **transformation):
        object = self.minio_serv.get_object_file_from_bucket(image['bucket_name'], image['blob_name'])
        
        # Open the image
        img = Image.open(object)
        original_width, original_height = img.size

        # Determine target width and height
        target_width = transformation['width'] or original_width
        target_height = transformation['height'] or original_height

        if transformation['fit'] == "fill":
            # Simply resize ignoring aspect ratio
            resized_img = img.resize((target_width, target_height))
        
        else:
            # Calculate scaling factor
            scale_w = target_width / original_width
            scale_h = target_height / original_height

            if transformation['fit'] == "contain":
                scale = min(scale_w, scale_h)
            elif transformation['fit'] == "cover":
                scale = max(scale_w, scale_h)
            else:
                raise ValueError("Invalid fit value")

            new_width = int(original_width * scale)
            new_height = int(original_height * scale)

            # Avoid upscaling if not allowed
            if not transformation['upscale']:
                new_width = min(new_width, original_width)
                new_height = min(new_height, original_height)

            resized_img = img.resize((new_width, new_height))

            # If contain, add padding to match target size
            if transformation['fit'] == "contain":
                padded_img = Image.new("RGB", (target_width, target_height), transformation['background'])
                paste_x = (target_width - new_width) // 2
                paste_y = (target_height - new_height) // 2
                padded_img.paste(resized_img, (paste_x, paste_y))
                resized_img = padded_img
        buffer = io.BytesIO()
        resized_img.save(buffer, format="PNG")
        buffer.seek(0)
        
        self.minio_serv.update_blob(image['bucket_name'], image['blob_name'], buffer)
        return image

    def crop(self, image, **transformation):
        obj = self.minio_serv.get_object_file_from_bucket(image['bucket_name'], image['blob_name'])
    
        img = Image.open(obj)
        original_width, original_height = img.size

        x = int(transformation["x"])
        y = int(transformation["y"])
        w = int(transformation["width"])
        h = int(transformation["height"])

        right = min(x + w, original_width)
        bottom = min(y + h, original_height)

        cropped_img = img.crop((x, y, right, bottom))

        buffer = io.BytesIO()
        cropped_img.save(buffer, format="PNG")
        buffer.seek(0)

        self.minio_serv.update_blob(image['bucket_name'], image['blob_name'], buffer)
        return image        

    def rotate(self, image, **transformation):
        """
        Rotate the image based on transformation attributes:
        - angle: float, rotation angle in degrees (clockwise)
        - background_color: fill color for empty areas after rotation
        - auto_orient: bool, correct orientation based on EXIF
        """
        obj = self.minio_serv.get_object_file_from_bucket(image['bucket_name'], image['blob_name'])

        img = Image.open(obj)

        if transformation.get("auto_orient", False):
            try:
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break
                exif = img._getexif()
                if exif:
                    orientation_value = exif.get(orientation, None)
                    if orientation_value == 3:
                        img = img.rotate(180, expand=True)
                    elif orientation_value == 6:
                        img = img.rotate(270, expand=True)
                    elif orientation_value == 8:
                        img = img.rotate(90, expand=True)
            except Exception:
                pass

        angle = float(transformation.get("angle", 0))
        background_color = transformation.get("background_color", "#ffffff")

        rotated_img = img.rotate(-angle, expand=True, fillcolor=background_color)

        buffer = io.BytesIO()
        rotated_img.save(buffer, format="PNG")
        buffer.seek(0)

        self.minio_serv.update_blob(image['bucket_name'], image['blob_name'], buffer)
        return image

    def flip(self, image, direction):
        obj = self.minio_serv.get_object_file_from_bucket(image['bucket_name'], image['blob_name'])
        img = Image.open(obj)
        if direction == "horizontal":
            fliped_img = ImageOps.mirror(img)
        elif direction == "vertical":
            fliped_img = ImageOps.flip(img)
        buffer = io.BytesIO()
        fliped_img.save(buffer, format="PNG")
        buffer.seek(0)

        self.minio_serv.update_blob(image['bucket_name'], image['blob_name'], buffer)
        return image

    def compress(self, image, user_id, **transformation):
        obj = self.minio_serv.get_object_file_from_bucket(image['bucket_name'], image['blob_name'])
        img = Image.open(obj)
        params = {}

        # Handle compression method
        if transformation["method"] == "progressive":
            params["progressive"] = True
        elif transformation["method"] == "lossless":
            transformation["quality"] = 100 
        # keep maximum quality, just strip metadata
        # "lossy" → just use the quality value

        params["optimize"] = transformation["optimize"]
        params["quality"] = transformation["quality"]

        # Prepare image saving
        buffer = io.BytesIO()
        save_kwargs = {
            "format": "JPEG",
            **params
        }

        # Strip metadata if required
        if transformation["strip_metadata"]:
            data = list(img.getdata())
            image = Image.new(img.mode, img.size)
            image.putdata(data)

        img.save(buffer, **save_kwargs)
        buffer.seek(0)

        self.minio_serv.update_blob(image['bucket_name'], image['blob_name'], buffer)
        return image

    def change_format(self, image, user_id:int, **transformation):
        obj = self.minio_serv.get_object_file_from_bucket(image['bucket_name'], image['blob_name'])
        img = Image.open(obj)
        params = {}

        format_map = {
            "jpeg": "JPEG",
            "png": "PNG",
            "webp": "WEBP",
            "avif": "AVIF",
            "gif": "GIF",
        }
        pil_format = format_map[transformation["format"].lower()]

        # Quality if supported
        if 'quality' in transformation and pil_format in ["JPEG", "WEBP", "AVIF"]:
            params["quality"] = transformation["quality"]

        # If converting an image with transparency → JPEG (or other non-alpha format)
        if pil_format in ["JPEG"] and img.mode in ("RGBA", "LA"):
            changed_image = Image.new("RGB", img.size, transformation["background"])
            changed_image.paste(img, mask=img.split()[-1])  # use alpha channel
        elif img.mode == "P":
            changed_image = img.convert("RGB")
        else:
            changed_image = img

        buffer = io.BytesIO()
        changed_image.save(buffer, format=pil_format, **params)
        buffer.seek(0)

        new_blob_name = '.'.join([image['blob_name'].split('.')[0], pil_format])
        image = self.img_serv.create(image['bucket_name'], new_blob_name, buffer, user_id)
        return image

    def apply_filter(self, img_record, user_id, **transformation):
        obj = self.minio_serv.get_object_file_from_bucket(img_record['bucket_name'], img_record['blob_name'])
        image = Image.open(obj)
        if transformation["intensity"] is None:
            transformation["intensity"] = 1.0
        
        transformation["filter_type"] = transformation["filter_type"].lower()
        
        if transformation["filter_type"] == "grayscale":
            image = image.convert("L").convert("RGB")
        elif transformation["filter_type"] == "sepia":
            sepia_img = image.convert("RGB")
            pixels = sepia_img.load()
            for y in range(sepia_img.height):
                for x in range(sepia_img.width):
                    r, g, b = pixels[x, y]
                    tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                    tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                    tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                    pixels[x, y] = (
                        min(int(tr * transformation["intensity"]), 255),
                        min(int(tg * transformation["intensity"]), 255),
                        min(int(tb * transformation["intensity"]), 255)
                    )
            image = sepia_img
        elif transformation["filter_type"] == "blur":
            if 'radius' in transformation:
                radius = int(transformation["radius"])
            else:
                radius = int((transformation["intensity"] * 2))
            image = image.filter(ImageFilter.GaussianBlur(radius=radius))
        elif transformation["filter_type"] == "brightness":
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(transformation["intensity"])
        elif transformation["filter_type"] == "contrast":
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(transformation["intensity"])
        elif transformation["filter_type"] == "sharpen":
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(transformation["intensity"])
        elif transformation["filter_type"] == "edge":
            if 'radius' in transformation:
                radius = transformation["radius"]
            else:
                radius = 2
            image = image.filter(ImageFilter.FIND_EDGES, radius=radius)
        else:
            raise ValueError(f"Unsupported filter type: {transformation["filter_type"]}")

        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)

        new_blob_name = '.'.join([img_record['blob_name'].split('.')[0], "PNG"])
        image = self.img_serv.create(img_record['bucket_name'], new_blob_name, buffer, user_id)
        return image