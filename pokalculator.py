from PyQt5 import QtWidgets, QtCore
# import pandas as pd
from backend_service.ledger_to_transfer import ledger_tranfer_calculator as ltc

class CsvDropBox(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Poker Transfer Calculator (떡준이꺼)")
        #self.setFixedSize(1200, 900)
        self.resize(500, 400)
        
        # Layout setup
        self.layout = QtWidgets.QVBoxLayout(self)
        
        # Label for drag-and-drop
        self.drop_label = QtWidgets.QLabel("Drop CSV Here", self)
        self.drop_label.setFixedSize(400, 300)
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

        # Text area to display the file contents
        # self.text_area = QtWidgets.QTextEdit(self)
        # self.text_area.setReadOnly(True)
        # self.layout.addWidget(self.text_area)

        # Enable drag-and-drop on the label
        self.drop_label.dragEnterEvent = self.dragEnterEvent
        self.drop_label.dropEvent = self.dropEvent
        
        #Table Area
        # self.table_widget = QtWidgets.QTableWidget(self)
        # self.table_widget.setFixedSize(1000, 1000)
        # self.layout.addWidget(self.table_widget, alignment=QtCore.Qt.AlignCenter)

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
                self.text_area.setText("Invalid file type. Please drop a CSV file.")
                break

    def upload_csv(self):
        """Open a file dialog to upload a CSV file."""
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        if file_path:
            self.load_csv(file_path)

    def load_csv(self, file_path):
        """Load and display the contents of the CSV file."""
        try:
            # df = pd.read_csv(file_path)
            # self.text_area.setText(f"Loaded: {file_path}\n\n{df.head().to_string()}")
            transfers = ltc(file_path)
            self.print_transfers(transfers)

        except Exception as e:
            self.text_area.setText(f"Error loading file: {str(e)}")
            
    def adjust_window_to_table(self):
        # Get table size
        table_width = self.table_widget.horizontalHeader().length() + self.table_widget.verticalScrollBar().sizeHint().width()
        table_height = self.table_widget.verticalHeader().length() + self.table_widget.horizontalScrollBar().sizeHint().height()
        
        # Add margins to account for window decorations and layout spacing
        margin = 50
        self.resize(table_width + margin, table_height + margin)

    def adjust_table_height(self):
        # Calculate the total height required for all rows
        total_height = sum(self.table_widget.rowHeight(row) for row in range(self.table_widget.rowCount()))

        # Add the height of the horizontal header
        total_height += self.table_widget.horizontalHeader().height()

        # Add some margins to account for spacing
        total_height += 2 * self.table_widget.frameWidth()

        # Set the table's height
        self.table_widget.setFixedHeight(total_height)

    def print_transfers(self, transfers):
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
            self.layout.addWidget(self.table_widget)
app = QtWidgets.QApplication([])
window = CsvDropBox()
window.show()
app.exec_()
