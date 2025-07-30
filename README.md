# 🪴 SysTradeHub

> **Trade your ideas like you trade your code.**  
> 自分の学び・アイデア・トレードの知見を育てていくデジタルガーデンです。

## About

SysTradeHub は [Quartz v4](https://quartz.jzhao.xyz/) をフォークして構築した、個人用のナレッジベース & アウトプットプラットフォームです。  
ソースは全て公開しており、だれでもクローン & フォークして自身のデジタルガーデンを作成できます。

### 公開サイト

| 用途 | URL |
| :--- | :--- |
| 💻 GitHub Pages (`content` フォルダ) | https://bottersatoshi.github.io/SysTradeHub/ |
| ✍️ Zenn (`books` / `articles` フォルダ) | https://zenn.dev/bottersatoshi |

## ディレクトリ構成

```text
SysTradeHub/
├─ content/        # GitHub Pages で公開される MD/MDX ノート
├─ books/          # Zenn Book 原稿
├─ articles/       # Zenn Article 原稿
├─ .github/
│   └─ workflows/
│       └─ deploy.yml  # content → GitHub Pages 自動デプロイ
└─ quartz/         # Quartz エンジン（独自カスタマイズ）
```

## CI / CD

`main` ブランチへの push をトリガに GitHub Actions で以下を実行します。

1. 依存パッケージのインストール
2. Quartz ビルド (`pnpm build`)
3. 生成した静的サイトを `gh-pages` ブランチへデプロイ

YAML 定義は `.github/workflows/deploy.yml` を参照してください。

## Development

```bash
# 依存パッケージを取得
pnpm install

# 開発サーバを立ち上げ
pnpm dev
# http://localhost:3000 で確認
```

## License

This repository is licensed under the MIT License – see `LICENSE.txt` for details.

---

Made with ❤️ & ☕ by [botterSatoshi](https://github.com/bottersatoshi)
