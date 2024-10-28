from pdf2image import convert_from_bytes
from PIL import Image
from io import BytesIO
from os.path import exists, dirname, join
from tkinter import filedialog

root_poppler_path = join(dirname(__file__), 'poppler_path.txt')

def image_to_bytes(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return buffered.getvalue()

def get_valid_poppler_path(poppler_path:str = None):
    if poppler_path == root_poppler_path:
        with open(root_poppler_path, 'r', encoding='utf-8') as f:
            poppler_path = f.read()
    if not exists(poppler_path):
        poppler_path = None
    valid_poppler_path = False
    while not valid_poppler_path:
        if not poppler_path:
            poppler_path = filedialog.askopenfilename(title='Select the poppler...')
        if not poppler_path:
            return
        try:
            with open(join(dirname(__file__), 'valid.pdf'), 'rb') as f:
                data = f.read()
            convert_from_bytes(pdf_file=data, poppler_path=poppler_path)
            valid_poppler_path = True
        except Exception as e:
            print(e)
            valid_poppler_path = False
            poppler_path = None
    if data != poppler_path:
        with open(root_poppler_path, 'w', encoding='utf-8') as f:
            f.write(poppler_path)    
    return poppler_path

class PDFImageHandler:
    poppler_path = get_valid_poppler_path(root_poppler_path)
    
    @classmethod
    def get_list_of_images_bytes(cls, file_path_or_bytes:str|bytes):
        try:
            file_bytes = cls.check_and_get_file_bytes_from_path_or_bytes(file_path_or_bytes)
            if not cls.is_pdf(file_bytes):
                if not cls.is_image(file_path_or_bytes=file_bytes):
                    raise ValueError("input is not a pdf or image file!")
                return [file_bytes]
            else:
                to_convert = convert_from_bytes(file_bytes, poppler_path=cls.poppler_path)
                return [image_to_bytes(im) for im in to_convert]
        except Exception as e:
            raise ValueError(f"Error processing input. Check if file_path_or_bytes passed is a valid pdf or image path or bytes!\n\nError message: {e}")
    
    @classmethod
    def set_poppler_path(cls, poppler_path:str):
        cls.poppler_path = get_valid_poppler_path(poppler_path)

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