from PyQt5 import QtWidgets, QtCore
from backend_service.ledger_to_transfer import ledger_tranfer_calculator as ltc
from money_service.money_calculator import calculate_minimal_transfers as cmt

class OfflineWidget(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.resize(400, 300)
        self.main_window = main_window
        self.layout = QtWidgets.QVBoxLayout(self)
        self.table = QtWidgets.QTableWidget(0, 5)
        width_adjuster = 20
        self.table.setHorizontalHeaderLabels([" " * width_adjuster + "ID" + " " * width_adjuster, 
                                              " " * width_adjuster + "Nickname" + " " * width_adjuster , 
                                              " " * width_adjuster + "Buy-in" + " " * width_adjuster, 
                                              " " * width_adjuster + "Buy-out" + " " * width_adjuster, 
                                              " " * width_adjuster + "Net" + " " * width_adjuster])
        #self.table.horizontalHeader().setStretchLastSection(True)
        # Optionally resize based on content
        self.layout.addWidget(self.table)

        self.add_row_button = QtWidgets.QPushButton("Add New Row")
        self.add_row_button.clicked.connect(self.add_new_row)
        self.layout.addWidget(self.add_row_button)

        self.delete_row_button = QtWidgets.QPushButton("Delete Selected Row")
        self.delete_row_button.clicked.connect(self.delete_selected_row)
        self.layout.addWidget(self.delete_row_button)

        self.calculate_button = QtWidgets.QPushButton("Calculate Transfers")
        self.calculate_button.clicked.connect(self.calculate_transfers)
        self.layout.addWidget(self.calculate_button)
        
        #Initialize instances
        self.table_widget = None
        self.transfer_label = None
        self.text_area = None

        # Connect itemChanged signal only once here
        self.table.itemChanged.connect(self.calculate_net)

        # Initialize table with one row
        self.add_new_row()

    def adjust_table_size(self):
        # Optionally resize based on content
        if self.table is not None:
            self.table.resizeColumnsToContents()
            self.table.resizeRowsToContents()
        if self.table_widget is not None:
            self.table_widget.resizeColumnsToContents()
            self.table_widget.resizeRowsToContents()
        self.adjust_input_table_height()
        self.adjust_window_to_table()
        
    def adjust_window_to_table(self):
        # Get table size
        if self.table_widget is not None:
            #print("table exists")
            table_width = self.table_widget.horizontalHeader().length() + self.table_widget.verticalScrollBar().sizeHint().width()
            table_height = self.table_widget.verticalHeader().length() + self.table_widget.horizontalScrollBar().sizeHint().height()
        else:
            table_width = 0
            table_height = 0
            
        if self.table is not None:
            edit_table_width = self.table.horizontalHeader().length() + self.table.verticalScrollBar().sizeHint().width()
            edit_table_height = self.table.verticalHeader().length() + self.table.horizontalScrollBar().sizeHint().height()
            #print("input table exists", edit_table_height, edit_table_width)
        else:
            edit_table_height = 0
            edit_table_width = 0
        # Add margins to account for window decorations and layout spacing
        margin = 50
        self.main_window.resize(max(table_width, edit_table_width) + margin, max(table_height, edit_table_height) + margin)
        
        
    def add_new_row(self):
        row_count = self.table.rowCount()
        self.table.insertRow(row_count)
        self.table.setItem(row_count, 0, QtWidgets.QTableWidgetItem(str(row_count + 1)))
        self.table.setItem(row_count, 1, QtWidgets.QTableWidgetItem(""))
        self.table.setItem(row_count, 2, QtWidgets.QTableWidgetItem(""))
        self.table.setItem(row_count, 3, QtWidgets.QTableWidgetItem(""))
        self.table.setItem(row_count, 4, QtWidgets.QTableWidgetItem("0")) 

    def delete_selected_row(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            self.table.removeRow(selected_row)

    def calculate_net(self, item):
        row = item.row()
        column = item.column()
        self.adjust_table_size()
        if column in (2, 3):  # Check if column is for Buy-in or Buy-out
            # Ensure there is an item in both the Buy-in and Buy-out cells
            buy_in_item = self.table.item(row, 2)
            buy_out_item = self.table.item(row, 3)
            
            # Use '0' if the item is None or the text is empty
            buy_in = int(buy_in_item.text() if buy_in_item and buy_in_item.text() else "0")
            buy_out = int(buy_out_item.text() if buy_out_item and buy_out_item.text() else "0")

            # Calculate and update the net value
            net = buy_out - buy_in
            self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(net)))


    def extract_table_data(self):
        data_list = []
        error_msg = None

        for row in range(self.table.rowCount()):
            try:
                id_value = int(self.table.item(row, 0).text())
                nickname = self.table.item(row, 1).text()
                net = int(self.table.item(row, 4).text())
            except ValueError:
                error_msg = f"Error processing row {row+1}: Invalid data found."
                break  # Stop processing if an error occurs

            data_list.append((id_value, nickname, net))

        if error_msg:
            return None, error_msg  # Return None to indicate an error
        else:
            return data_list, None

    def calculate_transfers(self):
        data_list, error_msg1 = self.extract_table_data()
        if error_msg1:
            self.print_error(error_msg1)
            return None
        else:
            transfers, error_msg2 = cmt(data_list)  # Assuming money_calculate is the function processing data
        if error_msg2:
            self.print_error(error_msg2)
            return None
        else:
            # Now print/display transfers, for now, let's assume we print it to console
            print(transfers)  # Replace with your actual display logic
            self.print_transfers(transfers)

    def print_error(self, error_msg):
        # Text area to display the file contents
            self.text_area_exists()
            self.text_area = QtWidgets.QTextEdit(self)
            self.text_area.setReadOnly(True)
            self.layout.addWidget(self.text_area)
            self.text_area.setText(error_msg)
            
    def print_transfers(self, transfers):
            self.transfer_table_exists()
            # Create QTableWidget
            self.table_widget = QtWidgets.QTableWidget(self)
            self.table_widget.setRowCount(len(transfers))
            self.table_widget.setColumnCount(3)
            width_adjuster = 20
            self.table_widget.setHorizontalHeaderLabels([" " * width_adjuster + 'From' + " " * width_adjuster, 
                                                         " " * width_adjuster + 'To' + " " * width_adjuster, 
                                                         " " * width_adjuster + 'Amount' + " " * width_adjuster])
            # Populate table
            for row, (from_player, to_player, amount) in enumerate(transfers):
                self.table_widget.setItem(row, 0, QtWidgets.QTableWidgetItem(from_player))
                self.table_widget.setItem(row, 1, QtWidgets.QTableWidgetItem(to_player))
                self.table_widget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(amount)))
            
            # Optionally resize based on content
            self.table_widget.resizeColumnsToContents()
            self.table_widget.resizeRowsToContents()
            #self.adjust_table_height()
            self.adjust_table_size()
            # Add table widget to layout
            self.transfer_label = QtWidgets.QLabel("Transfers", self)
            self.transfer_label.setStyleSheet("font-size: 16px; font-weight: bold;")
            self.text_area_exists()
            self.layout.addWidget(self.transfer_label)
            self.layout.addWidget(self.table_widget)
            
    def text_area_exists(self):
        if self.text_area is not None:
            self.layout.removeWidget(self.text_area)
            self.text_area = None
    
    def transfer_table_exists(self):
        if self.table_widget is not None:
            self.layout.removeWidget(self.table_widget)
            self.layout.removeWidget(self.transfer_label)
            self.table_widget = None
            self.transfer_label = None

    def adjust_table_height(self):
        # Calculate the total height required for all rows
        total_height = sum(self.table_widget.rowHeight(row) for row in range(self.table_widget.rowCount()))

        # Add the height of the horizontal header
        total_height += self.table_widget.horizontalHeader().height()

        # Add some margins to account for spacing
        total_height += 2 * self.table_widget.frameWidth()

        # Set the table's height
        self.table_widget.setFixedHeight(total_height)
        
    def adjust_input_table_height(self):
        # Calculate the total height required for all rows
        total_height = sum(self.table.rowHeight(row) for row in range(self.table.rowCount()))
        # Add the height of the horizontal header
        total_height += self.table.horizontalHeader().height()
        # Add some margins to account for spacing
        total_height += 2 * self.table.frameWidth()
        # Set the table's height
        self.table.setFixedHeight(total_height)




class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tabbed Interface Example")
        self.resize(400, 300)

        # Create the tab widget
        self.tabs = QtWidgets.QTabWidget()
        self.setCentralWidget(self.tabs)

        # Create the tab pages
        #self.online_tab = OnlineWidget()
        self.offline_tab = OfflineWidget(self)

        # Add tabs
        #self.tabs.addTab(self.online_tab, "Online")
        self.tabs.addTab(self.offline_tab, "Offline")
        

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec_()
