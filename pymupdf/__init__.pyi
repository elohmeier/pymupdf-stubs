import collections.abc
import types
from collections.abc import Iterator, Sequence
from io import BufferedReader, BytesIO
from pathlib import Path
from typing import Any, Literal, TypedDict, overload

from .table import TableFinder

PDF_ENCRYPT_NONE = 1
PDF_REDACT_IMAGE_NONE = 0
PDF_REDACT_IMAGE_PIXELS = 2
PDF_REDACT_LINE_ART_IF_TOUCHED = 2
PDF_REDACT_LINE_ART_NONE = 0
PDF_REDACT_TEXT_REMOVE = 0
TEXT_FUZZY_VECTORS: int

class Colorspace:
    @property
    def n(self) -> int: ...

csRGB: Colorspace

class Quad: ...

class Pixmap:
    @overload
    def __init__(
        self,
        colorspace: Colorspace,
        irect: IRect | Rect | tuple[int | float, int | float, int | float, int | float],
        alpha: bool = False,
    ) -> None: ...
    @overload
    def __init__(self, colorspace: Colorspace | None, source: Pixmap) -> None: ...
    @overload
    def __init__(self, source: Pixmap, mask: Pixmap) -> None: ...
    @overload
    def __init__(
        self,
        source: Pixmap,
        width: int | float,
        height: int | float,
        clip: IRect
        | Rect
        | tuple[int | float, int | float, int | float, int | float]
        | None = None,
    ) -> None: ...
    @overload
    def __init__(self, source: Pixmap, alpha: int | bool = 1) -> None: ...
    @overload
    def __init__(self, filename: str | Path) -> None: ...
    @overload
    def __init__(self, stream: bytes | bytearray | BytesIO) -> None: ...
    @overload
    def __init__(
        self,
        colorspace: Colorspace,
        width: int,
        height: int,
        samples: bytes | bytearray | BytesIO,
        alpha: int | bool,
    ) -> None: ...
    @overload
    def __init__(self, doc: Document, xref: int) -> None: ...
    @property
    def width(self) -> int: ...
    @property
    def w(self) -> int: ...
    @property
    def height(self) -> int: ...
    @property
    def h(self) -> int: ...
    @property
    def irect(self) -> Rect: ...
    @property
    def colorspace(self) -> Colorspace | None: ...
    @property
    def n(self) -> int: ...
    @property
    def alpha(self) -> bool: ...
    @property
    def is_monochrome(self) -> bool: ...
    @property
    def is_unicolor(self) -> bool: ...
    @property
    def samples(self) -> bytes: ...
    @property
    def samples_mv(self) -> memoryview: ...
    @property
    def samples_ptr(self) -> int: ...
    def set_dpi(self, xres: int, yres: int) -> None: ...
    def tobytes(self, output: str = "png", jpg_quality: int = 95) -> bytes: ...
    def pil_tobytes(self, *args, unmultiply: bool = False, **kwargs) -> bytes: ...
    def pil_image(self) -> Any: ...
    def pil_save(self, *args, unmultiply: bool = False, **kwargs) -> None: ...

class Point:
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, x: float, y: float) -> None: ...
    @overload
    def __init__(self, point: Point) -> None: ...
    @overload
    def __init__(self, sequence: tuple[float, float] | list[float]) -> None: ...
    def distance_to(self, x: Point | Rect, unit: str = "px") -> float: ...
    def norm(self) -> float: ...
    def transform(self, m: Matrix) -> Point: ...
    @property
    def unit(self) -> Point: ...
    @property
    def abs_unit(self) -> Point: ...
    @property
    def x(self) -> float: ...
    @property
    def y(self) -> float: ...
    def __iter__(self) -> Iterator[float]: ...

class Matrix:
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, zoom_x: float, zoom_y: float) -> None: ...
    @overload
    def __init__(self, shear_x: float, shear_y: float, _: int) -> None: ...
    @overload
    def __init__(
        self, a: float, b: float, c: float, d: float, e: float, f: float
    ) -> None: ...
    @overload
    def __init__(self, matrix: Matrix | IdentityMatrix) -> None: ...
    @overload
    def __init__(self, degree: float) -> None: ...
    @overload
    def __init__(self, sequence: Sequence[float]) -> None: ...
    def norm(self) -> float: ...
    def prerotate(self, deg: float) -> None: ...
    def prescale(self, sx: float, sy: float) -> None: ...
    def preshear(self, sx: float, sy: float) -> None: ...
    def pretranslate(self, tx: float, ty: float) -> None: ...
    def concat(self, m1: Matrix, m2: Matrix) -> None: ...
    def invert(self, m: Matrix | None = None) -> int: ...
    @property
    def a(self) -> float: ...
    @property
    def b(self) -> float: ...
    @property
    def c(self) -> float: ...
    @property
    def d(self) -> float: ...
    @property
    def e(self) -> float: ...
    @property
    def f(self) -> float: ...
    @property
    def is_rectilinear(self) -> bool: ...
    def __iter__(self) -> Iterator[float]: ...

