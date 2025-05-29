#Imports para execução da DLL
import ctypes
from getpass import getpass
from ctypes import *
import struct
from datetime import *
from confluent_kafka import Producer
from profitTypes import *
from profit_dll import initializeDll
import json

conf = {
    'bootstrap.servers': 'localhost:9092'  # ou o endereço do seu broker
}
kafka_producer = Producer(conf)

profit_dll = initializeDll(r"C:\Users\vinic\OneDrive\Documentos\GitHub\smart-prop-ORH\doc\ProfitDLL\DLLs\Win64\ProfitDLL.dll")

# Error Codes
NL_OK                    = 0x00000000
NL_INTERNAL_ERROR        = -2147483647                   # Internal error
NL_NOT_INITIALIZED       = NL_INTERNAL_ERROR        + 1  # Not initialized
NL_INVALID_ARGS          = NL_NOT_INITIALIZED       + 1  # Invalid arguments
NL_WAITING_SERVER        = NL_INVALID_ARGS          + 1  # Aguardando dados do servidor
NL_NO_LOGIN              = NL_WAITING_SERVER        + 1  # Nenhum login encontrado
NL_NO_LICENSE            = NL_NO_LOGIN              + 1  # Nenhuma licença encontrada
NL_PASSWORD_HASH_SHA1    = NL_NO_LICENSE            + 1  # Senha não está em SHA1
NL_PASSWORD_HASH_MD5     = NL_PASSWORD_HASH_SHA1    + 1  # Senha não está em MD5
NL_OUT_OF_RANGE          = NL_PASSWORD_HASH_MD5     + 1  # Count do parâmetro maior que o tamanho do array
NL_MARKET_ONLY           = NL_OUT_OF_RANGE          + 1  # Não possui roteamento
NL_NO_POSITION           = NL_MARKET_ONLY           + 1  # Não possui posição
NL_NOT_FOUND             = NL_NO_POSITION           + 1  # Recurso não encontrado
NL_VERSION_NOT_SUPPORTED = NL_NOT_FOUND             + 1  # Versão do recurso não suportada
NL_OCO_NO_RULES          = NL_VERSION_NOT_SUPPORTED + 1  # OCO sem nenhuma regra
NL_EXCHANGE_UNKNOWN      = NL_OCO_NO_RULES          + 1  # Bolsa desconhecida
NL_NO_OCO_DEFINED        = NL_EXCHANGE_UNKNOWN      + 1  # Nenhuma OCO encontrada para a ordem
NL_INVALID_SERIE         = NL_NO_OCO_DEFINED        + 1  # (Level + Offset + Factor) inválido
NL_LICENSE_NOT_ALLOWED   = NL_INVALID_SERIE         + 1  # Recurso não liberado na licença
NL_NOT_HARD_LOGOUT       = NL_LICENSE_NOT_ALLOWED   + 1  # Retorna que não esta em HardLogout
NL_SERIE_NO_HISTORY      = NL_NOT_HARD_LOGOUT       + 1  # Série não tem histórico no servidor
NL_ASSET_NO_DATA         = NL_SERIE_NO_HISTORY      + 1  # Asset não tem o dados carregado
NL_SERIE_NO_DATA         = NL_ASSET_NO_DATA         + 1  # Série não tem dados (count = 0)
NL_HAS_STRATEGY_RUNNING  = NL_SERIE_NO_DATA         + 1  # Existe uma estratégia rodando
NL_SERIE_NO_MORE_HISTORY = NL_HAS_STRATEGY_RUNNING  + 1  # Não tem mais dados disponiveis para a serie
NL_SERIE_MAX_COUNT       = NL_SERIE_NO_MORE_HISTORY + 1  # Série esta no limite de dados possíveis
NL_DUPLICATE_RESOURCE    = NL_SERIE_MAX_COUNT       + 1  # Recurso duplicado
NL_UNSIGNED_CONTRACT     = NL_DUPLICATE_RESOURCE    + 1
NL_NO_PASSWORD           = NL_UNSIGNED_CONTRACT     + 1  # Nenhuma senha informada
NL_NO_USER               = NL_NO_PASSWORD           + 1  # Nenhum usuário informado no login
NL_FILE_ALREADY_EXISTS   = NL_NO_USER               + 1  # Arquivo já existe
NL_INVALID_TICKER        = NL_FILE_ALREADY_EXISTS   + 1
NL_NOT_MASTER_ACCOUNT    = NL_INVALID_TICKER        + 1  # Conta não é master

