```python
from pdf_image_handler import PDFImageHandler

handler = PDFImageHandler(poppler_path=poppler_path)

# converting a pdf to list of image_bytes
converted_images = handler.get_list_of_images_bytes(pdf_path)

# converting a iage to list of image_bytes (it can be converted from path or bytes)
converted_images = handler.get_list_of_images_bytes(image_path)

#checking if a path or bytes is an image
is_image = PDFImageHandler.is_image(file_path_or_bytes)

#checking if a path or bytes is a pdf
is_pdf = PDFImageHandler.is_pdf(file_path_or_bytes)

#checking and getting bytes from path or bytes
file_bytes = PDFImageHandler.check_and_get_file_bytes_from_path_or_bytes(file_path_or_bytes)
```