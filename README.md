# Hit&Blow Team F

====
hitblowの

hitblow_100times_auto.py - ターミナル上での100回自動通信対戦(パーサーでroom_id,ansを指定可能)

hitblow.py - web上での自動通信対戦(パーサーでansを指定可能), 実行は streamlit run hitblow.py

hitblow_solo.py - web上での自動com対戦(パーサーでansを指定可能), 実行は streamlit run hitblow_solo.py

hitblow_solo_manual.py - web上での手動com対戦(パーサーでansを指定可能) 実行は streamlit run hitblow_solo_manual.py

## 環境

-python = 3.9.1

## セットアップ方法

```sh
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
pyenv install 3.9.1
pyenv local 3.9.1
pyenv rehash
pipenv install --dev --python 3.9.1
pipenv shell
pipenv sync
.\.venv\Scripts\activate(vscode以外のターミナルで実行する際)
& c:/Users/Hayato/NEDO-Hit-Blow-teamF/.venv/Scripts/Activate.ps1
(2回目以降,仮想環境が自動で立ち上がらなかったら)
```
