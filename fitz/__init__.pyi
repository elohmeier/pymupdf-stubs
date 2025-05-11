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

class Colorspace:
    @property
    def n(self) -> int: ...

csRGB: Colorspace

class Quad: ...

class Pixmap:
    def __init__(self, filename: str) -> None: ...
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
    def samples(self) -> bytes: ...
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

class TextBlockRawDict(TypedDict):
    number: int
    type: int
    bbox: tuple[float, float, float, float]
    lines: list[TextLineRawDict]

class TextPageDict(TypedDict):
    width: float
    height: float
    blocks: list[TextBlockDict]

class TextPageRawDict(TypedDict):
    width: float
    height: float
    blocks: list[TextBlockRawDict]

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
    ) -> None: ...
    def close(self) -> None: ...
    def __getitem__(self, index: int) -> Page: ...
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
    def reload_page(self, page: Page) -> Page: ...
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
    ) -> bytes: ...

class Annot: ...

class TextPage:
    def extractText(self, sort: bool = False) -> str: ...
    def extractTEXT(self, sort: bool = False) -> str: ...
    def extractBLOCKS(
        self,
    ) -> list[tuple[float, float, float, float, str, int, int]]: ...
    def extractWORDS(
        self, delimiters: str | None = None
    ) -> list[tuple[float, float, float, float, str, int, int, int]]: ...
    def extractHTML(self) -> str: ...
    def extractDICT(self, sort: bool = False) -> TextPageDict: ...
    def extractJSON(self, sort: bool = False) -> str: ...
    def extractXHTML(self) -> str: ...
    def extractXML(self) -> str: ...
    def extractRAWDICT(self, sort: bool = False) -> TextPageRawDict: ...
    def extractRAWJSON(self, sort: bool = False) -> str: ...
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
    def get_textpage(self, clip: Rect | IRect | None = None) -> TextPage: ...
    @overload
    def get_text(
        self,
        option: Literal["text"] = "text",
        *,
        clip: Rect | None = None,
        flags: int | None = None,
        textpage: TextPage | None = None,
        sort: bool = False,
        delimiters: str | None = None,
    ) -> str: ...
    @overload
    def get_text(
        self,
        option: str,
        *,
        clip: Rect | None = None,
        flags: int | None = None,
        textpage: TextPage | None = None,
        sort: bool = False,
        delimiters: str | None = None,
    ) -> str | list | dict: ...
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
    @property
    def rect(self) -> Rect: ...
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
    def parent(self) -> Document: ...