class IdentityMatrix(Matrix): ...

Identity: IdentityMatrix

class Rect:
    @property
    def irect(self) -> Rect: ...
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(
        self, x0: int | float, y0: int | float, x1: int | float, y1: int | float
    ) -> None: ...
    @overload
    def __init__(
        self,
        rect: Rect
        | IRect
        | tuple[int | float, int | float, int | float, int | float]
        | Sequence[int | float],
    ) -> None: ...
    @overload
    def __init__(self, p1: Point, p2: Point) -> None: ...
    def get_area(self) -> float: ...
    def intersect(
        self, other: IRect | Rect | tuple[float, float, float, float] | list[float]
    ) -> Rect: ...
    def intersects(self, other: Rect | tuple[float, float, float, float]) -> bool: ...
    def include_rect(
        self, rect: Rect | tuple[float, float, float, float] | list[float]
    ) -> Rect: ...
    def contains(self, x: IRect | Rect | Point | float) -> bool: ...
    def __iter__(self) -> Iterator[float]: ...
    def __truediv__(self, other: float | Matrix) -> Rect: ...
    def __mul__(self, other: float | Matrix) -> Rect: ...
    def __or__(self, other: Rect) -> Rect: ...
    def __add__(self, other: IRect | Rect) -> Rect: ...
    def __sub__(self, other: IRect | Rect) -> Rect: ...
    def __getitem__(self, index: int) -> float: ...
    def __and__(self, other: IRect | Rect) -> Rect: ...
    def transform(self, m: Matrix) -> Rect: ...
    @property
    def x0(self) -> float: ...
    @property
    def y0(self) -> float: ...
    @property
    def x1(self) -> float: ...
    @property
    def y1(self) -> float: ...
    @property
    def top_left(self) -> Point: ...
    @property
    def tl(self) -> Point: ...
    @property
    def top_right(self) -> Point: ...
    @property
    def tr(self) -> Point: ...
    @property
    def bottom_left(self) -> Point: ...
    @property
    def bl(self) -> Point: ...
    @property
    def bottom_right(self) -> Point: ...
    @property
    def br(self) -> Point: ...
    @property
    def width(self) -> float: ...
    @property
    def height(self) -> float: ...
    @property
    def is_empty(self) -> bool: ...
    def is_valid(self) -> bool: ...
    def round(self) -> IRect: ...

class IRect:
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(
        self, x0: int | float, y0: int | float, x1: int | float, y1: int | float
    ) -> None: ...
    @overload
    def __init__(
        self,
        irect: IRect
        | tuple[int | float, int | float, int | float, int | float]
        | Sequence[int | float],
    ) -> None: ...
    @overload
    def __init__(self, p1: Point, p2: Point) -> None: ...
    def get_area(self, unit: str = "px") -> float: ...
    def intersect(self, ir: IRect) -> None: ...
    def contains(self, x: IRect | Rect | Point | int) -> bool: ...
    def intersects(self, r: IRect | Rect) -> bool: ...
    def torect(self, rect: IRect | Rect) -> Matrix: ...
    def morph(self, fixpoint: Point, matrix: Matrix) -> Quad: ...
    def norm(self) -> float: ...
    def normalize(self) -> None: ...
    def __add__(self, other: IRect) -> IRect: ...
    def __ior__(self, other: IRect) -> IRect: ...
    @property
    def top_left(self) -> Point: ...
    @property
    def tl(self) -> Point: ...
    @property
    def top_right(self) -> Point: ...
    @property
    def tr(self) -> Point: ...
    @property
    def bottom_left(self) -> Point: ...
    @property
    def bl(self) -> Point: ...
    @property
    def bottom_right(self) -> Point: ...
    @property
    def br(self) -> Point: ...
    @property
    def rect(self) -> Rect: ...
    @property
    def quad(self) -> Quad: ...
    @property
    def width(self) -> int: ...
    @property
    def height(self) -> int: ...
    @property
    def x0(self) -> int: ...
    @property
    def y0(self) -> int: ...
    @property
    def x1(self) -> int: ...
    @property
    def y1(self) -> int: ...
    @property
    def is_infinite(self) -> bool: ...
    @property
    def is_empty(self) -> bool: ...
    def __iter__(self) -> Iterator[int]: ...
    def is_valid(self) -> bool: ...

RectLike = (
    Rect
    | IRect
    | tuple[int | float, int | float, int | float, int | float]
    | Sequence[int | float]
)
PointLike = Point | tuple[int | float, int | float] | Sequence[int | float]
MatrixTuple = tuple[float, float, float, float, float, float]
TextBlock = tuple[float, float, float, float, str, int, int]
TextWord = tuple[float, float, float, float, str, int, int, int]

