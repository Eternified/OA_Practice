from collections import defaultdict

def arbitrate_disputes(events: list[str]) -> dict[str, int]:
    if not events:
        return {}

    merchant_balances = defaultdict(int)
    cleaned_events = []
    dispute_registry = defaultdict(int)

    for event in mock_events:

        if not isinstance(event, str) or not event or not event.strip():
            continue

        parts = event.split(",")

        if len(parts) != 5:
            continue

        try:
            timestamp = int(parts[0])
            merchant_id = parts[1].strip()
            event_type = parts[2].strip()
            amount = int(parts[3])
            dispute_id = parts[4].strip()

            cleaned_events.append((timestamp, merchant_id, event_type, amount, dispute_id))
        except ValueError:
            continue

    cleaned_events.sort()

    for timestamp, merchant_id, event_type, amount, dispute_id in cleaned_events:
        if event_type == "REVENUE_INBOUND" and amount > 0:
            merchant_balances[merchant_id] += amount

        elif event_type == "DISPUTE_LODGED" and amount > 0:
            merchant_balances[merchant_id] -= amount

            dispute_registry[dispute_id] = amount
            
        elif event_type == "DISPUTE_REVERSED":
            if dispute_id not in dispute_registry: continue

            if not amount:
                merchant_balances[merchant_id] += dispute_registry[dispute_id]
            else:
                merchant_balances[merchant_id] += amount

    return dict(merchant_balances)


mock_events = [
    "200,merch_abc,DISPUTE_LODGED,4000,disp_11",
    "220,merch_abc,DISPUTE_REVERSED,0,disp_11",
    "190,merch_abc,REVENUE_INBOUND,5000,disp_none",
    "210,merch_abc,DISPUTE_REVERSED,3000,disp_99"
]

# Expected output: {"merch_abc": 5000}

print(arbitrate_disputes(mock_events))
