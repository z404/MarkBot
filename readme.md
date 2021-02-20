# Project-Mark v4

This project aims to combine basic discord functions with advanced functions like an alexa interface, Natural Language Processing, Text to speech etc.
[Click here to invite the bot to your server](https://discord.com/api/oauth2/authorize?client_id=781403770721402901&permissions=8&scope=bot)
## Installation
To make your own bot with this source code, you will have to follow these instructions carefully. These steps assume that you are a little comfortable in using the repl.it environment, as well as git

  - **Step 1: Creating an application**
      - Sign up for a discord developer account [here](https://discord.com/developers/)
      - Create an application under the developer console, and name it the name of your bot
      - Under the "General Information" of your bot, set the icon you want for your bot
      

  - **Step 2: Creating a Discord Bot**
      - In the application you created above, navigate to the "Bot" menu on the left
      - Under the "Build-A-Bot" menu, add a new bot, and set the name and image accordingly
      - Notice the "Copy token" button. This will come in handy later

  - **Step 3: Creating a repl.it server to run your bot**
      - Create a new account in repl.it [here](https://repl.it/signup)
      - Once you've created your account, navigate to your [dashboard](https://repl.it/~), and create a new repl by pressing the blue "+" button on the top left
      - Set language as Bash, name it accordingly. Make it private if you wish to keep your source code private

  - **Step 4: Uploading the bot to repl.it**
      - Clone this repository into your local computer
      - Go to your repl that you just created, and press the three dots and choose the option to "Upload files"
      - Select all files of the repository, and wait for them to upload
      - Don't upload the .git file (It changes the repl to a python repl, and then won't work at all)

  - **Step 5: Creating other required accounts**
      - Create a [spotify developer](https://developer.spotify.com/) account, make an application and copy the client id and client secret
      - Create a [giphy developer](https://developers.giphy.com/) account, and copy the API key after creating a new application
      - Create a [Wolfram Alpha](https://www.wolframalpha.com/) Account, navigate to the api page, create an application. Copy the AppID
  - **Step 6: Creating required credentials file**
      - Create a new file in the repl by pressing the "Add file" button
      - Name it ```creds.txt```
      - Open ```creds.txt```, and set the first line to your `discord bot's token` ("Copy Token" Button in the discord developer console)
      - Set the second line to `spotify client id`
      - Set the third line to the `spotify client secret`
      - Set the fourth line to your `giphy api key`
      - Set the fifth line to `your Wolfram Alpha AppID`
  - **Step 7: Creating required prefix file**
      - Create a new file in the repl by pressing the "Add file" button
      - name it `.prefix`
      - Type your prefix in the file (for example, if my prefix is !, then I type `!` in the file)
  - **Step 8: Hit run**
      - If everything ran properly, then the Project Mark Logo should be displayed in the console window of repl.
      - If something didn't work, feel free to raise an issue here, and I'll help you out
    
  - **Step 9: Keeping your bot always on**
      - Follow the guide given [here](https://repl.it/talk/learn/Hosting-discordpy-bots-with-replit/11008)
<!---
## Info
### Basic functions to be added:
- [ ] Natural Language Processor ---In Development
- [ ] Text to Speech
- [ ] Speech to Text
- [ ] Video Processing
  - [ ] Face Recognition
  - [ ] Object detection
  
### Functions as a discord bot:
- [x] Music bot

#### Do not run any programs in the subfolders, as they will not work, and might also break your packages and installations --->
