def test_old():
    import fitz

    doc = fitz.Document()
    page = doc[0]
    page.draw_rect(fitz.Rect([1, 2, 3, 4]))

    fdr = page.find_tables()
    tbl = fdr.tables[0]
    print(tbl.bbox)


def test_new():
    import pymupdf

    doc = pymupdf.Document()
    page = doc[0]
    page.draw_rect(pymupdf.Rect([1, 2, 3, 4]))

    fdr = page.find_tables()
    tbl = fdr.tables[0]
    print(tbl.bbox)
