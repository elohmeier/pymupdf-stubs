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


def test_get_drawings_usage_pattern() -> None:
    import pymupdf

    doc = pymupdf.Document()
    page = doc[0]

    min_line_len = 10.0
    h_lines: list[float] = []
    v_lines: list[float] = []
    header_fill_y0: float | None = None

    for path in page.get_drawings():
        fill = path.get("fill")
        items = path.get("items")
        if not items:
            continue
        for item in items:
            if item[0] == "l":
                assert_type(item, pymupdf.DrawingLineItem)
                p1, p2 = item[1], item[2]
                length = ((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2) ** 0.5
                if length < min_line_len:
                    continue
                if abs(p1.y - p2.y) < 2:
                    h_lines.append((p1.y + p2.y) / 2)
                elif abs(p1.x - p2.x) < 2:
                    v_lines.append((p1.x + p2.x) / 2)
            elif item[0] == "re":
                assert_type(item, pymupdf.DrawingRectItem)
                r = item[1]
                w = abs(r.x1 - r.x0)
                h = abs(r.y1 - r.y0)
                if fill and w > 100 and h > 10:
                    header_fill_y0 = r.y0

    assert_type(h_lines, list[float])
    assert_type(v_lines, list[float])
    assert_type(header_fill_y0, float | None)


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
    page_by_chapter = doc[(0, 0)]
    page_slice = doc[:1]
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
    assert_type(page_by_chapter, pymupdf.Page)
    assert_type(page_slice, list[pymupdf.Page])
    assert_type(doc.load_page(), pymupdf.Page)
    assert_type(doc.load_page((0, 0)), pymupdf.Page)

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

    # paper_rect / paper_size (issue #4)
    assert_type(pymupdf.paper_rect("A4"), pymupdf.Rect)
    assert_type(pymupdf.paper_size("letter"), tuple[int, int])

    # show_pdf_page (issue #3)
    src_doc = pymupdf.Document()
    xref = page.show_pdf_page(pymupdf.Rect(0, 0, 100, 100), src_doc, pno=0)
    assert_type(xref, int)

    # xref_object and Page.xref
    assert_type(page.xref, int)
    obj_str = doc.xref_object(page.xref)
    assert_type(obj_str, str)

    textpage = page.get_textpage(flags=0, matrix=pymupdf.Identity)
    assert_type(textpage, pymupdf.TextPage)
    assert_type(page.get_text(), str)
    assert_type(page.get_text("html"), str)
    assert_type(page.get_text("dict"), pymupdf.TextPageDict)
    assert_type(page.get_text("rawdict"), pymupdf.TextPageRawDict)
    assert_type(page.get_text("words"), list[pymupdf.TextWord])
    assert_type(page.get_text("blocks"), list[pymupdf.TextBlock])
    assert_type(doc.get_page_text(0), str)
    assert_type(doc.get_page_text(0, "dict"), pymupdf.TextPageDict)
    assert_type(doc.get_page_text(0, "rawdict"), pymupdf.TextPageRawDict)
    assert_type(doc.get_page_text(0, "words"), list[pymupdf.TextWord])
    assert_type(doc.get_page_text(0, "blocks"), list[pymupdf.TextBlock])
    assert_type(textpage.extractDICT(), pymupdf.TextPageDict)
    assert_type(textpage.extractRAWDICT(), pymupdf.TextPageRawDict)
    assert_type(textpage.extractTextbox(pymupdf.Rect(0, 0, 10, 10)), str)
    assert_type(
        textpage.extractSelection(pymupdf.Point(0, 0), pymupdf.Point(1, 1)), str
    )
    assert_type(textpage.poolsize(), int)

    # 1.27 additions
    doc.repair()
    doc.save("out.pdf", raise_on_repair=True)
    assert_type(doc.write(raise_on_repair=True), bytes)

    annot = page.add_redact_annot(pymupdf.Rect(0, 0, 10, 10))
    assert_type(bool(annot), bool)

    assert_type(pymupdf.TEXT_FUZZY_VECTORS, int)

    # Document methods (moved from utils.py)
    assert_type(doc.get_toc(), list)
    assert_type(doc.has_annots(), bool)
    assert_type(doc.has_links(), bool)
    assert_type(doc.get_page_labels(), list)
    assert_type(doc.get_page_numbers("1"), list[int])
    doc.set_metadata({"title": "test"})
    doc.set_page_labels([])
    assert_type(doc.set_toc([]), int)
    assert_type(doc.subset_fonts(), int | None)
    for p in doc.pages():
        assert_type(p, pymupdf.Page)
