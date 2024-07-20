from shinybroker.functionary import functionary


class Contract:

    def __init__(self, contract_params={}):
        contract_ = functionary['contract'].copy()
        contract_.update(contract_params)
        for key, value in contract_.items():
            setattr(self, key, value)

    def __repr__(self):
        return str(self.__dict__)


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
