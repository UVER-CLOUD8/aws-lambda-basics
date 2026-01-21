# aws-lambda-basics

このリポジトリは **AWS Lambda の基本機能を体系的に学習するための学習ログ** です。  
Lambda の仕組み理解だけでなく、**コード管理・GitHub 運用に慣れること**も目的としています。

## 学習内容

### AWS Lambda（基本編）

- はじめての AWS Lambda
- Lambda の設定値変更（メモリ、タイムアウト）
- Lambda の環境変数
- Lambda のレイヤー
- 複数の Lambda をデプロイ
- Lambda の定期実行（EventBridge）

---

## ディレクトリ構成

```text
.
├── docs/
│   ├── 01_intro_lambda.md        # Lambda の概要・基本概念
│   └── 02_first_lambda.md        # 初めての Lambda 実装メモ
│   └── 03_lambda_settings.md     # Lambdaの設定値変更
│
├── src/
│   └── hello_lambda/
│       └── lambda_function.py   # Lambda 関数本体（Python）
│
├── main.tf                      # Terraform による Lambda 定義
├── README.md                    # このファイル
└── .gitignore