terraform {
  # Terraformの状態（state）をローカルに保存する設定
  backend "local" {
    # stateファイルの保存場所
    # GitHubには載せない（.gitignoreで除外する）
    path = ".tfstate/hello-lambda.tfstate"
  }
}

# ===== 変数定義 =====

variable "aws_profile" {
  # AWS CLIで設定しているプロファイル名
  type    = string
  default = "develop"
}

variable "region" {
  # 利用するAWSリージョン（東京）
  type    = string
  default = "ap-northeast-1"
}

# ===== AWSプロバイダー設定 =====

provider "aws" {
  # どのAWSアカウントを使うか
  profile = var.aws_profile

  # どのリージョンを使うか
  region  = var.region
}

# ===== 既存IAMロールの取得 =====

data "aws_iam_role" "lambda_exec" {
  # 既にAWS上に存在するLambda実行用ロールを参照する
  # （このロール自体はTerraformでは作らない）
  name = "LambdaBasicExecutionRole"
}

# ===== LambdaコードをZIP化 =====

data "archive_file" "lambda_zip" {
  # ZIP形式で圧縮する
  type = "zip"

  # 圧縮元のファイル（PythonのLambdaコード）
  source_file = "${path.module}/lambda_function.py"

  # 出力されるZIPファイルのパス
  output_path = "${path.module}/.build/lambda_function.zip"
}

# ===== Lambda関数の作成 =====

resource "aws_lambda_function" "hello" {
  # AWS上に作成されるLambda関数名
  function_name = "hello-lambda-tf-demo"

  # Lambda実行時に使われるIAMロールのARN
  role = data.aws_iam_role.lambda_exec.arn

  # Lambdaのエントリーポイント
  # 「ファイル名.関数名」の形式
  handler = "lambda_function.lambda_handler"

  # 実行環境（Python 3.12）
  runtime = "python3.12"

  # アップロードするZIPファイル
  filename = data.archive_file.lambda_zip.output_path

  # ZIPファイルのハッシュ値
  # ソースコードが変更されたことをTerraformに検知させるために必要
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  # Lambdaに渡す環境変数
  environment {
    variables = {
      GREETING_TARGET = "World"
    }
  }
}
