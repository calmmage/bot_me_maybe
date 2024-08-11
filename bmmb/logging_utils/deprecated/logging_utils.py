

def configure_logger(
        logger,
        to_stdout=True,
        to_disk=True, log_path=None,
        to_mongo=True, mongo_db=None, mongo_table_name=None
):
    if to_stdout:
        if not any(
                isinstance(h, logging.StreamHandler) for h in logger.handlers):
            handler = create_console_handler()
            logger.addHandler(handler)

    if to_disk:
        if not any(isinstance(h, logging.FileHandler) for h in logger.handlers):
            # todo: check if disk destination is available
            handler = create_file_handler(log_path)
            logger.addHandler(handler)

    if to_mongo:
        if not any(isinstance(h, MongoHandler) for h in logger.handlers):
            # todo: check if mongo destination is available
            handler = create_mongo_handler(mongo_db, mongo_table_name)
            logger.addHandler(handler)

    return logger
def create_file_handler(log_path=None, level=None):
    if log_path is None:
        log_path = os.getenv('LOGGING_FILE_PATH', 'logs.txt')
    handler = logging.FileHandler(log_path)
    if level is not None:
        handler.setLevel(level)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    return handler

def create_console_handler():
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    return handler

def create_mongo_handler(mongo_conn_str, mongo_table_name):
    if mongo_conn_str is None:
        mongo_conn_str = os.getenv('MONGO_CONNECTION_STRING')
    if mongo_table_name is None:
        mongo_table_name = os.getenv('MONGO_TABLE_NAME', 'logs')
    mongoengine.connect(db=app_name, alias=app_alias, host=mongo_conn_str)
    mongo_table = MongoTable(mongo_table_name, LogItem)
#     handler = MongoHandler(mongo_table, level=logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    return handler


logger = logging.getLogger(logger_name)
logger.setLevel(logging.DEBUG)
