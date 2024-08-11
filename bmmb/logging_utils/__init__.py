from typing import Union

# from loguru import Logger
from logger_master.logger import MongoLogger


def get_logger(
        to_stdout=True,
        to_file=True, file_path='log.txt', rotation='1 Day', serialize=False,
        to_mongo=False, client=None, name=None, collection='logs', **kwargs
):
    if not to_mongo:
        from loguru import logger

        if not to_stdout:
            logger.remove(0)

        if to_file:
            logger.add(file_path, rotation=rotation, serialize=serialize,
                       **kwargs)

        return logger

    # to_mongo == True
    assert client is not None, "Client is required for MongoLogger"
    kwargs.update(
        mongo_instance=client,
        mongo_db=name,
        mongo_collection=collection,
        terminal_displayed=to_stdout,
        rotation=rotation,
        serialize=serialize
    )
    if to_file:
        kwargs['log_path'] = file_path

    logger = MongoLogger(**kwargs)
    return logger
