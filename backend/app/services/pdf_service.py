import fitz


def extract_pdf_text(file_path: str) -> str:
    """
    Extract all text from a PDF.
    """

    document = fitz.open(file_path)

    text = "\n".join(page.get_text() for page in document)

    document.close()

    return text


def extract_pdf_pages(file_path: str):
    document = fitz.open(file_path)
    pages = [
        {"location": f"page {index + 1}", "text": page.get_text()}
        for index, page in enumerate(document)
    ]
    document.close()
    return pages
