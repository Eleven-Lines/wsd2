import sys
import re
import json
from typing import List
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

w2v_thre = 0.7
pre_strength = 0.5

punctuations = r"(\(|\)|（|）|　)"
punctuations_pat = re.compile(punctuations)

class MorphemeScore:
    def __init__(self, score: np.ndarray, midasi: str, genkei: str):
        self.score = score
        self.midasi = midasi
        self.genkei = genkei
    def to_dict(self):
        return {"score": self.score.tolist(), "midasi": self.midasi, "genkei": self.genkei}
class SentenceScore:
    def __init__(self, score: np.ndarray, sentence: str, morphemes: List[MorphemeScore]):
        self.score = score
        self.sentence = sentence
        self.morphemes = morphemes
    def to_dict(self):
        return {"score": self.score.tolist(), "sentence": self.sentence, "morphemes": [a.to_dict() for a in self.morphemes]}
class LyricsScore:
    def __init__(self, score: np.ndarray, lyrics: str, sentences: List[SentenceScore]):
        self.score = score
        self.lyrics = lyrics
        self.sentences = sentences
    def to_dict(self):
        return {"score": self.score.tolist(), "lyrics": self.lyrics, "sentences": [a.to_dict() for a in self.sentences]}

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
    return (punctuations_pat.sub("", sentence)
            .strip())

def calc_mrph_score(genkei: str, midasi: str, pos: str = None, case: str = None) -> MorphemeScore:
    """
    形態素のスコアを計算する

    Parameters
    ------------------
    genkei: str
        調べたい形態素の原型
    pos: str
        形態素の品詞
        「名詞」や「形容詞」など
    """
    result = d18_score(genkei)
    if result.any() or not genkei:
        return MorphemeScore(result, midasi, genkei)
    if genkei[-1] == "だ":
        return calc_mrph_score(genkei[:-1], midasi)
    if pos and (pos == "名詞" or pos == "形容詞" or pos == "動詞"):
        # 発見できなかった場合、w2vから類似語を拾う
        try:
            sim = model.wv.most_similar(positive=[genkei], topn=1)
            if(sim[0][1] >= w2v_thre):
                mrph_score = calc_mrph_score(sim[0][0], midasi)
                mrph_score.score *= sim[0][1]
                return mrph_score
        except KeyError:
            print(f"No vocabulary for {genkei}", file=sys.stderr)
    # その他すべて0
    return MorphemeScore(result, midasi, genkei)

def calc_sentence_score(sentence: str) -> SentenceScore:
    """
    文章のスコアを計算する

    Parameters
    ------------------
    sentence: str
        スコアを得たい文章
    """
    preprocessed = preprocess_sentence(sentence)
    try:
        bnst_list = knp.parse(preprocessed)
    except Exception:
        print(f"parse failed: {sentence}", file=sys.stderr)
        return SentenceScore(np.zeros(emo_dim), sentence, [])

    scores = dict()
    mrph_scores = []
#     print(preprocessed)

    for bnst in bnst_list[::-1]:
        bnst_id = bnst.bnst_id
        parent_id = bnst.parent_id

        bnst_mrph_scores = []
        scores[bnst_id] = np.zeros(emo_dim)
        is_nagation = "否定表現" in bnst.features

        for mrph in bnst.mrph_list():
            # 文節ごとのスコア計算
            mrph_score = calc_mrph_score(mrph.genkei, mrph.midasi, mrph.hinsi)
            bnst_mrph_scores.insert(0, mrph_score)
            scores[bnst_id] += mrph_score.score

        mrph_scores.extend(bnst_mrph_scores)

        if is_nagation:
            # 否定表現は自身のスコアを逆転させる
            scores[bnst_id] = negate_emo(scores[bnst_id])

        if parent_id != -1:
            # 文のlinkがあるものは強く判断しない
            if parent_id not in scores:
                scores[parent_id] = np.zeros(emo_dim)
            scores[parent_id] += scores[bnst_id] * pre_strength
#         print("----------------------------------")
    score =  sum(scores.values()) / len(scores)
    return SentenceScore(score, sentence, mrph_scores[::-1])

def calc_song_score(lyrics: str) -> np.ndarray:
    """
    歌詞のスコアを計算する

    Parameters
    ------------------
    lyrics: str
        改行区切りの歌詞データ
    """
    sentence_scores = []

    for l in lyrics.splitlines():
        if l == "":
            continue
        sentence_score = calc_sentence_score(l)
        sentence_scores.append(sentence_score)

        score = sentence_score.score
        normalized_score = score / sum(score)

    mean_score = sum([s.score for s in sentence_scores]) / len(sentence_scores)
    lyrics_score = LyricsScore(mean_score, "", sentence_scores)

    return json.dumps(lyrics_score.to_dict())

if __name__ == "__main__":
    df = pd.DataFrame(columns=emo_elements)
    sentence_scores = []
    with open(sys.argv[1]) as f:
        for l in f:
            if l == "\n":
                continue
            sentence_score = calc_sentence_score(l)
            sentence_scores.append(sentence_score)

            score = sentence_score.score
            normalized_score = score / sum(score)
            rounded_score = np.around(normalized_score, 3)
            df.loc[l.strip()] = rounded_score
    mean_score = sum([s.score for s in sentence_scores]) / len(sentence_scores)
    lyrics_score = LyricsScore(mean_score, "", sentence_scores)
    print(json.dumps(lyrics_score.to_dict()))
    df.to_csv("result.csv")
