from paddleocr import PaddleOCR
from PIL import Image
import pypdfium2 as pdfium
import numpy as np
import io

# ===============================
# Lazy OCR initialization
# ===============================

_ocr = None

def get_ocr():
    global _ocr
    if _ocr is None:
        _ocr = PaddleOCR(
            use_angle_cls=False,
            lang="en",
            use_gpu=False,
            enable_mkldnn=False
        )
    return _ocr


# ===============================
# OCR IMAGE
# ===============================

def ocr_image(image: Image.Image) -> str:
    """
    Extract RAW text from a PIL image.
    NO cleanup, NO normalization.
    """
    ocr = get_ocr()

    # PaddleOCR accepts numpy arrays
    img_array = np.array(image)

    result = ocr.ocr(img_array, cls=False)

    lines = []
    for page in result:
        for block in page:
            lines.append(block[1][0])  # text only

    return "\n".join(lines)


# ===============================
# OCR PDF
# ===============================

def ocr_pdf(pdf_bytes: bytes) -> str:
    """
    Convert PDF → images → OCR → raw text
    """
    pdf = pdfium.PdfDocument(pdf_bytes)
    pages_text = []

    for page in pdf:
        bitmap = page.render_to(
            scale=2.0,   # good quality
            rotation=0
        )
        image = Image.fromarray(bitmap.to_numpy())
        pages_text.append(ocr_image(image))

    return "\n\n".join(pages_text)
