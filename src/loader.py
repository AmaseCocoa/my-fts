"""Loader for pre-built FTS index."""

from pathlib import Path

from .fts import SimpleFTS


_SINGLETON_INSTANCE: SimpleFTS | None = None


def get_fts(index_path: str | Path = "./index.msgpack") -> SimpleFTS:
    """Get or create singleton FTS instance with pre-built index.
    
    On first call, loads the index from disk.
    Subsequent calls return the cached instance.
    """
    global _SINGLETON_INSTANCE
    
    if _SINGLETON_INSTANCE is None:
        _SINGLETON_INSTANCE = SimpleFTS()
        _SINGLETON_INSTANCE.load(index_path)
    
    return _SINGLETON_INSTANCE
