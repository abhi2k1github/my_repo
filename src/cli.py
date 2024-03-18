import click
import uvicorn
import socket
from IPython.core.ultratb import VerboseTB
import os
from configs.definitions import ROOT_DIR
import datetime
import logging
import sys
import IPython
from IPython.terminal.ipapp import load_default_config
from database.db_session import db
from configs.definitions import ROOT_DIR
from IPython.core.profiledir import ProfileDir

EXEC_LINES = [
    "%load_ext autoreload",
    "%autoreload 2",
]

EXCLUDE_FILES = ["setup.py", "env.py"]


def configure_logger(level=logging.DEBUG):
    loggers = ("peewee", "httpx")
    handler = logging.StreamHandler()
    handler.setFormatter(
        ColoredFormatter(
            "%(levelname)s:%(message)s:%(pathname)s:%(funcName)s:%(lineno)d"
        )
    )
    for logger in loggers:
        logger = logging.getLogger(logger)
        logger.addHandler(handler)
        logger.setLevel(level)


class ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\x1b[38;5;39m",  # Blue
        "INFO": "\033[92m",  # Green
        "WARNING": "\033[31m",  # Orange
        "ERROR": "\033[91m",  # Red
        "CRITICAL": "\033[91m",  # Red
        "RESET": "\033[0m",  # Reset color
    }

    def _query_val_transform(self, v):
        if isinstance(v, bool):
            pass
        elif isinstance(v, (str, datetime.datetime, datetime.date, datetime.time)):
            v = "'%s'" % v
        elif isinstance(v, bytes):
            try:
                v = v.decode("utf8")
            except UnicodeDecodeError:
                v = v.decode("raw_unicode_escape")
            v = "'%s'" % v
        elif isinstance(v, int):
            v = "%s" % int(v)
        elif v is None:
            v = "NULL"
        else:
            v = str(v)
        return v

    def format(self, record):
        if record.name == "httpx":
            if (
                len(record.args) >= 2
                and not isinstance(record.args[-2], bool)
                and record.args[-2] != 200
            ):
                record.levelname = "ERROR"
        message = super(ColoredFormatter, self).format(record)
        if isinstance(record.msg, tuple):
            try:
                sql, params = record.msg
                if params is None:
                    message = sql
                elif isinstance(params, list):
                    params = tuple(params)
                    message = sql % tuple(map(self._query_val_transform, params))
                elif isinstance(params, tuple):
                    message = sql % tuple(map(self._query_val_transform, params))
                elif isinstance(params, dict):
                    params = {
                        k: self._query_val_transform(v) for k, v in params.items()
                    }
                    message = sql % params
            except Exception as exc:
                if isinstance(exc, TypeError):
                    message = sql
        elif isinstance(record.msg, str):
            message = record.msg % record.args
        color = self.COLORS.get(record.levelname, self.COLORS["RESET"])
        return f'{color}{message}{self.COLORS["RESET"]}'


def get_py_files(directory, excluded_dirs):
    py_files = []
    main_files = []
    for root, dirs, files in os.walk(directory):
        if any(excluded_dir in root for excluded_dir in excluded_dirs):
            continue

        for file in files:
            if file.endswith(".py") and file not in EXCLUDE_FILES:
                relative_path = os.path.relpath(os.path.join(root, file), directory)
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    content = f.read()
                    if (
                        "__name__ == '__main__'" in content
                        or '__name__ == "__main__"' in content
                    ):
                        main_files.append(relative_path)
                        continue
                py_files.append(relative_path)
    return py_files, main_files


dirs_to_ignore = [
    ".git",
    ".venv",
    "tests",
    "__pycache__",
    "src/database/migrations",
]
EXEC_FILES, IMPORT_FILES = get_py_files(ROOT_DIR, dirs_to_ignore)

if IMPORT_FILES:
    for f in IMPORT_FILES:
        f = f.replace("/", ".")
        EXEC_LINES.append(f"from {f[:-3]} import *")


@click.group()
def shipment_cli():
    os.environ['PYTHONBREAKPOINT'] = 'IPython.terminal.debugger.set_trace'


@shipment_cli.group("server")
def my_server():
    pass


@my_server.command("config")
def show_config():
    import inspect
    from tabulate import tabulate
    from configs.env import env
    func_members = inspect.getmembers(env)
    table = []
    for key, value in func_members:
        if key.isupper():
            table.append([key, value])
    click.secho(tabulate(table, headers=["Key", "Value"], tablefmt = "grid"), fg="green")


@my_server.command("develop")
def run_development_server(port: int = 8000):
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(("127.0.0.1", port))
            sock.close()
            break
        except OSError:
            port += 1
    if port != 8000:
        print(f"Starting server on http://127.0.0.1:{port}/")
        user_input = input("Press 'y' to continue or any other key to quit: ")
        if user_input.lower() != "y":
            return
    uvicorn.run("main:app", reload=True, port=port)


@my_server.command("shell")
@click.argument("ipython_args", nargs=-1, type=click.UNPROCESSED)
@click.option("--nolog", is_flag=True, default=False)
def shell(ipython_args, nolog):
    profile_name = "shipment"
    ProfileDir.create_profile_dir_by_name(name=profile_name, path="./")
    if not nolog:
        configure_logger()
    config = load_default_config()
    config.TerminalInteractiveShell.banner1 = (
        f"""Python {sys.version} on {sys.platform} IPython: {IPython.__version__}"""
    )
    config.TerminalInteractiveShell.autoindent = True
    config.InteractiveShellApp.exec_lines = [
        "%load_ext autoreload",
        "%autoreload 2",
    ]
    config.TerminalInteractiveShell.autoformatter = "black"
    VerboseTB._tb_highlight = "bg:#4C5656"
    config.InteractiveShell.ast_node_interactivity = "all"
    config.InteractiveShell.debug = True
    config.TerminalInteractiveShell.highlighting_style = "paraiso-dark"
    config.TerminalIPythonApp.profile = profile_name
    config.InteractiveShell.colors = 'linux'
    user_ns = {"database": db}
    with db.connection_context():
        IPython.start_ipython(argv=ipython_args, user_ns=user_ns, config=config)


my_server.add_command(uvicorn.main, name="start")


def entrypoint():
    try:
        shipment_cli()
    except Exception as e:
        click.secho(f"ERROR: {e}", bold=True, fg="red")


if __name__ == "__main__":
    entrypoint()
