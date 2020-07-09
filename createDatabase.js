const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('tokusentai.db');

db.run(`CREATE TABLE IF NOT EXISTS "messages" (
    "id" TEXT NOT NULL UNIQUE,
    "message" TEXT,
    "author" TEXT NOT NULL,
    "username" TEXT,
    "channel" TEXT,
    "created_at" TEXT NOT NULL,
    "length" INTEGER,
    "ignore" INTEGER,
    PRIMARY KEY("id"))
`, (result, err) => {
    if (err) throw err;
    db.run('CREATE INDEX "author" ON "messages" ("author");',
    (result, err) => {
        if (err) throw err;
        db.run('CREATE INDEX "channel" ON "messages" ("channel");',
        (result, err) => {
            if (err) throw err;
            db.run('CREATE INDEX "length" ON "messages" ("length");');
        });
    });
});