#Variaveis de Controle
bAtivo = False
bMarketConnected = False
bConnectado = False
bBrokerConnected = False

def NResultToString(nResult: int) -> str:
    if nResult == NL_INTERNAL_ERROR:
        return "NL_INTERNAL_ERROR"
    elif nResult == NL_NOT_INITIALIZED:
        return "NL_NOT_INITIALIZED"
    elif nResult == NL_INVALID_ARGS:
        return "NL_INVALID_ARGS"
    elif nResult == NL_WAITING_SERVER:
        return "NL_WAITING_SERVER"
    elif nResult == NL_NO_LOGIN:
        return "NL_NO_LOGIN"
    elif nResult == NL_NO_LICENSE:
        return "NL_NO_LICENSE"
    elif nResult == NL_PASSWORD_HASH_SHA1:
        return "NL_PASSWORD_HASH_SHA1"
    elif nResult == NL_PASSWORD_HASH_MD5:
        return "NL_PASSWORD_HASH_MD5"
    elif nResult == NL_OUT_OF_RANGE:
        return "NL_OUT_OF_RANGE"
    elif nResult == NL_MARKET_ONLY:
        return "NL_MARKET_ONLY"
    elif nResult == NL_NO_POSITION:
        return "NL_NO_POSITION"
    elif nResult == NL_NOT_FOUND:
        return "NL_NOT_FOUND"
    elif nResult == NL_VERSION_NOT_SUPPORTED:
        return "NL_VERSION_NOT_SUPPORTED"
    elif nResult == NL_OCO_NO_RULES:
        return "NL_OCO_NO_RULES"
    elif nResult == NL_EXCHANGE_UNKNOWN:
        return "NL_EXCHANGE_UNKNOWN"
    elif nResult == NL_NO_OCO_DEFINED:
        return "NL_NO_OCO_DEFINED"
    elif nResult == NL_INVALID_SERIE:
        return "NL_INVALID_SERIE"
    elif nResult == NL_LICENSE_NOT_ALLOWED:
        return "NL_LICENSE_NOT_ALLOWED"
    elif nResult == NL_NOT_HARD_LOGOUT:
        return "NL_NOT_HARD_LOGOUT"
    elif nResult == NL_SERIE_NO_HISTORY:
        return "NL_SERIE_NO_HISTORY"
    elif nResult == NL_ASSET_NO_DATA:
        return "NL_ASSET_NO_DATA"
    elif nResult == NL_SERIE_NO_DATA:
        return "NL_SERIE_NO_DATA"
    elif nResult == NL_HAS_STRATEGY_RUNNING:
        return "NL_HAS_STRATEGY_RUNNING"
    elif nResult == NL_SERIE_NO_MORE_HISTORY:
        return "NL_SERIE_NO_MORE_HISTORY"
    elif nResult == NL_SERIE_MAX_COUNT:
        return "NL_SERIE_MAX_COUNT"
    elif nResult == NL_DUPLICATE_RESOURCE:
        return "NL_DUPLICATE_RESOURCE"
    elif nResult == NL_UNSIGNED_CONTRACT:
        return "NL_UNSIGNED_CONTRACT"
    elif nResult == NL_NO_PASSWORD:
        return "NL_NO_PASSWORD"
    elif nResult == NL_NO_USER:
        return "NL_NO_USER"
    elif nResult == NL_FILE_ALREADY_EXISTS:
        return "NL_FILE_ALREADY_EXISTS"
    elif nResult == NL_INVALID_TICKER:
        return "NL_INVALID_TICKER"
    elif nResult == NL_NOT_MASTER_ACCOUNT:
        return "NL_NOT_MASTER_ACCOUNT"
    else:
        return str(nResult)

