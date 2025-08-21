# 安裝套件: pip install bip-utils

from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins

# 使用者輸入助記詞
mnemonic = input("請輸入助記詞 (以空格分隔): ")

# 產生 seed
seed = Bip39SeedGenerator(mnemonic).Generate()

# 支援的幾個常見鏈
chains = {
    "Bitcoin": Bip44Coins.BITCOIN,
    "Ethereum": Bip44Coins.ETHEREUM,
    "Solana": Bip44Coins.SOLANA,
}

for name, coin in chains.items():
    wallet = Bip44.FromSeed(seed, coin).DeriveDefaultPath()
    print(f"{name} 地址: {wallet.PublicKey().ToAddress()}")
