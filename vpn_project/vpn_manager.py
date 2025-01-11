import os
from wireguard_tools import WireguardDevice
import logging

class MyWireguardDevice(WireguardDevice):
    def __init__(self, name):
        super().__init__(name)
        self.config = {}
        self.name = name

    def get_config(self):
        """
        Возвращает текущую конфигурацию WireGuard в виде словаря.
        """
        return self.config

    def set_config(self, config_file):
        """
        Загружает конфигурацию из файла и сохраняет её в атрибуте self.config.
        """
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Config file {config_file} not found.")
        
        if os.path.getsize(config_file) == 0:
            raise ValueError(f"Config file {config_file} is empty.")

        with open(config_file, "r") as f:
            config_data = f.read()

        # Разбор конфигурации
        self.config = self.parse_config(config_data)

    def parse_config(self, config_data):
        """
        Парсит строку конфигурации WireGuard и возвращает её в виде словаря.
        """
        config = {}
        lines = config_data.split("\n")
        section = None
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("[Interface]"):
                section = "Interface"
                config["Interface"] = {}
            elif line.startswith("[Peer]"):
                section = "Peer"
                config["Peer"] = {}
            elif "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                if section == "Interface":
                    config["Interface"][key] = value
                elif section == "Peer":
                    config["Peer"][key] = value
        return config

    def apply_config(self):
        """
        Применяет конфигурацию из self.config в WireGuard.
        """
        # Пример: применение настроек из интерфейса и пира
        interface = self.config.get("Interface", {})
        peer = self.config.get("Peer", {})

        # Применение конфигурации из интерфейса
        if "PrivateKey" in interface:
            print(f"Setting private key: {interface['PrivateKey']}")
        if "Address" in interface:
            print(f"Setting address: {interface['Address']}")
        if "DNS" in interface:
            print(f"Setting DNS: {interface['DNS']}")
        
        # Применение конфигурации пира
        if "PublicKey" in peer:
            print(f"Setting peer public key: {peer['PublicKey']}")
        if "PresharedKey" in peer:
            print(f"Setting preshared key: {peer['PresharedKey']}")
        if "AllowedIPs" in peer:
            print(f"Setting allowed IPs: {peer['AllowedIPs']}")
        if "Endpoint" in peer:
            print(f"Setting endpoint: {peer['Endpoint']}")

    def up(self):
        """
        Запуск интерфейса WireGuard.
        """
        self.apply_config()
        # Дальше код для поднятия интерфейса, например, через systemd или другие средства
        print(f"Bringing up WireGuard interface {self.name}")

    def down(self):
        """
        Остановка интерфейса WireGuard.
        """
        # Остановка интерфейса (реализуйте по своему)
        print(f"Bringing down WireGuard interface {self.name}")


class VPNManager:
    def __init__(self, config_path):
        self.config_path = config_path
        self.device = None
        self.logger = logging.getLogger("VPNManager")
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler("resources/logs/vpn_app.log")
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)

    def connect(self):
        if not os.path.exists(self.config_path):
            self.logger.error(f"Config file not found: {self.config_path}")
            return "Config file not found"

        try:
            self.device = MyWireguardDevice("wg0")
            self.device.set_config(self.config_path)
            self.device.up()
            self.logger.info(f"VPN connected with config: {self.config_path}")
            return "VPN connected successfully"
        except FileNotFoundError as e:
            self.logger.error(f"Failed to connect VPN: {e}")
            return f"Failed to connect: {e}"
        except ValueError as e:
            self.logger.error(f"Failed to connect VPN: {e}")
            return f"Failed to connect: {e}"
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return f"Failed to connect: {e}"

    def disconnect(self):
        if not self.device:
            return "No active VPN connection"

        try:
            self.device.down()
            self.logger.info("VPN disconnected.")
            return "VPN disconnected successfully"
        except Exception as e:
            self.logger.error(f"Failed to disconnect VPN: {e}")
            return f"Failed to disconnect: {e}"
