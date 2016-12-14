# python 3.5.2
import sqlite3
import os

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

def get_sms_freq(c):
    '''Calculate the frequency of messages received from each number'''

    # dictionary of each number that has sent messages and their counts
    freq = {}
    for row in c.execute("SELECT handle.id, message.text FROM message JOIN handle ON message.handle_id = handle.ROWID WHERE message.is_from_me = 0;"):
        if row[0] in freq:
            freq[row[0]] += 1
        else:
            freq[row[0]] = 1

    # convert to list of phone numbers and count; sort by frequency
    freq_tup = list(freq.items())
    for i in range(len(freq_tup)):
        freq_tup[i] = list(freq_tup[i])
        freq_tup[i].reverse()
    freq_tup.sort()

    return freq_tup

def main():

    sms_dir, sms_db = locate_sms_db()
    os.chdir(sms_dir)

    conn2 = sqlite3.connect(sms_db)
    c2 = conn2.cursor()

    sms_freq = get_sms_freq(c2)


    print(sms_freq[-1][1] + ' texted you the most often. You received ' + str(sms_freq[-1][0]) + ' messages from them!')

main()