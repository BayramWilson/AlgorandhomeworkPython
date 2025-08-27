# app_boxes.py
from pyteal import *

def approval():
    # On create: einfach erlauben
    on_create = Approve()

    # deposit(handle): schreibe handle in Box "github"
    # Erwartete App-Args: ["deposit", <github_handle_bytes>]
    deposit = Seq(
        App.box_put(Bytes("github"), Txn.application_args[1]),
        Approve(),
    )

    program = Cond(
        [Txn.application_id() == Int(0), on_create],                          # Create
        [Txn.on_completion() == OnComplete.NoOp,                              # NoOp: Methoden anhand des 1. Args
         Cond(
            [Txn.application_args.length() == Int(2),                         # "deposit" + handle
             If(Txn.application_args[0] == Bytes("deposit"), deposit, Reject())
            ],
            [Int(1), Reject()]                                                # sonst: reject
         )
        ],
        [Int(1), Reject()]
    )
    return program

def clear():
    return Approve()

if __name__ == "__main__":
    print(compileTeal(approval(), mode=Mode.Application, version=8))
