require('dotenv').config();

const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('tokusentai.db');
const Discord = require('discord.js');

var currentChannelIndex = 0;
var client;
var channels = [];

async function storeMessageHistory (before) {
    let lastMessage = null;
    let currentChannel = channels[currentChannelIndex];

    console.log('fetching message history...');

    if (!before) {
        before = await new Promise(resolve => {
            db.each('SELECT MIN(id) as id FROM messages', (err, res) => {
                if (err || !res) resolve(undefined);
                resolve(res.id);
            })
        });
    }

    if (before) console.log('before: ' + before);
    return (function () {
        if (before) return currentChannel.messages.fetch({ limit: 100, before: before });
        return currentChannel.messages.fetch({ limit: 100 });
    })()
    .then(history => {
        if (history.size === 0) {
            if (channels[currentChannelIndex + 1]) {
                currentChannelIndex += 1;
                return;
            } else {
                console.log('finished!');
                db.close();
                process.exit();
                return;
            }
        }
        console.log('messagehistory length: ' + history.size);

        let statement = db.prepare('INSERT INTO messages VALUES (?, ?, ?, ?, ?, ?, ?, ?)');
        history.forEach(message => {
            statement.run(
                message.id,
                message.content,
                message.author.id,
                message.author.username,
                currentChannel.id,
                message.createdTimestamp,
                message.content.length,
                0,
            );
            lastMessage = message;
        });

        statement.finalize();

        var fetchMore = true;

        console.log(`saved messages in the database`);
        if (fetchMore) {
            setTimeout(() => {
                storeMessageHistory(lastMessage.id);
            }, 500);
        }
    })
    .catch(console.error);
}

function run () {
    client = new Discord.Client()
    client.on('ready', () => {
        console.log(`Logged in as ${client.user.tag}!`)

        // channels = channels.concat(client.guilds.map(guild => guild.channels)).flat().flat();
        for (channel of client.channels.cache) {
            let channelId = channel[0];
            channel = channel[1];
            if (channel.type === 'text') {
                channels.push(channel);
            }
        }
        storeMessageHistory();
    })

    client.login(process.env.TOKEN)
}

run();
