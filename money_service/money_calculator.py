def calculate_minimal_transfers(id_nick_net):
    """
    Return the list of transfers to be made with amount, or an error message if applicable.
    Input
    [(1, "name1", 10000), (2, "name2", -10000)]
    
    Output
    (transfers, error)
    Where transfers might be [("name2", "name1", 10000)] and error is None if successful,
    or transfers is None and error is a descriptive string if an error occurs.
    """
    
    # Check if the total balance sum is 0
    total = sum(net for _, _, net in id_nick_net)
    if total != 0:
        return None, f"Error: The total balance sum is not 0. Current sum: {total}"

    # Separate positive (credit) and negative (debit) balances
    positive_balances = [(nickname, net) for _, nickname, net in id_nick_net if net > 0]
    negative_balances = [(nickname, -net) for _, nickname, net in id_nick_net if net < 0]

    transfers = []  # Store the final transfer details

    try:
        while positive_balances and negative_balances:
            # Sort positive and negative balances (process the largest amounts first)
            positive_balances.sort(key=lambda x: -x[1])
            negative_balances.sort(key=lambda x: -x[1])

            matched = False

            # Match amounts that are exactly the same first
            for i, (pos_nickname, pos_amount) in enumerate(positive_balances):
                for j, (neg_nickname, neg_amount) in enumerate(negative_balances):
                    if pos_amount == neg_amount:
                        transfers.append((neg_nickname, pos_nickname, neg_amount))
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
            pos_nickname, pos_amount = positive_balances[0]
            neg_nickname, neg_amount = negative_balances[0]
            transfer_amount = min(pos_amount, neg_amount)
            transfers.append((neg_nickname, pos_nickname, transfer_amount))

            # Update balances
            if pos_amount > transfer_amount:
                positive_balances[0] = (pos_nickname, pos_amount - transfer_amount)
            else:
                positive_balances.pop(0)

            if neg_amount > transfer_amount:
                negative_balances[0] = (neg_nickname, neg_amount - transfer_amount)
            else:
                negative_balances.pop(0)
        
        return transfers, None
    except Exception as e:
        return None, f"An unexpected error occurred: {str(e)}"
