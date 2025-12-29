from paddleocr import PaddleOCR
from PIL import Image
import fitz  # PyMuPDF
import io

# Initialize once (important for performance)
ocr = PaddleOCR(
    use_angle_cls=False,
    lang="en",
    use_gpu=False,
    enable_mkldnn=False
)

def ocr_image(image: Image.Image) -> str:
    """
    Extract RAW text from an image.
    NO cleanup, NO normalization.
    """
    result = ocr.ocr(image, cls=True)

    lines = []
    for page in result:
        for block in page:
            lines.append(block[1][0])  # text only

    return "\n".join(lines)


def ocr_pdf(pdf_bytes: bytes) -> str:
    """
    Convert PDF → images → OCR → raw text
    """
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    pages_text = []

    for page in doc:
        pix = page.get_pixmap(dpi=300)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        pages_text.append(ocr_image(img))

    return "\n\n".join(pages_text)
