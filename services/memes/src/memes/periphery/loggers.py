import logging


main_logger = logging.getLogger("main_logger")

main_logger.setLevel(logging.DEBUG)

_console_handler = logging.StreamHandler()

_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
_console_handler.setFormatter(_formatter)

main_logger.addHandler(_console_handler)
