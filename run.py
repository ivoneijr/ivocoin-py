import argparse
from src import app

parser = argparse.ArgumentParser(description='HistoryBlocks fullnode miner')
parser.add_argument('--port', type=int, default='5001', help='exposed comm port')
args = parser.parse_args()

app.run(host='0.0.0.0', port=args.port)
