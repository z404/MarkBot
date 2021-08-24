const Discord = require("discord.js");
const client = new Discord.Client({
  intents: [Discord.Intents.FLAGS.GUILDS, Discord.Intents.FLAGS.GUILD_MESSAGES],
});
const { DiscordTogether } = require("discord-together");
const fs = require("fs");

let rawdata = fs.readFileSync("config.json");
let config_vars = JSON.parse(rawdata);

client.on("ready", () => {
  console.log("Bot is ready");
});

client.discordTogether = new DiscordTogether(client);

client.on("message", async (message) => {
  if (message.content === "start") {
    if (message.member.voice.channel) {
      client.discordTogether
        .createTogetherCode(message.member.voice.channel.id, "youtube")
        .then(async (invite) => {
          return message.channel.send(`${invite.code}`);
        });
    }
  }
});

client.login(config_vars["discord_token"]);
