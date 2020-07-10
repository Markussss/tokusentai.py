require('dotenv').config({
    path: '../../.env',
});

const Database = require('better-sqlite3');
const db = new Database(`../../${process.env.NAME}.db`, { verbose: console.log });
const Discord = require('discord.js');

var currentChannelIndex = 0;
var client;
var channels = [];

const WAIT_TIME_BETWEEN_API_CALLS = 500;

async function storeMessageHistoryBefore(before) {
    let lastMessage = null;
    let currentChannel = channels[currentChannelIndex];

    console.log('fetching message history...');

    if (!before) {
        before = await new Promise(resolve => {
            let res = db.prepare('SELECT MIN(id) as id FROM messages WHERE channel = ?').get(currentChannel.id);
            if (!res) {
                resolve(undefined);
            }
            resolve(res.id);
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
                storeMessageHistoryBefore();
                return;
            } else {
                setTimeout(() => {
                    currentChannelIndex = 0;
                    storeMessageHistoryAfter();
                }, WAIT_TIME_BETWEEN_API_CALLS);
                return;
            }
        }
        console.log('messagehistory length: ' + history.size);

        const insert = db.prepare('INSERT INTO messages VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)');
        const insertMany = db.transaction((messages) => {
            for (const message of messages) insert.run(message);
        });
        insertMany(history.map(message => {
            lastMessage = message;
            return [
                message.id,
                message.content,
                message.author.id,
                message.author.username,
                currentChannel.id,
                message.createdTimestamp,
                message.content.length,
                message.author.bot |0,
                0,
            ];
        }));

        var fetchMore = true;

        console.log(`saved messages in the database`);
        if (fetchMore) {
            setTimeout(() => {
                storeMessageHistoryBefore(lastMessage.id);
            }, WAIT_TIME_BETWEEN_API_CALLS);
        }
    })
    .catch(error => {
        if (error.httpStatus === 403) {
            currentChannelIndex += 1;
            setTimeout(() => {
                storeMessageHistoryBefore();
            }, WAIT_TIME_BETWEEN_API_CALLS);
        }
    });
}
async function storeMessageHistoryAfter(after) {
    let lastMessage = null;
    let currentChannel = channels[currentChannelIndex];

    console.log('fetching message history...');

    if (!after) {
        after = await new Promise(resolve => {
            let res = db.prepare('SELECT max(id) as id FROM messages WHERE channel = ?').get(currentChannel.id);
            if (!res) {
                resolve(undefined);
            }
            resolve(res.id);
        });
    }

    if (after) console.log('after: ' + after);
    return (function () {
        if (after) return currentChannel.messages.fetch({ limit: 100, after: after });
        return currentChannel.messages.fetch({ limit: 100 });
    })()
    .then(history => {
        if (history.size === 0) {
            if (channels[currentChannelIndex + 1]) {
                currentChannelIndex += 1;
                storeMessageHistoryAfter();
                return;
            } else {
                console.log('finished!');
                db.close();
                process.exit();
                return;
            }
        }
        console.log('messagehistory length: ' + history.size);

        const insert = db.prepare('INSERT INTO messages VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT IGNORE');
        const insertMany = db.transaction((messages) => {
            for (const message of messages) insert.run(message);
        });
        insertMany(history.map(message => {
            lastMessage = message;
            return [
                message.id,
                message.content,
                message.author.id,
                message.author.username,
                currentChannel.id,
                message.createdTimestamp,
                message.content.length,
                message.author.bot |0,
                0,
            ];
        }));
        console.log(lastMessage);

        var fetchMore = true;

        console.log(`saved messages in the database`);
        if (fetchMore) {
            setTimeout(() => {
                storeMessageHistoryAfter(lastMessage.id);
            }, WAIT_TIME_BETWEEN_API_CALLS);
        }
    })
    .catch(error => {
        if (error.httpStatus === 403) {
            currentChannelIndex += 1;
            setTimeout(() => {
                storeMessageHistoryAfter();
            }, WAIT_TIME_BETWEEN_API_CALLS);
        }
    });
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
        storeMessageHistoryBefore();
    })

    client.login(process.env.TOKEN)
}

run();
