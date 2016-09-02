# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import os
import tempfile
import time

__author__ = "Tyson Smith"
__credits__ = ["Tyson Smith"]


class BaseWorker(object):
    """

    """
    name = "BaseWorker" # override in subclass

    def __init__(self):
        self._log = self._create_logfile()
        self._worker = None


    @staticmethod
    def _create_logfile():
        tmp_fd, log = tempfile.mkstemp(
            suffix="_log.txt",
            prefix=time.strftime("ffp_%m-%d_%H-%M-%S_worker"))
        os.close(tmp_fd)

        return log


    def clean_up(self):
        if os.path.isfile(self._log):
            os.remove(self._log)


    def collect_log(self):
        if self._worker.is_alive():
            raise RuntimeError("Worker must exit before collecting log")

        if not os.path.isfile(self._log):
            return None

        with open(self._log, "r") as log_fp:
            log_data = log_fp.read()

        return log_data.strip()


    def join(self):
        self._worker.join()