from bip_utils import (
    Bip39SeedGenerator, Bip44, Bip44Coins, Bip84, Bip84Coins,
    Bip32Slip10Ed25519, Bip44Changes, Base58Encoder
)

mnemonic = input("mnemonic: ").strip()
count = int(input("count (default 1): ") or "1")
seed = Bip39SeedGenerator(mnemonic).Generate()  # 無 passphrase

def sol_addr(idx: int) -> str:
    # Solana: m/44'/501'/${index}'/0' （Phantom 相容）
    node = Bip32Slip10Ed25519.FromSeed(seed).DerivePath(f"m/44'/501'/{idx}'/0'")
    pub = node.PublicKey().RawCompressed().ToBytes()   # 預期 32 bytes
    # 保險：若意外拿到 33 bytes 且首位 0x00，去掉前綴，確保 32 bytes
    if len(pub) == 33 and pub[0] == 0x00:
        pub = pub[1:]
    return Base58Encoder.Encode(pub)  # Solana 位址 = 公鑰的 Base58

for i in range(count):
    # EVM (ETH/POL/BASE 同一地址規則與 derivation；僅網路不同)
    evm = (Bip44.FromSeed(seed, Bip44Coins.ETHEREUM)
           .Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT)
           .AddressIndex(i).PublicKey().ToAddress())

    # Bitcoin SegWit (BIP84)
    btc = (Bip84.FromSeed(seed, Bip84Coins.BITCOIN)
           .Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT)
           .AddressIndex(i).PublicKey().ToAddress())

    # Solana (Phantom 相容)
    sol = sol_addr(i)

    print(f"index {i}\nSOL   {sol}\nETH   {evm}\nBTC   {btc}\n")
