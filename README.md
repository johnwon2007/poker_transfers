# Pokalculator

## Overview
Pokalculator is a simple tool that helps users automatically calculate payouts for their private games on [PokerNow](https://www.pokernow.club). After downloading the ledger (CSV file) from PokerNow, users can upload it to the program, which then computes how much each player should transfer to settle the game fairly. The tool also offers an offline mode where users can manually enter player details, and it will calculate the transactions accordingly.

## Features
- **Automated Balance Calculation**: Upload your PokerNow ledger file, and the program determines who owes whom and how much.
- **Online & Offline Modes**:
  - **Online Mode**: Uses the PokerNow ledger downloaded from the website.
  - **Offline Mode**: Manually enter player names, buy-ins, and buy-outs to calculate settlements.
- **Simple and Fast**: No manual calculations required. The tool does everything for you in seconds.
- **CSV Processing**: Parses PokerNow's CSV ledger to extract relevant data and compute net balances.

## Requirements
- Windows or Mac OS (separate `.exe` and `.dmg` files available)
- [PokerNow](https://www.pokernow.club) ledger file in CSV format (for online mode)

## Installation
1. Download the appropriate version of the tool:
   - **Windows**: `Pokalculator.exe`
     - build code in windows
     - pyinstaller --windowed --icon="img/logo.ico" pokalculator.py
   - **Mac**: `Pokalculator.dmg`
     - build code in mac
     - pyinstaller --icon="img/logo.icns" pokalculator.py
  - The exe or dmg file will be saved under dist folder
  - You can learn more about from https://pyinstaller.org/en/stable/
2. Save it in a location of your choice.
3. Ensure you have a PokerNow ledger CSV file ready for processing (if using online mode).

## How to Use
1. Play your PokerNow game and download the ledger (CSV file) after the session ends.
2. Open `Pokalculator`.
3. Choose between **Online Mode** and **Offline Mode**:
   - **Online Mode**: Click on **Upload Ledger** and select your CSV file.
   - **Offline Mode**: Click on the **Offline** tab, enter player names, buy-ins, and buy-outs manually.
4. The tool will automatically process the ledger or manual entries and display how much each player should transfer to settle the game.
5. Make the necessary transfers based on the calculations provided.

## How It Works
- The program is built using **Python** and **pandas**.
- In **Online Mode**, it reads the CSV file, extracts player balances, and determines the optimal transactions needed to settle the game efficiently.
- In **Offline Mode**, users manually enter player details, and the tool calculates the net balances and transactions accordingly.
- It ensures the minimum number of transactions to balance all players.

## Example Output
If three players played a game:
```
Alice: +$50
Bob: -$30
Charlie: -$20
```
The tool will suggest:
- Bob pays $30 to Alice.
- Charlie pays $20 to Alice.

## Troubleshooting
- **Invalid CSV Format**: Ensure you're uploading the correct PokerNow ledger CSV file.
- **Incorrect Balances**: Double-check that the ledger includes all hands played.
- **Program Not Opening**: Try running as administrator or re-downloading the correct version for your OS.

## Future Improvements
- Add support for different file formats (e.g., Excel `.xlsx`)
- Provide a GUI interface for better user experience
- Implement a web-based version for easier access

## Contributing
If you'd like to improve the tool, feel free to reach out or fork the project.

## License
This project is licensed under the MIT License.

## Contact
For issues or suggestions, feel free to reach out at: [Your Email or GitHub]

---

Enjoy your Poker games and let **Pokalculator** handle the math for you!

