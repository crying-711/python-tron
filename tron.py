import ctypes
import sys
import time
from ctypes import cdll, c_char_p,c_int
import os


#使用单利模式
class TronUtil(object):
    # 静态变量
    _instanc = None
    _flag = False

    def __new__(cls, *args, **kwargs):

        if cls._instanc is None:
            cls._instanc = super().__new__(cls)
        return cls._instanc

    def __init__(self):
        if not TronUtil._flag:

            if sys.platform != "win32":
                self.lib = cdll.LoadLibrary("library/libsigntron-amd64-linux.so")
            else:
                self.lib = cdll.LoadLibrary("library/signtron-amd64-winnt.dll")

            self.lib.tron_transaction_sign_trc10.restype = c_char_p
            self.lib.tron_transaction_sign_trc20.restype = c_char_p
            self.lib.tron_easy_transfer.restype = c_char_p
            self.lib.tron_easy_transfer_usdt.restype = c_char_p
            self.lib.getTransactions.restype = c_char_p
            self.lib.getTransactionsTRC20.restype = c_char_p


            TronUtil._flag = True

    # 转账TRX
    def tron_easy_transfer(self, key, to_address, amount):
        to_address_l = c_char_p(bytes(to_address, 'utf-8'))
        key_l = c_char_p(bytes(key, 'utf-8'))
        return self.lib.tron_easy_transfer(key_l, to_address_l, amount).decode('UTF-8')


    # TRC20 转账 也就是USDT转账  key是私钥 to_address 是转账地址  amount 是金额 contract是合约地址
    def tron_easy_transfer_usdt(self, key, to_address, amount, contract="TG3XXyExBkPp9nzdajDZsozEu4BkaSJozs"):
        to_address_l = c_char_p(bytes(to_address, 'utf-8'))
        key_l = c_char_p(bytes(key, 'utf-8'))
        contract_l = c_char_p(bytes(contract, 'utf-8'))

        return self.lib.tron_easy_transfer_usdt(key_l, to_address_l, amount, contract_l).decode('UTF-8')


    # TRC10 交易签名 inp 是创建交易后的json key是私钥

    def tron_transaction_sign_trc10(self, inp, key):
        in_l = c_char_p(bytes(inp, 'utf-8'))
        key_l = c_char_p(bytes(key, 'utf-8'))
        return self.lib.tron_transaction_sign_trc10(in_l, key_l).decode('UTF-8')

    # TRC20 交易签名 inp 是创建交易后的json key是私钥
    def tron_transaction_sign_trc20(self, inp, key):
        in_l = c_char_p(bytes(inp, 'utf-8'))
        key_l = c_char_p(bytes(key, 'utf-8'))
        return self.lib.tron_transaction_sign_trc20(in_l, key_l).decode('UTF-8')

    # 1是主网  2是测试网
    def set_network(self, network=2):
        self.lib.setNetWork(network)

    #设置api key token是key
    def set_api_token(self, token):
        self.lib.setApiToken( c_char_p(bytes(token, 'utf-8')))

    #    获取交易信息根据合约
    #    1是fase 0是true
    def get_transactions_trc20(self, address, only_to=1, only_from=1, limit=20, fingerprint="", min_timestamp=0,
                               max_timestamp=int(time.time()), search_internal=1,
                               contract_address="TG3XXyExBkPp9nzdajDZsozEu4BkaSJozs"):
        return self.lib.getTransactionsTRC20(c_char_p(bytes(address, 'utf-8')), only_to, only_from, limit,  c_char_p(bytes(fingerprint,'utf-8')),
                                             max_timestamp, max_timestamp, search_internal,
                                             c_char_p(bytes(contract_address, 'utf-8'))).decode('UTF-8')
    #获取交易
    def get_transactions(self, address, only_to=1, only_from=1, limit=20, fingerprint="", min_timestamp=0,
                         max_timestamp=int(time.time()), search_internal=1):
        return self.lib.getTransactions(c_char_p(bytes(address, 'utf-8')), only_to, only_from, limit,  c_char_p(bytes(fingerprint,'utf-8')),
                                        max_timestamp, max_timestamp, search_internal).decode('UTF-8')


if __name__ == '__main__':
    print()

    print(TronUtil().get_transactions("TFTGMfp7hvDtt4fj3vmWnbYsPSmw5EU8oX"))

    TronUtil().set_api_token("sb")

    key = "2d2c8062fa668ea168172d0926f391c033b4c3699c3b79afed028b027e05bb31"
    # json='{"result":{"result":true},"transaction":{"visible":true,"txID":"6b501aaae1d82a3d30fd1c5b50305bb0e24bd92d3589cf99ed458371781ceca9","raw_data":{"contract":[{"parameter":{"value":{"data":"a9059cbb0000000000000000000000003c2713a6d04e74b1fe0f9a370c7e96aad21268dd000000000000000000000000000000000000000000000000000000001dcd6500","owner_address":"TJigfkHs1QrbZbKwWd7CY7HSUKLX71FFFF","contract_address":"TG3XXyExBkPp9nzdajDZsozEu4BkaSJozs"},"type_url":"type.googleapis.com/protocol.TriggerSmartContract"},"type":"TriggerSmartContract"}],"ref_block_bytes":"a2f1","ref_block_hash":"d22237be586463e3","expiration":1667042817000,"fee_limit":1000000000,"timestamp":1667042759371},"raw_data_hex":"0a02a2f12208d22237be586463e340e8e7fa9bc2305aae01081f12a9010a31747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e54726967676572536d617274436f6e747261637412740a15415ff9fce781452ce0a031472d8a58fae6c8cc70b612154142a1e39aefa49290f2b3f9ed688d7cecf86cd6e02244a9059cbb0000000000000000000000003c2713a6d04e74b1fe0f9a370c7e96aad21268dd000000000000000000000000000000000000000000000000000000001dcd650070cba5f79bc23090018094ebdc03"}}'
    # print(Native().tron_transaction_sign_trc20(json,key))
    # print(Native().tron_transaction_sign_trc10(json,key))
    # print(Native().tron_transaction_sign_trc10(json,key))
    # print(Native().tron_transaction_sign_trc10(json,key))
    print(TronUtil().tron_easy_transfer_usdt(key, "TFTGMfp7hvDtt4fj3vmWnbYsPSmw5EU8oX", 10 * 1000000))
    # print(  Native().tron_easy_transfer(key,"TFTGMfp7hvDtt4fj3vmWnbYsPSmw5EU8oX",10*1000000))
