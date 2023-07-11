import logging

my_logger = logging.getLogger(__name__)  # custom logger
my_logger.setLevel(logging.DEBUG)

# create handlers
stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler('hw_2.log', encoding='utf-8')
stream_handler.setLevel(logging.INFO)
file_handler.setLevel(logging.DEBUG)

# create parameters for handlers and add them to the handlers
stream_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(stream_format)
file_handler.setFormatter(file_format)

# add handlers to my_logger
my_logger.addHandler(stream_handler)
my_logger.addHandler(file_handler)
