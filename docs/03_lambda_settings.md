# Lambdaの設定値変更（メモリ・タイムアウト）

## 学習目的
- Lambda のメモリサイズと計算性能の関係を理解する
- タイムアウト設定の役割を理解する
- Terraform で Lambda の設定値を変更できるようになる

## 実施内容
- 素数をカウントする Lambda 関数を作成
- 入力値（n）によって処理負荷を変更
- memory_size を変更して実行時間を比較
- timeout を変更して挙動を確認

## 設定変更（Terraform）
- aws_lambda_function に以下の属性を追加
  - timeout
  - memory_size
- 値を変更して terraform apply を実行

## 気づき
- Lambda はメモリサイズに応じて CPU 性能も変わる
- タイムアウトを延ばすだけでは処理は速くならない
- メモリを増やすことで実行時間が短くなるケースがある
- Lambda は「短時間で処理を終わらせる」設計が前提だと感じた
