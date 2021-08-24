const Discord = require("discord.js");
const client = new Discord.Client({
  intents: [Discord.Intents.FLAGS.GUILDS, Discord.Intents.FLAGS.GUILD_MESSAGES],
});

client.on("ready", () => {
  console.log("Bot is ready");
});

const { DiscordTogether } = require("discord-together");

client.discordTogether = new DiscordTogether(client);

client.on("message", async (message) => {
  if (message.content === "start") {
    if (message.member.voice.channel) {
      client.discordTogether
        .createTogetherCode(message.member.voice.channel.id, "poker")
        .then(async (invite) => {
          return message.channel.send(`${invite.code}`);
        });
    }
  }
});

client.login("ODA4OTczMzMyOTg4OTUyNTg2.YCOVIA.oWhmJJL6cxpH8KwdmWhoQmSb8Zo");
