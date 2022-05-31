import unittest

from src.categorizing.content_categorizer import WordCounter
from src.filtering.content_filter import WordFilter
from src.filtering.wfilter import MatchWFilter
from src.tools.message_finder import MessageFinder

def get_sample_contents():
    return [
            "foo",
            "foo foo",
            "foo bar",
            "bar foo",
            "bar bar",
            "foo bar foo",
            "bar foo bar",
            "irrelevant data",
            "i am foo",
            "barring"
        ]

class MessageFinderTest(unittest.TestCase):
    def test_finding_words(self):
        wfilter = MatchWFilter("foo", "whole")
        filter = WordFilter(wfilter)

        finder = MessageFinder(filter)
        contents = get_sample_contents()

        for content in contents:
            finder.search_message("", "", None, {"content": content, "sender_name": "Whatever"})
        
        self.assertEqual(finder.message_count, 7)
        self.assertEqual(finder.verbosity, 0)
        self.assertEqual(finder.count, 0)
        self.assertEqual(finder.counts_by_category, {})
        self.assertEqual(finder.messages_by_category, {"Whatever": 7})
        self.assertFalse(finder.counting)

    def test_counting_words(self):
        wfilter = MatchWFilter("foo", "whole")
        counter = WordCounter(wfilter)

        finder = MessageFinder(counter)
        contents = get_sample_contents()

        for content in contents:
            finder.search_message("", "", None, {"content": content, "sender_name": "Whatever"})

        self.assertEqual(finder.message_count, 7)
        self.assertEqual(finder.verbosity, 0)
        self.assertEqual(finder.count, 9)
        self.assertEqual(finder.counts_by_category, {"Whatever": 9})
        self.assertEqual(finder.messages_by_category, {"Whatever": 7})
        self.assertTrue(finder.counting)