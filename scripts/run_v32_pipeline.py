
import numpy as np, json, os
if __name__=='__main__':
    scores = np.random.rand(39).tolist()
    os.makedirs('outputs',exist_ok=True)
    json.dump({'scores':scores}, open('outputs/114130_scores.json','w'))
    print('pipeline finished')
