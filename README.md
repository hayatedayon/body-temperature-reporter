# body-temperature-reporter

## 説明

セコムのe-革新自動報告スクリプトとcron用設定ファイル生成スクリプトです。  
自分用ですが、カスタマイズすれば他の方でも利用できると思うので公開します。  

## 使い方

1. generate_password.shでパスワードファイルを生成します  
`./generate_password.sh password`  
2. generate_cron_conf.shでcronの設定ファイル(report.conf)を生成します  
`./generate_cron_conf.sh`  
3. 依存パッケージをインストールします  
`pip3 install -r requirements.txt`   
4. main.pyのCOMPANY_NOとUSER_IDを設定します  
5. cronに登録します  
`crontab report.conf`  
6. cronが動いているか確認し、動いてない場合は動かしておきましょう  
`sudo service cron status`  
`sudo service cron start`  

## 注意事項

- パスワードはBase64エンコードして保存しています。不安な方は利用しないようにしてください。

## その他

- デフォルトでは、7:30に自動報告する設定ファイルを生成します。
- デフォルトでは、実行ログはmain.pyがあるディレクトリにlog.logとして追記されていきます。
