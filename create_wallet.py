from algosdk import account, mnemonic

def create_algorand_wallet():
    """
    Generiert eine neue Algorand-Wallet und gibt die Adresse und die mnemonische Phrase aus.
    """
    # Erstellt ein neues Konto (Schlüsselpaar)
    private_key, public_address = account.generate_account()

    # Konvertiert den privaten Schlüssel in eine für Menschen lesbare mnemonische Phrase
    mnemonische_phrase = mnemonic.from_private_key(private_key)

    print("Neue Algorand-Wallet erfolgreich erstellt!")
    print("=" * 50)
    print(f"Öffentliche Adresse: {public_address}")
    print(f"Mnemonische Phrase (zur Wiederherstellung): {mnemonische_phrase}")
    print("=" * 50)
    print("\nWICHTIG:")
    print("Bewahre deine mnemonische Phrase sicher auf. Mit ihr kann jeder auf deine Wallet zugreifen.")
    print("Teile sie niemals mit jemandem, dem du nicht vertraust.")
    print("\nNächste Schritte:")
    print("Um diese Wallet im Algorand TestNet zu verwenden, benötigst du einige Test-Algos.")
    print("Gehe zum Algorand TestNet Dispenser, um dein Konto aufzuladen:")
    print("https://dispenser.testnet.aws.algodev.network/")
    print("-" * 50)


if __name__ == "__main__":
    create_algorand_wallet()
