from collections import defaultdict

def process_stripe_ledger(events: list[str]) -> dict[str, dict[str, int]]:
    if not events:
        return {}

    cleaned_events = []
    merchant_balance_holder = defaultdict(lambda: defaultdict(lambda: {"available": 0, "disputed": 0}))
    charge_history = defaultdict(list)
    merchant_refund_timelines = defaultdict(list)
    fraudulent_merchants = set()
    events_processed = set()

    for event in events:
        if not isinstance(event, str) or not event or not event.strip():
            continue

        parts = event.split(",")

        if len(parts) != 6:
            continue

        try:
            timestamp = int(parts[0])
            merchant_id = parts[1].strip()
            event_type = parts[2].strip()
            amount = int(parts[3])
            currency = parts[4].strip()
            transaction_id = parts[5].strip()

            cleaned_events.append((timestamp, merchant_id, event_type, amount, currency, transaction_id))

        except ValueError:
            continue

    cleaned_events.sort()

    for timestamp, merchant_id, event_type, amount, currency, transaction_id in cleaned_events:
        event_signature = (transaction_id, event_type, timestamp)
        if event_signature in events_processed or merchant_id in fraudulent_merchants:
            continue

        if event_type == "CHARGE" and amount > 0:
            merchant_balance_holder[merchant_id][currency]["available"] += amount
            charge_history[transaction_id] = [amount, 0]

        elif event_type == "REFUND_SETTLED":
            if transaction_id in charge_history:
                if not amount:
                    merchant_balance_holder[merchant_id][currency]["disputed"] -= charge_history[transaction_id][1]
                else:
                    merchant_balance_holder[merchant_id][currency]["disputed"] -= amount

        elif event_type == "REFUND_REQUEST" and amount > 0:

            cutoff_time = timestamp - 60
            fresh_window_timestamps = []
            
            for past_ts in merchant_refund_timelines[merchant_id]:
                if cutoff_time <= past_ts:
                    fresh_window_timestamps.append(past_ts)
                        
            merchant_refund_timelines[merchant_id] = fresh_window_timestamps
            
            if len(merchant_refund_timelines[merchant_id]) >= 3:
                fraudulent_merchants.add(merchant_id)
                continue

            

            if transaction_id not in charge_history:
                continue
            charge_amount, total_refunded = charge_history[transaction_id][0], charge_history[transaction_id][1]

            if total_refunded + amount > charge_amount: 
                continue

            merchant_balance_holder[merchant_id][currency]["available"] -= amount
            merchant_balance_holder[merchant_id][currency]["disputed"] += amount

            charge_history[transaction_id][1] += amount
            merchant_refund_timelines[merchant_id].append(timestamp)

        events_processed.add((transaction_id, event_type, timestamp))
            

    res = {}
    for merchant, currencies in merchant_balance_holder.items():
        res[merchant] = {}
        for currency, balances in currencies.items():
            res[merchant][currency] = {
                "available": balances["available"],
                "disputed": balances["disputed"]
            }

    return res


mock_stripe_stream = [
    "200,m_nike,CHARGE,10000,USD,tx_101",
    "210,m_nike,REFUND_REQUEST,3000,USD,tx_101",
    "220,m_nike,REFUND_REQUEST,4000,USD,tx_101",
    "230,m_nike,REFUND_REQUEST,4000,USD,tx_101",
    "190,m_nike,CHARGE,5000,EUR,tx_102",
    "240,m_nike,REFUND_SETTLED,0,USD,tx_101"
]

# Expected output structure:
# {"m_nike": {"EUR": {"available": 5000, "disputed": 0}, "USD": {"available": 3000, "disputed": 0}}}

print(process_stripe_ledger(mock_stripe_stream))
