# deploy_and_deposit.py
import base64
from algosdk.v2client import algod
from algosdk import account, mnemonic, transaction
from algosdk.logic import get_application_address
from algosdk.transaction import OnComplete, StateSchema, wait_for_confirmation

from pyteal import compileTeal, Mode
import app_boxes  # das PyTeal-Modul von oben

# ====== KONFIG ======
ALGOD_ADDRESS = "https://testnet-api.algonode.cloud"  # kein Token nötig
ALGOD_TOKEN   = ""
GITHUB_HANDLE = "BayramWilson"

SENDER_MNEMONIC = "reduce arm battle badge trigger tag barely pipe sell monitor text theory shuffle ask claw spray metal orange sense lounge property nature frost abandon useless"
# ====================

def compile_program(client: algod.AlgodClient, teal_source: str) -> bytes:
    compile_response = client.compile(teal_source)
    return base64.b64decode(compile_response["result"])

def main():
    client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)

    # Sender laden
    sender_sk = mnemonic.to_private_key(SENDER_MNEMONIC)
    sender_addr = account.address_from_private_key(sender_sk)

    # PyTeal -> TEAL
    approval_teal = compileTeal(app_boxes.approval(), mode=Mode.Application, version=8)
    clear_teal    = compileTeal(app_boxes.clear(),    mode=Mode.Application, version=8)

    approval = compile_program(client, approval_teal)
    clear    = compile_program(client, clear_teal)

    sp = client.suggested_params()

    # App erstellen (ohne State-Schema, Boxen brauchen keins)
    txn = transaction.ApplicationCreateTxn(
        sender=sender_addr,
        sp=sp,
        on_complete=OnComplete.NoOpOC.real,
        approval_program=approval,
        clear_program=clear,
        global_schema=StateSchema(0, 0),
        local_schema=StateSchema(0, 0),
    )
    stx = txn.sign(sender_sk)
    txid = client.send_transaction(stx)
    res  = wait_for_confirmation(client, txid, 4)
    app_id = res["application-index"]
    print("✅ App created. App ID:", app_id)

    # App-Adresse mit etwas ALGO funden (Box-MBR ~0.1 ALGO -> wir schicken 0.2)
    app_addr = get_application_address(app_id)
    sp = client.suggested_params()
    pay = transaction.PaymentTxn(sender_addr, sp, app_addr, 200_000, note=b"fund for box")
    stx = pay.sign(sender_sk)
    client.send_transaction(stx)
    wait_for_confirmation(client, stx.get_txid(), 4)
    print("✅ App funded:", app_addr)

    # deposit(github_handle) aufrufen – Box "github" referenzieren!
    sp = client.suggested_params()
    app_call = transaction.ApplicationNoOpTxn(
        sender=sender_addr,
        sp=sp,
        index=app_id,
        app_args=[b"deposit", GITHUB_HANDLE.encode()],
        boxes=[(app_id, "github".encode())],  # <--- Box-Referenz wichtig
    )
    stx = app_call.sign(sender_sk)
    client.send_transaction(stx)
    wait_for_confirmation(client, stx.get_txid(), 4)
    print(f"✅ deposit() called. Handle '{GITHUB_HANDLE}' gespeichert in Box 'github'.")

    print("\n📌 Merke dir deine Application ID:", app_id)
    print("   (Für Explorer/Test später nötig.)")

if __name__ == "__main__":
    main()
