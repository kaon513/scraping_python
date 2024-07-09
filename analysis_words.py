from janome.tokenizer import Tokenizer
from collections import Counter

text = """
分析したい文章を記述する
"""

# テキストを単語に分割するためにjanomeを使用
tokenizer = Tokenizer()
tokens = tokenizer.tokenize(text, wakati=True)

# 単語の出現回数をカウント
word_count = Counter(tokens)

# 複数回出現する単語のみ抽出
multiple_occurrences = {word: count for word, count in word_count.items() if count > 1}

# 結果を表示
for word, count in multiple_occurrences.items():
    print(f"{word}: {count}")

# 出力した結果が多い場合、さらにChatGPTを使用して、カテゴリ別にしてもらうとよかった