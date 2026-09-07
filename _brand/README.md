# _brand — ブランド情報の一元管理

`brand.json` が **ブランド名と連絡先の唯一の真実源**。web/ 配下の 2,900 本超の
HTML / JSON / JS / TXT / PY は全部ここから配られた値を持っている。

## 変えたいとき

1. `brand.json` を直す。**旧い値は `previous_*` に足す（消さない）**。
2. 反映する。

```bash
python3 _brand/apply_brand.py --apply
```

例：連絡先を変える場合

```json
"contact": {
  "email": "hello@freetokyolabs.com",
  "previous_emails": [
    "freetokyo2020@yahoo.co.jp",
    "chenyangli123@gmail.com",
    "support@freetokyolabs.com"     ← 旧くなった値をここに足す
  ]
}
```

## 使い方

| コマンド | すること |
|---|---|
| `python3 _brand/apply_brand.py` | 確認のみ。ズレていれば件数を出して exit 1（既定・書かない） |
| `python3 _brand/apply_brand.py --apply` | 書き込む |
| `python3 _brand/apply_brand.py -v` | ファイルごとの内訳も出す |

冪等。`--apply` を二度流しても二度目は 0 件になる。引数なしの実行はズレ検出なので、
出荷前チェックや CI にそのまま噛ませられる。

## なぜ静的置換なのか（JS で参照しない理由）

`<title>` / `og:site_name` / JSON-LD / `<meta description>` を JS で書き換えると、
**JS を実行しない OGP クローラ（X・Facebook・LINE・Bing）に届かない**。SNS のシェア
カードと検索結果に旧名や空白が出る。各 HTML は共通 JS を読み込まない完全自己完結の
構造でもあるため、出力は静的 HTML のままにして、真実源からの反映をビルド時（=この
スクリプト）に寄せている。

## 触らない場所

`apply_brand.py` の `SKIP_DIRS` に `_brand` が入っている。ここを外すと `brand.json` の
`previous_*` に積んだ履歴自体が置換されて消える。