def evalDllReturn(function: str, ret: int) -> bool:
    if ret < NL_OK:
        print("{0}: {1}".format(
            function,
            NResultToString(ret)
        ))

        return False
    else:
        return True
    
def system_time_to_datetime(system_time):
    try:
        return datetime(
            year=system_time.wYear,
            month=system_time.wMonth,
            day=system_time.wDay,
            hour=system_time.wHour,
            minute=system_time.wMinute,
            second=system_time.wSecond,
            microsecond=system_time.wMilliseconds * 1000
        )
    except:
        return None
    
 
#BEGIN DEF
@WINFUNCTYPE(None, c_int32, c_int32)
def stateCallback(nType, nResult):
    global bAtivo
    global bMarketConnected
    global bConnectado

    nConnStateType = nType
    result = nResult

    if nConnStateType == 0: # notificacoes de login
        if result == 0:
            bConnectado = True
            print("Login: conectado")
        else :
            bConnectado = False
            print('Login: ' + str(result))
    elif nConnStateType == 1:
        if result == 5:
            # bBrokerConnected = True
            print("Broker: Conectado.")
        elif result > 2:
            # bBrokerConnected = False
            print("Broker: Sem conexão com corretora.")
        else:
            # bBrokerConnected = False
            print("Broker: Sem conexão com servidores (" + str(result) + ")")

    elif nConnStateType == 2:  # notificacoes de login no Market
        if result == 4:
            print("Market: Conectado" )
            bMarketConnected = True
        else:
            print("Market: " + str(result))
            bMarketConnected = False

    elif nConnStateType == 3: # notificacoes de login
        if result == 0:
            print("Ativação: OK")
            bAtivo = True
        else:
            print("Ativação: " + str(result))
            bAtivo = False

    if bMarketConnected and bAtivo and bConnectado:
        print("Serviços Conectados")

    return

@WINFUNCTYPE(None, TAssetID, c_wchar_p, c_uint, c_double, c_double, c_int, c_int, c_int, c_int)
def newHistoryCallback(assetId, date, tradeNumber, price, vol, qtd, buyAgent, sellAgent, tradeType):
    print(assetId.ticker + ' | Trade History | ' + date + ' (' + str(tradeNumber) + ') ' + str(price))
    return

@WINFUNCTYPE(None, TAssetID, c_int)
def progressCallBack(assetId, nProgress):
    print(assetId.ticker + ' | Progress | ' + str(nProgress))
    return

@WINFUNCTYPE(None, c_int, c_wchar_p, c_wchar_p, c_wchar_p)
def accountCallback(nCorretora, corretoraNomeCompleto, accountID, nomeTitular):
    print("Conta | " + accountID + ' - ' + nomeTitular + ' | Corretora ' + str(nCorretora) + ' - ' + corretoraNomeCompleto)
    return

@WINFUNCTYPE(None, TAssetID, c_int, c_int, c_int, c_int, c_int, c_double, POINTER(c_int), POINTER(c_int))
def priceBookCallback(assetId, nAction, nPosition, Side, nQtd, nCount, sPrice, pArraySell, pArrayBuy):
    if pArraySell is not None:
        print("todo - priceBookCallBack")
    return


@WINFUNCTYPE(None, TAssetID, c_wchar_p, c_uint, c_double, c_double, c_int, c_int, c_int, c_int, c_wchar)
def newTradeCallback(assetId, date, tradeNumber, price, vol, qtd, buyAgent, sellAgent, tradeType, bIsEdit):
    print(assetId.ticker + ' | Trade | ' + str(date) + '(' + str(tradeNumber) + ') ' + str(price))
    return


@WINFUNCTYPE(None, TAssetID, c_double, c_int, c_int)
def newTinyBookCallBack(assetId, price, qtd, side):
    if side == 0 :
        print(assetId.ticker + ' | TinyBook | Buy: ' + str(price) + ' ' + str(qtd))
    else :
        print(assetId.ticker + ' | TinyBook | Sell: ' + str(price) + ' ' + str(qtd))

    return


