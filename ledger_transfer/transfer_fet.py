from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.aerial.tx import Transaction
from cosmpy.protos.cosmos.bank.v1beta1.tx_pb2 import MsgSend
from cosmpy.protos.cosmos.base.v1beta1.coin_pb2 import Coin
import cosmpy.aerial.tx as tx_module  # Internal module for SigningMode

# === Get SigningMode.Direct from internals ===
SigningMode_Direct = getattr(tx_module.SigningMode, "Direct")

# === Fake SigningCfg for seal() compatibility ===
class FakeSigningCfg:
    def __init__(self, signer, sequence):
        self.signer = signer
        self.mode = SigningMode_Direct
        self.public_key = signer.public_key()
        self.sequence_num = sequence

def transfer_fet(mnemonic: str, dest_addr: str, amount_fet: float):
    wallet = LocalWallet.from_mnemonic(mnemonic)
    client = LedgerClient(NetworkConfig.fetchai_dorado_testnet())
    sender_address = str(wallet.address())
    account = client.query_account(wallet.address())

    print(f"🔐 From: {sender_address}")
    print(f"➡️  To: {dest_addr} | Amount: {amount_fet} FET")

    msg = MsgSend(
        from_address=sender_address,
        to_address=dest_addr,
        amount=[Coin(denom="atestfet", amount=str(int(amount_fet * 1_000_000)))]
    )

    tx = Transaction()
    tx.add_message(msg)
    tx._chain_id = "dorado-1"
    tx._account_number = account.number
    tx._sequence = account.sequence

    signing_cfg = FakeSigningCfg(wallet, sequence=account.sequence)

    # Use string-based fee to match current cosmpy compatibility
    tx.seal(signing_cfgs=[signing_cfg], fee="200000000000000atestfet", gas_limit=200000)
    tx.sign(wallet.signer(), chain_id="dorado-1", account_number=account.number)
    tx.complete()

    response = client.broadcast_tx(tx)
    print(f"✅ TX submitted. Hash: {response.tx_hash}")
    print("🔗 Explorer: https://hub.fetch.ai/dorado-1/transactions/" + response.tx_hash)

    # === Display balance after transfer ===
    try:
        balance = client.query_bank_balance(wallet.address(), denom="atestfet")
        print(f"\n📦 Wallet Balance After Transfer: {balance} atestfet")
    except Exception as e:
        print(f"\n⚠️ Failed to fetch balance: {e}")

# === EXECUTION ===
if __name__ == "__main__":
    transfer_fet(
        mnemonic="praise frost bubble arrest vital drill option never permit extend tragic valve",
        dest_addr="fetch16vstnzcew34zlxenagse7s8l4rc6mkp6fxkjyr",
        amount_fet=2
    )
