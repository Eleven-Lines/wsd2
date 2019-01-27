import sys
import numpy as np
import pandas as pd
from gensim.models import word2vec
from pyknp import KNP, Bunsetsu

dict_path = "d18_8d-level3-reduced.csv"
model_path = "/Volumes/Macintosh_SD/data/latest-ja-word2vec-gensim-model/word2vec.gensim.model"

knp = KNP()
d18 = pd.read_csv(dict_path, index_col=0)
model = word2vec.Word2Vec.load(model_path)

emo_elements = d18.columns
emo_dim = len(emo_elements)

w2v_thre = 0.5
pre_strength = 0.5

def d18_score(word: str) -> np.ndarray:
    """
    D18辞書からスコアを取得する

    Parameters
    ------------------
    word: str
        検索する語

    Returns
    ------------------
    score: np.ndarray
        D18のスコア、存在しなかった場合は零ベクトル
    """
    if word in d18.index:
        return d18.loc[word].values
    return np.zeros(emo_dim)

def negate_emo(emo: np.ndarray) -> np.ndarray:
    """
    感情を反転させる
    """
    return emo[[1, 0, 3, 2, 5, 4, 7, 6]]

def preprocess_sentence(sentence: str) -> str:
    """
    文章の前処理を行う

    Parameters
    ------------------
    sentence: str
        前処理を行う文章
    """
    return sentence.strip()

def calc_mrph_score(genkei: str, pos: str = None, case: str = None) -> np.ndarray:
    """
    形態素のスコアを計算する

    Parameters
    ------------------
    genkei: str
        調べたい形態素の原型
    pos: str
        形態素の品詞
        「名詞」や「形容詞」など
    case: str
        用いられている文節のの格
        「ガ」や「ヲ」など
    """
    result = d18_score(genkei)
    if result.any():
        return result
    if genkei[-1] == "だ":
        return d18_score(genkei[:-1])
    if pos and (pos == "名詞" or pos == "形容詞" or pos == "動詞"):
        # 発見できなかった場合、w2vから類似語を拾う
        try:
            sim = model.wv.most_similar(positive=[genkei], topn=1)
            print(f"sim for \"{genkei}\": {sim[0]}")
            if(sim[0][1] >= w2v_thre):
                return calc_mrph_score(sim[0][0]) * sim[0][1]
        except KeyError:
            print(f"No vocabulary for {genkei}")
    # その他すべて0
    return result

def calc_sentence_score(sentence: str) -> np.ndarray:
    """
    文章のスコアを計算する

    Parameters
    ------------------
    sentence: str
        スコアを得たい文章
    """
    preprocessed = preprocess_sentence(sentence)
    bnst_list = knp.parse(preprocessed)

    scores = dict()

    for bnst in bnst_list[::-1]:
        bnst_id = bnst.bnst_id
        parent_id = bnst.parent_id
        print(f"bnst_id: {bnst.bnst_id}")
        print(f"parent_id: {bnst.parent_id}")

        scores[bnst_id] = np.zeros(emo_dim)
        is_nagation = "否定表現" in bnst.features

        for mrph in bnst.mrph_list():
            mrph_score = calc_mrph_score(mrph.genkei, mrph.hinsi)
            print(f"{mrph.midasi}: {mrph_score}")
            scores[bnst_id] += mrph_score

        print("Score", end="")
        if is_nagation:
            print("[Negation]", end="")
            scores[bnst_id] = negate_emo(scores[bnst_id])
        print(f": {scores[bnst_id]}")

        if parent_id != -1:
            # 文のlinkがあるものは強く判断しない
            if parent_id not in scores:
                scores[parent_id] = np.zeros(emo_dim)
            scores[parent_id] += scores[bnst_id] * pre_strength
        print("----------------------------------")
    return sum(scores.values()) / len(scores)

def calc_song_score(lyrics: str) -> np.ndarray:
    """
    歌詞のスコアを計算する

    Parameters
    ------------------
    lyrics: str
        改行区切りの歌詞データ
    """
    scores = [calc_sentence_score(l) for l in lyrics.split("\n")]
    return sum(scores) / len(scores)

if __name__ == "__main__":
    lyrics = "描いたのは僕らの空想だ"
    print(emo_elements)
    print(calc_sentence_score(lyrics))
