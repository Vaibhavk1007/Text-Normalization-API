from paddleocr import PaddleOCR
from PIL import Image
import pypdfium2 as pdfium
import numpy as np   # ✅ ADD
import io

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


def ocr_image(image: Image.Image) -> str:
    ocr = get_ocr()

    # ✅ FIX: PIL → numpy array
    img_np = np.array(image)

    result = ocr.ocr(img_np, cls=False)

    lines = []
    for block in result:
        for line in block:
            lines.append(line[1][0])

    return "\n".join(lines)


def ocr_pdf(pdf_bytes: bytes) -> str:
    pdf = pdfium.PdfDocument(pdf_bytes)
    text_pages = []

    for page in pdf:
        pil_image = page.render_to(
            pdfium.BitmapConv.pil_image,
            scale=2
        )
        text_pages.append(ocr_image(pil_image))

    return "\n\n".join(text_pages)
