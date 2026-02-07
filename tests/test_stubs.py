from typing import TYPE_CHECKING


def test_old():
    import fitz

    doc = fitz.Document()
    page = doc[0]
    page.draw_rect(fitz.Rect([1, 2, 3, 4]))
    drawings = page.get_drawings()
    for drawing in drawings:
        print(drawing.get("type"))

    fdr = page.find_tables()
    tbl = fdr.tables[0]
    print(tbl.bbox)


def test_new():
    import pymupdf

    doc = pymupdf.Document()
    page = doc[0]
    page.draw_rect(pymupdf.Rect([1, 2, 3, 4]))
    drawings: list[pymupdf.DrawingDict] = page.get_drawings()
    for drawing in drawings:
        print(drawing.get("type"))

    fdr = page.find_tables()
    tbl = fdr.tables[0]
    print(tbl.bbox)

    # Pixmap constructor/property typing coverage.
    pix = pymupdf.Pixmap(pymupdf.csRGB, pymupdf.IRect(0, 0, 2, 2), False)
    mask = pymupdf.Pixmap(None, pix)
    pix2 = pymupdf.Pixmap(pix, 0)
    pix2.set_dpi(72, 72)
    print(
        mask.alpha,
        pix2.is_monochrome,
        pix2.is_unicolor,
        len(pix2.samples_mv),
        pix2.samples_ptr,
    )

    if TYPE_CHECKING:
        pymupdf.Pixmap(b"fake-image-bytes")
