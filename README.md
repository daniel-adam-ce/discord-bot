# PostgreSQL database project with a Python Discord bot

The purpose of this project is to use a database system that uses SQL (PostgreSQL) to log live data of some environment. To utilize Postgres with the bot in python, the library 'psycopg2'* was used.
The environment that was chosen was a private discord, where the data measured is (at this moment) only tracking the length of time a user spends in voice channels.
Currently, users can use bot commands (both normal and slash** commands) to display their data from the database. In the future, the data may be available on a website hosted on github pages.

Example output from a slash command: https://imgur.com/a/aLAmoHy

\* https://www.psycopg.org/

** https://discord-py-slash-command.readthedocs.io/en/latest/
