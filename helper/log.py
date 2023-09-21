import logging


def load_logging(name):
    # create a custom logger and set to INFO level
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # create logging format
    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # create handlers
    # log_file_path = os.path.abspath("log_records/") tried specifying directory to save log files wasn't successful.

    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler("{name}.log".format(name=name))

    # setting the format the log records will be saved
    console_handler.setFormatter(log_format)
    file_handler.setFormatter(log_format)

    # add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger
