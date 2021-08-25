const Discord = require("discord.js");
const client = new Discord.Client({
  intents: [Discord.Intents.FLAGS.GUILDS, Discord.Intents.FLAGS.GUILD_MESSAGES],
});
const { DiscordTogether } = require("discord-together");
const fs = require("fs");
var request = require("request-promise");

let rawdata = fs.readFileSync("config.json");
let config_vars = JSON.parse(rawdata);

client.on("ready", () => {
  console.log("Activity commands loaded");
});

client.discordTogether = new DiscordTogether(client);

client.on("messageCreate", async (message) => {
  if (message.content === config_vars["prefix"] + "activity youtube") {
    if (message.member.voice.channel) {
      client.discordTogether
        .createTogetherCode(message.member.voice.channel.id, "youtube")
        .then(async (invite) => {
          const button = new Discord.MessageButton()
            .setStyle("LINK")
            .setURL(invite.code)
            .setLabel("Click me for Youtube Together!");
          const row = new Discord.MessageActionRow().addComponents([button]);
          return message.channel.send({
            content:
              "Click the below button to join the Youtube Together activity!",
            components: [row],
          });
        });
    }
  } else if (message.content === config_vars["prefix"] + "activity poker") {
    if (message.member.voice.channel) {
      client.discordTogether
        .createTogetherCode(message.member.voice.channel.id, "poker")
        .then(async (invite) => {
          const button = new Discord.MessageButton()
            .setStyle("LINK")
            .setURL(invite.code)
            .setLabel("Click me for Poker Night!");
          const row = new Discord.MessageActionRow().addComponents([button]);
          return message.channel.send({
            content: "Click the below button to join the Poker Night activity!",
            components: [row],
          });
        });
    }
  } else if (message.content === config_vars["prefix"] + "activity chess") {
    if (message.member.voice.channel) {
      client.discordTogether
        .createTogetherCode(message.member.voice.channel.id, "chess")
        .then(async (invite) => {
          const button = new Discord.MessageButton()
            .setStyle("LINK")
            .setURL(invite.code)
            .setLabel("Click me for Chess in the park!");
          const row = new Discord.MessageActionRow().addComponents([button]);
          return message.channel.send({
            content:
              "Click the below button to join the Chess in the park activity!",
            components: [row],
          });
        });
    }
  } else if (
    message.content ===
    config_vars["prefix"] + "activity fishington"
  ) {
    if (message.member.voice.channel) {
      client.discordTogether
        .createTogetherCode(message.member.voice.channel.id, "fishing")
        .then(async (invite) => {
          const button = new Discord.MessageButton()
            .setStyle("LINK")
            .setURL(invite.code)
            .setLabel("Click me for Fishington.io!");
          const row = new Discord.MessageActionRow().addComponents([button]);
          return message.channel.send({
            content:
              "Click the below button to join the Fishington.io activity!",
            components: [row],
          });
        });
    }
  } else if (message.content === config_vars["prefix"] + "activity betrayal") {
    if (message.member.voice.channel) {
      client.discordTogether
        .createTogetherCode(message.member.voice.channel.id, "betrayal")
        .then(async (invite) => {
          const button = new Discord.MessageButton()
            .setStyle("LINK")
            .setURL(invite.code)
            .setLabel("Click me for Betrayal!");
          const row = new Discord.MessageActionRow().addComponents([button]);
          return message.channel.send({
            content: "Click the below button to join the Betrayal activity!",
            components: [row],
          });
        });
    }
  }
});

client.login(config_vars["discord_token"]);
