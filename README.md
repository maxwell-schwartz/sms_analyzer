# sms_analyzer

Task: locate and analyze the sms database in the directory created when an iPhone is backed-up to a computer.

When an iPhone is backed-up to a computer, it creates a complicated directory tree that can be difficult to manually navigate. This directory includes a sqlite database of sms messages and metadata associated with them. This database can be difficult both the locate and navigate.

The current version of this code (written in Python 3.5) will generate (based on bigrams) a message in the voice of the person who has sent the most messages. This can be edited to generate in the voice of any person, of course.

Functions exist to identify the most frequent texter, a texter's most frequent words (excluding stop words), and a texter's most frequent bigrams.
