"""
Train entry point for Sales Lead Scorer.
"""

import argparse
from model.trainer import train

def parse_args():
    parser = argparse.ArgumentParser(description="Train Sales Lead Scorer")
    parser.add_argument("--data", type=str, required=True, help="Path to CSV data file")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    train(args.data)
