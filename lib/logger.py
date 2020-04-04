import time
import datetime

class Logger():
    def __init__(self):
        self.buffer = []
        startDate = datetime.datetime.now().isoformat()
        self._file = None
        self._openLogFile()
        self._startTime = time.monotonic()
        self.log('#' * 80)
        self.log('Application started at {}'.format(startDate))

    def _openLogFile(self):
        self._file = open('RMTS.log', 'a')

    def log(self, message):
        self._write('LOG', message)

    def warn(self, message):
        self._write('WRN', message)

    def error(self, message):
        self._write('ERR', message)

    def _write(self, level, content):
        message = '{:.4f} [{}] {}'.format(time.monotonic() - self._startTime, level, content)
        print(message)
        if self._file is not None:
            self._file.write('{}\n'.format(message))
            self._file.flush()

logger = Logger()
