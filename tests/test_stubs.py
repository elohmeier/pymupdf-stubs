from typing import TYPE_CHECKING, assert_type


def test_drawing_item_narrowing() -> None:
    import pymupdf

    def _assert_narrow(item: pymupdf.DrawingItem) -> None:
        if item[0] == "l":
            assert_type(item, pymupdf.DrawingLineItem)
        elif item[0] == "c":
            assert_type(item, pymupdf.DrawingCurveItem)
        elif item[0] == "re":
            assert_type(item, pymupdf.DrawingRectItem)
        else:
            assert_type(item, pymupdf.DrawingQuadItem)

    _assert_narrow(("l", pymupdf.Point(), pymupdf.Point()))
    _assert_narrow(
        ("c", pymupdf.Point(), pymupdf.Point(), pymupdf.Point(), pymupdf.Point())
    )
    _assert_narrow(("re", pymupdf.Rect(), 1))
    _assert_narrow(("qu", pymupdf.Quad()))


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
    drawings: list[pymupdf.DrawingPathDict] = page.get_drawings()
    for drawing in drawings:
        print(drawing.get("type"))
    drawings_extended: list[pymupdf.DrawingDict] = page.get_drawings(extended=True)
    for drawing in drawings_extended:
        print(drawing.get("type"))
    assert_type(page.get_drawings(), list[pymupdf.DrawingPathDict])
    assert_type(page.get_drawings(extended=False), list[pymupdf.DrawingPathDict])
    assert_type(page.get_drawings(extended=True), list[pymupdf.DrawingDict])

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
