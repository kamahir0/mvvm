# MVVMアーキテクチャ入門 - Slidevプレゼンテーション

Slidevを使ったプレゼンテーション作成環境です。  
AIとの対話でスライドの内容を作成・編集できます。

## セットアップ

```bash
npm install
```

## 開発サーバー起動

```bash
npm run dev
```

ブラウザで [http://localhost:3030](http://localhost:3030) を開いてスライドを確認できます。

## スライドの編集

`slides.md` をMarkdownで編集するだけでスライドが更新されます。  
AIに指示してスライドの追加・変更が可能です。

## ビルド・エクスポート

```bash
# SPAとしてビルド
npm run build

# PDFにエクスポート
npm run export
```

## 便利なコマンド

| コマンド | 説明 |
|---------|------|
| `npm run dev` | 開発サーバーを起動 |
| `npm run build` | SPAとしてビルド |
| `npm run export` | PDFにエクスポート |

## Slidevの機能

- **Markdownベース**: スライドをMarkdownで記述
- **テーマ**: `slides.md` のfrontmatterでテーマを変更可能
- **コードハイライト**: Shiki/Prismによるシンタックスハイライト
- **Mermaid図**: Mermaid記法で図表を描画
- **Vueコンポーネント**: カスタムコンポーネントの埋め込み
- **ライブコーディング**: Monaco Editorの組み込み
- **アニメーション**: スライドトランジション、クリックアニメーション

## 参考リンク

- [Slidev公式ドキュメント](https://sli.dev)
- [Slidev GitHub](https://github.com/slidevjs/slidev)
- [Slidevテーマギャラリー](https://sli.dev/themes/gallery)