ExtractImageDict = TypedDict(
    "ExtractImageDict",
    {
        "ext": str,
        "smask": int,
        "width": int,
        "height": int,
        "colorspace": int,
        "cs-name": str,
        "xres": int,
        "yres": int,
        "image": bytes,
    },
)

class TextCharDict(TypedDict):
    origin: tuple[float, float]
    bbox: tuple[float, float, float, float]
    c: str
    synthetic: bool

class TextSpanDict(TypedDict):
    size: float
    flags: int
    bidi: int
    char_flags: int
    font: str
    color: int
    alpha: int
    ascender: float
    descender: float
    text: str
    origin: tuple[float, float]
    bbox: tuple[float, float, float, float]

class TextSpanRawDict(TypedDict):
    size: float
    flags: int
    bidi: int
    char_flags: int
    font: str
    color: int
    alpha: int
    ascender: float
    descender: float
    chars: list[TextCharDict]
    origin: tuple[float, float]
    bbox: tuple[float, float, float, float]

class TextLineDict(TypedDict):
    spans: list[TextSpanDict]
    wmode: int
    dir: tuple[float, float]
    bbox: tuple[float, float, float, float]

class TextLineRawDict(TypedDict):
    spans: list[TextSpanRawDict]
    wmode: int
    dir: tuple[float, float]
    bbox: tuple[float, float, float, float]

class TextBlockDict(TypedDict):
    number: int
    type: int
    bbox: tuple[float, float, float, float]
    lines: list[TextLineDict]

class TextImageBlockDict(TypedDict):
    number: int
    type: int
    bbox: tuple[float, float, float, float]
    width: int
    height: int
    ext: str
    colorspace: int
    xres: int
    yres: int
    bpc: int
    size: int
    image: bytes
    mask: bytes | None
    transform: MatrixTuple

class TextBlockRawDict(TypedDict):
    number: int
    type: int
    bbox: tuple[float, float, float, float]
    lines: list[TextLineRawDict]

class TextImageBlockRawDict(TypedDict):
    number: int
    type: int
    bbox: tuple[float, float, float, float]
    width: int
    height: int
    ext: str
    colorspace: int
    xres: int
    yres: int
    bpc: int
    size: int
    image: bytes
    mask: bytes | None
    transform: MatrixTuple

class TextPageDict(TypedDict):
    width: float
    height: float
    blocks: list[TextBlockDict | TextImageBlockDict]

class TextPageRawDict(TypedDict):
    width: float
    height: float
    blocks: list[TextBlockRawDict | TextImageBlockRawDict]

DrawingLineItem = tuple[Literal["l"], Point, Point]
DrawingCurveItem = tuple[Literal["c"], Point, Point, Point, Point]
DrawingRectItem = tuple[Literal["re"], Rect, int]
DrawingQuadItem = tuple[Literal["qu"], Quad]
DrawingItem = DrawingLineItem | DrawingCurveItem | DrawingRectItem | DrawingQuadItem

class DrawingPathDict(TypedDict, total=False):
    type: Literal["f", "s", "fs"]
    closePath: bool | None
    color: tuple[float, ...] | None
    dashes: str | None
    even_odd: bool | None
    fill: tuple[float, ...] | None
    items: list[DrawingItem]
    lineCap: tuple[int, int, int] | None
    lineJoin: int | None
    fill_opacity: float | None
    stroke_opacity: float | None
    rect: Rect
    layer: str | None
    level: int
    seqno: int
    width: float | None

class DrawingClipDict(TypedDict, total=False):
    type: Literal["clip"]
    closePath: bool | None
    even_odd: bool | None
    items: list[DrawingItem]
    rect: Rect
    layer: str | None
    level: int
    seqno: int
    scissor: Rect

class DrawingGroupDict(TypedDict, total=False):
    type: Literal["group"]
    rect: Rect
    layer: str | None
    level: int
    seqno: int
    isolated: bool
    knockout: bool
    blendmode: str
    opacity: float

DrawingDict = DrawingPathDict | DrawingClipDict | DrawingGroupDict

# https://pymupdf.readthedocs.io/en/latest/how-to-open-a-file.html#how-to-open-a-file
def open(
    filename: str | Path | BufferedReader | None = None,
    stream: bytes | BytesIO | None = None,
    *,
    filetype: str | None = None,
    rect: Rect | None = None,
    width: float = 0,
    height: float = 0,
    fontsize: float = 11,
) -> Document: ...
def paper_size(s: str) -> tuple[int, int]: ...
def paper_rect(s: str) -> Rect: ...

