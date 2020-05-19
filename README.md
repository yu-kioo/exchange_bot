## 開発環境立ち上げ
- `python app.py`

## Flask
- [official-doc](https://a2c.bitbucket.io/flask/)

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


## Heroku

### deploy
- 最低限必要なファイル
  - 実行ファイル
  - requirements.txt
- option
  - Procfile

- [HerokuにFlaskアプリ(hello world)をデプロイする方法まとめ
](https://tanuhack.com/deploy-flask-heroku/)

### 環境変数

基本的な管理は python-dotenv

#### heroku
```
heroku login
heroku config:set SECRET_KEY="SECRET_KEY" --app heroku_app_name
heroku config --app {heroku_app_name}
```

## その他メモ
- requirements.txtの出力
  - `pip freeze > requirements.txt`
- postの確認
  - `curl -X POST -d '{"para1": val1, "para2": val2}' https://exchange-trading-bot.herokuapp.com/post`
