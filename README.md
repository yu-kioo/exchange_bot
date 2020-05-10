## 開発環境立ち上げ
- `source venv/bin/activate`
- `python app.py`

## Flask
- [official_doc](https://a2c.bitbucket.io/flask/)

## venv管理

- 仮想環境の起動
  - `source venv/bin/activate`
- 解除
  - `deactivate`
- pythonのversion確認
  - `python -V`

- ref
  - [venv: Python 仮想環境管理
](https://qiita.com/fiftystorm36/items/b2fd47cf32c7694adc2e)

## Herokuへのデプロイ
- 最低限必要なファイル
  - 実行ファイル
  - requirements.txt
- option
  - Procfile：

- [HerokuにFlaskアプリ(hello world)をデプロイする方法まとめ
](https://tanuhack.com/deploy-flask-heroku/)

## その他メモ
- postの確認
  - `curl -X POST -d '{"para1": val1, "para2": val2}' https://exchange-trading-bot.herokuapp.com/post`