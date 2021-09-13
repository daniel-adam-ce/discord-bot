# PostgreSQL database project with a Python Discord bot

The purpose of this project is to use a database system that uses SQL (PostgreSQL) to log live data of some environment. The bot was programmed in Python using the discord.py* library, and the library psycopg2** was used to be abke to use Postgres in Python.

The environment that was chosen was a private discord, where the data measured is only (at this moment) tracking the length of time a user spends in voice channels.
Currently, users can use bot commands (slash*** commands using discord-interactions library) to display their data from the database. There is also a second command that can display the voice channel session time of a queried user. 

Discord.py is no longer being updated by the original author. Because of this, the programming language of the bot may change to Javascript to use discord.js. Additionally, the data collected may used in a website in the future to be able to make and visualize probabilistic statements about future voice channel traffic.

Example output from a slash command: https://imgur.com/a/aLAmoHy

\* https://github.com/Rapptz/discord.py

** https://www.psycopg.org/

*** https://discord-py-slash-command.readthedocs.io/en/latest/
