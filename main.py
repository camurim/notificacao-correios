#!/usr/bin/python3

import argparse
import json
import os
import signal
import sys
from datetime import datetime
from os.path import isfile
from pathlib import Path

import requests
from icecream import ic
from playsound import playsound
from plyer import notification
from rich.console import Console


def handler(num, frame):
    console = Console()
    console.clear()

    console.print("\n[red bold]Deseja interromper? (S/N) [red bold/]: ", end="")
    resp = sys.stdin.read(1)

    if resp in ["s", "S"]:
        console.clear()
        exit(1)


def current_time():
    now = datetime.now()
    return "%s |> " % (now.strftime("%H:%M:%S"))


def log_to_file(s):
    script_dir = Path(__file__).parent.absolute()
    with open(script_dir.joinpath("execution.log"), "a") as f:
        f.write(s + "\n")


def log(p_str, p_logtofile):
    if p_logtofile:
        ic.configureOutput(prefix=current_time(), outputFunction=log_to_file)
    else:
        ic.configureOutput(prefix=current_time())

    ic(p_str)


def write_last_status(p_status):
    script_dir = Path(__file__).parent.absolute()

    with open(script_dir.joinpath("laststatus.txt"), "w") as file:
        file.write(p_status)
        file.close()


def read_last_status():
    script_dir = Path(__file__).parent.absolute()

    if not isfile(script_dir.joinpath("laststatus.txt")):
        return None

    with open(script_dir.joinpath("laststatus.txt"), "r") as file:
        return str(file.read()).strip()


if __name__ == "__main__":
    DEBUGMODE = os.getenv("DEBUGMODE")
    script_dir = Path(__file__).parent.absolute()

    signal.signal(signal.SIGINT, handler)

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--code", required=True)
    parser.add_argument("-l", "--logtofile", required=False, action="store_true")
    args = parser.parse_args()

    url = f"https://api.linketrack.com/track/json?user=teste&token=1abcd00b2731640e886fb41a8a9671ad1434c599dbaa0a0de9a5aa619f29a83f&codigo={args.code}"

    response = requests.request("GET", url, headers={}, data={})

    console = Console()
    console.clear()

    if response.status_code != 200:
        if DEBUGMODE:
            log(str(response.text.encode("utf8")), args.logtofile)
        exit(1)

    res = json.loads(response.text.encode("utf8"))

    if not res:
        if DEBUGMODE:
            log("Não foi possível parsear o JSON da resposta!", args.logtofile)
        exit(1)

    last_status = read_last_status()

    if (
        last_status
        and last_status != f"{res['eventos'][0]['data']}-{res['eventos'][0]['hora']}"
    ):
        if notification.notify:
            notification.notify(
                title="Correios",
                message=res["eventos"][0]["status"],
                app_icon=None,
                timeout=10,
            )
            playsound(script_dir.joinpath("sounds").joinpath("doraemon.mp3"))

    if DEBUGMODE:
        log(res["eventos"][0]["status"], args.logtofile)

    write_last_status(f"{res['eventos'][0]['data']}-{res['eventos'][0]['hora']}")
