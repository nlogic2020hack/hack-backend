from pdf2image import convert_from_path


def slice_pdf_on_images(pdf_path):
    pages = convert_from_path(pdf_path, 500)
    return pages
