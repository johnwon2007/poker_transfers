from ledger_service.ledger_reader import process_csv as pc
from money_service.money_calculator import calculate_minimal_transfers as cmt

def ledger_tranfer_calculator(file_path):
    balances, id_nick_net = pc(file_path)
    transactions = cmt(balances)
    return transactions, id_nick_net
if __name__ == "__main__":
    ledger_tranfer_calculator('/Users/johnwon/Desktop/Projects/poker_money/ledger_service/ledger_test.csv')