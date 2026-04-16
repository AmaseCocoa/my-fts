import math
import msgpack
import threading
from pathlib import Path
from typing import TypedDict

from fugashi import Tagger


class Result(TypedDict):
    dl: int
    text: str


class BM25Data(TypedDict):
    avgdl: int | float
    N: int


class SimpleFTS:
    __slots__ = ("__tagger", "__index", "__results", "__lock", "__bm25", "__k1", "__b")

    def __init__(self, k1: float = 1.2, b: float = 0.75) -> None:
        self.__lock = threading.RLock()
        self.__tagger = Tagger()

        self.__index: dict[str, set[tuple[int, int]]] = {}
        self.__results: dict[int, Result] = {}
        self.__bm25: BM25Data = {"avgdl": 0, "N": 0}
        self.__k1 = k1
        self.__b = b

    def save(self, filepath: str | Path) -> None:
        """Save index to msgpack file."""
        with self.__lock:
            filepath = Path(filepath)
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            data = {
                "index": {k: list(v) for k, v in self.__index.items()},
                "results": {str(k): v for k, v in self.__results.items()},
                "bm25": self.__bm25,
                "k1": self.__k1,
                "b": self.__b,
            }
            
            with open(filepath, "wb") as f:
                f.write(msgpack.packb(data, use_bin_type=True))

    def load(self, filepath: str | Path) -> None:
        """Load index from msgpack file."""
        with self.__lock:
            filepath = Path(filepath)
            
            with open(filepath, "rb") as f:
                data = msgpack.unpackb(f.read(), raw=False, strict_map_key=False)
            
            self.__index = {
                k: {tuple(item) for item in v}
                for k, v in data["index"].items()
            }
            self.__results = {int(k): v for k, v in data["results"].items()}
            self.__bm25 = data["bm25"]
            self.__k1 = data["k1"]
            self.__b = data["b"]

    def __update_count(
        self, data_list: set[tuple[int, int]], target_id: int
    ) -> set[tuple[int, int]]:
        d = dict(data_list)
        d[target_id] = d.get(target_id, 0) + 1
        return set(d.items())

    def __update_avgdl(self):
        num_left = 0
        results = self.__results.values()

        for result in results:
            num_left += result["dl"]

        self.__bm25["avgdl"] = num_left / len(results)
        self.__bm25["N"] = len(self.__results.keys())

    def __tokenize(self, text: str) -> list[str]:
        result = []
        for word in self.__tagger(text):
            orig_text = word.surface
            fmt_text = word.feature.lemma
            pos1 = word.feature.pos1
            if pos1 in ["名詞", "動詞", "形容詞", "代名詞"]:
                result.append(fmt_text if fmt_text else orig_text)
        return result

    def __calculate_final_score(
        self, important_words: list[str], document_text: str, bm25_score: float
    ):
        final_score = bm25_score

        for word in important_words:
            if word not in document_text:
                final_score *= 0.1

        return max(0.0, min(final_score, 1.0))

    def add_index(self, text: str) -> None:
        with self.__lock:
            texts_id = len(self.__results)
            self.__results[len(self.__results)] = {"dl": len(text), "text": text}
            for text_to_index in self.__tokenize(text):
                self.__index[text_to_index] = self.__update_count(
                    self.__index.setdefault(text_to_index, set()), texts_id
                )
            self.__results.update(self.__results)

            self.__update_avgdl()

    def search(self, text: str) -> list[str]:
        scores: dict[int, int | float] = {}
        targets = []
        result = []
        final_result = []

        for text_to_index in self.__tokenize(text):
            targets.append(text_to_index)
        if not targets:
            return []

        common_ids = set.intersection( # union
            *[{t[0] for t in self.__index.get(k, set())} for k in targets]
        )
        key_id = targets[0]
        target_entries = self.__index.get(key_id, set())

        filtered_entries = (
            (entry_id, count)
            for entry_id, count in target_entries
            if entry_id in common_ids
        )

        avgdl = self.__bm25["avgdl"]
        N = self.__bm25["N"]
        n = len(target_entries)

        for id, count in filtered_entries:
            dl = self.__results[id]["dl"]
            result.append(self.__results[id]["text"])
            tf = count
            denominator = tf + self.__k1 * (1.0 - self.__b + self.__b * (dl / avgdl))
            idf = math.log(1.0 + (N - n + 0.5) / (n + 0.5))
            score = idf * (tf * (self.__k1 + 1.0)) / denominator
            scores[id] = scores.get(id, 0) + score

        for id, score in scores.items():
            text = self.__results[id]["text"]
            scores[id] = self.__calculate_final_score(targets, text, score)

        sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        for id, final_score in sorted_results:
            text = self.__results[id]["text"]
            final_result.append(f"[{final_score:.4f}] {text}")

        return final_result
