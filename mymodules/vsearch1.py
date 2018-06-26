import re
from collections import Counter


def search_for_vowels(phrase: str) -> set:
    """ 入力された単語内の母音を返す。 """
    vowels = set('aeiou')
    return vowels.intersection(set(phrase))

# phrase = input('単語を入力してください。母音を探します。=> ')
# search_for_vowels(phrase)


def search_for_letters(phrase: str, letters: str='aeiou') -> set:
    """ phrase内のlettersの集合を返す。 """
    return set(letters).intersection(set(phrase))


def search_for_words(phrase: str, words: str='word') -> set:
    """ phrase内のwordsの集合を返す。 """
    set_word_in_phrase = {word for word in phrase.strip().replace(",", "").replace(".", "").split()}
    set_word_in_words = {word for word in words.strip().replace(",", " ").replace(".", " ").split()}
    return set_word_in_words.intersection(set_word_in_phrase)


def search_for_titles(phrase: str='Hello, Python!!') -> set:
    """ phrase内の大文字で始まる単語の集合を返す。 """
    set_word_in_phrase = {word for word in phrase.strip().replace(",", "").replace(".", "").split()}
    pattern = re.compile(r'^[A-Z].*')
    set_title_in_phrase = {pattern.match(word).group()
                           for word in set_word_in_phrase
                           if pattern.match(word) is not None}
    return set_title_in_phrase


def search_and_count_words(phrase: str, words: str='Python') -> dict:
    """ phrase内の「wordsとその出現回数」の辞書を返す。 """
    list_word_in_phrase = phrase.strip().replace(",", "").replace(".", "").split()
    dict_word_in_phrase = {word: cnt for word, cnt in Counter(list_word_in_phrase).most_common()}
    set_word_in_words = set(words.strip().replace(",", " ").split())
    dict_word = {}
    for word in set_word_in_words:
        if word in dict_word_in_phrase.keys():
            dict_word[word] = dict_word_in_phrase[word]
        dict_word.setdefault(word, 0)
    return dict_word
