# Copilot Instructions for CamFesProject

## 概要
このリポジトリは、学園祭向けのWebアプリケーションです。バックエンド（FastAPI + MySQL）とフロントエンド（React + Vite）で構成されています。Docker Composeでローカル開発環境を構築します。

## アーキテクチャ
- **backend/**: FastAPIベースのAPIサーバー。`app/routers/system.py` などでAPIエンドポイントを定義。
  - DBはMySQL（`db/`）、SQLAlchemyによるORM利用。
  - 認証はAPIキー依存（`core/verify_apikey.py`）。
  - 静的ファイル・テンプレートは `static/`・`templates/` 配下。
- **frontend/**: React（TypeScript, Vite）製SPA。API通信は `src/api/apiClient.ts` でラップ。
- **ArUco/**: 画像認識・マーカー生成用Pythonスクリプト群。
- **docker-compose.yml**: バックエンド・DBのローカル開発用。`docker-compose up` で起動。

## 開発・ビルド・テスト
- バックエンド起動: `docker-compose up`（初回はDB初期化に時間がかかる場合あり）
- フロントエンド起動: `cd frontend && npm install && npm run dev`
- バックエンド依存: `backend/requirements.txt` で管理。必要に応じて `pip install -r requirements.txt`。
- APIエンドポイント例: `/api/get-users`（GET）、`/api/get-user`（POST, APIキー必要）
- DBスキーマ変更時は `backend/app/db/base.py` などを修正

## コーディング規約・パターン
- フロントエンドのAPI通信は必ず `src/api/apiClient.ts` 経由で行う
- バックエンドのAPI追加は `routers/` 配下にルーターを追加し、`main.py` で `include_router` する
- 認証が必要なAPIは `Depends(verify_api_key)` を利用
- DBアクセスは `AsyncSession` + SQLAlchemy ORM
- 静的ファイルは `/static`、テンプレートは `/templates` で管理
- フロントエンドの型定義は `src/types/` にまとめる

## 参考ファイル
- バックエンドAPI例: `backend/app/routers/system.py`
- フロントエンドAPI利用例: `frontend/src/api/apiClient.ts`
- DBモデル例: `backend/app/models/users.py`
- マーカー認識: `ArUco/aruco_detected.py`

## 注意点
- APIキーは `.env` で管理（リポジトリには含めない）
- DB初期化やマイグレーションは手動で行う場合あり
- Docker環境でのパスやボリュームマウントに注意

---
このドキュメントはAIエージェント向けのガイドです。内容に不明点や追加要望があればフィードバックしてください。
