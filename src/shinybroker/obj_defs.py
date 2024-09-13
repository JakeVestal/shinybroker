from shinybroker.functionary import functionary


class Contract:
    """
    All tradable assets -- even stocks and currencies -- are 'contracts'.
    Whether you're placing a trade order, requesting market data,
    or searching for details about a particular financial instrument,
    the `Contract` object is how you specify to Interactive Brokers exactly
    *which* asset you're referring to.

    Parameters
    ----------
    contract_params : dict
        Dictionary for which each named element defines a contract property.
        See IBKR's [Contract Management](
        https://www.interactivebrokers.com/campus/ibkr-api-page/contracts/#contract-management
        ) documentation for more examples.
    contract_params : str or int
        If you pass a single string or an integer, it will be interpreted as
        `conId` in the resultant `Contract` object.
    contract_params : None
        Passing `None` (the default) to `Contract()` will return an empty
        instance of the `Contract` object class that you can manipulate by
        setting attributes directly.

    Returns
    -------
    Contract
        A Contract object that IBKR will understand to mean the tradable
        asset you are referring to.

    "Why not just use ticker"?
    ----------
    To see why we use a `Contract` object system instead of just referring to an
     asset by its symbol, pick a common ticker like "AAPL" and search for it
    using the "Matching Symbols" tool in ShinyBroker. You will quickly note
    that there are many contracts matching that description available for
    trading. The `Contract` object system lets you specify which asset you're
    interested in by allowing you to pass in additional parameters like
    *secType*, *currency*, *exchange*.

    Writing & Checking Contract Definitions
    ----------
    As a general rule of thumb, a well-defined `Contract` object uses the
    minimum number of specified parameters needed to uniquely define one
    single tradable asset. If you're unsure whether a `Contract` object
    you've created works, or whether it defines only one unique asset,
    you can copy-paste your code into the "Contract Details" tool in
    ShinyBroker. If it returns only one asset, and it's the asset that you
    had in mind, then you can be sure your definition is good.

    Contract ID is Sufficient On its Own
    ----------
    Every tradable asset at IBKR is given its own unique `conId`, which is
    the minimum information you need in order to specify that instrument. If
    you pass a single `int` or `str` object to the `Contract` constructor,
    then it will be treated as the `conId`.

    Three Ways of Creating / Updating Contracts
    ------------------
    **Way 1**: Instantiate a contract object and then assign parameters to the
    attributes as you require:
    ```
    from shinybroker import Contract
    aapl_contract = Contract()
    aapl_contract.symbol = "AAPL"
    aapl_contract.secType = "STK"
    aapl_contract.exchange = "SMART"
    aapl_contract.currency = "USD"
    ```

    **Way 2**: Pass everything in as a dictionary all at once:
    ```
    from shinybroker import Contract
    aapl_contract = Contract({
        'symbol': "AAPL",
        'secType': "STK",
        'exchange': "SMART",
        'currency': "USD"
    })
    ```

    **Way 3**: Pass in just the `conId` as a string or integer:
    *Note*: If you create contracts in this way then ShinyBroker will assume
    that since you didn't pass an `exchange` parameter the exchange doesn't
    matter to your use case and will create a contract object with
    `exchange='SMART'`, allowing IBKR to select the exchange its algorithm picks
     as 'best'.
    ```
    from shinybroker import Contract
    aapl_contract = Contract(265598)
    print(aapl_contract)
    aapl_contract = Contract("265598")
    print(aapl_contract)
    ```

    Compact Printing
    -----------
    By default, all instances of the `Contract()` class possess all
    attributes, but not all attributes are set to something meaningful. To
    understand this point, run:
    ```
    import shinybroker as sb
    aapl_us_stock = sb.Contract()
    aapl_us_stock.symbol = "AAPL"
    aapl_us_stock.secType = "STK"
    aapl_us_stock.exchange = "SMART"
    aapl_us_stock.currency = "USD"
    print(aapl_us_stock)
    ```
    ...and you will see that all parameters are represented in `aapl_us_stock`,
    but not all the parameters have meaningful, non-empty values (e.g, `strike`,
    because stocks don't have a strike price).

    To get a clean dictionary containing only the non-empty values, run:
    ```
    print(aapl_us_stock.compact())
    ```

    Use Compact to Copy Contract Objects
    ---------------
    Say you want to create contracts for the put and the call options for a
    particular strike, expiry, and underlying, so you write a code like this:
    ```
    import shinybroker as sb
    goog_call = sb.Contract({
        'symbol': 'GOOG',
        'secType': 'OPT',
        'exchange': 'SMART',
        'currency': 'USD',
        'lastTradeDateOrContractMonth': '20261218',
        'strike': 160,
        'right': 'C',
        'multiplier': '100'
    })
    goog_put = goog_call
    goog_put.right = "P"
    print(goog_call)
    print(goog_put)
    ```
    If you're used to Python, you know what's coming because... [mutability](
    https://shiny.posit.co/py/docs/reactive-mutable.html
    ). `goog_put` isn't a true copy of `goog_call`, it's just a pointer that
    points to the same value as `goog_call`. Therefore, when you ran
    `goog_put.right = "P"` you actually set the original value to "P" for
    "put" for **both** `goog_put` and `goog_call`.

    This inelegant solecism is a feature of Python that one must simply endure.
    You may, however, accomplish what you're after by using the `compact()`
    method on `goog_call` to instantiate a new object as in the modified
    code below, which correctly declares a put and a call contract as expected:
    ```
    import shinybroker as sb
    goog_call = sb.Contract({
        'symbol': 'GOOG',
        'secType': 'OPT',
        'exchange': 'SMART',
        'currency': 'USD',
        'lastTradeDateOrContractMonth': "20261218",
        'strike': 160,
        'right': 'C',
        'multiplier': '100'
    })
    goog_put = sb.Contract(goog_call.compact())
    goog_put.right = "P"
    print(goog_call)
    print(goog_put)
    ```

    "So why not always specify contracts using contract ID only"?
    --------------------
    If you're OK with always using the SMART exchange (the default),
    then you can. Go right ahead -- you can probably adopt that practice and
    build apps for quite a while without a problem. However, in some use
    cases it might be handy for you to NOT have to look up all the `conId`s
    and, instead, just loop through contract parameters like this:
    ```
    for strike in list_of_strikes:
        for expiry in list_of_expiries:
            goog_call = sb.Contract({
                'symbol': 'GOOG',
                'secType': 'OPT',
                'exchange': 'SMART',
                'currency': 'USD',
                'lastTradeDateOrContractMonth': expiry,
                'strike': strike,
                'right': 'C',
                'multiplier': '100'
            })
            goog_put = sb.Contract(goog_call.compact())
            goog_put.right = "P"
            your_super_clever_trading_logic(goog_call, goog_put)
    ```
    """
    def __init__(self, contract_params=None):
        if contract_params is None:
            for key, value in functionary['contract'].items():
                setattr(self, key, value)
        elif type(contract_params) is dict:
            contract_ = functionary['contract'].copy()
            contract_.update(contract_params)
            for key, value in contract_.items():
                setattr(self, key, value)
        else:
            contract_ = functionary['contract'].copy()
            contract_.update({'conId': contract_params})
            for key, value in contract_.items():
                setattr(self, key, value)

    def __repr__(self):
        return str(self.__dict__)

    def compact(self):
        def lentest(x):
            try:
                y = len(x) > 0
            except TypeError:
                y = True
            return y
        return {
            key: value for (key, value) in self.__dict__.items() if
            value is not None and value != 0 and value != '' and lentest(value)
        }


class ComboLeg:

    def __init__(self, comboleg_params={}):
        comboleg_ = functionary['combo_leg'].copy()
        comboleg_.update(comboleg_params)
        for key, value in comboleg_.items():
            setattr(self, key, value)

    def __repr__(self):
        return str(self.__dict__)


class DeltaNeutralContract:

    def __init__(self, dnt_params={}):
        dnt_ = functionary['delta_neutral_contract'].copy()
        dnt_.update(dnt_params)
        for key, value in dnt_.items():
            setattr(self, key, value)

    def __repr__(self):
        return str(self.__dict__)
