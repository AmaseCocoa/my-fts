import threading

from fugashi import Tagger


class SimpleFTS:
    __slots__ = ('__tagger', '__index', '__results', '__lock')

    def __init__(self) -> None:
        self.__tagger = Tagger()
        self.__index: dict[str, set[tuple[int, int]]] = {}
        self.__results = {}
        self.__lock = threading.RLock()
        
    def __update_count(self, data_list: set[tuple[int, int]], target_id: int) -> set[tuple[int, int]]:
        d = dict(data_list)
        d[target_id] = d.get(target_id, 0) + 1
        return set(d.items())

    def __tokenize(self, text: str) -> list[str]:
        result = []
        for word in self.__tagger(text):
            if text == "最新のGalaxy":
                print(word)
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
                self.__index[text_to_index] = self.__update_count(self.__index.setdefault(text_to_index, set()), texts_id)
            self.__results.update(self.__results)

    def search(self, text: str) -> list[str]:
        targets = []
        final_result = []

        for text_to_index in self.__tokenize(text):
            targets.append(text_to_index)
        if not targets: 
            return []

        for id, count in set.intersection(*[set(self.__index.get(k, set())) for k in targets]):
            print(count)
            final_result.append(self.__results[id])
        return final_result


fts = SimpleFTS()
to_index = [
    "最新のiPhoneで、あそこの美しい風景を楽しく撮影しました。 #全文検索ロジック",
    "最新のAndroidで、あそこの美しい風景を楽しく撮影しました。 #全文検索ロジック",
    "最新のGalaxy Note 7で、あそこの美しい風景を楽しく撮影しました。Galaxyはとても便利です。 #全文検索ロジック",
    "iPhoneの最新ロジック"
]

for text in to_index:
    fts.add_index(text)

print(fts.search(
    "最新のGalaxy"
))