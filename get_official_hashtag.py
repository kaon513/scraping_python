import requests
import time
import re
from datetime import datetime, date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from collections import Counter

def extract_username(url):
    # 正規表現パターンを定義
    pattern = r'正規表現パターン'
    # 正規表現でURLからユーザー名を抽出
    match = re.search(pattern, url)
    
    if match:
        return match.group(1)
    else:
        return None
    
# ページャーを表示して、h2から全てのaタグのURLを取得する
def get_all_pages_and_links(base_url, target_url):
    # ChromeDriverを使用してブラウザを起動
    driver = webdriver.Chrome()
    driver.get(base_url)
    
    while True:
        # 現在のページのURLをリストに追加
        current_url = driver.current_url
        all_urls.append(current_url)

        # 現在のページのHTMLを取得
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # ページから要素を取得する
        # すべての<li>要素を取得
        elements = soup.find_all('li', class_='p-topics__item')
        
        for element in elements:
            # <li>の中の<a>タグを見つける
            a_tag = element.find('a')
            # <li>の中の<p>タグを見つける
            p_tag = element.find('p', {'class': 'p-topics__title'})

            if a_tag and a_tag.get('href') and p_tag:
                # <a>タグのhref属性を取得
                url = a_tag['href']
                username = extract_username(url)
                elements_list.append([p_tag.text, url, username])

        # 現在のページがターゲットURLの場合、ループを終了
        if current_url == target_url:
            print(f"Reached the target URL: {target_url}")
            break

        try:

            # 遷移前のURLを取得して出力
            prev_page_url = driver.current_url
            print(f"Navigated from: {prev_page_url}")

            # 全てのページャーボタンをクラス名で検索
            pager_buttons = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'c-pager__button'))
            )

            # "Next" というテキストを持つ<span>タグを含むボタンを見つけてクリック
            next_button = None
            for button in pager_buttons:
                span = button.find_element(By.TAG_NAME, 'span')
                if span.text == '次のページ':
                    next_button = button
                     break
            
            if next_button:
                next_button.click()
                time.sleep(2)  # ページ遷移が完了するのを待つための一時停止
                # 遷移先のURLを取得して出力
                next_page_url = driver.current_url
                print(f"Navigated to: {next_page_url}")
            else:
                print("Next page button not found")
                break
        except Exception as e:
            # 次のページのリンクが見つからない場合、またはエラーが発生した場合、終了
            print(f"Error or no more pages: {str(e)}")
            break

    # ブラウザを閉じる
    driver.quit()
    return elements_list

# 取得したデータをファイルに保存
def save_texts_to_file(texts, filename, mode='w'):
    result = []
    # テキストデータをファイルに保存
    with open(filename, mode, encoding='utf-8') as file:
        for text in texts:
            result.append(", ".join(text))
        file.write("\n".join(result) + '\n')

# 初期ページのURLを設定
base_url = '開始URL'
target_url = '停止URL'  # 特定のURL
all_urls = []
all_links = []
# リンクを格納するリストを作成
elements_list = []
d = date.today()
d_str = d.strftime("%Y%m%d")
filename = 'output_genres_topics_'+d_str+'.txt'
links = get_all_pages_and_links(base_url, target_url)

# 3つ目の要素の重複回数をカウント
third_elements = [row[2] for row in links]
count_map = Counter(third_elements)

# 重複回数を4つ目の要素として追加
for row in links:
    row.append(str(count_map[row[2]]))

save_texts_to_file(links, filename, mode='a')  # 'a'モードで追記

print(f"Texts have been saved to {filename}")
