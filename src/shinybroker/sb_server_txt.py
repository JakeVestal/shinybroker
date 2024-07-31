import os
import re

with (open(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "sb_server.py"
        ), "r"
) as f):
    sb_server_code = re.sub(
        "\n    ",
        "\n",
        re.sub("\n\ndef sb_server.*?\n", "", f.read())
    )
