mock_transactions = [
    {"id": "tx_1", "status": "success", "amount": 100, "currency": "USD"},
    {"id": "tx_2", "status": "success", "amount": 50, "currency": "EUR"},
    {"id": "tx_3", "status": "failed", "amount": 200, "currency": "USD"},   # Ignore: failed
    {"id": "tx_4", "status": "success", "amount": 30, "currency": "USD"},
    {"id": "tx_5", "status": "success", "amount": 80, "currency": "EUR"},
    {"id": "tx_6", "status": "success", "amount": 40},                      # No currency key! Default to "USD"
    {"id": "tx_7", "status": "success", "amount": None, "currency": "GBP"}, # Ignore: amount is None
    None,                                                                   # Ignore: transaction is Null
    {"id": "tx_8", "status": "success", "amount": 60, "currency": "GBP"}
]


def calculate_revenue_by_currency(transactions):
    if not transactions:
        return {}

    successful_sums = {}

    for transaction in transactions:
        if transaction == None:
            continue


        status = transaction.get("status")
        amount = transaction.get("amount")
        currency = transaction.get("currency") or "USD"

        if amount is not None and status == "success":
            successful_sums[currency] = successful_sums.get(currency, 0) + amount
            
    return successful_sums


print(calculate_revenue_by_currency(mock_transactions))