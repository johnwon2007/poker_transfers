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
            #balances = dict(zip(grouped_df['player_nickname'], grouped_df['net']))
            id_nick_net = [(index, nickname, net) for index, nickname, net in zip(grouped_df.index, grouped_df['player_nickname'], grouped_df['net'])]
            print(id_nick_net)
            return id_nick_net
        except Exception as e:
            print(f"An error occurred while processing the file: {e}")
    else:
        print(f"The file path provided does not exist: {file_path}")
