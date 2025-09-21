import logging
import json
import time
import os
import config

class JsonLogger:
    def __init__(self, log_name="web_agent", console=True):
        log_dir = getattr(config, "LOG_DIR", "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, f"{log_name}_{int(time.time())}.log")
        log_level = getattr(config, "LOG_LEVEL", "INFO").upper()
        level = getattr(logging, log_level, logging.INFO)
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(level)
        fh = logging.FileHandler(log_path)
        fh.setLevel(level)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        fh.setFormatter(formatter)
        if not self.logger.hasHandlers():
            self.logger.addHandler(fh)
        if console:
            ch = logging.StreamHandler()
            ch.setLevel(level)
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

    def log(self, data, prefix="web_agent"):
        log_entry = {"prefix": prefix, "data": data}
        self.logger.info(json.dumps(log_entry))