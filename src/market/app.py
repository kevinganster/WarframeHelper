import json

from PyQt5.Qt import Qt
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QTabWidget, QHeaderView

from core import constants, wfmarket
from market import instance


def calc_profit(sell_price, buy_price):
    if not sell_price or not buy_price:
        return None
    else:
        return sell_price - buy_price


class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        
        self.setWindowTitle("Warframe Market Helper")
        self.setWindowIcon(QIcon(constants.RES_LOC + "relic.png"))
        self.resize(QSize(1200, 700))
        self.setupUi()
    
    def setupUi(self):
        wTabs = QTabWidget()
        self.setCentralWidget(wTabs)
        
        with open(constants.MARKET_NAMES_LOC, "r", encoding="utf-8") as f:
            market_names = json.load(f)

        wTabs.addTab(self.createItemTable(market_names), "Parts")
        wTabs.addTab(self.createModTable(market_names), "Mods")

    def createItemTable(self, market_names):
        market_data = wfmarket.get_all(wfmarket.CAT_ITEMS)

        table = QTableWidget()
        table.setColumnCount(5)
        table.setRowCount(len(market_data))
        table.setHorizontalHeaderLabels(["Name", "Set (Sell)", "Components (Sell)", "Components (Buy)", "Potential Profit"])
        table.verticalHeader().hide()

        for i, (item_name, components) in enumerate(market_names["items"].items()):
            set_repr = instance.config["calc_sell_repr"](market_data[item_name + "_set"])
            
            component_prices = [market_data[item_name + "_" + comp_name] for comp_name in components]
            
            comp_sell_repr = instance.config["calc_component_repr"](component_prices, "sell")
            comp_buy_repr = instance.config["calc_component_repr"](component_prices, "buy")

            
            table.setItem(i, 0, QTableWidgetItem(" ".join(item_name.split("_"))))

            item = QTableWidgetItem()
            item.setData(Qt.EditRole, set_repr)
            table.setItem(i, 1, item)

            item = QTableWidgetItem()
            item.setData(Qt.EditRole, comp_sell_repr)
            table.setItem(i, 2, item)

            item = QTableWidgetItem()
            item.setData(Qt.EditRole, comp_buy_repr)
            table.setItem(i, 3, item)

            item = QTableWidgetItem()
            item.setData(Qt.EditRole, calc_profit(set_repr, comp_buy_repr))
            table.setItem(i, 4, item)

        table.sortByColumn(4, Qt.DescendingOrder)
        table.setSortingEnabled(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        return table
    
    def createModTable(self, market_names):
        market_data = wfmarket.get_all(wfmarket.CAT_MODS)

        table = QTableWidget()
        table.setColumnCount(4)
        table.setRowCount(len(market_data))
        table.setHorizontalHeaderLabels(["Name", "Sell Price", "Buy Price", "Potential Profit"])
        table.verticalHeader().hide()

        for i, mod_name in enumerate(market_names["mods"]):
            mod_prices = market_data[mod_name]
            if mod_prices is None:
                continue
            
            buy_repr = instance.config["calc_buy_repr"](mod_prices)
            sell_repr = instance.config["calc_sell_repr"](mod_prices)

            table.setItem(i, 0, QTableWidgetItem(" ".join(mod_name.split("_"))))

            item = QTableWidgetItem()
            item.setData(Qt.EditRole, sell_repr)
#                 item.setData(Qt.DisplayRole, "-")
            table.setItem(i, 1, item)

            item = QTableWidgetItem()
            item.setData(Qt.EditRole, buy_repr)
            table.setItem(i, 2, item)
            
            item = QTableWidgetItem()
            item.setData(Qt.EditRole, calc_profit(sell_repr, buy_repr))
            table.setItem(i, 3, item)

        table.sortByColumn(3, Qt.DescendingOrder)
        table.setSortingEnabled(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        return table
