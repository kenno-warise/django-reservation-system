#!/bin/bash
# コードチェックとテストを実行するためのシェルスクリプト
# 作成日 2022-10-14

# pep8に準拠した妥協のないコードフォーマッター
black reserve/views.py reserve/urls.py reserve/forms.py reserve/models.py reserve/admin.py config/urls.py config/settings.py
# pep8に準拠していないコードを取得する
flake8 reserve/views.py reserve/urls.py reserve/forms.py reserve/models.py reserve/admin.py config/urls.py config/settings.py
# pep8に準拠したimport文を綺麗にコーディングし直す
isort reserve config/urls.py
# DjangoのUnitTest
coverage run --include=reserve/* --omit=reserve/migrations/* manage.py test reserve
# Coverageレポートの出力
coverage report
# カバレッジの進捗をHTMLで表示
coverage html
# カバレッジHTMLのリンク↓↓
echo file:///C:/Users/warik/Documents/PYTHON/django-app/django-reserve/htmlcov/index.html
