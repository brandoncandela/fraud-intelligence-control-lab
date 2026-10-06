"""Create a deterministic, synthetic fraud-intelligence dataset and dashboard export."""
from __future__ import annotations

import csv
import json
import random
import sqlite3
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "dist" / "data"
DB = DATA / "lab.sqlite"
RNG = random.Random(20261006)
START = datetime(2026, 8, 1, tzinfo=timezone.utc)


def iso(dt: datetime) -> str:
    return dt.isoformat().replace("+00:00", "Z")


def build() -> dict:
    DATA.mkdir(parents=True, exist_ok=True)
    if DB.exists():
        DB.unlink()
    con = sqlite3.connect(DB)
    con.executescript((ROOT / "sql" / "schema.sql").read_text())

    accounts = []
    devices = []
    links = []
    transactions = []
    labels = {}
    industries = ["marketplace", "creator", "retail", "professional_services"]

    for i in range(1, 61):
        account_id = f"A{i:03d}"
        labels[account_id] = "benign"
        accounts.append((account_id, f"Synthetic Customer {i:03d}", industries[i % 4], "US", iso(START - timedelta(days=60 + i)), 0))
        device_id = f"D{i:03d}"
        devices.append((device_id, "ios" if i % 2 else "web", "US", iso(START - timedelta(days=30 + i))))
        links.append((account_id, device_id, iso(START - timedelta(days=20))))

    # A connected mule-style cluster. Labels are synthetic ground truth for evaluation only.
    ring_accounts = ["A006", "A012", "A018", "A024", "A030"]
    for account_id in ring_accounts:
        labels[account_id] = "review_worthy"
        links.append((account_id, "D900", iso(START + timedelta(days=18))))
    devices.append(("D900", "web", "US", iso(START + timedelta(days=18))))

    # Benign lookalikes make threshold tuning non-trivial: a shared household
    # device and a marketplace seller receiving from many buyers.
    devices.append(("D833", "ios", "US", iso(START - timedelta(days=45))))
    links.extend([
        ("A033", "D833", iso(START - timedelta(days=40))),
        ("A034", "D833", iso(START - timedelta(days=40))),
    ])

    # Two account-takeover patterns using new foreign devices.
    for account_id, device_id, country in [("A041", "D941", "GB"), ("A052", "D952", "RO")]:
        labels[account_id] = "review_worthy"
        devices.append((device_id, "web", country, iso(START + timedelta(days=24))))
        links.append((account_id, device_id, iso(START + timedelta(days=24))))

    tx_no = 1
    for day in range(31):
        for i in range(1, 61):
            account_id = f"A{i:03d}"
            count = 1 + (i + day) % 3
            for n in range(count):
                direction = "in" if (i + day + n) % 2 else "out"
                amount = round(25 + RNG.random() * 425, 2)
                counterparty = f"CP{((i * 13 + day * 7 + n) % 120) + 1:03d}"
                device_id = f"D{i:03d}"
                timestamp = START + timedelta(days=day, hours=8 + (i % 10), minutes=n * 11)
                transactions.append((f"T{tx_no:05d}", account_id, counterparty, direction, amount, "USD", device_id, iso(timestamp)))
                tx_no += 1

    # Fan-in followed by rapid cash-out across the linked cluster.
    for offset, account_id in enumerate(ring_accounts):
        event = START + timedelta(days=20, hours=14, minutes=offset * 3)
        for sender in range(7):
            transactions.append((f"T{tx_no:05d}", account_id, f"R{offset}{sender}", "in", 900 + sender * 17, "USD", "D900", iso(event + timedelta(minutes=sender))))
            tx_no += 1
        transactions.append((f"T{tx_no:05d}", account_id, "CP-CASHOUT", "out", 6200 + offset * 50, "USD", "D900", iso(event + timedelta(minutes=31))))
        tx_no += 1

    # Large outbound payments immediately after first seen on a foreign device.
    for idx, (account_id, device_id) in enumerate([("A041", "D941"), ("A052", "D952")]):
        event = START + timedelta(days=24 + idx, hours=3)
        transactions.append((f"T{tx_no:05d}", account_id, "CP-NEW-PAYEE", "out", 8400 + idx * 2100, "USD", device_id, iso(event)))
        tx_no += 1

    # Legitimate marketplace settlement: fan-in and same-day supplier payout.
    merchant_event = START + timedelta(days=21, hours=10)
    for sender in range(8):
        transactions.append((f"T{tx_no:05d}", "A015", f"BUYER{sender:02d}", "in", 430 + sender * 22, "USD", "D015", iso(merchant_event + timedelta(minutes=sender * 4))))
        tx_no += 1
    transactions.append((f"T{tx_no:05d}", "A015", "SUPPLIER-SETTLEMENT", "out", 3900, "USD", "D015", iso(merchant_event + timedelta(minutes=47))))
    tx_no += 1

    con.executemany("INSERT INTO accounts VALUES (?,?,?,?,?,?)", accounts)
    con.executemany("INSERT INTO devices VALUES (?,?,?,?)", devices)
    con.executemany("INSERT INTO account_devices VALUES (?,?,?)", links)
    con.executemany("INSERT INTO transactions VALUES (?,?,?,?,?,?,?,?)", transactions)
    con.executemany("INSERT INTO labels VALUES (?,?)", labels.items())
    con.commit()

    rows = con.execute((ROOT / "sql" / "account_features.sql").read_text()).fetchall()
    columns = [d[0] for d in con.execute((ROOT / "sql" / "account_features.sql").read_text()).description]
    features = [dict(zip(columns, row)) for row in rows]
    for row in features:
        row["risk_score"] = min(100, round(
            row["shared_device_peers"] * 12
            + row["distinct_in_senders_24h"] * 4
            + row["rapid_outbound_amount"] / 500
            + row["new_foreign_device_amount"] / 350
        ))

    weeks = []
    for week in range(1, 5):
        volume = con.execute("SELECT COUNT(*) FROM transactions WHERE occurred_at >= ? AND occurred_at < ?", (iso(START + timedelta(days=(week - 1) * 7)), iso(START + timedelta(days=week * 7)))).fetchone()[0]
        weeks.append({"week": f"W{week}", "transactions": volume, "alert_rate": round((0.017 + week * 0.004) * 100, 1), "data_quality": 99.8 if week < 4 else 98.9})

    export = {
        "generated_at": iso(datetime.now(timezone.utc)),
        "method": "Deterministic synthetic data; rules and labels are educational examples.",
        "accounts": features,
        "weeks": weeks,
        "links": [{"source": a, "target": d} for a, d, _ in links if d == "D900"],
        "totals": {"accounts": len(accounts), "transactions": len(transactions), "devices": len(devices), "review_worthy": sum(v == "review_worthy" for v in labels.values())},
    }
    (DATA / "dashboard.json").write_text(json.dumps(export, indent=2))
    with (DATA / "account_features.csv").open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=features[0].keys())
        writer.writeheader(); writer.writerows(features)
    con.close()
    return export


if __name__ == "__main__":
    summary = build()["totals"]
    print(json.dumps(summary))
