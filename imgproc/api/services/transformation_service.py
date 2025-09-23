from .minio_service import MinioService
from .image_service import ImageService
from PIL import Image
import io


class TransformationService:
    def __init__(self):
        pass

    def resize(self, id:int, **transformation):
        img_serv = ImageService()
        minio_serv = MinioService()
        image = img_serv.get(id)
        object = minio_serv.get_object_file_from_bucket(image['bucket_name'], image['blob_name'])
        
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
        
        minio_serv.update_blob(image['bucket_name'], image['blob_name'], buffer)
        return image

    def crop(self):
        pass

    def rotate(self):
        pass

    def flip(self):
        pass

    def mirror(self):
        pass

    def compress(self):
        pass

    def change_format(self):
        pass

    def apply_filter(self):
        pass