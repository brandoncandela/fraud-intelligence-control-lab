WITH device_peers AS (
  SELECT ad.account_id, COUNT(DISTINCT peer.account_id) - 1 AS shared_device_peers
  FROM account_devices ad
  JOIN account_devices peer ON peer.device_id = ad.device_id
  GROUP BY ad.account_id
),
daily_inbound AS (
  SELECT account_id, date(occurred_at) AS activity_date,
         COUNT(DISTINCT counterparty_id) AS senders
  FROM transactions WHERE direction = 'in'
  GROUP BY account_id, date(occurred_at)
),
max_senders AS (
  SELECT account_id, MAX(senders) AS distinct_in_senders_24h
  FROM daily_inbound GROUP BY account_id
),
rapid_out AS (
  SELECT o.account_id, COALESCE(SUM(o.amount),0) AS rapid_outbound_amount
  FROM transactions o
  WHERE o.direction='out' AND EXISTS (
    SELECT 1 FROM transactions i
    WHERE i.account_id=o.account_id AND i.direction='in'
      AND i.occurred_at BETWEEN datetime(o.occurred_at,'-60 minutes') AND o.occurred_at
  ) GROUP BY o.account_id
),
new_foreign AS (
  SELECT t.account_id, COALESCE(SUM(t.amount),0) AS new_foreign_device_amount
  FROM transactions t JOIN devices d ON d.device_id=t.device_id JOIN accounts a ON a.account_id=t.account_id
  WHERE t.direction='out' AND d.country<>a.country
    AND julianday(t.occurred_at)-julianday(d.first_seen_at) <= 2
  GROUP BY t.account_id
)
SELECT a.account_id,a.customer_name,a.segment,l.outcome,
       COALESCE(dp.shared_device_peers,0) AS shared_device_peers,
       COALESCE(ms.distinct_in_senders_24h,0) AS distinct_in_senders_24h,
       ROUND(COALESCE(ro.rapid_outbound_amount,0),2) AS rapid_outbound_amount,
       ROUND(COALESCE(nf.new_foreign_device_amount,0),2) AS new_foreign_device_amount
FROM accounts a JOIN labels l USING(account_id)
LEFT JOIN device_peers dp USING(account_id)
LEFT JOIN max_senders ms USING(account_id)
LEFT JOIN rapid_out ro USING(account_id)
LEFT JOIN new_foreign nf USING(account_id)
ORDER BY a.account_id;
