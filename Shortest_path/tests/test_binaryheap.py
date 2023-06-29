import unittest
from dijkstra import binaryheap

class BinaryHeapTestCase(unittest.TestCase):
    def setUp(self):
        self.heap = binaryheap()

        #test push and pop, checks if retrns to expected results. 
    def test_push_and_pop(self):
        self.heap.push('A', 5)
        self.heap.push('B', 3)
        self.heap.push('C', 7)

        self.assertFalse(self.heap.is_empty())
        self.assertEqual(self.heap.pop(), (3, 'B'))
        self.assertEqual(self.heap.pop(), (5, 'A'))
        self.assertEqual(self.heap.pop(), (7, 'C'))
        self.assertIsNone(self.heap.pop())
        self.assertTrue(self.heap.is_empty())

    # test update
    def test_update(self):
        self.heap.push('A', 5)
        self.heap.push('B', 3)
        self.heap.push('C', 7)

        self.heap.update('A', 2)

        self.assertEqual(self.heap.pop(), (3, 'A'))
        self.assertEqual(self.heap.pop(), (7, 'B'))
        self.assertEqual(self.heap.pop(), (7, 'C'))
        self.assertIsNone(self.heap.pop())
        self.assertTrue(self.heap.is_empty())

        #test sift_down
    def test_sift_down(self):
        self.heap.heap = [[1, 0, 'A'], [3, 1, 'B'], [2, 2, 'C'], [4, 3, 'D']]
        self.heap._sift_down(0)
        self.assertEqual(self.heap.heap, [[1, 0, 'A'], [3, 1, 'B'], [2, 2, 'C'], [4, 3, 'D']])

        self.heap.heap = [[3, 0, 'A'], [1, 1, 'B'], [4, 2, 'C'], [2, 3, 'D']]
        self.heap._sift_down(0)
        self.assertEqual(self.heap.heap, [[1, 1, 'B'], [2, 3, 'D'], [4, 2, 'C'], [3, 0, 'A']])

        self.heap.heap = [[3, 0, 'A'], [4, 1, 'B'], [1, 2, 'C'], [2, 3, 'D']]
        self.heap._sift_down(0)
        self.assertEqual(self.heap.heap, [[1, 2, 'C'], [4, 1, 'B'], [3, 0, 'A'], [2, 3, 'D']])

        self.heap.heap = [[1, 0, 'A'], [2, 1, 'B'], [3, 2, 'C'], [4, 3, 'D']]
        self.heap._sift_down(0)
        self.assertEqual(self.heap.heap, [[1, 0, 'A'], [2, 1, 'B'], [3, 2, 'C'], [4, 3, 'D']])


if __name__ == '__main__':
    unittest.main()