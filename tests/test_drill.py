"""Offline checks for Buzz Drill's server: which Anki decks a question's category is matched against."""
import unittest

import drill_server


class FakeAnki:
    def __init__(self, decks):
        self.decks = decks

    def _call(self, action, **params):
        assert action == "deckNames"
        return self.decks


class CategoryDeckTests(unittest.TestCase):
    def test_decks_named_after_the_category_or_its_subjects(self):
        anki = FakeAnki(["Default", "QB::Science::Physics", "QB::Literature", "Biology", "Art History"])
        self.assertEqual(drill_server._category_query(anki, "science"), 'deck:"QB::Science::Physics" OR deck:"Biology"')
        self.assertEqual(drill_server._category_query(anki, "literature"), 'deck:"QB::Literature"')
        self.assertEqual(drill_server._category_query(anki, "fine arts"), 'deck:"Art History"')

    def test_author_deck_names_still_match(self):
        anki = FakeAnki(["VFA", "OVFA::Film", "AFA", "Geography"])
        self.assertEqual(drill_server._category_query(anki, "fine arts"), 'deck:"VFA" OR deck:"OVFA::Film" OR deck:"AFA"')

    def test_no_matching_deck_searches_the_whole_collection(self):
        anki = FakeAnki(["Default", "My Quizbowl Cards"])
        self.assertEqual(drill_server._category_query(anki, "mythology"), "deck:*")
        self.assertEqual(drill_server._category_query(anki, "general"), "deck:*")

    def test_search_characters_in_deck_names_are_escaped(self):
        anki = FakeAnki(['History_1 "AP"'])
        self.assertEqual(drill_server._category_query(anki, "history"), "deck:*")
        anki = FakeAnki(["Science::AP_Bio*"])
        self.assertEqual(drill_server._category_query(anki, "science"), 'deck:"Science::AP\\_Bio\\*"')


if __name__ == "__main__":
    unittest.main()
