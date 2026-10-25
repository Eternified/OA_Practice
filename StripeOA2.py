events = [
    "cust_A:START:50",
    "cust_B:START:120",
    "cust_A:CANCEL:0",
    "cust_C:START:200"
]

def process_subscription_stream(events):
    validCusts = {}
    blocked_customers = set()
    last_id = "None"
    last_action = "None"

    for event in events:
        if event == "":
            continue

        customer_id, action, mrr_amount = event.split(":")


        if customer_id in blocked_customers:
            continue

        mrr_amount = int(mrr_amount)

        if last_id == customer_id and last_action == "START" and action == "CANCEL":
            blocked_customers.add(customer_id)
            validCusts.pop(customer_id, None)

            last_action = action
            last_id = customer_id
            continue


        if action == "START" and mrr_amount > 0:
            if customer_id not in validCusts:
                validCusts[customer_id] = mrr_amount
        elif action == "CANCEL" and mrr_amount == 0:
            validCusts.pop(customer_id, None)

        
        last_action = action
        last_id = customer_id
    return validCusts

print(process_subscription_stream(events))