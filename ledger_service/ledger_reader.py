import pandas as pd
import os

# Custom aggregation for nicknames
def unique_nicknames(series):
    return ', '.join(series.unique())

# Custom aggregation dictionary
aggregations = {
    'player_nickname': unique_nicknames,  # Applying the custom function for nicknames
    'net': 'sum'
}

def process_csv(file_path):
    if os.path.isfile(file_path):
        try:
            df = pd.read_csv(file_path)
            # sum buy-in, buy-out, stack, net values by player_id and somehow handle the names
            grouped_df = df.groupby('player_id').agg(aggregations)
            # Convert player_nickname and net into a dictionary
            result = dict(zip(grouped_df['player_nickname'], grouped_df['net']))
            print(result)
            return result
        except Exception as e:
            print(f"An error occurred while processing the file: {e}")
    else:
        print(f"The file path provided does not exist: {file_path}")

if __name__ == '__main__':
    process_csv('/Users/johnwon/Desktop/Projects/poker_money/ledger_service/ledger_test.csv')
