import pandas as pd

initial_rx_values = {
    'matching_symbols': {
        'stocks': pd.DataFrame(
            columns=[
                'con_id', 'symbol', 'sec_type', 'primary_exchange', 'currency',
                'derivative_sec_types', 'description'
            ]
        ),
        'bonds': pd.DataFrame(columns=['issuer', 'issuer_id'])
    }
}
