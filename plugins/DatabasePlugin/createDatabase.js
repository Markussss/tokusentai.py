require('dotenv').config({
    path: '../../.env',
});

const Database = require('better-sqlite3');
const db = new Database(`../../${process.env.NAME}.db`, {verbose: console.log });

db.exec('DROP TABLE IF EXISTS "messages"');

db.exec(`
    CREATE TABLE IF NOT EXISTS "messages" (
        "id" TEXT NOT NULL UNIQUE,
        "message" TEXT,
        "author" TEXT NOT NULL,
        "username" TEXT,
        "channel" TEXT,
        "created_at" TEXT NOT NULL,
        "length" INTEGER,
        "ignore" INTEGER,
        "bot" INTEGER,
        PRIMARY KEY("id")
    )
`);

db.exec(`
    CREATE INDEX "author" ON "messages" ("author");
    CREATE INDEX "channel" ON "messages" ("channel");
    CREATE INDEX "length" ON "messages" ("length");
`);

db.close();