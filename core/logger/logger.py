import datetime
import json
import logging
from pathlib import Path
from typing import Optional, Union

from core.logger.request_context import request_id_ctx_var


class Logger:
    def __init__(
        self,
        name: str = "fastapi",
        level: str = "INFO",
        rotation_days: int = 5,
        log_to_console: bool = True,
        log_file: Optional[str] = None,
    ):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
        self.logger.handlers = []

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        )

        # Terminal logging
        if log_to_console and not log_file:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

        # Arquivo com data no nome
        if log_file:
            self._setup_file_logging(log_file, rotation_days, formatter)

    def _setup_file_logging(self, base_path: str, rotation_days: int, formatter):
        today = datetime.datetime.now(datetime.UTC).strftime("%Y%m%d")
        base_path = Path(base_path)
        log_dir = base_path.parent
        app_name = base_path.stem 

        log_dir.mkdir(parents=True, exist_ok=True)

        dated_log_name = f"{today}-{app_name}.log"
        dated_log_path = log_dir / dated_log_name

        file_handler = logging.FileHandler(dated_log_path, encoding="utf-8")
        json_formatter = logging.Formatter("%(message)s")
        file_handler.setFormatter(json_formatter)
        self.logger.addHandler(file_handler)

        self._cleanup_old_logs(log_dir, app_name, rotation_days)

    def _cleanup_old_logs(self, log_dir: Path, app_name: str, keep_days: int):
        logs = sorted(
            [f for f in log_dir.glob(f"*-{app_name}.log") if f.name[:8].isdigit()],
            key=lambda f: f.name,
        )

        for file in logs[:-int(keep_days)]:
            file.unlink()

    def _log(
        self, level: str, data: Union[str, dict], request_id: Optional[str] = None
    ):
        current_request_id = request_id or request_id_ctx_var.get()
        if isinstance(data, dict):
            type_ = data.get("type", "Log")
            log_data = {k: v for k, v in data.items() if k != "type"}
        else:
            type_ = "Log"
            log_data = {"message": str(data)}

        log = {
            "timestamp": datetime.datetime.now(datetime.UTC).isoformat() + "Z",
            "level": level.upper(),
            "request_id": current_request_id,
            "type": type_,
            "data": log_data,
        }

        log_str = json.dumps(log)

        match level.upper():
            case "DEBUG":
                self.logger.debug(log_str)
            case "INFO":
                self.logger.info(log_str)
            case "WARNING":
                self.logger.warning(log_str)
            case "ERROR":
                self.logger.error(log_str)
            case _:
                self.logger.info(log_str)

    def debug(self, data: Union[str, dict], request_id: Optional[str] = None):
        self._log("DEBUG", data, request_id)

    def info(self, data: Union[str, dict], request_id: Optional[str] = None):
        self._log("INFO", data, request_id)

    def warning(self, data: Union[str, dict], request_id: Optional[str] = None):
        self._log("WARNING", data, request_id)

    def error(self, data: Union[str, dict], request_id: Optional[str] = None):
        self._log("ERROR", data, request_id)

    def get_logger(self):
        return self.logger
