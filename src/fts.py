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
        counts = []
        result = []

        for text_to_index in self.__tokenize(text):
            targets.append(text_to_index)
        if not targets: 
            return []

        common_ids = set.intersection(*[{t[0] for t in self.__index.get(k, set())} for k in targets])
        for id, count in {t for t in self.__index.get(targets[0], set()) if t[0] in common_ids}:
            counts.append(count)
            result.append(self.__results[id])
        sorted_pairs = sorted(zip(counts, result))
            
        final_result = [result for _, result in sorted_pairs]
        return final_result