@WINFUNCTYPE(None, TAssetID, c_wchar_p, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double,
           c_double, c_int, c_int, c_int, c_int, c_int, c_int, c_int)
def newDailyCallback(assetID, date, sOpen, sHigh, sLow, sClose, sVol, sAjuste, sMaxLimit, sMinLimit, sVolBuyer,
                     sVolSeller, nQtd, nNegocios, nContratosOpen, nQtdBuyer, nQtdSeller, nNegBuyer, nNegSeller):
    print(assetID.ticker + ' | DailySignal | ' + date + ' Open: ' + str(sOpen) + ' High: ' + str(sHigh) + ' Low: ' + str(sLow) + ' Close: ' + str(sClose))
    return

price_array_sell = []
price_array_buy = []

def descript_offer_array_v2(price_array):
    price_array_descripted = []
    n_qtd = price_array[0]
    n_tam = price_array[1]
    print(f"qtd: {n_qtd}, n_tam: {n_tam}")

    arr = cast(price_array, POINTER(c_char))
    frame = bytearray()
    for i in range(n_tam):
        c = arr[i]
        frame.append(c[0])

    start = 8
    for i in range(n_qtd):
        price = struct.unpack('d', frame[start:start + 8])[0]
        start += 8
        qtd = struct.unpack('q', frame[start:start+8])[0]
        start += 8
        agent = struct.unpack('i', frame[start:start+4])[0]
        start += 4
        offer_id = struct.unpack('q', frame[start:start+8])[0]
        start += 8
        date_length = struct.unpack('h', frame[start:start+2])[0]
        start += 2
        date = frame[start:start+date_length]
        start += date_length

        price_array_descripted.append([price, qtd, agent, offer_id, date])

    return price_array_descripted

@WINFUNCTYPE(None, TAssetID, c_int, c_int, c_int, c_int, c_int, c_longlong, c_double, c_int, c_int, c_int, c_int, c_int,
           c_wchar_p, POINTER(c_int), POINTER(c_int))
def offerBookCallbackV2(assetId, nAction, nPosition, Side, nQtd, nAgent, nOfferID, sPrice, bHasPrice,
                      bHasQtd, bHasDate, bHasOfferID, bHasAgent, date, pArraySell, pArrayBuy):
    global price_array_buy
    global price_array_sell

    if bool(pArraySell):
        price_array_sell = descript_offer_array_v2(pArraySell)

    if bool(pArrayBuy):
        price_array_buy = descript_offer_array_v2(pArrayBuy)

    if Side == 0:
        lst_book = price_array_buy
    else:
        lst_book = price_array_sell

    if lst_book and 0 <= nPosition <= len(lst_book):
        """
        atAdd = 0
        atEdit = 1
        atDelete = 2
        atDeleteFrom = 3
        atFullBook = 4
        """
        if nAction == 0:
            group = [sPrice, nQtd, nAgent]
            idx = len(lst_book)-nPosition
            lst_book.insert(idx, group)
        elif nAction == 1:
            group = lst_book[-nPosition - 1]
            group[1] = group[1] + nQtd
            group[2] = group[2] + nAgent
        elif nAction == 2:
            del lst_book[-nPosition - 1]
        elif nAction == 3:
            del lst_book[-nPosition - 1:]
    return


@WINFUNCTYPE(None, TAssetID, c_wchar_p, c_uint, c_double)
def changeCotationCallback(assetId, date, tradeNumber, sPrice):
    print("todo - changeCotationCallback")
    return

@WINFUNCTYPE(None, TAssetID, c_wchar_p)
def assetListCallback(assetId, strName):
    print ("assetListCallback Ticker=" + str(assetId.ticker) + " Name=" + str(strName))
    return

@WINFUNCTYPE(None, TAssetID, c_double, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_uint, c_double)
def adjustHistoryCallbackV2(assetId, value, strType, strObserv, dtAjuste, dtDelib, dtPagamento, nFlags, dMult):
    print("todo - adjustHistoryCallbackV2")
    return

