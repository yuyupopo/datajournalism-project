import datetime
import logging
import logging.handlers
import os

from christmas.common.util import colored


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
    file_handler.level = logging.DEBUG
    stream_handler = ColoredStreamHandler()
    stream_handler.level = logging.WARNING

    LOG.addHandler(file_handler)
    LOG.addHandler(stream_handler)


class ColoredStreamHandler(logging.StreamHandler):
    """Color the stream text accordingly"""

    def emit(self, record):
        try:
            msg = self.format(record)
            msg = self._color_text(msg, record.levelno)

            stream = self.stream
            stream.write(msg)
            stream.write(self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)

    def _color_text(self, msg, levelno):
        if levelno >= logging.ERROR:
            msg = colored(msg)
        return msg
