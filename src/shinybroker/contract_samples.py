contract_samples = {
	"""contract = Contract()
contract.symbol="AAPL"
contract.secType="STK"
contract.exchange="SMART"
contract.currency="USD"
""": 'Apple Inc. (Stock)',
	"""contract = Contract()
contract.symbol = "GOOG"
contract.secType = "OPT"
contract.exchange = "SMART"
contract.currency = "USD"
contract.lastTradeDateOrContractMonth = "20261218"
contract.strike = 160
contract.right = "C"
contract.multiplier = "100"
""": 'Google Call Option (US Option)',
	"""contract = Contract()
contract.symbol = "IBKR,MCD"
contract.secType = "BAG"
contract.currency = "USD"
contract.exchange = "SMART"

leg1 = ComboLeg()
leg1.conId = 43645865
leg1.ratio = 1
leg1.action = "BUY"
leg1.exchange = "SMART"

leg2 = ComboLeg()
leg2.conId = 9408
leg2.ratio = 1
leg2.action = "SELL"
leg2.exchange = "SMART"

contract.comboLegs.append(leg1)
contract.comboLegs.append(leg2)
""": 'IBKR and MCD Stock Combo (BAG)',
	"""contract = Contract()
contract.symbol = 'DAX'
contract.secType = 'IND'
contract.currency = 'EUR'
contract.exchange = 'EUREX'
""": 'Index',
"""contract = Contract()
contract.secIdType = 'ISIN'
contract.secId = 'US45841N1072'
contract.exchange = 'SMART'
contract.currency = 'USD'
contract.secType = 'STK'""": 'ByISIN',
	'contract = Contract()\ncontract.symbol = "EUR"\ncontract.secType = "CASH"\ncontract.currency = "GBP"\ncontract.exchange = "IDEALPRO"': 'EurGbpFx',
	'contract = Contract()\ncontract.symbol = "IBDE30"\ncontract.secType = "CFD"\ncontract.currency = "EUR"\ncontract.exchange = "SMART"': 'CFD',
	'contract = Contract()\ncontract.symbol = "BMW"\ncontract.secType = "STK"\ncontract.currency = "EUR"\ncontract.exchange = "SMART"\ncontract.primaryExchange = "IBIS"': 'EuropeanStock',
	'contract = Contract()\ncontract.symbol = "NOKIA"\ncontract.secType = "STK"\ncontract.currency = "EUR"\ncontract.exchange = "SMART"\ncontract.primaryExchange = "HEX"': 'EuropeanStock2',
	'contract = Contract()\ncontract.symbol = "COF"\ncontract.secType = "OPT"\ncontract.currency = "USD"\ncontract.exchange = "ISE"\ncontract.lastTradeDateOrContractMonth = "20190315"\ncontract.right = "P"\ncontract.strike = 105\ncontract.multiplier = "100"': 'OptionAtIse',
	'contract = Contract()\ncontract.symbol= "449276AA2"\ncontract.secType = "BOND"\ncontract.exchange = "SMART"\ncontract.currency = "USD"': 'BondWithCusip',
	'contract = Contract()\ncontract.conId = 456467716\ncontract.exchange = "SMART"': 'Bond',
	'contract = Contract()\ncontract.symbol = "VINIX"\ncontract.secType = "FUND"\ncontract.exchange = "FUNDSERV"\ncontract.currency = "USD"': 'MutualFund',
	'contract = Contract()\ncontract.symbol = "XAUUSD"\ncontract.secType = "CMDTY"\ncontract.exchange = "SMART"\ncontract.currency = "USD"': 'Commodity',
	'contract = Contract()\ncontract.symbol = "SPY"\ncontract.secType = "STK"\ncontract.currency = "USD"\ncontract.exchange = "ARCA"': 'USStock',
	'contract = Contract()\ncontract.symbol = "SPY"\ncontract.secType = "STK"\ncontract.currency = "USD"\ncontract.exchange = "SMART"\ncontract.primaryExchange = "ARCA"': 'USStockWithPrimaryExch',
	'contract = Contract()\ncontract.symbol = "IBM"\ncontract.secType = "STK"\ncontract.currency = "USD"\ncontract.exchange = "SMART"': 'USStockAtSmart',
	'contract = Contract()\ncontract.symbol = "QQQ"\ncontract.secType = "STK"\ncontract.currency = "USD"\ncontract.exchange = "SMART"': 'etf',
	'contract = Contract()\ncontract.symbol = "GOOG"\ncontract.secType = "OPT"\ncontract.exchange = "BOX"\ncontract.currency = "USD"\ncontract.lastTradeDateOrContractMonth = "20190315"\ncontract.strike = 1180\ncontract.right = "C"\ncontract.multiplier = "100"': 'OptionAtBOX',
	'contract = Contract()\ncontract.symbol = "SANT"\ncontract.secType = "OPT"\ncontract.exchange = "MEFFRV"\ncontract.currency = "EUR"\ncontract.lastTradeDateOrContractMonth = "20190621"\ncontract.strike = 7.5\ncontract.right = "C"\ncontract.multiplier = "100"\ncontract.tradingClass = "SANEU"': 'OptionWithTradingClass',
	'contract = Contract()\ncontract.localSymbol = "P BMW  20221216 72 M"\ncontract.secType = "OPT"\ncontract.exchange = "EUREX"\ncontract.currency = "EUR"': 'OptionWithLocalSymbol',
	'contract = Contract()\ncontract.localSymbol = "B881G"\ncontract.secType = "IOPT"\ncontract.exchange = "SBF"\ncontract.currency = "EUR"': 'DutchWarrant',
	'contract = Contract()\ncontract.symbol = "GBL"\ncontract.secType = "FUT"\ncontract.exchange = "EUREX"\ncontract.currency = "EUR"\ncontract.lastTradeDateOrContractMonth = "202303"': 'SimpleFuture',
	'contract = Contract()\ncontract.secType = "FUT"\ncontract.exchange = "EUREX"\ncontract.currency = "EUR"\ncontract.localSymbol = "FGBL MAR 23"': 'FutureWithLocalSymbol',
	'contract = Contract()\ncontract.symbol = "DAX"\ncontract.secType = "FUT"\ncontract.exchange = "EUREX"\ncontract.currency = "EUR"\ncontract.lastTradeDateOrContractMonth = "202303"\ncontract.multiplier = "1"': 'FutureWithMultiplier',
	'contract = Contract()\ncontract.symbol = " IJR "\ncontract.conId = 9579976\ncontract.secType = "STK"\ncontract.exchange = "SMART"\ncontract.currency = "USD"': 'WrongContract',
	'contract = Contract()\ncontract.symbol = "GBL"\ncontract.secType = "FOP"\ncontract.exchange = "EUREX"\ncontract.currency = "EUR"\ncontract.lastTradeDateOrContractMonth = "20230224"\ncontract.strike = 138\ncontract.right = "C"\ncontract.multiplier = "1000"': 'FuturesOnOptions',
	'contract = Contract()\ncontract.symbol = "GOOG"\ncontract.secType = "WAR"\ncontract.exchange = "FWB"\ncontract.currency = "EUR"\ncontract.lastTradeDateOrContractMonth = "20201117"\ncontract.strike = 1500.0\ncontract.right = "C"\ncontract.multiplier = "0.01"': 'Warrants',
	'contract = Contract()\ncontract.secType = "CASH"\ncontract.conId = 12087792\ncontract.exchange = "IDEALPRO"': 'ByConId',
	'contract = Contract()\ncontract.symbol = "FISV"\ncontract.secType = "OPT"\ncontract.exchange = "SMART"\ncontract.currency = "USD"': 'OptionForQuery',
	'contract = Contract()\ncontract.symbol = "DBK"\ncontract.secType = "BAG"\ncontract.currency = "EUR"\ncontract.exchange = "EUREX"\nleg1 = ComboLeg()\nleg1.conId = 577164786\nleg1.ratio = 1\nleg1.action = "BUY"\nleg1.exchange = "EUREX"\nleg2 = ComboLeg()\nleg2.conId = 577164767\nleg2.ratio = 1\nleg2.action = "SELL"\nleg2.exchange = "EUREX"\ncontract.comboLegs = []\ncontract.comboLegs.append(leg1)\ncontract.comboLegs.append(leg2)': 'OptionComboContract',
	'contract = Contract()\ncontract.symbol = "VIX"\ncontract.secType = "BAG"\ncontract.currency = "USD"\ncontract.exchange = "CFE"\nleg1 = ComboLeg()\nleg1.conId = 326501438\nleg1.ratio = 1\nleg1.action = "BUY"\nleg1.exchange = "CFE"\nleg2 = ComboLeg()\nleg2.conId = 323072528\nleg2.ratio = 1\nleg2.action = "SELL"\nleg2.exchange = "CFE"\ncontract.comboLegs = []\ncontract.comboLegs.append(leg1)\ncontract.comboLegs.append(leg2)': 'FutureComboContract',
	'contract = Contract()\ncontract.symbol = "WTI"\ncontract.secType = "BAG"\ncontract.currency = "USD"\ncontract.exchange = "SMART"\nleg1 = ComboLeg()\nleg1.conId = 55928698\nleg1.ratio = 1\nleg1.action = "BUY"\nleg1.exchange = "IPE"\nleg2 = ComboLeg()\nleg2.conId = 55850663\nleg2.ratio = 1\nleg2.action = "SELL"\nleg2.exchange = "IPE"\ncontract.comboLegs = []\ncontract.comboLegs.append(leg1)\ncontract.comboLegs.append(leg2)': 'SmartFutureComboContract',
	'contract = Contract()\ncontract.symbol = "COL.WTI"\ncontract.secType = "BAG"\ncontract.currency = "USD"\ncontract.exchange = "IPE"\nleg1 = ComboLeg()\nleg1.conId = 183405603\nleg1.ratio = 1\nleg1.action = "BUY"\nleg1.exchange = "IPE"\nleg2 = ComboLeg()\nleg2.conId = 254011009\nleg2.ratio = 1\nleg2.action = "SELL"\nleg2.exchange = "IPE"\ncontract.comboLegs = []\ncontract.comboLegs.append(leg1)\ncontract.comboLegs.append(leg2)': 'InterCmdtyFuturesContract',
	'contract = Contract()\ncontract.secType = "NEWS"\ncontract.exchange = "BRFG"': 'NewsFeedForQuery',
	'contract = Contract()\ncontract.symbol  = "BRF:BRF_ALL"\ncontract.secType = "NEWS"\ncontract.exchange = "BRF"': 'BTbroadtapeNewsFeed',
	'contract = Contract()\ncontract.symbol = "BZ:BZ_ALL"\ncontract.secType = "NEWS"\ncontract.exchange = "BZ"': 'BZbroadtapeNewsFeed',
	'contract = Contract()\ncontract.symbol  = "FLY:FLY_ALL"\ncontract.secType = "NEWS"\ncontract.exchange = "FLY"': 'FLYbroadtapeNewsFeed',
	'contract = Contract()\ncontract.symbol = "GBL"\ncontract.secType = "CONTFUT"\ncontract.exchange = "EUREX"': 'ContFut',
	'contract = Contract()\ncontract.symbol = "GBL"\ncontract.secType = "FUT+CONTFUT"\ncontract.exchange = "EUREX"': 'ContAndExpiringFut',
	'contract = Contract()\ncontract.symbol = "AAPL"\ncontract.secType = "STK"\ncontract.exchange = "JEFFALGO"\ncontract.currency = "USD"': 'JefferiesContract',
	'contract = Contract()\ncontract.symbol = "IBKR"\ncontract.secType = "STK"\ncontract.exchange = "CSFBALGO"\ncontract.currency = "USD"': 'CSFBContract',
	'contract = Contract()\ncontract.symbol = "IBM"\ncontract.secType = "CFD"\ncontract.currency = "USD"\ncontract.exchange = "SMART"': 'USStockCFD',
	'contract = Contract()\ncontract.symbol = "BMW"\ncontract.secType = "CFD"\ncontract.currency = "EUR"\ncontract.exchange = "SMART"': 'EuropeanStockCFD',
	'contract = Contract()\ncontract.symbol = "EUR"\ncontract.secType = "CFD"\ncontract.currency = "USD"\ncontract.exchange = "SMART"': 'CashCFD',
	'contract = Contract()\ncontract.symbol = "ES"\ncontract.secType = "FUT"\ncontract.exchange = "QBALGO"\ncontract.currency = "USD"\ncontract.lastTradeDateOrContractMonth = "202003"': 'QBAlgoContract',
	'contract = Contract()\ncontract.symbol = "SPY"\ncontract.secType = "STK"\ncontract.currency = "USD"\ncontract.exchange = "IBKRATS"': 'IBKRATSContract',
	'contract = Contract()\ncontract.symbol = "ETH"\ncontract.secType = "CRYPTO"\ncontract.currency = "USD"\ncontract.exchange = "PAXOS"': 'CryptoContract',
	'contract = Contract()\ncontract.symbol = "EMCGU"\ncontract.secType = "STK"\ncontract.currency = "USD"\ncontract.exchange = "SMART"': 'StockWithIPOPrice',
	'contract = Contract()\ncontract.secIdType = "FIGI"\ncontract.secId = "BBG000B9XRY4"\ncontract.exchange = "SMART"': 'ByFIGI',
	'contract = Contract()\ncontract.issuerId = "e1453318"': 'ByIssuerId',
	'contract = Contract()\ncontract.symbol = "I406801954"\ncontract.secType = "FUND"\ncontract.exchange = "ALLFUNDS"\ncontract.currency = "USD"': 'FundContract'
}