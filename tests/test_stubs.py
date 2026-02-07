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
