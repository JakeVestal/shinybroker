import struct, datetime, re

import pandas as pd

from shiny import ui
from shinybroker.obj_defs import Contract


def pack_element(msg_emt) -> str:
    match type(msg_emt).__name__:
        case 'str':
            return msg_emt + "\0"
        case 'NoneType':
            raise ValueError("Cannot send None to a message function")
        case 'bool':
            return str(int(msg_emt)) + "\0"
        case _:
            return str(msg_emt) + "\0"


def pack_message(msg_txt) -> bytes:
    return struct.pack(
        f"!I{len(msg_txt)}s",
        len(msg_txt),
        str.encode(msg_txt)
    )

def formatter2(hrs_str):

    z = [y.split("-") for y in [x for x in hrs_str.split(";")]]

    for i in range(len(z)):
        if len(z[i]) == 1 and z[i][0].split(":")[1] == 'CLOSED':
            z[i] = [z[i][0], z[i][0]]

    df = pd.merge(
        pd.DataFrame(
            data={
                "end_time": [a[1].split(":")[1] for a in z]
            },
            index=[datetime.datetime.strptime(x, "%Y%m%d").date()
                   for x in [a[1].split(":")[0] for a in z]]
        ),
        pd.DataFrame(
            data = {
                "start_time": [a[0].split(":")[1] for a in z]
            },
            index = [datetime.datetime.strptime(x, "%Y%m%d").date()
                     for x in [a[0].split(":")[0] for a in z]]
        ),
        left_index=True,
        right_index=True,
        how="outer"
    )

    df = df.fillna('')

    return df


def remove_contractinator_modal():
    ui.modal_remove()
    ui.remove_ui(
        selector="#contractinator_validate_table_div",
        immediate=True
    )


def inject_js(
        script_str: str,
        selector: str = "body",
        where: str = "beforeEnd"
):
    ui.insert_ui(
        ui.tags.script(script_str, id="sb_injected_script"),
        selector = "body",
        where = "beforeEnd"
    )
    ui.remove_ui("#sb_injected_script")

def add_contractinator_btns_column(df):
    end_index = df.shape[0]
    df[" "] = [
        ui.input_action_button(
            id=f"contractinator_add_a_row{i}",
            label="+",
            onclick=f"add_a_contractinator_row({i})"
        ).add_class("plus-button") for i in range(0, end_index)
    ]
    if(df.shape[0] == 1):
        df["  "] = ['']
    else:
        df["  "] = [
            ui.input_action_button(
                id=f"contractinator_remove_a_row{i}",
                label=ui.span("-"),
                onclick=f"rmv_a_contractinator_row({i})"
            ).add_class("minus-button") for i in range(0, end_index)
        ]

    df.reset_index()
    return df

def is_valid_html_id(id_string):
    # Check if the string is empty
    if not id_string:
        return False

    # Check for whitespace
    if re.search(r'\s', id_string):
        return False

    # Check if it starts with a letter or underscore, followed by ONLY:
        # letters, digits, hyphens, or underscores
    # HTML5 is more permissive, but this approach is safer for CSS and
        # cross-browser compatibility
    pattern = r'^[a-zA-Z_][a-zA-Z0-9_-]*$'
    return bool(re.match(pattern, id_string))

def check_if_string_is_contract_definition(list_or_string_might_be_contracts):
    # Accepts a string or a list of strings that should contain a contract
    # definition of the form:
    #   contract_name = Contract({definition}) or
    #   contract_name = sb.Contract({definition})
    # If a sring is passed into list_or_string_might_be_contracts, returns true
    #   if the string is a valid line of code defining a single contract, false
    #   otherwise, and prints any exceptions encountered.
    if isinstance(list_or_string_might_be_contracts, str):
        might_be_a_contract_def_str = list_or_string_might_be_contracts
        try:
            namespace = {}
            exec('from shinybroker import Contract', namespace)
            exec(might_be_a_contract_def_str, namespace)
        except Exception as e:
            print("There was an error in evaluating the contract definition \""
                  f"{might_be_a_contract_def_str}\".")
            print(f"error: {e}")
            return None


    contract_list = []



    return True
