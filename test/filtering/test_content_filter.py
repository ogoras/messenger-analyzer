from tkinter import W
import unittest
from src.filtering.content_filter import WordFilter
from src.filtering.wfilter import MatchWFilter, WFilter

class TestWordFilter(unittest.TestCase):
    def test_one_word(self):
        content = "this is a test"

        wfilter = MatchWFilter("this", "whole")
        wordfilter = WordFilter(wfilter)
        self.assertTrue(wordfilter.filter("", "", None, {"content": content}))
        
        wfilter = MatchWFilter("test", "whole")
        wordfilter = WordFilter(wfilter)
        self.assertTrue(wordfilter.filter("", "", None, {"content": content}))

        wfilter = MatchWFilter("badoo", "whole")
        wordfilter = WordFilter(wfilter)
        self.assertFalse(wordfilter.filter("", "", None, {"content": content}))

    def test_all_words(self):
        wfilter = MatchWFilter("foo", "whole")
        wordfilter = WordFilter(wfilter, "and")
        self.assertTrue(wordfilter.filter("", "", None,  {"content": "foo"}))
        self.assertTrue(wordfilter.filter("", "", None,  {"content": "foo foo"}))
        self.assertFalse(wordfilter.filter("", "", None,  {"content": "foo bar"}))
        self.assertFalse(wordfilter.filter("", "", None,  {"content": "bar foo"}))
        self.assertFalse(wordfilter.filter("", "", None,  {"content": "bar bar"}))

        wfilter = MatchWFilter("the", "left")
        wordfilter = WordFilter(wfilter, "and")
        self.assertTrue(wordfilter.filter("", "", None,  {"content": "the the"}))
        self.assertTrue(wordfilter.filter("", "", None,  {"content": "the the the"}))
        self.assertFalse(wordfilter.filter("", "", None,  {"content": "the the bar"}))
        self.assertFalse(wordfilter.filter("", "", None,  {"content": "the bar the"}))
        self.assertTrue(wordfilter.filter("", "", None,  {"content": "the thesis"}))
        self.assertTrue(wordfilter.filter("", "", None,  {"content": "theoretical thesis"}))
    
    def test_and_composition(self):
        wfilter1 = MatchWFilter("foo", "whole")
        wfilter2 = MatchWFilter("bar", "whole")
        wordfilter = WordFilter(wfilter1) & WordFilter(wfilter2)
        self.assertTrue(wordfilter.filter("", "", None,  {"content": "foo bar"}))
        self.assertFalse(wordfilter.filter("", "", None,  {"content": "foo"}))
        self.assertFalse(wordfilter.filter("", "", None,  {"content": "bar"}))
        self.assertTrue(wordfilter.filter("", "", None,  {"content": "foo bar foo"}))
        self.assertFalse(wordfilter.filter("", "", None,  {"content": ""}))

    def test_or_composition(self):
        wfilter1 = MatchWFilter("foo", "whole")
        wfilter2 = MatchWFilter("bar", "whole")
        wordfilter = WordFilter(wfilter1) | WordFilter(wfilter2)
        self.assertTrue(wordfilter.filter("", "", None,  {"content": "foo"}))
        self.assertTrue(wordfilter.filter("", "", None,  {"content": "bar"}))
        self.assertTrue(wordfilter.filter("", "", None,  {"content": "foo bar"}))
        self.assertTrue(wordfilter.filter("", "", None,  {"content": "bar foo"}))
        self.assertTrue(wordfilter.filter("", "", None,  {"content": "foo bar foo"}))
        self.assertTrue(wordfilter.filter("", "", None,  {"content": "bar foo bar"}))
        self.assertFalse(wordfilter.filter("", "", None,  {"content": ""}))
        self.assertFalse(wordfilter.filter("", "", None,  {"content": "something irrelevant"}))

    def test_xor_composition(self):
        wfilter1 = MatchWFilter("foo", "whole")
        wfilter2 = MatchWFilter("bar", "whole")
        wordfilter = WordFilter(wfilter1) ^ WordFilter(wfilter2)
        self.assertTrue(wordfilter.filter("", "", None,  {"content": "foo"}))
        self.assertTrue(wordfilter.filter("", "", None,  {"content": "bar"}))
        self.assertFalse(wordfilter.filter("", "", None,  {"content": "foo bar"}))
        self.assertFalse(wordfilter.filter("", "", None,  {"content": "bar foo"}))
        self.assertFalse(wordfilter.filter("", "", None,  {"content": "foo bar foo"}))
        self.assertTrue(wordfilter.filter("", "", None,  {"content": "bar bar bar"}))
        self.assertFalse(wordfilter.filter("", "", None,  {"content": ""}))
        self.assertFalse(wordfilter.filter("", "", None,  {"content": "something irrelevant"}))
