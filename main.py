import threading

from fugashi import Tagger


class SimpleFTS:
    __slots__ = ('__tagger', '__index', '__results', '__lock')

    def __init__(self) -> None:
        self.__tagger = Tagger()
        self.__index: dict[str, set] = {}
        self.__results = {}
        self.__lock = threading.RLock()

    def __tokenize(self, text: str) -> list[str]:
        result = []
        for word in self.__tagger(text):
            orig_text = word.surface
            fmt_text = word.feature.lemma
            pos1 = word.feature.pos1
            if (
                pos1 == "名詞"
                or pos1 == "動詞"
                or pos1 == "形容詞"
                or pos1 == "代名詞"
            ):
                result.append(fmt_text if fmt_text else orig_text)
        return result


    def add_index(self, text: str) -> None:
        with self.__lock:
            texts_id = len(self.__results)
            self.__results[len(self.__results)] = text
            for text_to_index in self.__tokenize(text):
                self.__index.setdefault(text_to_index, set()).add(texts_id)
            self.__results.update(self.__results)

    def search(self, text: str) -> list[str]:
        targets = []
        final_result = []

        for text_to_index in self.__tokenize(text):
            targets.append(text_to_index)
        if not targets: 
            return []

        for id in set.intersection(*[set(self.__index.get(k, set())) for k in targets]):
            final_result.append(self.__results[id])
        return final_result


fts = SimpleFTS()

fts.add_index(
    "最新のiPhoneで、あそこの美しい風景を楽しく撮影しました。 #全文検索ロジック"
)
fts.add_index(
    "最新のAndroidで、あそこの美しい風景を楽しく撮影しました。 #全文検索ロジック"
)
fts.add_index(
    "最新のGalaxy Note 7で、あそこの美しい風景を楽しく撮影しました。 #全文検索ロジック"
)
fts.add_index(
    "iPhoneの最新ロジック"
)

print(fts.search(
    "Galaxy 7"
))

print(fts.search(
    "あ、"
))
