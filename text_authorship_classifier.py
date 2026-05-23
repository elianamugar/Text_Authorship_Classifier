#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 13:23:02 2020

@author: Eliana Mugar
"""
import math

class TextModel:
    """ for objects that model a collection of one or more text documents
    """
    
    def __init__(self, model_name):
        """ constructs new TextModel object
            input self: TextModel object
            input model_name: string
        """
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.conjunctions = {}
    
    def __repr__(self):
        """ returns string for text model name and size of dictionary for each text
            input self: TextModel object
        """
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += '  number of stems: ' + str(len(self.stems)) + '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += '  number of conjunctions: ' + str(len(self.conjunctions)) + '\n'
        return s
    
    def add_string(self, s):
        """ analyzes the string txt and adds its pieces 
            to all of the dicts in this txt model
        """
        text = s.split()
        punctuation = '.!?'
        length = 0
        list_lengths = []
        for i in text:
            length += 1
            if i[-1] in punctuation:
                list_lengths += [length]
                length = 0
        for j in list_lengths:
            if j not in self.sentence_lengths:
                self.sentence_lengths[j] = 1
            else:
                self.sentence_lengths[j] += 1
                
        word_list = clean_text(s)
        
        for w in word_list:
            if w not in self.words:
                self.words[w] = 1
            else:
                self.words[w] += 1
        for w in word_list:
            if len(w) not in self.word_lengths:
                self.word_lengths[len(w)] = 1
            else:
                self.word_lengths[len(w)] += 1
        for w in word_list:
            if stem(w) not in self.stems:
                self.stems[stem(w)] = 1
            else:
                self.stems[stem(w)] += 1
                
        conj_list = ['and', 'or', 'but', 'nor', 'yet', 'so', 'because']
                
        for w in word_list:
            if w in conj_list:
                if w not in self.conjunctions:
                    self.conjunctions[w] = 1
                else:
                    self.conjunctions[w] += 1
            
                
    def add_file(self, filename):
        """ adds all text in the file identified by filename to model
        """
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        self.add_string(f.read())
        f.close()
        
    def save_model(self):
        """ saves TextModel object by writing various feature dicts to files
        """
        f = open(self.name + '_words', 'w')
        f.write(str(self.words))
        f.close()
        
        f = open(self.name + '_word_lengths', 'w')
        f.write(str(self.word_lengths))
        f.close()
        
        f = open(self.name + '_stems', 'w')
        f.write(str(self.stems))
        f.close()
        
        f = open(self.name + '_sentence_lengths', 'w')
        f.write(str(self.sentence_lengths))
        f.close()
        
        f = open(self.name + '_conjunctions', 'w')
        f.write(str(self.conjunctions))
        f.close()
        
    def read_model(self):
        """ reads sorted dicts for TextModel object from their files and
            assigns them to attributes of TextModel
        """
        f = open(self.name + '_words', 'r')
        words_str = f.read()
        f.close()
        self.words = dict(eval(words_str))
        
        f = open(self.name + '_word_lengths', 'r')
        word_lengths_str = f.read()
        f.close()
        self.word_lengths = dict(eval(word_lengths_str))
        
        f = open(self.name + '_stems', 'r')
        stems_str = f.read()
        f.close()
        self.stems = dict(eval(stems_str))
        
        f = open(self.name + '_sentence_lengths', 'r')
        sentence_lengths_str = f.read()
        f.close()
        self.sentence_lengths = dict(eval(sentence_lengths_str))
        
        f = open(self.name + '_conjunctions', 'r')
        conjunctions_str = f.read()
        f.close()
        self.conjunctions = dict(eval(conjunctions_str))
    
    def similarity_scores(self, other):
        """ computes and returns list of log similarity scores measuring
            self and other
        """
        words_score = compare_dictionaries(other.words, self.words)
        word_lengths_score = compare_dictionaries(other.word_lengths, self.word_lengths)
        stems_score = compare_dictionaries(other.stems, self.stems)
        sentence_lengths_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        conjunctions_score = compare_dictionaries(other.conjunctions, self.conjunctions)
        return [words_score, word_lengths_score, stems_score, sentence_lengths_score, conjunctions_score]
    
    def classify(self, source1, source2):
        """ compares self to source1 and source 2
            determines which of these are more likely source of self
        """
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        print('scores for ' + source1.name + ': ' + str(scores1) + '\n')
        print('scores for ' + source2.name + ': ' + str(scores2) + '\n')
        i = 0
        count1 = 0
        count2 = 0
        for i in range(len(scores1)):
            if scores1[i] > scores2[i]:
                count1 += 1
            elif scores2[i] > scores1[i]:
                count2 += 1
        if count1 > count2:
            print(self.name + ' is more likely to have come from ' + source1.name + '\n')
        elif count2 > count1:
            print(self.name + ' is more likely to have come from ' + source2.name + '\n')

def clean_text(txt):
    """ returns list of words in txt after cleaning
        used when processing each word in text individually
        input txt: string
    """
    punctuation = '.,?!;:"'
    txt = str.lower(txt)
    new_txt = ''
    for ch in txt:
        if ch not in punctuation:
            new_txt += ch
    return new_txt.split()

def stem(s):
    """ returns the stem of s
    """
    if len(s) < 5 and s[-3:] == 'ing' or (len(s) < 5 and s[-2:] == 'er') or (len(s) < 5 and s[-2:] == 'ed') or (len(s) < 5 and s[-4:] == 'able'):
        return s
    if s[-1:] == 's':
        s = s[:-1]
        s = stem(s)
    elif s[-2:] == 'es':
        s = s[:-2]
    elif s[-3:] == 'ing':
        if s[-4] == s[-5]:
            s = s[:-4]
        else:
            s = s[:-3]
    elif s[-2:] == 'er':
        if s[-3] == s[-4]:
            s = s[:-3]
        else:
            s = s[:-2]
    elif s[-2:] == 'ed':
        if s[-3] == s[-4]:
            s = s[:-3]
        else:
            s = s[:-2]
    elif s[0:2] == 're':
        s = s[2:]
        s = stem(s)
    elif s[0:3] == 'pre':
        s = s[3:]
        s = stem(s)
    return s

def compare_dictionaries(d1, d2):
    """ returns log similarity score of 2 feature dictionaries
    """
    score = 0
    # I made the total small because in the test(), both sources don't have 
    # conjunctions (my additional attribute)
    # so I couldn't make the total 0 or else it won't divide
    # In larger paras, this won't be a problem, but for test simple sentences
    # that contain no conjunctions, it won't work
    total = 0.00000001
    for key in d1:
        total += d1[key]
    for key in d2:
        if key in d1:
            score += math.log(d1[key] / total) * d2[key]
        elif key not in d1:
            score += math.log(0.5 / total) * d2[key]
    return score

# Copy and paste the following function into finalproject.py
# at the bottom of the file, *outside* of the TextModel class.
def test():
    """ tests comparison"""
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)

# at the bottom of the file, *outside* of the TextModel class.
def run_tests():
    """ tests code """
    source1 = TextModel('churchill')
    source1.add_file('churchill.txt')

    source2 = TextModel('shakespeare')
    source2.add_file('shaks12.txt')

    new1 = TextModel('sad')
    new1.add_file('sad..txt')
    new1.classify(source1, source2)

    # Add code for three other new models below.
    new2 = TextModel('shakespeare_comparison')
    new2.add_file('sonnets.txt')
    new2.classify(source1, source2)
    
    new3 = TextModel('churchill_comparison')
    new3.add_file('ch1churchill.txt')
    new3.classify(source1, source2)
    
    new4 = TextModel('poems')
    new4.add_file('poems.txt')
    new4.classify(source1, source2)

    
    
                
