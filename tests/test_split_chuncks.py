import logging
import pytest
import yaml
import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)


class SplitChunks:
    @staticmethod
    def split_to_chunks(size, chunk_size):
        if chunk_size < 0:
            raise ValueError(f"chunk_size must be > 0, {chunk_size}")
        if size < 0:
            raise ValueError(f"size must be > 0, {size}")
        return SplitChunks._split_to_chunks(size, chunk_size)

    @staticmethod
    def _split_to_chunks(size, chunk_size):
        start = 0
        while start < size:
            end = min(start + chunk_size, size)
            # returns tuples generator
            yield start, end
            start = end

    @staticmethod
    def split_to_chunks2(size, chunk_size):
        if chunk_size < 0:
            raise ValueError(f"chunk_size must be > 0, {chunk_size}")
        if size < 0:
            raise ValueError(f"size must be > 0, {size}")
        return SplitChunks._split_to_chunks2(size, chunk_size)

    @staticmethod
    def _split_to_chunks2(size, chunk_size):
        start = 0
        chunks = []
        while start < size:
            end = min(start + chunk_size, size)
            chunks.append([start, end])
            start = end
        return chunks


class TestSplitChunks:
    @pytest.mark.parametrize("size, chunk_size, expected", [
        (10, 3, [[0, 3], [3, 6], [6, 9], [9, 10]]),
        (10, 10, [[0, 10]]),
        (10, 100, [[0, 10]]),
    ], ids=[
        "size_bigger_chunk_size",
        "size_equals_chunk_size",
        "size_smaller_chunk_size"
    ])
    def test_split_to_chunks(self, size, chunk_size, expected):
        chunks = SplitChunks.split_to_chunks(size, chunk_size)
        chunks = [list(c) for c in chunks]
        logging.info(chunks)
        assert chunks == expected

    @staticmethod
    def load_split_test_cases():
        with open("../files/split_cases.yml") as tc_file:
            data = yaml.safe_load(tc_file)
        for tc in data:
            yield tc['size'], tc['chunk_size'], tc['chunks']

    @staticmethod
    def load_split_test_cases2():
        with open("../files/split_cases.yml") as tc_file:
            data = yaml.safe_load(tc_file)
        # return map(lambda tc: (tc['size'], tc['chunk_size'], tc['chunks']), data)
        return [(tc['size'], tc['chunk_size'], tc['chunks']) for tc in data]

    @pytest.mark.parametrize("size, chunk_size, expected", load_split_test_cases(), ids=[
        "size_bigger_chunk_size",
        "size_equals_chunk_size",
        "size_smaller_chunk_size"
    ])
    def test_split_to_chunks_with_yaml(self, size, chunk_size, expected):
        chunks = SplitChunks.split_to_chunks(size, chunk_size)
        chunks = [list(c) for c in chunks]
        logging.info(chunks)
        assert chunks == expected

    @pytest.mark.parametrize("size, chunk_size, expected", load_split_test_cases2(), ids=[
        "size_bigger_chunk_size",
        "size_equals_chunk_size",
        "size_smaller_chunk_size"
    ])
    def test_split_to_chunks2_with_yaml(self, size, chunk_size, expected):
        logging.info(f"size: {size}, chunk_size: {chunk_size}")
        chunks = SplitChunks.split_to_chunks2(size, chunk_size)
        logging.info(chunks)
        assert chunks == expected