class Document:
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(
        self,
        filename: str | Path | BufferedReader | None = None,
        stream: bytes | BytesIO | None = None,
        *,
        filetype: str | None = None,
        rect: Rect | None = None,
        width: float = 0,
        height: float = 0,
        fontsize: float = 11,
    ) -> None: ...
    def authenticate(self, password: str) -> int: ...
    def insert_pdf(
        self,
        docsrc: Document,
        from_page: int = -1,
        to_page: int = -1,
        start_at: int = -1,
        rotate: int = -1,
        links: bool = True,
        annots: bool = True,
        show_progress: int = 0,
        final: int = 1,
    ) -> None: ...
    @property
    def page_count(self) -> int: ...
    def __len__(self) -> int: ...
    def tobytes(
        self,
        garbage: int = 0,
        clean: bool = False,
        deflate: bool = False,
        deflate_images: bool = False,
        deflate_fonts: bool = False,
        ascii: bool = False,
        expand: int = 0,
        linear: bool = False,
        pretty: bool = False,
        no_new_id: bool = False,
        encryption: int = PDF_ENCRYPT_NONE,
        permissions: int = -1,
        owner_pw: str | None = None,
        user_pw: str | None = None,
        use_objstms: int = 0,
    ) -> bytes: ...
    def save(
        self,
        outfile: str | Path | object,
        garbage: int = 0,
        clean: bool = False,
        deflate: bool = False,
        deflate_images: bool = False,
        deflate_fonts: bool = False,
        incremental: bool = False,
        ascii: bool = False,
        expand: int = 0,
        linear: bool = False,
        pretty: bool = False,
        no_new_id: bool = False,
        encryption: int = PDF_ENCRYPT_NONE,
        permissions: int = -1,
        owner_pw: str | None = None,
        user_pw: str | None = None,
        use_objstms: int = 0,
        raise_on_repair: bool = False,
    ) -> None: ...
    def repair(self) -> None: ...
    def close(self) -> None: ...
    @overload
    def __getitem__(self, index: int) -> Page: ...
    @overload
    def __getitem__(self, index: slice) -> list[Page]: ...
    @overload
    def __getitem__(self, index: tuple[int, int]) -> Page: ...
    def convert_to_pdf(self, from_page=-1, to_page=-1, rotate=0) -> bytes: ...
    def new_page(
        self, pno: int = -1, width: float = 595, height: float = 842
    ) -> Page: ...
    def __enter__(self) -> Document: ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: types.TracebackType | None,
    ) -> None: ...
    def extract_image(self, xref: int) -> ExtractImageDict: ...
    def load_page(self, page_id: int | tuple[int, int] | None = 0) -> Page: ...
    def reload_page(self, page: Page) -> Page: ...
    def select(self, pyliste: Sequence[int]) -> None: ...
    @property
    def needs_pass(self) -> bool: ...
    @property
    def is_encrypted(self) -> bool: ...
    @property
    def name(self) -> bool: ...
    def write(
        self,
        garbage=False,
        clean=False,
        deflate=False,
        deflate_images=False,
        deflate_fonts=False,
        incremental=False,
        ascii=False,
        expand=False,
        linear=False,
        no_new_id=False,
        appearance=False,
        pretty=False,
        encryption=1,
        permissions=4095,
        owner_pw=None,
        user_pw=None,
        preserve_metadata=1,
        use_objstms=0,
        compression_effort=0,
        raise_on_repair=False,
    ) -> bytes: ...
    def xref_object(self, xref: int, compressed: int = 0, ascii: int = 0) -> str: ...
    def scrub(
        self,
        attached_files: bool = True,
        clean_pages: bool = True,
        embedded_files: bool = True,
        hidden_text: bool = True,
        javascript: bool = True,
        metadata: bool = True,
        redactions: bool = True,
        redact_images: int = 0,
        remove_links: bool = True,
        reset_fields: bool = True,
        reset_responses: bool = True,
        thumbnails: bool = True,
        xml_metadata: bool = True,
    ) -> None: ...
    def get_char_widths(
        self, xref: int, limit: int = 256, idx: int = 0, fontdict: dict | None = None
    ) -> list: ...
    def get_oc(self, xref: int) -> int: ...
    def get_ocmd(self, xref: int) -> dict: ...
    def get_page_labels(self) -> list: ...
    def get_page_numbers(self, label: str, only_one: bool = False) -> list[int]: ...
    def get_page_pixmap(
        self,
        pno: int,
        *,
        matrix: Matrix | None = None,
        dpi: int | None = None,
        colorspace: Colorspace | None = None,
        clip: Rect | IRect | tuple[float, float, float, float] | None = None,
        alpha: bool = False,
        annots: bool = True,
    ) -> Pixmap: ...
    @overload
    def get_page_text(
        self,
        pno: int,
        option: Literal["text"] = "text",
        clip: RectLike | None = None,
        flags: int | None = None,
        textpage: TextPage | None = None,
        sort: bool = False,
        delimiters: str | None = None,
    ) -> str: ...
    @overload
    def get_page_text(
        self,
        pno: int,
        option: Literal["html", "xml", "xhtml", "json", "rawjson"],
        clip: RectLike | None = None,
        flags: int | None = None,
        textpage: TextPage | None = None,
        sort: bool = False,
        delimiters: str | None = None,
    ) -> str: ...
    @overload
    def get_page_text(
        self,
        pno: int,
        option: Literal["dict"],
        clip: RectLike | None = None,
        flags: int | None = None,
        textpage: TextPage | None = None,
        sort: bool = False,
        delimiters: str | None = None,
    ) -> TextPageDict: ...
    @overload
    def get_page_text(
        self,
        pno: int,
        option: Literal["rawdict"],
        clip: RectLike | None = None,
        flags: int | None = None,
        textpage: TextPage | None = None,
        sort: bool = False,
        delimiters: str | None = None,
    ) -> TextPageRawDict: ...
    @overload
    def get_page_text(
        self,
        pno: int,
        option: Literal["words"],
        clip: RectLike | None = None,
        flags: int | None = None,
        textpage: TextPage | None = None,
        sort: bool = False,
        delimiters: str | None = None,
    ) -> list[TextWord]: ...
    @overload
    def get_page_text(
        self,
        pno: int,
        option: Literal["blocks"],
        clip: RectLike | None = None,
        flags: int | None = None,
        textpage: TextPage | None = None,
        sort: bool = False,
        delimiters: str | None = None,
    ) -> list[TextBlock]: ...
    @overload
    def get_page_text(
        self,
        pno: int,
        option: str = "text",
        clip: RectLike | None = None,
        flags: int | None = None,
        textpage: TextPage | None = None,
        sort: bool = False,
        delimiters: str | None = None,
    ) -> str | TextPageDict | TextPageRawDict | list[TextWord] | list[TextBlock]: ...
    def get_toc(self, simple: bool = True) -> list: ...
    def has_annots(self) -> bool: ...
    def has_links(self) -> bool: ...
    def insert_page(
        self,
        pno: int,
        text: str | list | None = None,
        fontsize: float = 11,
        width: float = 595,
        height: float = 842,
        fontname: str = "helv",
        fontfile: str | None = None,
        color: tuple[float, ...] | None = (0,),
    ) -> int: ...
    def pages(
        self,
        start: int | None = None,
        stop: int | None = None,
        step: int | None = None,
    ) -> collections.abc.Iterable[Page]: ...
    def search_page_for(
        self,
        pno: int,
        text: str,
        quads: bool = False,
        clip: Rect | IRect | tuple[float, float, float, float] | None = None,
        flags: int | None = None,
        textpage: TextPage | None = None,
    ) -> list: ...
    def set_metadata(self, m: dict | None = None) -> None: ...
    def set_oc(self, xref: int, oc: int) -> None: ...
    def set_ocmd(
        self,
        xref: int = 0,
        ocgs: list | None = None,
        policy: str | None = None,
        ve: list | None = None,
    ) -> int: ...
    def set_page_labels(self, labels: list) -> None: ...
    def set_toc(self, toc: list, collapse: int = 1) -> int: ...
    def set_toc_item(
        self,
        idx: int,
        dest_dict: dict | None = None,
        kind: int | None = None,
        pno: int | None = None,
        uri: str | None = None,
        title: str | None = None,
        to: Point | tuple[float, float] | None = None,
        filename: str | None = None,
        zoom: float = 0,
    ) -> None: ...
    def subset_fonts(
        self, verbose: bool = False, fallback: bool = False
    ) -> int | None: ...

