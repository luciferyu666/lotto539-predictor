
from lotto_v24_predictor import data_loader, feature_extractor, neural_net

def test_loader(tmp_path):
    sample = tmp_path / "sample.txt"
    sample.write_text("114100 01 02 03 04 05\n114101 06 07 08 09 10\n")
    draws = data_loader.load_draws(str(sample))
    assert len(draws) == 2
    assert draws[0]['period'] == '114100'

def test_feature_extractor():
    draws = [{'period':'1','nums':[1,2,3,4,5]}]*334
    feats = feature_extractor.extract_features(draws)
    assert len(feats['freq']) == 39
    assert feats['freq'][1] == 334
    scorer = neural_net.SimpleHeuristicScorer(feats)
    s = scorer.score(1)
    assert 0.0 <= s <= 1.0
