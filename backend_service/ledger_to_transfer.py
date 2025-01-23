from ledger_service.ledger_reader import process_csv as pc
from money_service.money_calculator import calculate_minimal_transfers as cmt

def ledger_tranfer_calculator(file_path):
    id_nick_net, error_msg1 = pc(file_path)
    if error_msg1:
        return None, None, error_msg1
    transactions, error_msg2 = cmt(id_nick_net)
    if error_msg2:
        return None, None, error_msg2
    return transactions, id_nick_net, None