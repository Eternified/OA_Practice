from collections import defaultdict

def process_settlements(events: list[str]) -> dict[str, dict[str, int]]:
    if not events:
        return {}

    merchants_holder = defaultdict(dict)
    seen_tokens = set()
    cleaned_events = []

    for event in events:
        if not event or not event.strip():
            continue
        
        parts = event.split(",")
        if len(parts) != 6:
            continue  

        timestamp = int(parts[0])
        merchant_id = parts[1].strip()
        event_type = parts[2].strip()
        amount = int(parts[3])
        currency = parts[4].strip()
        transfer_token = parts[5].strip()

        cleaned_events.append((timestamp, merchant_id, event_type, amount, currency, transfer_token))

    cleaned_events.sort()

    for timestamp, merchant_id, event_type, amount, currency, transfer_token in cleaned_events:
        
        if transfer_token in seen_tokens:
            continue
        seen_tokens.add(transfer_token)

        if event_type == "INBOUND":
            merchants_holder[merchant_id][currency] = merchants_holder[merchant_id].get(currency, 0) + amount
        elif event_type in ("PAYOUT", "REFUND"):
            merchants_holder[merchant_id][currency] = merchants_holder[merchant_id].get(currency, 0) - amount

    
    return dict(merchants_holder)

events_p1 = [
    "200,m_01,INBOUND,5000,USD,tok_1",
    "210,m_01,PAYOUT,2000,USD,tok_2",
    "200,m_01,INBOUND,5000,USD,tok_1", 
    "190,m_01,INBOUND,3000,EUR,tok_3"  
]

print(process_settlements(events_p1)
