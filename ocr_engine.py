from PIL import Image
import pypdfium2 as pdfium
import numpy as np

_ocr = None

def get_ocr():
    global _ocr
    if _ocr is None:
        print("🔁 Lazy-loading PaddleOCR...")
        from paddleocr import PaddleOCR
        _ocr = PaddleOCR(
            use_angle_cls=False,
            lang="en",
            use_gpu=False
        )
        print("✅ PaddleOCR loaded")
    return _ocr


def ocr_image(image: Image.Image) -> str:
    ocr = get_ocr()
    img_np = np.array(image)

    result = ocr.ocr(img_np, cls=False)

    lines = []
    for block in result:
        for line in block:
            lines.append(line[1][0])

    return "\n".join(lines)


def ocr_pdf(pdf_bytes: bytes) -> str:
    pdf = pdfium.PdfDocument(pdf_bytes)
    pages_text = []

    for page in pdf:
        img = page.render_to(
            pdfium.BitmapConv.pil_image,
            scale=2
        )
        pages_text.append(ocr_image(img))

    return "\n\n".join(pages_text)
