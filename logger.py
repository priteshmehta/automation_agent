import logging
import json
import time
import os
import config

class JsonLogger:
    def __init__(self, log_path=None):
        log_dir = getattr(config, "LOG_DIR", "log")
        os.makedirs(log_dir, exist_ok=True)
        if log_path is None:
            log_path = os.path.join(log_dir, f"web_agent_{int(time.time())}.log")
        log_level = getattr(config, "LOG_LEVEL", "INFO").upper()
        level = getattr(logging, log_level, logging.INFO)
        self.logger = logging.getLogger("web_agent")
        self.logger.setLevel(level)
        fh = logging.FileHandler(log_path)
        fh.setLevel(level)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        fh.setFormatter(formatter)
        if not self.logger.hasHandlers():
            self.logger.addHandler(fh)

    def log(self, data, prefix="web_agent"):
        log_entry = {"prefix": prefix, "data": data}
        self.logger.info(json.dumps(log_entry))