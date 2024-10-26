import shutil
import tempfile
import traceback
import unittest
from pathlib import Path
from GRT_filesystem import GRT


class TestGraphBehavior(unittest.TestCase):
    def setUp(self) -> None:
        DIRECTORY = "C:/temp/graph"
        Path(DIRECTORY).mkdir(parents=True, exist_ok=True)
        args = {
            "directory": DIRECTORY,
        }
        self.GRT = GRT(**args)
        self.GRT.nodes.create(node_id="1", properties="1")
        self.GRT.nodes.create(node_id="2", properties="1")
        self.GRT.nodes.create(node_id="3", properties="1")
        self.GRT.nodes.create(node_id="4", properties="1")
        self.GRT.nodes.create(node_id="5", properties="1")
        self.GRT.nodes.create(node_id="6", properties="1")
        self.GRT.nodes.create(node_id="7", properties="1")
        self.GRT.nodes.create(node_id="8", properties="1")
        self.GRT.nodes.create(node_id="9", properties="1")
        self.GRT.nodes.create(node_id="10", properties="1")

        self.GRT.edges.create(src="1", dest="10", properties="1")
        self.GRT.edges.create(src="2", dest="9", properties="1")
        self.GRT.edges.create(src="3", dest="8", properties="1")
        self.GRT.edges.create(src="4", dest="7", properties="1")
        self.GRT.edges.create(src="5", dest="6", properties="1")
        self.GRT.edges.create(src="6", dest="5", properties="1")
        self.GRT.edges.create(src="7", dest="4", properties="1")
        self.GRT.edges.create(src="8", dest="3", properties="1")
        self.GRT.edges.create(src="9", dest="2", properties="1")
        self.GRT.edges.create(src="10", dest="1", properties="1")
        self.GRT.edges.create(src="10", dest="10", properties="1")

    def tearDown(self) -> None:
        DIRECTORY = "C:/temp/graph"
        shutil.rmtree(DIRECTORY)
        pass

    def test_node_create(self):
        self.assertEqual(self.GRT.nodes.get(node_id="10"), "1")

    def test_node_get(self):
        self.assertEqual(self.GRT.nodes.get(node_id="1"), "1")
        self.assertIsNone(self.GRT.nodes.get(node_id="0"), None)

    def test_node_get_all(self):
        self.GRT.nodes.create(node_id="11", properties="1")
        count = 0
        for _ in self.GRT.nodes.all():
            count += 1
        self.assertEqual(count, 11)

    def test_node_update(self):
        self.GRT.nodes.update(node_id="1", properties="1")
        self.assertEqual(self.GRT.nodes.get(node_id="1"), "1")

    def test_node_delete(self):
        self.GRT.nodes.delete(node_id="1")
        count = 0
        for _ in self.GRT.nodes.all():
            count += 1
        self.assertEqual(count, 9)

    def test_edge_create(self):
        self.GRT.edges.create(src="0", dest="11", properties="1")
        self.assertEqual(self.GRT.edges.get(src="0", dest="11"), "1")
        self.GRT.edges.create(src="1", dest="2", properties="1")
        self.assertEqual(self.GRT.edges.get(src="1", dest="2"), "1")
        self.GRT.edges.create(src="2", dest="1", properties="1")
        self.assertEqual(self.GRT.edges.get(src="2", dest="1"), "1")

    def test_edge_get(self):
        self.GRT.edges.create(src="2", dest="1", properties="1")
        self.assertIsNotNone(self.GRT.edges.get(src="1", dest="10"))
        self.assertEqual(self.GRT.edges.get(src="1", dest="10"), "1")
        self.assertIsNone(self.GRT.edges.get(src="5", dest="1"))
        self.assertEqual(self.GRT.edges.get(src="2", dest="1"), "1")
        self.assertEqual(len(self.GRT.edges.incoming(node_id="1")), 2)
        self.assertEqual(len(self.GRT.edges.incoming(node_id="2")), 1)
        self.assertEqual(len(self.GRT.edges.outgoing(node_id="1")), 1)
        self.assertEqual(len(self.GRT.edges.all()), 12)

    def test_edge_update(self):
        self.GRT.edges.create(src="200", dest="100", properties="200")
        self.GRT.edges.update(src="200", dest="100", properties="201")
        self.assertEqual(self.GRT.edges.get(src="200", dest="100"), "201")

    def test_edge_deletion(self):
        self.GRT.edges.delete(src="1", dest="2")
        self.assertIsNone(self.GRT.edges.get(src="1", dest="2"))

    def test_edge_deletion_of_node(self):
        self.GRT.nodes.delete(node_id="1")
        self.assertEqual(len(self.GRT.edges.outgoing(node_id="1")), 0)


if __name__ == "__main__":
    unittest.main()
