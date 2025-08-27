from __future__ import annotations

import threading
import traceback
from typing import Optional

from swiplserver import (
    PrologMQI,
    PrologQueryTimeoutError,
    PrologResultNotAvailableError,
    PrologThread,
)

from daplacer.utils import CONSULT


class PrologSession:
    _instance = None

    def __init__(self):
        self.thread: PrologThread = None

    @classmethod
    def start(cls) -> PrologSession:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def stop(cls):
        if cls._instance:
            # cls._instance.thread.stop()
            # cls._instance.mqi.stop()
            cls._instance = None
        print("Prolog session stopped.")

    @classmethod
    def get_thread(cls) -> PrologThread:
        if cls._instance is None:
            raise RuntimeError("PrologSession not started")
        return cls._instance.thread

    @classmethod
    def consult(cls, file: str):
        query = CONSULT.format(file)
        cls.timed_query(query, clean=False)

    @classmethod
    def timed_query(
        cls,
        query: str,
        timeout: Optional[int] = None,
        clean: bool = True,
    ):
        if clean:
            query = query.replace("'", "")
        try:
            return cls.get_thread().query(query, query_timeout_seconds=timeout)
        except PrologQueryTimeoutError:
            print(f"Timeout: {query} took longer than {timeout} seconds.")
            return None
        except Exception as e:
            print(f"Error executing query '{query}': {e}")
            traceback.print_exc()
            return None

    @classmethod
    def timed_async_query(
        cls,
        query: str,
        timeout: Optional[int] = None,
        find_all: Optional[bool] = False,
    ):
        prolog = cls.get_thread()
        try:
            prolog.query_async(query, find_all=find_all)
            result = prolog.query_async_result(wait_timeout_seconds=timeout)
            if not find_all:
                prolog.cancel_query_async()
            return result[0] if isinstance(result, list) else result
        except PrologResultNotAvailableError:
            print(f"Timeout: {query} took longer than {timeout} seconds.")
            prolog.cancel_query_async()
            return None
