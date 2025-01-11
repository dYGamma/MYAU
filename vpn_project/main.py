from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
import sys
from vpn_manager import VPNManager

class VPNApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Personal VPN Client")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("background-color: #2e2e2e; color: white;")

        # Указываем путь к конфигурационному файлу
        config_path = r"D:\GIT\MYAU\vpn_project\resources\configs\my_vpn.conf"
        
        self.vpn_manager = VPNManager(config_path)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.status_label = QLabel("Status: Disconnected")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        connect_button = QPushButton("Connect")
        connect_button.clicked.connect(self.connect_vpn)
        layout.addWidget(connect_button)

        disconnect_button = QPushButton("Disconnect")
        disconnect_button.clicked.connect(self.disconnect_vpn)
        layout.addWidget(disconnect_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def connect_vpn(self):
        result = self.vpn_manager.connect()
        self.status_label.setText(f"Status: {result}")

    def disconnect_vpn(self):
        result = self.vpn_manager.disconnect()
        self.status_label.setText(f"Status: {result}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    vpn_app = VPNApp()
    vpn_app.show()
    sys.exit(app.exec())
