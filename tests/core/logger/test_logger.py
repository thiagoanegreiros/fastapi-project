import datetime
import json
import logging
from pathlib import Path

import pytest

from core.logger.logger import Logger
from core.logger.request_context import request_id_ctx_var


@pytest.fixture
def log_dir(tmp_path):
    return tmp_path


def test_creates_log_file_with_date(log_dir):
    log_path = log_dir / "app.log"
    logger = Logger(log_file=str(log_path), log_to_console=False)

    logger.info("Hello log")

    today = (
        Path(log_dir)
        / f"{datetime.datetime.now(datetime.UTC).strftime('%Y%m%d')}-app.log"
    )
    assert today.exists()
    content = today.read_text()
    assert "Hello log" in content


def test_logger_formats_json_and_includes_request_id(log_dir):
    log_path = log_dir / "app.log"
    request_id_ctx_var.set("abc-123")

    logger = Logger(log_file=str(log_path), log_to_console=False)
    logger.info({"type": "CustomType", "foo": "bar"})

    today_file = (
        Path(log_dir)
        / f"{datetime.datetime.now(datetime.UTC).strftime('%Y%m%d')}-app.log"
    )
    assert today_file.exists()

    lines = today_file.read_text().strip().splitlines()
    log_json = json.loads(lines[0])

    assert log_json["type"] == "CustomType"
    assert log_json["request_id"] == "abc-123"
    assert log_json["data"]["foo"] == "bar"


def test_logger_removes_old_logs(log_dir):
    rotation_days = 5

    # Criar 6 arquivos antigos (1 extra além do rotation_days)
    for i in range(6):
        date = (
            datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=i + 1)
        ).strftime("%Y%m%d")
        (log_dir / f"{date}-app.log").write_text("old log")

    # Isso criará o log de hoje (dia atual)
    Logger(
        log_file=str(log_dir / "app.log"),
        rotation_days=rotation_days,
        log_to_console=False,
    )

    # Após a limpeza, deve restar só os 5 mais recentes (incluindo o de hoje)
    remaining_files = list(log_dir.glob("*-app.log"))

    assert len(remaining_files) == rotation_days


def test_logger_respects_manual_request_id(log_dir):
    log_path = log_dir / "app.log"
    logger = Logger(log_file=str(log_path), log_to_console=False)

    logger.info("Manual ID test", request_id="manual-456")

    today_file = (
        log_dir / f"{datetime.datetime.now(datetime.UTC).strftime('%Y%m%d')}-app.log"
    )
    line = today_file.read_text().strip().splitlines()[0]
    log_json = json.loads(line)

    assert log_json["request_id"] == "manual-456"


@pytest.mark.parametrize("level", ["debug", "info", "warning", "error", "custom"])
def test_logger_handles_all_levels(level, log_dir):
    log_path = log_dir / "app.log"
    logger = Logger(log_file=str(log_path), log_to_console=False, level="DEBUG")

    logger._log(level, {"message": f"Testing {level}"})

    today_file = (
        log_dir / f"{datetime.datetime.now(datetime.UTC).strftime('%Y%m%d')}-app.log"
    )
    lines = today_file.read_text().strip().splitlines()
    assert lines, f"Log não foi escrito para nível: {level}"

    log_json = json.loads(lines[-1])
    assert log_json["level"] == level.upper()
    assert log_json["data"]["message"] == f"Testing {level}"


def test_logger_console_only(capsys):
    logging.getLogger("fastapi").handlers.clear()

    logger = Logger(log_to_console=True, log_file=None, level="INFO")
    logger.info("Hello console")

    captured = capsys.readouterr()
    assert "Hello console" in captured.out or "Hello console" in captured.err


def test_logger_uses_request_id_from_context(log_dir):
    log_path = log_dir / "app.log"
    request_id_ctx_var.set("from-context-789")

    logger = Logger(log_file=str(log_path), log_to_console=False)
    logger.info("Test with ctx")

    today_file = (
        Path(log_dir)
        / f"{datetime.datetime.now(datetime.UTC).strftime('%Y%m%d')}-app.log"
    )
    lines = today_file.read_text().strip().splitlines()
    log_json = json.loads(lines[-1])

    assert log_json["request_id"] == "from-context-789"


def test_logger_methods_cover_all_levels(log_dir):
    log_path = log_dir / "app.log"
    logger = Logger(log_file=str(log_path), log_to_console=False, level="DEBUG")

    logger.debug("Debug test")
    logger.warning("Warn test")
    logger.error("Error test")

    assert isinstance(logger.get_logger(), logging.Logger)

    today_file = (
        log_dir / f"{datetime.datetime.now(datetime.UTC).strftime('%Y%m%d')}-app.log"
    )
    lines = today_file.read_text().strip().splitlines()
    assert len(lines) >= 3
