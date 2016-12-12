# sms_analyzer

Task: locate and analyze the sms database in the directory created when an iPhone is backed-up to a computer.

When an iPhone is backed-up to a computer, it creates a complicated directory tree that can be difficult to manually navigate. This directory includes a sqlite database of sms messages and metadata associated with them. This database can be difficult both the locate and navigate.

The current version of this code (written in Python 3.5) will identify the phone number that has texted the user most frequently. The next version will include further analysis, including word frequency and related information.
