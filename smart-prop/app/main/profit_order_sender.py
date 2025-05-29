from getpass import getpass
from ctypes import byref, c_wchar_p, c_double, c_int
from profitTypes import *
from profit_dll import initializeDll
from datetime import datetime


class ProfitOrderSender:
    def __init__(self, dll_path, key="1747419014493122621", user="renan@mesasmartprop.com.br", password="SmartProp2024@"):
        self.dll = initializeDll(dll_path)
        self._key = key
        self._user = user
        self._password = password
        self._connect()

    def _connect(self):
        result = self.dll.DLLInitializeLogin(
            c_wchar_p(self._key),
            c_wchar_p(self._user),
            c_wchar_p(self._password),
            None, None, None, None,
            None, None, None,
            None, None, None, None
        )
        print(f"DLLInitialize: {result}")

    def send_market_order(self, broker_id, account_id, sub_account_id, rot_password,
                          ticker, exchange, amount, side="buy"):
        order_type = TConnectorOrderType.Market.value
        order_side = TConnectorOrderSide.Buy.value if side == "buy" else TConnectorOrderSide.Sell.value

        send_order = TConnectorSendOrder(
            Version=0,
            Password=rot_password,
            OrderType=order_type,
            OrderSide=order_side,
            Price=-1,
            StopPrice=-1,
            Quantity=amount
        )

        send_order.AccountID = TConnectorAccountIdentifier(
            Version=0,
            BrokerID=broker_id,
            AccountID=account_id,
            SubAccountID=sub_account_id,
            Reserved=0
        )

        send_order.AssetID = TConnectorAssetIdentifier(
            Version=0,
            Ticker=ticker,
            Exchange=exchange,
            FeedType=0
        )

        result = self.dll.SendOrder(byref(send_order))

        if result < 0:
            print(f"Erro ao enviar ordem. Código: {result}")
        else:
            print(f"Ordem enviada com sucesso. ProfitID: {result}")
