from distraction import Distraction
import unittest


class TestBot(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.distraction = Distraction()

    def test_counts(self):
        results = self.distraction.ask_question()
        self.assertIsInstance(results, tuple)
        self.assertEqual(len(results), 2)
        self.assertEqual(len(results[0]), 8)
        self.assertEqual(len(results[1]), self.distraction.number_of_options)
        self.assertEqual(list(set([len(r) for r in results[1]]))[0], 8)
        self.assertGreaterEqual(
            sum([sorted(results[0]) == sorted(r) for r in results[1]]),
            1
        )

    def test_comparison(self):
        self.distraction.current_word = "ANALYSIS"
        words = self.distraction.ask_question()
        self.assertEqual(sorted(self.distraction.current_word), sorted(words[0]))
        self.assertTrue(self.distraction.answer("ANALYSIS"))
        self.distraction.current_word = "ANALYSIS"
        self.assertFalse(self.distraction.answer("AMERICAN"))


if __name__ == '__main__':
    unittest.main()
