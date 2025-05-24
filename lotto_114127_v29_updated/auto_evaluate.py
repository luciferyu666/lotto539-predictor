
"""
auto_evaluate.py
~~~~~~~~~~~~~~~~
開獎後對預測組合進行自動評估，輸出 JSON 與可視化 PNG。

使用方式
--------
python auto_evaluate.py --history 最新清洗檔 \
                        --wheels wheel_combinations.csv
"""
from __future__ import annotations
import argparse, csv, json, collections, matplotlib.pyplot as plt, statistics, pathlib

def load_history(path: str) -> dict[str, list[int]]:
    data={}
    with open(path, encoding="utf-8") as fp:
        for line in fp:
            parts=line.strip().split()
            if len(parts)>=6:
                period=parts[0]
                nums=[int(p) for p in parts[1:6]]
                data[period]=nums
    return data

def load_wheels(path: str) -> list[list[int]]:
    wheels=[]
    with open(path, encoding="utf-8") as fp:
        rdr=csv.DictReader(fp)
        for row in rdr:
            wheels.append([int(n) for n in row["Numbers"].split()])
    return wheels

def evaluate(wheels, result_nums):
    hit_core=sum(1 for n in result_nums if n in wheels["core_pool"])
    stats=[]
    for combo in wheels["wheels"]:
        hit=len(set(combo) & set(result_nums))
        stats.append(hit)
    return stats, hit_core

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--history",required=True)
    ap.add_argument("--wheels",required=True)
    args=ap.parse_args()
