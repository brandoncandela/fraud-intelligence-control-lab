PRAGMA foreign_keys = ON;
CREATE TABLE accounts(account_id TEXT PRIMARY KEY, customer_name TEXT NOT NULL, segment TEXT NOT NULL, country TEXT NOT NULL, opened_at TEXT NOT NULL, is_employee INTEGER NOT NULL CHECK(is_employee IN (0,1)));
CREATE TABLE devices(device_id TEXT PRIMARY KEY, platform TEXT NOT NULL, country TEXT NOT NULL, first_seen_at TEXT NOT NULL);
CREATE TABLE account_devices(account_id TEXT NOT NULL REFERENCES accounts(account_id), device_id TEXT NOT NULL REFERENCES devices(device_id), linked_at TEXT NOT NULL, PRIMARY KEY(account_id,device_id));
CREATE TABLE transactions(transaction_id TEXT PRIMARY KEY, account_id TEXT NOT NULL REFERENCES accounts(account_id), counterparty_id TEXT NOT NULL, direction TEXT NOT NULL CHECK(direction IN ('in','out')), amount REAL NOT NULL CHECK(amount>0), currency TEXT NOT NULL, device_id TEXT NOT NULL REFERENCES devices(device_id), occurred_at TEXT NOT NULL);
CREATE TABLE labels(account_id TEXT PRIMARY KEY REFERENCES accounts(account_id), outcome TEXT NOT NULL CHECK(outcome IN ('benign','review_worthy')));
CREATE INDEX idx_tx_account_time ON transactions(account_id,occurred_at);
CREATE INDEX idx_tx_device_time ON transactions(device_id,occurred_at);
CREATE INDEX idx_links_device ON account_devices(device_id,account_id);