@WINFUNCTYPE(None, TAssetID, c_wchar_p, c_wchar_p, c_int, c_int, c_int, c_int, c_int, c_double, c_double, c_wchar_p, c_wchar_p)
def assetListInfoCallback(assetId, strName, strDescription, iMinOrdQtd, iMaxOrdQtd, iLote, iSecurityType, iSecuritySubType, dMinPriceInc, dContractMult, strValidDate, strISIN):
    print('TAssetListInfoCallback = Ticker: ' + str(assetId.ticker) +
          'Name: ' + str(strName) +
          'Descrição: ' + str(strDescription))
    return

@WINFUNCTYPE(None, TAssetID, c_wchar_p, c_wchar_p, c_int, c_int, c_int, c_int, c_int, c_double, c_double, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p)
def assetListInfoCallbackV2(assetId, strName, strDescription, iMinOrdQtd, iMaxOrdQtd, iLote, iSecurityType, iSecuritySubType, dMinPriceInc, dContractMult, strValidDate, strISIN, strSetor, strSubSetor, strSegmento):
    print('TAssetListInfoCallbackV2 = Ticker: ' + str(assetId.ticker) +
          'Name: ' + str(strName) +
          'Descrição: ' + str(strDescription) +
          'Setor: ' + str(strSetor))
    return

@WINFUNCTYPE(None, TConnectorOrderIdentifier)
def orderCallback(orderId : TConnectorOrderIdentifier):
    printOrder("", orderId, log_file="ordens.txt")

@WINFUNCTYPE(None, TConnectorAssetIdentifier)
def invalidAssetCallback(assetID : TConnectorAssetIdentifier):
    print("invalidAssetCallback: " + assetID.Ticker)

#END DEF

def wait_login():
    global bMarketConnected
    global bAtivo

    bWaiting = True
    while bWaiting:
        if bMarketConnected  :

            print("DLL Conected")

            bWaiting = False
    print('stop waiting')

def sendBuyMarketOrder():
    
    key = "1747419014493122621"
    user = "renan@mesasmartprop.com.br"
    password ="SmartProp2024@"

    profit_dll.DLLInitializeLogin(c_wchar_p(key), c_wchar_p(user), c_wchar_p(password), stateCallback, None, None, accountCallback,
                                              newTradeCallback, newDailyCallback, priceBookCallback,
                                              None, newHistoryCallback, progressCallBack, newTinyBookCallBack)
    profit_dll.DLLInitializeMarketLogin(c_wchar_p(key), c_wchar_p(user), c_wchar_p(password), stateCallback, newTradeCallback, newDailyCallback, priceBookCallback,
                                                 None, newHistoryCallback, progressCallBack, newTinyBookCallBack)
    
    wait_login()

    print(" ===[ENVIO ORDEM]=== ")

    brokerId = 513
    accountId = "1358568"
    subAccountId = "9"
    rotPassword = "Mic@123456"
    #Mic@123456 Mic@123456

    ticker = "WDOM25"
    exchange = "F"
    amount = 1

    send_order = TConnectorSendOrder(
        Version = 0,
        Password = rotPassword,
        OrderType = TConnectorOrderType.Market.value,
        OrderSide = TConnectorOrderSide.Buy.value,
        Price = -1,
        StopPrice = -1,
        Quantity = amount
    )
    send_order.AccountID = TConnectorAccountIdentifier(
        Version=0,
        BrokerID=brokerId,
        AccountID=accountId,
        #SubAccountID=subAccountId,
        Reserved=0
    )
    send_order.AssetID = TConnectorAssetIdentifier(
        Version=0,
        Ticker=ticker,
        Exchange=exchange,
        FeedType=0
    )

    profitID = profit_dll.SendOrder(byref(send_order))

    if evalDllReturn("SendOrder", profitID):
        print("ProfitID: " + str(profitID))

if __name__ == '__main__':
    sendBuyMarketOrder()