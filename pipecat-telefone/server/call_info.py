"""Mostra o status e os avisos/erros da Twilio para uma chamada (somente leitura).

Uso: uv run call_info.py CAxxxxxxxx
"""

import base64
import json
import os
import sys
import urllib.request

from dotenv import load_dotenv

load_dotenv(override=True)

sid = os.getenv("TWILIO_ACCOUNT_SID")
token = os.getenv("TWILIO_AUTH_TOKEN")
call_sid = sys.argv[1]
auth = base64.b64encode(f"{sid}:{token}".encode()).decode()


def get(path):
    req = urllib.request.Request(f"https://api.twilio.com/2010-04-01/Accounts/{sid}/{path}")
    req.add_header("Authorization", f"Basic {auth}")
    with urllib.request.urlopen(req) as r:
        return json.load(r)


if call_sid == "latest":
    for c in get("Calls.json?PageSize=3").get("calls", []):
        print(c["sid"], c["start_time"], c["status"], f'{c.get("duration")}s')
    call_sid = get("Calls.json?PageSize=1")["calls"][0]["sid"]

call = get(f"Calls/{call_sid}.json")
print("status:", call.get("status"), "| duracao(s):", call.get("duration"), "| respondida_por:", call.get("answered_by"))

notes = get(f"Calls/{call_sid}/Notifications.json").get("notifications", [])
print(f"avisos/erros: {len(notes)}")
for n in notes:
    print("-", n.get("error_code"), n.get("message_text", "")[:300])