class Annot:
    def __bool__(self) -> bool: ...

class TextPage:
    def extractText(self, sort: bool = False) -> str: ...
    def extractTEXT(self, sort: bool = False) -> str: ...
    def extractBLOCKS(
        self,
    ) -> list[TextBlock]: ...
    def extractWORDS(self, delimiters: str | None = None) -> list[TextWord]: ...
    def extractHTML(self) -> str: ...
    def extractDICT(
        self, cb: Rect | None = None, sort: bool = False
    ) -> TextPageDict: ...
    def extractJSON(self, cb: Rect | None = None, sort: bool = False) -> str: ...
    def extractXHTML(self) -> str: ...
    def extractXML(self) -> str: ...
    def extractRAWDICT(
        self, cb: Rect | None = None, sort: bool = False
    ) -> TextPageRawDict: ...
    def extractRAWJSON(self, cb: Rect | None = None, sort: bool = False) -> str: ...
    def extractTextbox(self, rect: RectLike) -> str: ...
    def extractSelection(self, pointa: PointLike, pointb: PointLike) -> str: ...
    def extractIMGINFO(self, hashes: int = 0) -> list[dict[str, Any]]: ...
    def poolsize(self) -> int: ...
    @overload
    def search(self, needle: str, quads: Literal[False] = False) -> list[Rect]: ...
    @overload
    def search(self, needle: str, quads: Literal[True]) -> list[Quad]: ...
    def search(self, needle: str, quads: bool = False) -> list[Rect | Quad]: ...
    @property
    def rect(self) -> Rect: ...

