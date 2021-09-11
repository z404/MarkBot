# MarkBot

A general purpose, easy to use discord bot

## Commands:

|          Command           | Description                                                                                          | Slash command |
| :------------------------: | ---------------------------------------------------------------------------------------------------- | :-----------: |
|            help            | Displays the bot's commands                                                                          |      No       |
|           invite           | Displays the invite link for the bot, which you can use to invite the bot to your server             |      Yes      |
|            logo            | Displays MarkBot's logo and ascii art                                                                |      Yes      |
|            math            | Tries to solve a few basic math problems                                                             |      Yes      |
|           tinify           | Command to shorten a url using tiny url                                                              |      Yes      |
|            wiki            | Searches wikipedia and shows a summary of the search term                                            |      Yes      |
|         stealemoji         | If you have nitro, you can use this command to save an emoji of another server to the current server |      No       |
|     currency_converter     | Converts currency from one unit to another                                                           |      Yes      |
| activity (and subcommands) | Command to launch activities                                                                         |      Yes      |
| cleanup (and subcommands)  | Commands to clean up your channel                                                                    |      Yes      |
|           purge            | Mass deletes messages to clean a channel                                                             |      Yes      |
|            join            | Joins a voice channel                                                                                |      No       |
|           leave            | Leaves a voice channel                                                                               |      No       |
|            now             | Shows current song playing                                                                           |      No       |
|           pause            | Pauses playback of current audio                                                                     |      No       |
|            play            | Enqueues the song into the queue                                                                     |      No       |
|           queue            | Displays the current song queue                                                                      |      No       |
|           remove           | Removes a song from the queue                                                                        |      No       |
|           resume           | Resumes paused playback                                                                              |      No       |
|          shuffle           | Shuffles the queue                                                                                   |      No       |
|            skip            | Skips song that is currently playing                                                                 |      No       |
|            stop            | Stops playback                                                                                       |      No       |
|           summon           | Summons the bot to a voice channel                                                                   |      No       |
|       toggleannounce       | Stops announcement of new song in channel                                                            |      No       |

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
