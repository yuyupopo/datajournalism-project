import datetime
import logging
import logging.handlers
import os


def define_logger(log_path, verbose=False):
    LOG = logging.getLogger()

    log_level = logging.DEBUG if verbose else logging.INFO

    LOG.setLevel(log_level)

    formatter = logging.Formatter(
        '[%(levelname)s|%(filename)s:%(lineno)s] %(message)s > %(asctime)s')

    os.makedirs(log_path, exist_ok=True)

    file_handler = logging.FileHandler(
        os.path.join(log_path, '{}.log'.format(
            datetime.datetime.now().strftime('%Y-%m-%d:%H:%M:%S'))))
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.level = logging.WARNING

    LOG.addHandler(file_handler)
    LOG.addHandler(stream_handler)