class Page:
    def get_pixmap(
        self,
        *,
        matrix: Matrix = Identity,
        dpi=None,
        colorspace=csRGB,
        clip=None,
        alpha=False,
        annots=True,
    ) -> Pixmap: ...
    def set_rotation(self, rotation: int) -> None: ...
    def get_textpage(
        self,
        clip: RectLike | None = None,
        flags: int = 0,
        matrix: Matrix | None = None,
    ) -> TextPage: ...
    @overload
    def get_text(
        self,
        option: Literal["text"] = "text",
        *,
        clip: RectLike | None = None,
        flags: int | None = None,
        textpage: TextPage | None = None,
        sort: bool = False,
        delimiters: str | None = None,
    ) -> str: ...
    @overload
    def get_text(
        self,
        option: Literal["html", "xml", "xhtml", "json", "rawjson"],
        *,
        clip: RectLike | None = None,
        flags: int | None = None,
        textpage: TextPage | None = None,
        sort: bool = False,
        delimiters: str | None = None,
    ) -> str: ...
    @overload
    def get_text(
        self,
        option: Literal["dict"],
        *,
        clip: RectLike | None = None,
        flags: int | None = None,
        textpage: TextPage | None = None,
        sort: bool = False,
        delimiters: str | None = None,
    ) -> TextPageDict: ...
    @overload
    def get_text(
        self,
        option: Literal["rawdict"],
        *,
        clip: RectLike | None = None,
        flags: int | None = None,
        textpage: TextPage | None = None,
        sort: bool = False,
        delimiters: str | None = None,
    ) -> TextPageRawDict: ...
    @overload
    def get_text(
        self,
        option: Literal["words"],
        *,
        clip: RectLike | None = None,
        flags: int | None = None,
        textpage: TextPage | None = None,
        sort: bool = False,
        delimiters: str | None = None,
    ) -> list[TextWord]: ...
    @overload
    def get_text(
        self,
        option: Literal["blocks"],
        *,
        clip: RectLike | None = None,
        flags: int | None = None,
        textpage: TextPage | None = None,
        sort: bool = False,
        delimiters: str | None = None,
    ) -> list[TextBlock]: ...
    @overload
    def get_text(
        self,
        option: str,
        *,
        clip: RectLike | None = None,
        flags: int | None = None,
        textpage: TextPage | None = None,
        sort: bool = False,
        delimiters: str | None = None,
    ) -> str | TextPageDict | TextPageRawDict | list[TextWord] | list[TextBlock]: ...
    def find_tables(
        self,
        clip: Rect
        | IRect
        | tuple[float | int, float | int, float | int, float | int]
        | list[float | int]
        | None = None,
        strategy: str | None = None,
        vertical_strategy: str = "lines",
        horizontal_strategy: str = "lines",
        vertical_lines: list[float] | None = None,
        horizontal_lines: list[float] | None = None,
        snap_tolerance: float = 3,
        snap_x_tolerance: float | None = None,
        snap_y_tolerance: float | None = None,
        join_tolerance: float = 3,
        join_x_tolerance: float | None = None,
        join_y_tolerance: float | None = None,
        edge_min_length: float = 3,
        min_words_vertical: float = 3,
        min_words_horizontal: float = 1,
        intersection_tolerance: float = 3,
        intersection_x_tolerance: float | None = None,
        intersection_y_tolerance: float | None = None,
        text_tolerance: float = 3,
        text_x_tolerance: float = 3,
        text_y_tolerance: float = 3,
        add_lines: Sequence[tuple[Point, Point]] | None = None,
    ) -> TableFinder: ...
    @overload
    def get_images(
        self, full: Literal[False] = False
    ) -> list[tuple[int, int, int, int, int, str, str, str, str]]: ...
    @overload
    def get_images(
        self, full: Literal[True]
    ) -> list[tuple[int, int, int, int, int, str, str, str, str, int]]: ...
    @overload
    def get_image_bbox(
        self,
        item: tuple[int, int, int, int, int, str, str, str, str, int],
        transform: Literal[False] = False,
    ) -> Rect: ...
    @overload
    def get_image_bbox(
        self,
        item: tuple[int, int, int, int, int, str, str, str, str, int],
        transform: Literal[True],
    ) -> tuple[Rect, Matrix]: ...
    def replace_image(
        self,
        xref: int,
        filename: str | None = None,
        pixmap: Pixmap | None = None,
        stream: bytes | None = None,
    ) -> None: ...
    def add_redact_annot(
        self,
        quad: Quad | Rect,
        text: str | None = None,
        fontname: str | None = None,
        fontsize: float = 11,
        align: Literal[0, 1, 2] = 0,  # 0: left, 1: center, 2: right
        fill: tuple[float, float, float] | None | Literal[False] = (1, 1, 1),
        text_color: tuple[float, float, float] = (0, 0, 0),
        cross_out: bool = True,
    ) -> Annot: ...
    def clean_contents(self, sanitize: bool = True) -> None: ...
    def get_texttrace(self) -> list[dict[str, Any]]: ...
    @overload
    def get_drawings(
        self, extended: Literal[False] = False
    ) -> list[DrawingPathDict]: ...
    @overload
    def get_drawings(self, extended: Literal[True]) -> list[DrawingDict]: ...
    def get_drawings(self, extended: bool = False) -> list[DrawingDict]: ...
    def insert_image(
        self,
        rect: Rect,
        *,
        alpha: int = -1,
        filename: str | None = None,
        height: int = 0,
        keep_proportion: bool = True,
        mask: bytes | bytearray | Any = None,  # io.BytesIO
        oc: int = 0,
        overlay: bool = True,
        pixmap: Pixmap | None = None,
        rotate: int = 0,
        stream: bytes | bytearray | Any = None,  # io.BytesIO
        width: int = 0,
        xref: int = 0,
    ) -> int: ...
    def apply_redactions(
        self,
        images: int = PDF_REDACT_IMAGE_PIXELS,
        graphics: int = PDF_REDACT_LINE_ART_IF_TOUCHED,
        text: int = PDF_REDACT_TEXT_REMOVE,
    ) -> bool: ...
    def draw_line(
        self,
        p1: Point,
        p2: Point,
        color: tuple[float, ...] = (0,),
        width: float = 1,
        dashes: str | None = None,
        lineCap: int = 0,
        lineJoin: int = 0,
        overlay: bool = True,
        morph: tuple[Point, Matrix] | None = None,
        stroke_opacity: float = 1,
        fill_opacity: float = 1,
        oc: int = 0,
    ) -> None: ...
    def draw_zigzag(
        self,
        p1: Point,
        p2: Point,
        breadth: float = 2,
        color: tuple[float, ...] = (0,),
        width: float = 1,
        dashes: str | None = None,
        lineCap: int = 0,
        lineJoin: int = 0,
        overlay: bool = True,
        morph: tuple[Point, Matrix] | None = None,
        stroke_opacity: float = 1,
        fill_opacity: float = 1,
        oc: int = 0,
    ) -> None: ...
    def draw_squiggle(
        self,
        p1: Point,
        p2: Point,
        breadth: float = 2,
        color: tuple[float, ...] = (0,),
        width: float = 1,
        dashes: str | None = None,
        lineCap: int = 0,
        lineJoin: int = 0,
        overlay: bool = True,
        morph: tuple[Point, Matrix] | None = None,
        stroke_opacity: float = 1,
        fill_opacity: float = 1,
        oc: int = 0,
    ) -> None: ...
    def draw_circle(
        self,
        center: Point,
        radius: float,
        color: tuple[float, ...] = (0,),
        fill: tuple[float, ...] | None = None,
        width: float = 1,
        dashes: str | None = None,
        lineCap: int = 0,
        lineJoin: int = 0,
        overlay: bool = True,
        morph: tuple[Point, Matrix] | None = None,
        stroke_opacity: float = 1,
        fill_opacity: float = 1,
        oc: int = 0,
    ) -> None: ...
    def draw_oval(
        self,
        quad: Rect | Quad,
        color: tuple[float, ...] = (0,),
        fill: tuple[float, ...] | None = None,
        width: float = 1,
        dashes: str | None = None,
        lineCap: int = 0,
        lineJoin: int = 0,
        overlay: bool = True,
        morph: tuple[Point, Matrix] | None = None,
        stroke_opacity: float = 1,
        fill_opacity: float = 1,
        oc: int = 0,
    ) -> None: ...
    def draw_sector(
        self,
        center: Point,
        point: Point,
        angle: float,
        color: tuple[float, ...] = (0,),
        fill: tuple[float, ...] | None = None,
        width: float = 1,
        dashes: str | None = None,
        lineCap: int = 0,
        lineJoin: int = 0,
        fullSector: bool = True,
        overlay: bool = True,
        closePath: bool = False,
        morph: tuple[Point, Matrix] | None = None,
        stroke_opacity: float = 1,
        fill_opacity: float = 1,
        oc: int = 0,
    ) -> None: ...
    def draw_polyline(
        self,
        points: list[Point],
        color: tuple[float, ...] = (0,),
        fill: tuple[float, ...] | None = None,
        width: float = 1,
        dashes: str | None = None,
        lineCap: int = 0,
        lineJoin: int = 0,
        overlay: bool = True,
        closePath: bool = False,
        morph: tuple[Point, Matrix] | None = None,
        stroke_opacity: float = 1,
        fill_opacity: float = 1,
        oc: int = 0,
    ) -> None: ...
    def draw_bezier(
        self,
        p1: Point,
        p2: Point,
        p3: Point,
        p4: Point,
        color: tuple[float, ...] = (0,),
        fill: tuple[float, ...] | None = None,
        width: float = 1,
        dashes: str | None = None,
        lineCap: int = 0,
        lineJoin: int = 0,
        overlay: bool = True,
        closePath: bool = False,
        morph: tuple[Point, Matrix] | None = None,
        stroke_opacity: float = 1,
        fill_opacity: float = 1,
        oc: int = 0,
    ) -> None: ...
    def draw_curve(
        self,
        p1: Point,
        p2: Point,
        p3: Point,
        color: tuple[float, ...] = (0,),
        fill: tuple[float, ...] | None = None,
        width: float = 1,
        dashes: str | None = None,
        lineCap: int = 0,
        lineJoin: int = 0,
        overlay: bool = True,
        closePath: bool = False,
        morph: tuple[Point, Matrix] | None = None,
        stroke_opacity: float = 1,
        fill_opacity: float = 1,
        oc: int = 0,
    ) -> None: ...
    def draw_rect(
        self,
        rect: Rect,
        color: tuple[float, ...] = (0,),
        fill: tuple[float, ...] | None = None,
        width: float = 1,
        dashes: str | None = None,
        lineCap: int = 0,
        lineJoin: int = 0,
        overlay: bool = True,
        morph: tuple[Point, Matrix] | None = None,
        stroke_opacity: float = 1,
        fill_opacity: float = 1,
        radius: float | tuple[float, float] | None = None,
        oc: int = 0,
    ) -> None: ...
    def draw_quad(
        self,
        quad: Quad,
        color: tuple[float, ...] = (0,),
        fill: tuple[float, ...] | None = None,
        width: float = 1,
        dashes: str | None = None,
        lineCap: int = 0,
        lineJoin: int = 0,
        overlay: bool = True,
        morph: tuple[Point, Matrix] | None = None,
        stroke_opacity: float = 1,
        fill_opacity: float = 1,
        oc: int = 0,
    ) -> None: ...
    def insert_text(
        self,
        point: Point | tuple[float, float] | list[float],
        text: str,
        *,
        fontsize: float = 11,
        fontname: str = "helv",
        fontfile: str | None = None,
        idx: int = 0,
        color: tuple[float, ...] | None = None,
        fill: tuple[float, ...] | None = None,
        render_mode: int = 0,
        miter_limit: float = 1,
        border_width: float = 0.05,
        encoding: int = 0,
        rotate: int = 0,
        morph: tuple[Point, Matrix] | None = None,
        stroke_opacity: float = 1,
        fill_opacity: float = 1,
        overlay: bool = True,
        oc: int = 0,
    ) -> int: ...
    def insert_textbox(
        self,
        rect: Rect,
        buffer: str,
        *,
        fontsize: float = 11,
        fontname: str = "helv",
        fontfile: str | None = None,
        idx: int = 0,
        color: tuple[float, ...] | None = None,
        fill: tuple[float, ...] | None = None,
        render_mode: int = 0,
        miter_limit: float = 1,
        border_width: float = 1,
        encoding: int = 0,
        expandtabs: int = 8,
        align: int = 0,
        charwidths: Any = None,
        rotate: int = 0,
        morph: tuple[Point, Matrix] | None = None,
        stroke_opacity: float = 1,
        fill_opacity: float = 1,
        oc: int = 0,
        overlay: bool = True,
    ) -> float: ...
    def show_pdf_page(
        self,
        rect: Rect | IRect | tuple[float, float, float, float] | list[float],
        docsrc: Document,
        pno: int = 0,
        keep_proportion: bool = True,
        overlay: bool = True,
        oc: int = 0,
        rotate: int = 0,
        clip: Rect
        | IRect
        | tuple[float, float, float, float]
        | list[float]
        | None = None,
    ) -> int: ...
    @property
    def rect(self) -> Rect: ...
    @property
    def mediabox(self) -> Rect: ...
    @property
    def mediabox_size(self) -> Point: ...
    @property
    def cropbox(self) -> Rect: ...
    @property
    def cropbox_position(self) -> Point: ...
    @property
    def bleedbox(self) -> Rect: ...
    @property
    def trimbox(self) -> Rect: ...
    def bound(self) -> Rect: ...
    @property
    def rotation_matrix(self) -> Matrix: ...
    @property
    def derotation_matrix(self) -> Matrix: ...
    @property
    def rotation(self) -> int: ...
    @property
    def number(self) -> int: ...
    @property
    def xref(self) -> int: ...
    @property
    def parent(self) -> Document: ...
