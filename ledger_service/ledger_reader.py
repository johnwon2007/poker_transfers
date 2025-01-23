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
    if not os.path.isfile(file_path):
        return None, f"The file path provided does not exist: {file_path}"
    
    try:
        df = pd.read_csv(file_path)
        # Sum buy-in, buy-out, stack, net values by player_id and handle the names
        grouped_df = df.groupby('player_id').agg(aggregations)
        # Convert player_nickname and net into a list of tuples
        id_nick_net = [(index, nickname, net) for index, nickname, net in zip(grouped_df.index, grouped_df['player_nickname'], grouped_df['net'])]
        return id_nick_net, None  # Return the data and no error
    except Exception as e:
        return None, f"An error occurred while processing the file: {e}"

# In your GUI part of the code, you would handle the error like this:
# data, error = process_csv('path_to_file.csv')
# if error:
#     showErrorDialog(error)
# else:
#     updateTableWithData(data)
