def calculate_minimal_transfers(balances: dict):
    """
    Return the list of tranfers to be made with amount
    Input
    {"name1": 10000, "name2": -10000}
    
    Output
    [('name2', 'name1', 10000)]
    """
    
    
    # Check if the total balance sum is 0
    total = sum(balances.values())
    if total != 0:
        raise ValueError(f"Error: The total balance sum is not 0. Current sum: {total}")

    # Separate positive (credit) and negative (debit) balances
    positive_balances = [(name, amount) for name, amount in balances.items() if amount > 0]
    negative_balances = [(name, -amount) for name, amount in balances.items() if amount < 0]

    transfers = []  # Store the final transfer details

    while positive_balances and negative_balances:
        # Sort positive and negative balances (process the largest amounts first)
        positive_balances.sort(key=lambda x: -x[1])
        negative_balances.sort(key=lambda x: -x[1])

        matched = False

        # Match amounts that are exactly the same first
        for i, (pos_name, pos_amount) in enumerate(positive_balances):
            for j, (neg_name, neg_amount) in enumerate(negative_balances):
                if pos_amount == neg_amount:
                    transfers.append((neg_name, pos_name, neg_amount))
                    positive_balances.pop(i)
                    negative_balances.pop(j)
                    matched = True
                    break
            if matched:
                break

        # If a match was found, recheck the lists
        if matched:
            continue

        # If amounts are different, match the smaller amount
        pos_name, pos_amount = positive_balances[0]
        neg_name, neg_amount = negative_balances[0]
        transfer_amount = min(pos_amount, neg_amount)
        transfers.append((neg_name, pos_name, transfer_amount))

        # Update balances
        if pos_amount > transfer_amount:
            positive_balances[0] = (pos_name, pos_amount - transfer_amount)
        else:
            positive_balances.pop(0)

        if neg_amount > transfer_amount:
            negative_balances[0] = (neg_name, neg_amount - transfer_amount)
        else:
            negative_balances.pop(0)

    return transfers