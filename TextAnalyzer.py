# -*- coding: utf-8 -*-

'''
Created on 09.07.2015

@author: Goetz Edinger
'''
import enchant
import nltk.data
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import string
import sys

debug = True

dict_sentence_length      = {}
dict_word_length          = {}

number_of_letters         = 0
number_of_words           = 0
number_of_sentences       = 0

average_length_word       = 0
number_of_foreign_words   = 0
average_length_sentence   = 0
length_shortest_word      = 10000
length_longest_word       = 0
length_of_all_words       = 0
length_shortest_sentence  = 10000
length_longest_sentence   = 0
length_of_all_sentences   = 0

number_of_words_long_sentence = 0

shortest_word = ""
longest_word = ""

def count_letters(text):
    global number_of_letters

    number_of_letters = len(text)

########################################################
#
# Split Text into words
# Count the letters of every word
# Count how many words have how many letters
#
########################################################

def tokenize_words(text):
    global number_of_words
    global dict_word_length
    global length_of_all_words
    global length_longest_word
    global length_shortest_word
    global shortest_word
    global longest_word

    word_tokenize_list = word_tokenize(text)
    count_foreign_words(word_tokenize_list)
    number_of_words = len(word_tokenize_list)

    for word in  word_tokenize_list:
        if word in [",", ".", ":", ";", "!", "?"]:
            number_of_words -= 1

    for word in  word_tokenize_list:
        if word not in [",", ".", ":", ";", "!", "?"]:
            # Get the length of the word
            word_length = len(word)

            # Get the longest word
            if word_length > length_longest_word:
                length_longest_word = word_length
                longest_word = word

            # Get the shortest word
            if word_length < length_shortest_word:
                length_shortest_word = word_length
                shortest_word = word

            # Add word_length to length_of_all_words which is a variable to compute the average_length_word
            length_of_all_words += word_length

            # Look up in the Dictionary dict_word_length, if there is already a key with the same length.
            if dict_word_length.has_key(word_length):
                # If yes, then get the value of that key ...
                old_key = dict_word_length.get(word_length)
                # ... increase the value ...
                new_key = old_key + 1
                # ... write the key/value pair to the Dictionary dict_word_length
                dict_word_length[word_length] = new_key
            else:
                # ... add new key (word_length) with value 1
                dict_word_length[word_length] = 1

########################################################
#
# Split Text into sentences
# Count the words of every sentence
# Count how many sentences have how many words
#
########################################################

def tokenize_sentences(text):
    global length_longest_sentence
    global length_shortest_sentence
    global dict_sentence_length
    global number_of_sentences
    global length_of_all_sentences

    german_tokenizer = nltk.data.load('tokenizers/punkt/german.pickle')
    sent_tokenize_list = german_tokenizer.tokenize(text)
    number_of_sentences = len(sent_tokenize_list)

    if debug:
        print "\nSätze\n"

    for sentence in sent_tokenize_list:
        if debug:
            print sentence
        # Get the length of the sentence
        sentence_length = len(sentence)

        # Add sentence_length to length_of_all_sentences which is a variable to compute the average_length_sentence
        length_of_all_sentences += sentence_length

        # Get the longest sentence
        if sentence_length > length_longest_sentence:
            length_longest_sentence = sentence_length

        # Get the shortest sentence
        if sentence_length < length_shortest_sentence:
            length_shortest_sentence = sentence_length

        # Look up in the Dictionary dict_sentence_length, if there is already a key with the same length.
        if dict_sentence_length.has_key(sentence_length):
            # If yes, then get the value of that key ...
            old_key = dict_sentence_length.get(sentence_length)
            # ... increase the value ...
            new_key = old_key + 1
            # ... write the key/value pair to the Dictionary dict_sentence_length
            dict_sentence_length[sentence_length] = new_key
        else:
            # ... add new key (sentence_length) with value 1
            dict_sentence_length[sentence_length] = 1

########################################################
#
# Count foreign words
#
########################################################

def count_foreign_words(word_list):
    global number_of_foreign_words

    d = enchant.Dict("de_DE")

    if debug:
        print "Fremdwörter\n"

    for word in word_list:
        if not d.check(word):
            if word not in [",", ".", ":", ";", "!", "?"]:
                number_of_foreign_words += 1
                if debug:
                    print word

########################################################
#
# Display results
#
########################################################

