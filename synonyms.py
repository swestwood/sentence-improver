#!/usr/bin/env python
"""
Replaces every word in a user-provided sentence with a random synonym. 

Run as "python synonyms.py" (or make executable)
Skips words less than 4 characters and words without synonyms.
Basic handling of capitalization and punctuation.
Uses the Big Huge Thesaurus API (limited to 10000 requests a day).
Primitive input reading (don't backspace).

Complete. (February 3, 2012)
"""
__author__ = 'Sophia Westwood'

import sys, random, string
import urllib2, BeautifulSoup

"""Rudimentary handling of words with punctuation.
   Return a (word, punctutation) tuple that potentially strips a character
   of punctuation from the end of the word."""
def deal_with_punctuation(word):
    punctuate = ''
    if word and word[-1] in string.punctuation:
        punctuate = word[-1:]
        word = word[:-1]
    return word, punctuate

"""Fetches a list of synonyms from Big Huge Thesaurus, returning the 
   empty list for short words or words with no synonyms."""
def fetch_synonyms(word):
    if len(word) < 4:
        return []
    try:
        response = urllib2.urlopen("http://words.bighugelabs.com/api/2/5a6ae2652f540a9079321b5479556f9f/" + 
                                   word + "/xml")
    except urllib2.HTTPError: # Connection failed or no synonym
        return []
    soup = BeautifulSoup.BeautifulSoup(response.read())
    return [syn.text for syn in soup.findAll('w', {'r':'syn'})]
    
"""Prints out the sentence with words replaced by synonyms."""
def make_synonyms(sentence):
    if sentence[-1] == '\n':  # Deal with new line
        sentence = sentence[:-1]
    sentence = sentence.split(' ')
    if not sentence: 
        return
    for word in sentence:
        word, punctuate = deal_with_punctuation(word)
        synonyms = fetch_synonyms(word)
        if not synonyms:
            print word + punctuate,
        else:
            synonym = random.choice(synonyms)  # Randomize which synonym we pick
            if word[0].isupper():  # Checks for basic capitalization
                synonym = synonym.capitalize()
            print synonym + punctuate,
    print  # Final new line

"""Prompts the user, returning True if yes and False if no."""
def yes_or_no(prompt):
   while (True):
        yes_or_no = raw_input(prompt + ' ')
        if yes_or_no:
            if yes_or_no[0].lower() == 'y':
                return True
            elif yes_or_no[0].lower() == 'n':
                return False
        print "Please enter yes or no."

"""Runs on sample lyrics in lyrics-test.txt. 
  Returns early if the file open fails."""
def test_on_lyrics():
    try: 
        sentences = open('lyrics-test.txt', 'r').readlines()
    except IOError:
        print "Sorry, opening the lyrics file failed."
        return
    for sentence in sentences:
        make_synonyms(sentence)
    print

# Run the script
if __name__ == '__main__':
    # Ask whether to run on lyrics file as an example
    if yes_or_no("Run on lyrics as an example?"):
        test_on_lyrics()
    # Prompt for sentences
    while (True):
        make_synonyms(raw_input("Enter a phrase: "))





