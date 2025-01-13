from ledger_service.ledger_reader import process_csv as pc
from money_service.money_calculator import calculate_minimal_transfers as cmt

def ledger_tranfer_calculator(file_path):
    balances = pc(file_path)
    return cmt(balances)
if __name__ == "__main__":
    ledger_tranfer_calculator('/Users/johnwon/Desktop/Projects/poker_money/ledger_service/ledger_test.csv')