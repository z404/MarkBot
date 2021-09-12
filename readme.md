# MarkBot

A general purpose, easy to use discord bot

## Commands:

|          Command           | Description                                               | Slash command | Cog              | Working? |
| :------------------------: | --------------------------------------------------------- | :-----------: | ---------------- | :------: |
|            help            | Displays the bot's commands                               |      No       | None             |   Yes    |
|           invite           | Displays the invite link for the bot                      |      Yes      | Functionality    |   Yes    |
|            logo            | Displays MarkBot's logo and ascii art                     |      Yes      | Functionality    |   Yes    |
|            math            | Tries to solve a few basic math problems                  |      Yes      | Functionality    |    No    |
|           tinify           | Command to shorten a url using tiny url                   |      Yes      | Functionality    |   Yes    |
|            wiki            | Searches wikipedia and shows a summary of the search term |      Yes      | Functionality    |  Buggy   |
|         stealemoji         | Steal an emoji from another server                        |      No       | Functionality    |   Yes    |
|     currency_converter     | Converts currency from one unit to another                |      Yes      | Functionality    |   Yes    |
| activity (and subcommands) | Command to launch activities                              |      Yes      | MarkBot-Activity |   Yes    |
| cleanup (and subcommands)  | Commands to clean up your channel                         |      Yes      | Cleanup          |   Yes    |
|           purge            | Mass deletes messages to clean a channel                  |      Yes      | Cleanup          |   Yes    |
|            join            | Joins a voice channel                                     |      No       | Music            |   Yes    |
|           leave            | Leaves a voice channel                                    |      No       | Music            |   Yes    |
|            now             | Shows current song playing                                |      No       | Music            |   Yes    |
|           pause            | Pauses playback of current audio                          |      No       | Music            |   Yes    |
|            play            | Enqueues the song into the queue                          |      No       | Music            |   Yes    |
|           queue            | Displays the current song queue                           |      No       | Music            |   Yes    |
|           remove           | Removes a song from the queue                             |      No       | Music            |   Yes    |
|           resume           | Resumes paused playback                                   |      No       | Music            |   Yes    |
|          shuffle           | Shuffles the queue                                        |      No       | Music            |   Yes    |
|            skip            | Skips song that is currently playing                      |      No       | Music            |   Yes    |
|            stop            | Stops playback                                            |      No       | Music            |   Yes    |
|           summon           | Summons the bot to a voice channel                        |      No       | Music            |   Yes    |
|       toggleannounce       | Stops announcement of new song in channel                 |      No       | Music            |   Yes    |

## Structure of the bot

V1 has been discarded as it is extremely uncomfortable to work with and develop. V2's structure will be defined here.

- 📂 **MARKBOT**
  - 📂 **MarkBot\-v2**
    - 📄 [bot.py](MARKBOT/MarkBot-v2/bot.py)
    - 📂 **cogs**
      - 📄 [Activity.py](MARKBOT/MarkBot-v2/cogs/Activity.py)
      - 📄 [Administration.py](MARKBOT/MarkBot-v2/cogs/Administration.py)
      - 📄 [Cleanup.py](MARKBOT/MarkBot-v2/cogs/Cleanup.py)
      - 📄 [Functionality.py](MARKBOT/MarkBot-v2/cogs/Functionality.py)
      - 📂 **MarkBot\-Activity**
        - 📄 config.json
        - 📄 [index.js](MARKBOT/MarkBot-v2/cogs/MarkBot-Activity/index.js)
        - 📄 node_modules
        - 📄 [package\-lock.json](MARKBOT/MarkBot-v2/cogs/MarkBot-Activity/package-lock.json)
        - 📄 [package.json](MARKBOT/MarkBot-v2/cogs/MarkBot-Activity/package.json)
      - 📄 [Music.py](MARKBOT/MarkBot-v2/cogs/Music.py)
      - 📄 [Shrug.py](MARKBOT/MarkBot-v2/cogs/Shrug.py)
- 📄 config.json
- 📄 database
- 📄 [readme.md](readme.md)
- 📄 [requirements.txt](requirements.txt)
- 📄 [runscript.sh](runscript.sh)

As is visible, the driver code for the bot exists in [bot.py](MARKBOT/MarkBot-v2/bot.py). Each file in the cogs folder contains a command cog. Each of these cogs have a bunch of commands that have the same theme. If a new set of commands were to be developed, they would be made in a new cog.
