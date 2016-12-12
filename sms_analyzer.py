# python 3.5.2
import sqlite3
import os

parent_dir = input('Enter path to directory >> ')
os.chdir(parent_dir)

conn1 = sqlite3.connect('Manifest.db')
c1 = conn1.cursor()
sms_location = []
for row in c1.execute("SELECT fileID FROM Files WHERE relativePath LIKE '%sms.db';"):
    sms_location.append(row)

sms_db = sms_location[0][0]
sms_dir = sms_db[:2]
os.chdir(sms_dir)

conn2 = sqlite3.connect(sms_db)
c2 = conn2.cursor()

freq = {}
for row in c2.execute("SELECT handle.id, message.text FROM message JOIN handle ON message.handle_id = handle.ROWID WHERE message.is_from_me = 0;"):
    if row[0] in freq:
        freq[row[0]] += 1
    else:
        freq[row[0]] = 1

freq_tup = list(freq.items())
for i in range(len(freq_tup)):
    freq_tup[i] = list(freq_tup[i])
    freq_tup[i].reverse()
freq_tup.sort()

print(freq_tup[-1][1] + ' texted you the most often. You received ' + str(freq_tup[-1][0]) + ' messages from them!')