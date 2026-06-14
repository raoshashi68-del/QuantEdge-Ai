"""
==========================================================

QuantEdge AI

Logger

Responsibilities
----------------
1. Console Logging
2. File Logging
3. Timestamp Logging
4. Error Logging

==========================================================
"""

import logging
import os


class QuantLogger:

    def __init__(

        self,

        name="QuantEdge",

        log_folder="logs",

    ):

        os.makedirs(log_folder, exist_ok=True)

        self.logger = logging.getLogger(name)

        self.logger.setLevel(logging.INFO)

        if not self.logger.handlers:

            formatter = logging.Formatter(

                "%(asctime)s | %(levelname)s | %(message)s"

            )

            file_handler = logging.FileHandler(

                os.path.join(

                    log_folder,

                    "quantedge.log"

                )

            )

            file_handler.setFormatter(formatter)

            console_handler = logging.StreamHandler()

            console_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)

            self.logger.addHandler(console_handler)

    # ------------------------------------------

    def info(self, message):

        self.logger.info(message)

    # ------------------------------------------

    def warning(self, message):

        self.logger.warning(message)

    # ------------------------------------------

    def error(self, message):

        self.logger.error(message)

    # ------------------------------------------

    def debug(self, message):

        self.logger.debug(message)