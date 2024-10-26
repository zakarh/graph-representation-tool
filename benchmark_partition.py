import shutil
import tempfile
import traceback
import unittest
from pathlib import Path
from GRT_partition import GRT
import time


class TestGraphBehavior(unittest.TestCase):
    def setUp(self) -> None:
        DIRECTORY = "C:/temp/database"
        Path(DIRECTORY).mkdir(parents=True, exist_ok=True)
        args = {
            "directory": DIRECTORY,
        }
        self.GRT = GRT(**args)

    def test_create_nodes(self):
        for i in range(1, 100_000 + 1):
            print(f"{i}/{100_000}", end="\r")
            self.GRT.nodes.create(key=str(i))
        print()


if __name__ == "__main__":
    unittest.main()
