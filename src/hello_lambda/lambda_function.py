import os      # 環境変数を扱うための標準ライブラリ
import json    # JSON形式の文字列を作るための標準ライブラリ

def lambda_handler(event, context):
    # 環境変数 GREETING_TARGET を取得
    # 設定されていない場合は "World" を使う
    target = os.getenv("GREETING_TARGET", "World")

    # Lambdaの戻り値（HTTPレスポンス風）
    return {
        # 正常終了を表すステータスコード
        "statusCode": 200,

        # レスポンスヘッダー
        "headers": {
            "content-type": "application/json; charset=utf-8"
        },

        # 実際に返すデータ（JSON文字列）
        "body": json.dumps({
            "message": f"Hello, {target}!"
        })
    }