def display_results():
    global number_of_letters
    global number_of_words
    global number_of_sentences
    global average_length_word
    global number_of_foreign_words
    global average_length_sentence
    global length_shortest_word
    global length_longest_word
    global length_shortest_sentence
    global length_longest_sentence
    global shortest_word
    global longest_word

    if debug:
        print "Number of letters              : " + str(number_of_letters)
        print "Number of words                : " + str(number_of_words)
        print "Number of sentences            : " + str(number_of_sentences)
        print "Average length of words        : " + str(average_length_word)
        print "Number of foreign words        : " + str(number_of_foreign_words)
        print "Average length of sentences    : " + str(average_length_sentence)
        print "Length of the shortest word    : " + str(length_shortest_word)
        print "Shortest word                  : " + shortest_word
        print "Length of the longest word     : " + str(length_longest_word)
        print "Longest word                   : " + longest_word
        print "Length of the shortest sentence: " + str(length_shortest_sentence)
        print "Length of the longest sentence : " + str(length_longest_sentence)

########################################################
#
# Statistics:
#
# Thresholds:
#
# for words:
# green  == good            ()
# yellow == acceptable      ()
# red    == not acceptable  ()
#
# for sentences:
# green  == good            ()
# yellow == acceptable      ()
# red    == not acceptable  ()
#
# Calculate the average length of the words
# Calculate the average length of the sentences
#
########################################################

def statistics():
    global length_of_all_words
    global number_of_words
    global average_length_word
    global length_of_all_sentences
    global number_of_sentences
    global average_length_sentence

    # Calculate the average length of the words
    average_length_word = length_of_all_words/number_of_words

    # Calculate the average length of the sentences
    average_length_sentence = length_of_all_sentences/number_of_sentences

def get_text_from_file(filename):
    text = ""
    try:
        file = open(filename, 'r')
        text = file.read()
        return text
    except:
        return text

def main(argv):
    text = """Raum- und Zeitangaben sind in der Relativitätstheorie keine universell gültigen Ordnungsstrukturen. Vielmehr werden der räumliche und zeitliche Abstand zweier Ereignisse oder auch deren Gleichzeitigkeit von Beobachtern mit verschiedenen Bewegungszuständen unterschiedlich beurteilt. Bewegte Objekte erweisen sich im Vergleich zum Ruhezustand in Bewegungsrichtung als verkürzt und bewegte Uhren als verlangsamt. Da jedoch jeder gleichförmig bewegte Beobachter den Standpunkt vertreten kann, er sei in Ruhe, beruhen diese Beobachtungen auf Gegenseitigkeit, das heißt, zwei relativ zueinander bewegte Beobachter sehen die Uhren des jeweils anderen langsamer gehen. Außerdem sind aus ihrer Sicht die Meterstäbe des jeweils anderen kürzer als ein Meter, wenn sie längs der Bewegungsrichtung ausgerichtet sind. Die Frage, wer die Situation korrekt beschreibt, ist hierbei prinzipiell nicht zu beantworten und daher sinnlos.
Diese Längenkontraktion und Zeitdilatation lassen sich vergleichsweise anschaulich anhand von Minkowski-Diagrammen und anhand des bekannten Zwillingsparadoxons nachvollziehen. In der mathematischen Formulierung ergeben sie sich aus der Lorentz-Transformation, die den Zusammenhang zwischen den Raum- und Zeitkoordinaten der verschiedenen Beobachter beschreibt. Diese Transformation lässt sich direkt aus den beiden obigen Axiomen und der Annahme, dass sie linear ist, herleiten.
Die meisten dieser relativistisch erklärbaren Phänomene machen sich erst bei Geschwindigkeiten bemerkbar, die im Vergleich zur Lichtgeschwindigkeit nennenswert groß sind. Solche Geschwindigkeiten werden im Alltag nicht annähernd erreicht. John Smith ist ein Märchenerzähler. Der 1. Mai ist ein Feiertag. Hol's der Kuckuck!"""

    if len(argv) > 0:
        text = get_text_from_file(argv[0])
    if len(argv) > 1:
        print "usage: python TextAnalyzer"
        print "or"
        print "python TextAnalyzer <filename>"
    else:
        if len(text) > 2:
            count_letters(text)
            tokenize_words(text)
            tokenize_sentences(text)
            statistics()
            display_results()
        else:
            print "Something went wrong ..."

if __name__ == '__main__':
    main(sys.argv[1:])
