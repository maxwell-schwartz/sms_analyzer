# python 3.5.2
import sqlite3
import os
import random

def locate_sms_db():
    '''Find the name and location of the sms database'''

    parent_dir = input('Enter path to directory >> ')
    os.chdir(parent_dir)

    conn1 = sqlite3.connect('Manifest.db')
    c1 = conn1.cursor()
    sms_location = []
    # only one item should be found, but just in case
    for row in c1.execute("SELECT fileID FROM Files WHERE relativePath LIKE '%sms.db';"):
        sms_location.append(row)

    # database name is first item in list
    sms_db = sms_location[0][0]
    # directory name is first two letters/numbers in database name
    sms_dir = sms_db[:2]

    return sms_dir, sms_db

def get_sorted_freqs(freq_dict):
    '''Convert dictionary of frequencies to list sorted by frequency'''
    
    freq_list = list(freq_dict.items())
    for i in range(len(freq_list)):
        freq_list[i] = list(freq_list[i])
        freq_list[i].reverse()
    freq_list.sort()

    return freq_list


def get_sms_freq(c):
    '''Calculate the frequency of messages received from each number'''

    # dictionary of each number that has sent messages and their counts
    freq = {}
    for row in c.execute("SELECT handle.id, message.text FROM message JOIN handle ON message.handle_id = handle.ROWID WHERE message.is_from_me = 0;"):
        if row[0] in freq:
            freq[row[0]] += 1
        else:
            freq[row[0]] = 1

    sorted_items = get_sorted_freqs(freq)

    return sorted_items

def remove_punctuation(s):
    '''Return string with punctuation removed'''

    puncs = ['.', ',', '?', '"']

    return (''.join(c.lower() for c in s if c not in puncs),)


def get_messages_by_num(phone_num, c):
    '''Return a list of all messages sent from a specified number'''

    messages = []
    for row in c.execute("SELECT message.text FROM message JOIN handle ON message.handle_id = handle.ROWID WHERE handle.id = ? and message.is_from_me = 0;", (phone_num,)):
        messages.append(row)

    clean = []
    for m, in messages:
        removed = remove_punctuation(m)
        clean.append(removed)

    return clean

def get_word_freq(m_list):
    '''Return sorted list of words sorted by their frequency'''

    word_freq_dict = {}
    # mostly taken from NLTK's list of stop words
    stop_words = ['i', "i'm", 'me', 'my', 'myself', 'we', "we're", 'our', 'ours', 'ourselves', 'you', "you're", 'your', 'yours',
    'yourself', 'yourselves', 'he', "he's", 'him', 'his', 'himself', 'she', "she's", 'her', 'hers',
    'herself', 'it', 'its', "it's", 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
    'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', "isn't", 'are', "aren't",
    'was', "wasn't", 'were', "weren't", 'be', 'been', 'being', 'have', "haven't", 'has', "hasn't", 'had', "hadn't", 'having', 'do', "don't", 'does', "doesn't",
    'did', "didn't", 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
    'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
    'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
    'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
    'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
    'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
    'than', 'too', 'very', 'can', 'will', "won't", 'just', 'should', "shouldn't", 'now']

    for m in m_list:
        for word in m:
            if word.lower() in word_freq_dict:
                word_freq_dict[word.lower()] += 1
            elif word.lower() not in stop_words:
                word_freq_dict[word.lower()] = 1

    sorted_items = get_sorted_freqs(word_freq_dict)

    return sorted_items

def get_bigram_freq(m_list):
    '''Return sorted list of bigrams and their frequencies'''

    bg_freq_dict = {}
    bg_list = []
    for m in m_list:
        for i in range(1, len(m)):
            bg = (m[i-1].lower(), m[i].lower())
            if bg in bg_freq_dict:
                bg_freq_dict[bg] += 1
            else:
                bg_freq_dict[bg] = 1
    
    sorted_items = get_sorted_freqs(bg_freq_dict)

    return sorted_items

def insert_tags(m_list):
    '''Insert open and close message tags'''

    for i in range(len(m_list)):
        m_list[i].insert(0, '<M>')
        m_list[i].append('</M>')

    return m_list

def get_bg_list(m_list):
    '''Return list of all bigrams'''

    bg_list = []

    for m in m_list:
        for i in range(1, len(m)):
            bg_list.append((m[i-1], m[i]))

    return bg_list

def generate_text(bg_list):
    '''Generate a message based on bigrams'''

    seed = '<M>'
    t = []
    while seed != '</M>':
        options = [bg for bg in bg_list if bg[0] == seed]
        random.shuffle(options)
        pick = options[0][1]
        t.append(pick)
        seed = pick
    t = t[:len(t)-1]
    print(' '.join(t))

def main():

    sms_dir, sms_db = locate_sms_db()
    os.chdir(sms_dir)

    conn2 = sqlite3.connect(sms_db)
    c2 = conn2.cursor()

    sms_freq = get_sms_freq(c2)
    most_often = sms_freq[-1][1]
    ms = get_messages_by_num(most_often, c2)
    for i in range(len(ms)):
        ms[i] = ms[i][0].split()

    tagged = insert_tags(ms)
    bg_list = get_bg_list(tagged)
    generate_text(bg_list)

    # word_freqs = get_word_freq(ms)
    # print(word_freqs[-1])


    # bg_freqs = get_bigram_freq(ms)
    # print(bg_freqs[-1], bg_freqs[-2])

    # print(ms[0])
    # print(most_often + ' texted you the most often. You received ' + str(sms_freq[-1][0]) + ' messages from them!')

main()