logs = [
    "merchant_A:tx_01:500:2",
    "merchant_B:tx_02:300:5",
    "merchant_A:tx_03:-50:1",
    "merchant_A:tx_04:200:4"
]

def calculate_locked_payouts(logs, target_day):
    prepared_dict = {}
    running_balances = {}
    output = []
    locked_merchants = set()

    def negbal_check(amount_str, merchant_ID):
        if amount_str < 0:
            locked_merchants.append(merchant_ID)

    for log in logs:
        merchant_ID, transaction_ID, amount_str, days_until = log.split(":")
        amount_str = int(amount_str)
        days_until = int(days_until)

        if merchant_ID in locked_merchants:
            continue

        if merchant_ID in running_balances:
            running_balances[merchant_ID] += amount_str
        else:
            running_balances[merchant_ID] = amount_str

        if running_balances[merchant_ID] < 0:
            locked_merchants.add(merchant_ID)
            continue

        if amount_str > 0 and days_until > 0 and days_until <= target_day:
            if merchant_ID in prepared_dict:
                prepared_dict[merchant_ID] += amount_str
            else:
                prepared_dict[merchant_ID] = amount_str


    for merchant_ID in sorted(prepared_dict.keys()):
        output.append(f"{merchant_ID}:{prepared_dict[merchant_ID]}")
    return output

print(calculate_locked_payouts(logs, 5))