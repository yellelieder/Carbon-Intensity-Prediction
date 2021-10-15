import logging
from epi import config
add=logging.getLogger(__name__)
add.setLevel(logging.INFO)
handler=logging.FileHandler(f"epi{config.slash}logs.log")
handler.setFormatter(logging.Formatter("%(asctime)s:%(filename)s:%(funcName)s:%(message)s"))
add.addHandler(handler)
