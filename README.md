# Hit&Blow Team F

====
hitblowの

hitblow.py - web上での通信対戦(パーサーでroom_id,mode,ansを指定可能), 実行は streamlit run hitblow.py

hitblow_100times_auto.py - ターミナル上での100回自動通信対戦(パーサーでroom_id,mode,ansを指定可能)

hitblow_play_solo.py - web上での一人でのcom対戦(パーサーでmode,ansを指定可能), 実行は streamlit run hitblow_play_solo.py

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
