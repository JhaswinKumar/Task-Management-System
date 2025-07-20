import logging

class LoggerManager:
    @staticmethod
    def get_logger(name: str, log_file: str = "app.log", level=logging.INFO):
        logger = logging.getLogger(name)
        logger.setLevel(level)

        if not logger.handlers:  # Prevent duplicate handlers
            formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')

            # File handler
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)

            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)

            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

        return logger