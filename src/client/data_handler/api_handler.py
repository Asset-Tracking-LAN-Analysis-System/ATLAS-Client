import sys
import json
import requests

from PySide6.QtWidgets import (
    QApplication,
)




class api_handler:
    def __init__(self):
        with open("client/config.json", "r") as config_file:
            config = json.load(config_file)
        self.api_url = f"{str(config['api_url'])}:{str(config['api_port'])}"
        print(f"Connecting to {self.api_url}")

    def fetch_data(self):

        response = requests.get(url=self.api_url + "/entities")
        data = response.json()

        return data





# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())
