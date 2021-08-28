mf_scraping
====

[![Upload MoneyForward JSON](https://github.com/legnoh/mf_scraping/actions/workflows/scrap.yml/badge.svg)](https://github.com/legnoh/mf_scraping/actions/workflows/scrap.yml)

MoneyForward にログインし、下記の内容をスクレイピングしたJSONを出力します。

- [トップページ](https://moneyforward.com/) 「＊月の収支」欄の当月収入、当月支出、当月収支
- [資産](https://moneyforward.com/bs/portfolio) ページの資産総額、各項目
- [負債](https://moneyforward.com/bs/liability) ページの負債総額、各項目

Usage
----

### local

```sh
brew install pipenv google-chrome
git clone https://github.com/legnoh/mf_scraping.git && cd mf_scraping
pipenv install && pipenv shell
pipenv run scrap
```

JSON 生成例
----

[moneyforward_sample.json](./moneyforward_sample.json) をご覧ください。

免責事項
----

- 当スクリプトは、MoneyForward 本家からは非公認のものです。
  - これらを利用したことによるいかなる損害についても当方では責任を負いかねます。
- 当スクリプトはこれらのサイトに対し、負荷をかけることを目的として制作したものではありません。
  - 利用の際は常識的な範囲でのアクセス頻度に抑えてください。
- 先方に迷惑をかけない範囲での利用を強く推奨します。
