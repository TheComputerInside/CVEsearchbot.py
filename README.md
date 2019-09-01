# CVEsearchbot.py
A bot that searches CVEs, metasploit entries, and shodan. 


There's a few things you should know:

This was programmed in a few days. Some decisions may not be optimal.
This project was designed for learning the discord.py rewrite branch, 
whilst also trying to make something useful.

I've learned so much just doing this(especially about dictionaries), and I'll keep learning as long
as I'm maintaining it. 

Note: Unfortunately I've noticed the script acting really REALLY sluggish, and that probably means
that there's gonna be a MASSIVE rewrite coming up to address this. I suspect it would be infinitely
easier to implement yaspy or something specifically for the purpose of trying to speed it up as I 
think that the entire script being loaded into memory is probably not particularly optimal. 
Especially considering the nature of Python as it stands. 

### You will need the following dependancies:

discord (pip install discord.py)

feedparser (pip install feedparser)

shodan (pip install shodan)

and pycvesearch (https://github.com/cve-search/PyCVESearch)

The rest should be a part of the core python install.

You will also need an account from https://shodan.io to use the shodan features, and
a discord bot token from https://discordapp.com/developers/applications/me in order
for the script to work.

(soon I will just make a dependency installer so you won't have to mess with this)

This script uses Python 3 and should be compatible with Python 3.6+
