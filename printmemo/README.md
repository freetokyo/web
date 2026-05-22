# App Store Connect / Marketing 用ドキュメント

このディレクトリには、App Store Connect の `Privacy Policy URL` と `Support URL`、および SNS・SEO・ASO の導線に使える静的 HTML を配置しています。

アプリのローカライズ戦略やメタデータ下書きは、[README.md](/Users/yanglichen/Applications/PrintMemo/AppStoreAssets/localizations/README.md) を参照してください。

## ファイル

- `printmemo.html`
  Marketing 用ランディングページ。SNS プロフィール、検索流入、補助導線向け。
- `printmemo-support.html`
  App Store Connect の `Support URL` 向け。
- `printmemo-privacy-policy.html`
  App Store Connect の `Privacy Policy URL` 向け。
- `printmemo-terms.html`
  利用規約ページ。必要に応じて外部公開 URL として案内用に使用。

## 公開方法の例

1. GitHub Pages、Cloudflare Pages、Netlify などの静的ホスティングへ配置する
2. 公開 URL を確認する
3. 必要に応じて以下へ設定する

- `Privacy Policy URL`: `printmemo-privacy-policy.html` の公開 URL
- `Support URL`: `printmemo-support.html` の公開 URL
- 利用規約案内: `printmemo-terms.html` の公開 URL
- SNS プロフィールや紹介ポスト: `printmemo.html` の公開 URL
- SEO 用の基本導線: `printmemo.html` を起点に `support` `privacy` `terms` を相互リンク

## 公開前の確認

- 問い合わせ先メールアドレスが最新であること
- App 名称が `PrintSummary / プリサマ` に統一されていること
- 記載内容が現行実装と一致していること
- App Store Connect に入力する説明文やスクリーンショット訴求と整合していること
