
import pandas as pd, requests, hashlib, json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / 'data'
DATA_PATH = DATA_DIR / 'lotto539.csv'
API_URL = 'https://www.taiwanlottery.com.tw/lotto539/history/api/{{issue}}'

class LotteryDataManager:
    def __init__(self, data_path=DATA_PATH):
        self.data_path = Path(data_path)
        if not self.data_path.exists():
            self.data_path.parent.mkdir(parents=True, exist_ok=True)
            self.data_path.write_text('issue,n1,n2,n3,n4,n5\n')

    def sha1(self):
        h=hashlib.sha1()
        h.update(self.data_path.read_bytes())
        return h.hexdigest()

    def load(self):
        return pd.read_csv(self.data_path)

    def append_draw(self, issue:int, numbers:list[int]):
        df=self.load()
        if issue in df['issue'].values:
            return False
        row={'issue':issue, **{f'n{i+1}':n for i,n in enumerate(numbers)}}
        df=pd.concat([df, pd.DataFrame([row])], ignore_index=True)
        df.to_csv(self.data_path, index=False)
        return True
