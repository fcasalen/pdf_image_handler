from mocks_handler import MocksHandler
from pytest import raises
from .main import PDFImageHandler, root_poppler_path, get_valid_poppler_path

mh = MocksHandler()
mh.get_mocks_folder()
image_path = mh.get_filepath('image.jpg')
pdf_path = mh.get_filepath('valid.pdf')
invalid_pdf = mh.get_filepath('invalid.pdf')

def test_get_valid_poppler_path():
    assert get_valid_poppler_path(poppler_path=None, search_for_path=False) == None
    assert get_valid_poppler_path(poppler_path=root_poppler_path, search_for_path=False)

def test_image():
    assert PDFImageHandler.is_image(image_path)
    with open(image_path, 'rb') as f:
        data = f.read()
    assert PDFImageHandler.is_image(data)

def test_all():
    with raises(ValueError) as e:
        PDFImageHandler.get_list_of_images_bytes('not_existing')
    assert str(e.value) == "Error processing input. Check if file_path_or_bytes passed is a valid pdf or image path or bytes!\n\nError message: not_existing doesn't exists!"
    with raises(ValueError) as e:
        PDFImageHandler.get_list_of_images_bytes(None)
    assert str(e.value) == "Error processing input. Check if file_path_or_bytes passed is a valid pdf or image path or bytes!\n\nError message: Not a path of bytes!"
    with raises(ValueError) as e:
        PDFImageHandler.get_list_of_images_bytes(invalid_pdf)
    assert str(e.value) == 'Error processing input. Check if file_path_or_bytes passed is a valid pdf or image path or bytes!\n\nError message: input is not a pdf or image file!'
    assert len(PDFImageHandler.get_list_of_images_bytes(pdf_path)) == 1
    assert len(PDFImageHandler.get_list_of_images_bytes(image_path)) == 1