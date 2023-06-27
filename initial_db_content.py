from git_lurker.models import project

start_projects = [
    {"repo": "lndconnect", "owner": "LN-Zap"},
    {"repo": "joinmarket-clientserver", "owner": "JoinMarket-Org"},
    {"repo": "jam", "owner": "joinmarket-webui"},
    {"repo": "specter-desktop", "owner": "cryptoadvance"},
    {"repo": "mempool", "owner": "mempool"},
    {"repo": "bitcoin", "owner": "bitcoin"},
    {"repo": "lnbits", "owner": "lnbits"},
    {"repo": "cashu", "owner": "lnbits"},
    {"repo": "sparrow", "owner": "sparrowwallet"},
    {"repo": "start-os", "owner": "Start9Labs"},
    {"repo": "robosats", "owner": "Robosats"},
    {"repo": "RTL", "owner": "Ride-The-Lightning"},
    {"repo": "lnd", "owner": "lightningnetwork"},
    {"repo": "lightning", "owner": "ElementsProject"},
    {"repo": "electrs", "owner": "romanz"},
    {"repo": "btc-rpc-explorer", "owner": "janoside"},
    {"repo": "btcpayserver", "owner": "btcpayserver"},
    {"repo": "bluewallet", "owner": "bluewallet"},
    {"repo": "raspibolt", "owner": "raspibolt"},
    {"repo": "raspiblitz", "owner": "raspiblitz"},
    {"repo": "umbrel", "owner": "getumbrel"},
    {"repo": "zeus", "owner": "ZeusLN"},
    {"repo": "eclair", "owner": "ACINQ"},
    {"repo": "phoenix", "owner": "ACINQ"},
    {"repo": "nunchuk-desktop", "owner": "nunchuk-io"}
]

for proj in start_projects:
    project.objects.get_or_create(repository=proj["repo"], owner=proj["owner"])

print("Database populated")