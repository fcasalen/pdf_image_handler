from pdf2image import convert_from_bytes
from PIL import Image
from io import BytesIO
from os.path import exists

def image_to_bytes(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return buffered.getvalue()

class PDFImageHandler:
    def __init__(self, poppler_path:str) -> None:
        self.poppler_path = poppler_path

    def get_list_of_images_bytes(self, file_path_or_bytes:str|bytes):
        try:
            file_bytes = self.check_and_get_file_bytes_from_path_or_bytes(file_path_or_bytes)
            if not self.is_pdf(file_bytes):
                if not self.is_image(file_path_or_bytes=file_bytes):
                    raise ValueError("input is not a pdf or image file!")
                return [file_bytes]
            else:
                to_convert = convert_from_bytes(file_bytes, poppler_path=self.poppler_path)
                return [image_to_bytes(im) for im in to_convert]
        except Exception as e:
            raise ValueError(f"Error processing input. Check if file_path_or_bytes passed is a valid pdf or image path or bytes!\n\nError message: {e}")

    @classmethod
    def check_and_get_file_bytes_from_path_or_bytes(cls, pdf_image_path_or_bytes):
        if isinstance(pdf_image_path_or_bytes, bytes):
            return pdf_image_path_or_bytes
        elif isinstance(pdf_image_path_or_bytes, str):
            if not exists(pdf_image_path_or_bytes):
                raise ValueError(f"{pdf_image_path_or_bytes} doesn't exists!")
            with open(pdf_image_path_or_bytes, 'rb') as f:
                data = f.read()
            return data
        else:
            raise ValueError('Not a path of bytes!')
        
    @classmethod
    def is_image(cls, file_path_or_bytes:str|bytes):
        try:
            if isinstance(file_path_or_bytes, bytes):
                file_path_or_bytes = BytesIO(file_path_or_bytes)
            Image.open(file_path_or_bytes).verify()
            return True
        except Exception as e:
            return False
    
    @classmethod
    def is_pdf(cls, file_path_or_bytes):
        if isinstance(file_path_or_bytes, str):
            with open(file_path_or_bytes, 'rb') as f:
                file_bytes = f.read()
        else:
            file_bytes = file_path_or_bytes
        if not file_bytes.startswith(b'%PDF-'):
            return False
        return True