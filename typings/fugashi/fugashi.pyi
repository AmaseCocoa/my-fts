from typing import Any, NamedTuple, Sequence

class UnidicFeatures17(NamedTuple):
    pos1: str | None
    pos2: str | None
    pos3: str | None
    pos4: str | None
    cType: str | None
    cForm: str | None
    lForm: str | None
    lemma: str | None
    orth: str | None
    pron: str | None
    orthBase: str | None
    pronBase: str | None
    goshu: str | None
    iType: str | None
    iForm: str | None
    fType: str | None
    fForm: str | None

class UnidicFeatures26(NamedTuple):
    pos1: str | None
    pos2: str | None
    pos3: str | None
    pos4: str | None
    cType: str | None
    cForm: str | None
    lForm: str | None
    lemma: str | None
    orth: str | None
    pron: str | None
    orthBase: str | None
    pronBase: str | None
    goshu: str | None
    iType: str | None
    iForm: str | None
    fType: str | None
    fForm: str | None
    kana: str | None
    kanaBase: str | None
    form: str | None
    formBase: str | None
    iConType: str | None
    fConType: str | None
    aType: str | None
    aConType: str | None
    aModeType: str | None

class UnidicFeatures29(NamedTuple):
    pos1: str | None
    pos2: str | None
    pos3: str | None
    pos4: str | None
    cType: str | None
    cForm: str | None
    lForm: str | None
    lemma: str | None
    orth: str | None
    pron: str | None
    orthBase: str | None
    pronBase: str | None
    goshu: str | None
    iType: str | None
    iForm: str | None
    fType: str | None
    fForm: str | None
    iConType: str | None
    fConType: str | None
    type: str | None
    kana: str | None
    kanaBase: str | None
    form: str | None
    formBase: str | None
    aType: str | None
    aConType: str | None
    aModType: str | None
    lid: str | None
    lemma_id: str | None

class Node:
    @property
    def surface(self) -> str: ...
    @surface.setter
    def surface(self, ss: str) -> None: ...
    @property
    def feature(self) -> Any: ...
    @property
    def feature_raw(self) -> str: ...
    @property
    def length(self) -> int: ...
    @property
    def rlength(self) -> int: ...
    @property
    def posid(self) -> int: ...
    @property
    def char_type(self) -> int: ...
    @property
    def stat(self) -> int: ...
    @property
    def is_unk(self) -> bool: ...
    @property
    def white_space(self) -> str: ...
    @white_space.setter
    def white_space(self, ws: str) -> None: ...

class UnidicNode(Node):
    @property
    def pos(self) -> str: ...

class GenericTagger:
    def __init__(self, args: str = '', wrapper: Any = ..., quiet: bool = False) -> None: ...
    def __call__(self, text: str) -> list[Node]: ...
    def parse(self, text: str) -> str: ...
    def parseToNodeList(self, text: str) -> list[Node]: ...
    def nbest(self, text: str, num: int = 10) -> str: ...
    def nbestToNodeList(self, text: str, num: int = 10) -> list[list[Node]]: ...
    @property
    def dictionary_info(self) -> list[dict[str, Any]]: ...

class Tagger(GenericTagger):
    def __init__(self, arg: str = '') -> None: ...
    def __call__(self, text: str) -> list[UnidicNode]: ...
    def parseToNodeList(self, text: str) -> list[UnidicNode]: ...
    def nbestToNodeList(self, text: str, num: int = 10) -> list[list[UnidicNode]]: ...

def make_tuple(*args: Any) -> tuple[Any, ...]: ...
def create_feature_wrapper(name: str, fields: Sequence[str], default: Any = None) -> type[tuple[Any, ...]]: ...
def build_dictionary(args: str) -> None: ...
def try_import_unidic() -> str | None: ...

__all__ = [
    "UnidicFeatures17",
    "UnidicFeatures26",
    "UnidicFeatures29",
    "Node",
    "UnidicNode",
    "GenericTagger",
    "Tagger",
    "make_tuple",
    "create_feature_wrapper",
    "build_dictionary",
    "try_import_unidic",
]