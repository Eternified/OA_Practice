mock_payouts = [
    {"id": "po_1", "type": "payout", "status": "failed", "amount": 500, "merchant_id": "acct_A"},
    {"id": "po_2", "type": "payout", "status": "success", "amount": 1200, "merchant_id": "acct_B"}, # Skip: successful
    {"id": "po_3", "type": "charge", "status": "failed", "amount": 100, "merchant_id": "acct_A"},  # Skip: type is charge, not payout
    {"id": "po_4", "type": "payout", "status": "failed", "amount": 300, "merchant_id": "acct_A"},  # Add to acct_A (total 800)
    {"id": "po_5", "type": "payout", "status": "failed", "amount": 400, "merchant_id": "acct_C"},
    {"id": "po_6", "type": "payout", "status": "failed", "amount": None, "merchant_id": "acct_B"}, # Skip: missing amount
    None                                                                                          # Skip: Null log
]


def audit_failed_payouts(payout_logs):
    if not payout_logs:
        return {}

    failed_payouts = {}

    for payout in payout_logs:
        if payout is None:
            continue

        payout_type = payout.get("type")
        status = payout.get("status")
        amount = payout.get("amount")
        merchant_id = payout.get("merchant_id")

        if amount is None or merchant_id is None:
            continue
        
        if status == "failed" and payout_type == "payout":
            failed_payouts[merchant_id] = failed_payouts.get(merchant_id, 0) + amount

    return failed_payouts

print(audit_failed_payouts(mock_payouts))