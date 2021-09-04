const Discord = require("discord.js");
const client = new Discord.Client({
  intents: [
    Discord.Intents.FLAGS.GUILDS,
    Discord.Intents.FLAGS.GUILD_MESSAGES,
    Discord.Intents.FLAGS.GUILD_VOICE_STATES,
  ],
});
const { DiscordTogether } = require("discord-together");
const fs = require("fs");
var request = require("request-promise");

let rawdata = fs.readFileSync("config.json");
let config_vars = JSON.parse(rawdata);

const slash_command_data = {
  name: "activity",
  description: "Starts a new activity in your voice channel!",
  options: [
    {
      name: "activity_name",
      type: "STRING",
      description: "The activity you want to start",
      required: true,
      choices: [
        {
          name: "Chess",
          value: "chess",
        },
        {
          name: "Poker",
          value: "poker",
        },
        {
          name: "Youtube",
          value: "youtube",
        },
        {
          name: "Betrayal.io",
          value: "betrayal",
        },
        {
          name: "Fishington.io",
          value: "fishing",
        },
      ],
    },
  ],
};

client.on("ready", async () => {
  setTimeout(async () => {
    await client.application?.commands.create(slash_command_data);
  }, 10000);
  console.log("Activity commands loaded");
});

client.discordTogether = new DiscordTogether(client);

client.on("interactionCreate", async (interaction) => {
  if (!interaction.isCommand()) return;

  if (interaction.commandName === "activity") {
    const activity_name = interaction.options.get("activity_name")["value"];
    client.channels.cache
      .get(config_vars["log-channel"])
      .send(
        "[Slash] " +
          interaction.guild.name +
          " > " +
          interaction.member.user.tag +
          " > activity " +
          activity_name
      );
    if (interaction.member.voice.channel) {
      await interaction.reply("Hold on a sec, making the invite..");
      if (activity_name === "youtube") {
        client.discordTogether
          .createTogetherCode(interaction.member.voice.channel.id, "youtube")
          .then(async (invite) => {
            const button = new Discord.MessageButton()
              .setStyle("LINK")
              .setURL(invite.code)
              .setLabel("Click me for Youtube Together!");
            const row = new Discord.MessageActionRow().addComponents([button]);
            await interaction.editReply({
              content:
                "Click the below button to join the Youtube Together activity!",
              components: [row],
            });
          });
      } else if (activity_name === "poker") {
        client.discordTogether
          .createTogetherCode(interaction.member.voice.channel.id, "poker")
          .then(async (invite) => {
            const button = new Discord.MessageButton()
              .setStyle("LINK")
              .setURL(invite.code)
              .setLabel("Click me for Poker Night!");
            const row = new Discord.MessageActionRow().addComponents([button]);
            await interaction.editReply({
              content:
                "Click the below button to join the Poker Night activity!",
              components: [row],
            });
          });
      } else if (activity_name === "chess") {
        client.discordTogether
          .createTogetherCode(interaction.member.voice.channel.id, "chess")
          .then(async (invite) => {
            const button = new Discord.MessageButton()
              .setStyle("LINK")
              .setURL(invite.code)
              .setLabel("Click me for Chess in the park!");
            const row = new Discord.MessageActionRow().addComponents([button]);
            await interaction.editReply({
              content:
                "Click the below button to join the Chess in the park activity!",
              components: [row],
            });
          });
      } else if (activity_name === "fishing") {
        client.discordTogether
          .createTogetherCode(interaction.member.voice.channel.id, "fishing")
          .then(async (invite) => {
            const button = new Discord.MessageButton()
              .setStyle("LINK")
              .setURL(invite.code)
              .setLabel("Click me for Fishington.io!");
            const row = new Discord.MessageActionRow().addComponents([button]);
            await interaction.editReply({
              content:
                "Click the below button to join the Fishington.io activity!",
              components: [row],
            });
          });
      } else if (activity_name === "betrayal") {
        client.discordTogether
          .createTogetherCode(interaction.member.voice.channel.id, "betrayal")
          .then(async (invite) => {
            const button = new Discord.MessageButton()
              .setStyle("LINK")
              .setURL(invite.code)
              .setLabel("Click me for Betrayal!");
            const row = new Discord.MessageActionRow().addComponents([button]);
            await interaction.editReply({
              content: "Click the below button to join the Betrayal activity!",
              components: [row],
            });
          });
      }
    } else {
      await interaction.reply("You aren't in a voice channel!");
    }
  }
});

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
