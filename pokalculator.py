from PyQt5 import QtWidgets, QtCore
from backend_service.ledger_to_transfer import ledger_tranfer_calculator as ltc
from money_service.money_calculator import calculate_minimal_transfers as cmt

class CsvDropBox(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Poker Transfer Calculator")
        self.resize(400, 300)
        
        # Layout setup
        self.layout = QtWidgets.QVBoxLayout(self)
        
        # Label for drag-and-drop
        self.drop_label = QtWidgets.QLabel("Drop CSV Here", self)
        self.drop_label.setFixedSize(300, 200)
        self.drop_label.setAlignment(QtCore.Qt.AlignCenter)
        self.drop_label.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaa;
                font-size: 16px;
                color: #555;
            }
        """)
        self.drop_label.setAcceptDrops(True)
        self.layout.addWidget(self.drop_label, alignment=QtCore.Qt.AlignCenter)

        # Button to upload CSV
        self.upload_button = QtWidgets.QPushButton("Upload CSV", self)
        self.upload_button.clicked.connect(self.upload_csv)
        self.layout.addWidget(self.upload_button, alignment=QtCore.Qt.AlignCenter)

        # Enable drag-and-drop on the label
        self.drop_label.dragEnterEvent = self.dragEnterEvent
        self.drop_label.dropEvent = self.dropEvent

        #initializing widgets
        self.table_widget = None
        self.text_area = None
        self.transfer_label = None
        self.edit_table = None
        self.edit_label = None

    def dragEnterEvent(self, event):
        """Handle when a file is dragged into the widget."""
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """Handle when a file is dropped into the widget."""
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            if f.endswith('.csv'):
                self.load_csv(f)
                break
            else:
                # Text area to display the file contents
                self.text_area_exists()
                self.text_area = QtWidgets.QTextEdit(self)
                self.text_area.setReadOnly(True)
                self.layout.addWidget(self.text_area)
                self.text_area.setText("Invalid file type. Please drop a CSV file.")
                break

    def upload_csv(self):
        """Open a file dialog to upload a CSV file."""
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        if file_path:
            self.load_csv(file_path)
    
    def print_error(self, error_msg):
        # Text area to display the file contents
            self.text_area_exists()
            self.text_area = QtWidgets.QTextEdit(self)
            self.text_area.setReadOnly(True)
            self.layout.addWidget(self.text_area)
            self.text_area.setText(error_msg)

    def load_csv(self, file_path):
        """Load and display the contents of the CSV file."""
        try:
            transfers, id_nick_net, error_msg = ltc(file_path)
            if error_msg:
                self.print_error(self, error_msg)
            else:
                self.print_edit_table(id_nick_net)
                self.print_transfers(transfers)

        except Exception as e:
            # Text area to display the file contents
            self.text_area_exists()
            self.text_area = QtWidgets.QTextEdit(self)
            self.text_area.setReadOnly(True)
            self.layout.addWidget(self.text_area)
            self.text_area.setText(f"Error loading file: {str(e)}")
            
    def adjust_window_to_table(self):
        # Get table size
        table_width = self.table_widget.horizontalHeader().length() + self.table_widget.verticalScrollBar().sizeHint().width()
        table_height = self.table_widget.verticalHeader().length() + self.table_widget.horizontalScrollBar().sizeHint().height()
        
        edit_table_width = self.edit_table.horizontalHeader().length() + self.edit_table.verticalScrollBar().sizeHint().width()
        edit_table_height = self.edit_table.verticalHeader().length() + self.edit_table.horizontalScrollBar().sizeHint().height()
        # Add margins to account for window decorations and layout spacing
        margin = 50
        self.resize(max(table_width, edit_table_width) + margin, max(table_height, edit_table_height) + margin)

    def adjust_table_height(self):
        # Calculate the total height required for all rows
        total_height = sum(self.table_widget.rowHeight(row) for row in range(self.table_widget.rowCount()))

        # Add the height of the horizontal header
        total_height += self.table_widget.horizontalHeader().height()

        # Add some margins to account for spacing
        total_height += 2 * self.table_widget.frameWidth()

        # Set the table's height
        self.table_widget.setFixedHeight(total_height)
        
    def adjust_edit_table_height(self):
        # Calculate the total height required for all rows
        total_height = sum(self.edit_table.rowHeight(row) for row in range(self.edit_table.rowCount()))

        # Add the height of the horizontal header
        total_height += self.edit_table.horizontalHeader().height()

        # Add some margins to account for spacing
        total_height += 2 * self.edit_table.frameWidth()

        # Set the table's height
        self.edit_table.setFixedHeight(total_height)
        
    def transfer_table_exists(self):
        if self.table_widget is not None:
            self.layout.removeWidget(self.table_widget)
            self.layout.removeWidget(self.transfer_label)
            self.table_widget = None
            self.transfer_label = None
            
    def text_area_exists(self):
        if self.text_area is not None:
            self.layout.removeWidget(self.text_area)
            self.text_area = None
    
    def edit_table_exists(self):
        if self.edit_table is not None:
            self.layout.removeWidget(self.edit_table)
            self.layout.removeWidget(self.edit_label)
            self.layout.removeWidget(self.calculate_button)
            self.edit_table = None
            self.edit_label = None
            self.calculate_button = None

    def print_edit_table(self, id_nick_net):
        self.edit_table_exists()
        
        # Create QTableWidget
        self.edit_table = QtWidgets.QTableWidget(self)
        self.edit_table.setRowCount(len(id_nick_net))
        self.edit_table.setColumnCount(3)
        self.edit_table.setHorizontalHeaderLabels(['Nickname', 'ID', 'Net'])
        
        # Populate table
        for row, (id, nickname, net) in enumerate(id_nick_net):
            self.edit_table.setItem(row, 0, QtWidgets.QTableWidgetItem(nickname))
            self.edit_table.setItem(row, 1, QtWidgets.QTableWidgetItem(id))
            self.edit_table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(net)))
        
        # Optionally resize based on content
        self.edit_table.resizeColumnsToContents()
        self.edit_table.resizeRowsToContents()
        self.adjust_edit_table_height()
        
        # Add label and table to layout
        self.edit_label = QtWidgets.QLabel("Edit", self)
        self.edit_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.text_area_exists()
        self.layout.addWidget(self.edit_label)
        self.layout.addWidget(self.edit_table)
        
        # Create a button
        self.calculate_button = QtWidgets.QPushButton("Re-calculate", self)
        self.calculate_button.setStyleSheet("font-size: 14px; padding: 5px 10px;")
        
        # Connect button's clicked signal to a wrapper function
        def on_calculate_button_clicked():
            # Extract data from the table into a dictionary
            id_nick_net = [ (self.edit_table.item(row, 1).text(),        # ID as string from column 1
                self.edit_table.item(row, 0).text(),       # Nickname from column 0
                int(self.edit_table.item(row, 2).text()))  # Net as int from column 2
                for row in range(self.edit_table.rowCount())
                if self.edit_table.item(row, 0) and self.edit_table.item(row, 1) and self.edit_table.item(row, 2)
            ]
            
            # Debug print to verify the extracted data
            print("Extracted balances dictionary:", id_nick_net)
            
            # Call the calculate_money function with the formatted data
            transfers, error_msg = cmt(id_nick_net)
            if error_msg:
                self.print_error(error_msg)
            else:
                self.print_transfers(transfers)
        
        self.calculate_button.clicked.connect(on_calculate_button_clicked)
        
        
        # Add button to layout
        self.layout.addWidget(self.calculate_button)
        


    def print_transfers(self, transfers):
            self.transfer_table_exists()
            # Create QTableWidget
            self.table_widget = QtWidgets.QTableWidget(self)
            self.table_widget.setRowCount(len(transfers))
            self.table_widget.setColumnCount(3)
            self.table_widget.setHorizontalHeaderLabels(['From', 'To', 'Amount'])
            # Populate table
            for row, (from_player, to_player, amount) in enumerate(transfers):
                self.table_widget.setItem(row, 0, QtWidgets.QTableWidgetItem(from_player))
                self.table_widget.setItem(row, 1, QtWidgets.QTableWidgetItem(to_player))
                self.table_widget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(amount)))
            
            # Optionally resize based on content
            self.table_widget.resizeColumnsToContents()
            self.table_widget.resizeRowsToContents()
            self.adjust_table_height()
            self.adjust_window_to_table()
            # Add table widget to layout
            self.transfer_label = QtWidgets.QLabel("Transfers", self)
            self.transfer_label.setStyleSheet("font-size: 16px; font-weight: bold;")
            self.text_area_exists()
            self.layout.addWidget(self.transfer_label)
            self.layout.addWidget(self.table_widget)
        
app = QtWidgets.QApplication([])
window = CsvDropBox()
window.show()
app.exec_()
