from tron import TronUtil

if __name__ == '__main__':

    #1 是主网 0是测试网
    TronUtil().set_network(1)
    #主网api token
    TronUtil().set_api_token("c0139474-6109-4b65-9a54-743cb1b2692f")
    key = "你的私钥"
    print("交易转账演示")
    print("------------------------------")
    print("USDT转账")
    print("------------------------------"
    print(TronUtil().tron_easy_transfer_usdt(key, "TTBpmGEF4GYGQfseZet1QVmQNDVz999999", 1 * 1000000,"TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"))
    print("TRX转账")
    print("------------------------------")
    print(TronUtil().tron_easy_transfer(key, "TTBpmGEF4GYGQfseZet1QVmQNDVz999999", 1 * 1000000))

    print("获取交易演示")
    print("------------------------------")
    print(TronUtil().get_transactions_trc20("TTBpmGEF4GYGQfseZet1QVmQNDVz999999",contract_address="TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"))
