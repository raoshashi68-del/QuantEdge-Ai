# Trade logger module
"""
==========================================================
Logger
==========================================================
"""

import logging

from pathlib import Path

from config import LOG_DIR


LOG_FILE = Path(LOG_DIR) / "quantedge.log"


logger = logging.getLogger("QuantEdge")

logger.setLevel(logging.INFO)


formatter = logging.Formatter(

    "%(asctime)s | %(levelname)s | %(message)s"

)


file_handler = logging.FileHandler(LOG_FILE)

file_handler.setFormatter(formatter)


console_handler = logging.StreamHandler()

console_handler.setFormatter(formatter)


logger.addHandler(file_handler)

logger.addHandler(console_handler)