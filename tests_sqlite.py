import shutil
import tempfile
import traceback
import unittest
from pathlib import Path
from GRT_sqlite import GRT


class TestGraphBehavior(unittest.TestCase):
    def setUp(self) -> None:
        DIRECTORY = "C:/temp/database"
        Path(DIRECTORY).mkdir(parents=True, exist_ok=True)
        args = {
            "directory": DIRECTORY,
        }
        self.GRT = GRT(**args)
        self.GRT.nodes.create(key="1", properties=1)
        self.GRT.nodes.create(key="2", properties=1)
        self.GRT.nodes.create(key="3", properties=1)
        self.GRT.nodes.create(key="4", properties=1)
        self.GRT.nodes.create(key="5", properties=1)
        self.GRT.nodes.create(key="6", properties=1)
        self.GRT.nodes.create(key="7", properties=1)
        self.GRT.nodes.create(key="8", properties=1)
        self.GRT.nodes.create(key="9", properties=1)
        self.GRT.nodes.create(key="10", properties=1)

        self.GRT.edges.create(source="1", target="10", properties=1)
        self.GRT.edges.create(source="2", target="9", properties=1)
        self.GRT.edges.create(source="3", target="8", properties=1)
        self.GRT.edges.create(source="4", target="7", properties=1)
        self.GRT.edges.create(source="5", target="6", properties=1)
        self.GRT.edges.create(source="6", target="5", properties=1)
        self.GRT.edges.create(source="7", target="4", properties=1)
        self.GRT.edges.create(source="8", target="3", properties=1)
        self.GRT.edges.create(source="9", target="2", properties=1)
        self.GRT.edges.create(source="10", target="1", properties=1)
        self.GRT.edges.create(source="10", target="10", properties=1)

    def tearDown(self) -> None:
        self.GRT.close()
        DIRECTORY = "C:/temp/database"
        shutil.rmtree(DIRECTORY)
        pass

    def test_node_create(self):
        self.assertEqual(self.GRT.nodes.get(key="10").properties, "1")

    def test_node_get(self):
        self.assertEqual(self.GRT.nodes.get(key="1").properties, "1")
        self.assertIsNone(self.GRT.nodes.get(key="0"), None)

    def test_node_get_all(self):
        self.GRT.nodes.create(key="11", properties=1)
        count = 0
        for _ in self.GRT.nodes.get_all():
            count += 1
        self.assertEqual(count, 11)

    def test_node_update(self):
        self.assertTrue(self.GRT.nodes.update(key="1", properties="1"))
        self.assertEqual(self.GRT.nodes.get(key="1").properties, "1")

    def test_node_delete(self):
        self.GRT.nodes.delete(key="1")
        count = 0
        for _ in self.GRT.nodes.get_all():
            count += 1
        self.assertEqual(count, 9)

    def test_edge_create(self):
        self.assertTrue(self.GRT.edges.create(source="0", target="11", properties=1))
        self.assertTrue(self.GRT.edges.create(source="1", target="2", properties=1))
        self.assertTrue(self.GRT.edges.create(source="2", target="1", properties=1))

    def test_edge_get(self):
        self.assertIsNotNone(self.GRT.edges.get(source="1", target="10"))
        self.assertEqual(self.GRT.edges.get(source="1", target="10").properties, "1")
        self.assertIsNone(self.GRT.edges.get(source="2", target="1"))
        self.assertEqual(self.GRT.edges.get(source="2", target="1"), None)
        self.assertEqual(len([_ for _ in self.GRT.edges.get_incoming(key="1")]), 1)
        self.assertEqual(len([_ for _ in self.GRT.edges.get_incoming(key="2")]), 1)
        self.assertEqual(len([_ for _ in self.GRT.edges.get_outgoing(key="1")]), 1)
        self.assertEqual(len([_ for _ in self.GRT.edges.get_all()]), 11)

    def test_edge_update(self):
        self.GRT.nodes.create(key="100", properties=10)
        self.GRT.nodes.create(key="200", properties=20)
        self.GRT.nodes.create(key="300", properties=30)
        self.GRT.nodes.create(key="400", properties=40)
        self.GRT.edges.create(source="100", target="200", properties="100")
        self.GRT.edges.create(source="200", target="100", properties="200")
        self.GRT.edges.create(source="300", target="300", properties="301")
        self.assertTrue(
            self.GRT.edges.update(source="200", target="100", properties="201")
        )
        self.assertEqual(
            self.GRT.edges.get(source="200", target="100").properties, "201"
        )

    def test_edge_deletion(self):
        self.assertTrue(self.GRT.edges.delete(source="1", target="2"))


    def test_edge_deletion_of_node(self):
        self.GRT.nodes.delete(key="1")
        self.assertEqual(len([_ for _ in self.GRT.edges.get_outgoing(key="1")]), 0)


if __name__ == "__main__":
    unittest.main()
