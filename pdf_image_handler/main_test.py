from mocks_handler import MocksHandler
from pytest import raises
from .main import PDFImageHandler

mh = MocksHandler()
mh.get_mocks_folder()
image_path = mh.get_filepath('image.jpg')
pdf_path = mh.get_filepath('valid.pdf')
invalid_pdf = mh.get_filepath('invalid.pdf')
converter = PDFImageHandler(poppler_path=r'C:\Users\bes8\OneDrive - PETROBRAS\Documents\projetos_automatizacao\poppler-24.08.0\Library\bin')

def test_image():
    assert PDFImageHandler.is_image(image_path)
    with open(image_path, 'rb') as f:
        data = f.read()
    assert PDFImageHandler.is_image(data)

def test_all():
    with raises(ValueError) as e:
        converter.get_list_of_images_bytes('not_existing')
    assert str(e.value) == "Error processing input. Check if file_path_or_bytes passed is a valid pdf or image path or bytes!\n\nError message: not_existing doesn't exists!"
    with raises(ValueError) as e:
        converter.get_list_of_images_bytes(None)
    assert str(e.value) == "Error processing input. Check if file_path_or_bytes passed is a valid pdf or image path or bytes!\n\nError message: Not a path of bytes!"
    with raises(ValueError) as e:
        converter.get_list_of_images_bytes(invalid_pdf)
    assert str(e.value) == 'Error processing input. Check if file_path_or_bytes passed is a valid pdf or image path or bytes!\n\nError message: input is not a pdf or image file!'
    assert len(converter.get_list_of_images_bytes(pdf_path)) == 1
    assert len(converter.get_list_of_images_bytes(image_path)) == 1