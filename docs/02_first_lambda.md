# はじめてのAWS Lambda（Terraform）

## 学習目的
- TerraformでLambdaをデプロイする流れを理解する

## 実施内容
- PythonのLambda関数を作成
- archive_fileでZIP化
- aws_lambda_functionでデプロイ

## 気づき
- LambdaはZIP化が必須
- source_code_hashがないと変更が反映されない
