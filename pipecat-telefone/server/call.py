"""Liga para um numero e conecta a chamada ao bot (via WebSocket do Twilio).

Uso: uv run call.py --to +55DDDNUMERO --from +1XXXXXXXXXX --host meu-tunel.exemplo.com
"""

import argparse
import base64
import json
import os
import urllib.parse
import urllib.request

from dotenv import load_dotenv

load_dotenv(override=True)

parser = argparse.ArgumentParser()
parser.add_argument("--to", required=True, help="Numero de destino (E.164), ex: +5519999999999")
parser.add_argument("--from", dest="from_", required=True, help="Numero Twilio de origem")
parser.add_argument("--host", required=True, help="Host publico do tunel, sem https://")
args = parser.parse_args()

sid = os.getenv("TWILIO_ACCOUNT_SID")
token = os.getenv("TWILIO_AUTH_TOKEN")
if not sid or not token:
    raise SystemExit("Faltam TWILIO_ACCOUNT_SID / TWILIO_AUTH_TOKEN no .env")

# Contas trial nao aceitam TwiML inline: a Twilio busca o TwiML em Url (o bot serve POST / com -x <host>).
data = urllib.parse.urlencode(
    {"To": args.to, "From": args.from_, "Url": f"https://{args.host}/"}
).encode()

req = urllib.request.Request(
    f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Calls.json", data=data, method="POST"
)
auth = base64.b64encode(f"{sid}:{token}".encode()).decode()
req.add_header("Authorization", f"Basic {auth}")

try:
    with urllib.request.urlopen(req) as resp:
        body = json.load(resp)
except urllib.error.HTTPError as e:
    detail = e.read().decode(errors="replace")
    raise SystemExit(f"Twilio recusou (HTTP {e.code}): {detail}")
print("Chamada criada:", body.get("sid"), "| status:", body.get("status"))
