
---

# Titanic Survival Prediction Web Application

このリポジトリには、機械学習モデルを使用してタイタニック号の乗客の生存を予測するためのFlaskベースのWebアプリケーションが含まれています。このアプリケーションは、モデル推論およびモデル更新をRESTfulエンドポイントを介して行うことができます。

This repository contains a Flask-based web application for predicting the survival of passengers on the Titanic using a machine learning model. The application allows for model inference and model updating via RESTful endpoints.

## Table of Contents 目次
- [Installation インストール](#installation-インストール)
- [Usage 使い方](#usage-使い方)
- [API Endpoints APIエンドポイント](#api-endpoints-apiエンドポイント)
- [Model Training and Updating モデルのトレーニングと更新](#model-training-and-updating-モデルのトレーニングと更新)
- [License ライセンス](#license-ライセンス)

## Installation インストール

1. Clone the repository リポジトリをクローン:
    ```bash
    git clone https://github.com/yourusername/titanic-survival-prediction.git
    cd titanic-survival-prediction
    ```

2. Create a virtual environment and activate it 仮想環境を作成してアクティブ化:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windowsの場合は `venv\Scripts\activate`
    ```

3. Install the required dependencies 必要な依存関係をインストール:
    ```bash
    pip install -r requirements.txt
    ```

## Usage 使い方

1. Start the Flask application Flaskアプリケーションを開始:
    ```bash
    python app.py
    ```

2. The application will be running on `http://127.0.0.1:5000/`. You can use tools like `curl`, `Postman`, or any other HTTP client to interact with the API.
   アプリケーションは`http://127.0.0.1:5000/`で実行されます。`curl`や`Postman`などのHTTPクライアントを使用してAPIと対話できます。

## API Endpoints APIエンドポイント

### Predict Endpoint 予測エンドポイント

- **URL:** `/predict`
- **Method:** `POST`
- **Description:** Predict the survival of a passenger based on their details.
  乗客の詳細に基づいて生存を予測します。
- **Request Body リクエストボディ:**
    ```json
    {
        "Pclass": [3],
        "Sex": [0],
        "Age": [22.0],
        "Fare": [7.25]
    }
    ```
- **Response レスポンス:**
    ```json
    {
        "prediction": [0]  # 0は生存しなかったことを示し、1は生存したことを示します。
    }
    ``*

### Update Model Endpoint モデル更新エンドポイント

- **URL:** `/update_model`
- **Method:** `POST`
- **Description:** Train a new model with the latest data and update the current model if it performs better.
  最新のデータで新しいモデルを訓練し、性能が良ければ現在のモデルを更新します。
- **Response レスポンス:**
    ```json
    {
        "status": "Model updated",
        "new_accuracy": 0.85,
        "old_accuracy": 0.82
    }
    ```

## Model Training and Updating モデルのトレーニングと更新

The model training and updating process is automated through the `/update_model` endpoint. This endpoint:
モデルのトレーニングと更新プロセスは、`/update_model`エンドポイントを通じて自動化されています。このエンドポイントは以下のことを行います:

1. Loads the latest Titanic dataset. 最新のタイタニックデータセットをロードします。
2. Preprocesses the data. データを前処理します。
3. Trains a new logistic regression model. 新しいロジスティック回帰モデルを訓練します。
4. Evaluates the new model against the test set. 新しいモデルをテストセットに対して評価します。
5. Compares the new model's performance with the current model. 新しいモデルの性能を現在のモデルと比較します。
6. Updates the current model if the new model performs better. 新しいモデルの性能が良ければ、現在のモデルを更新します。

## License ライセンス

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
このプロジェクトはMITライセンスの下でライセンスされています。詳細については[LICENSE](LICENSE)ファイルを参照してください。


---

### 追加のノート Additional Notes
1. **Requirements File 必要なファイル**: 必要な依存関係を記載した`requirements.txt`ファイルを含めてください。
    ```text
    Flask
    pandas
    scikit-learn
    joblib
    ```

2. **ファイル構成 File Structure**:
    - `app.py`: The main Flask application file. メインのFlaskアプリケーションファイル。
    - `requirements.txt`: Contains all the required Python packages. 必要なPythonパッケージを含みます。
    - `README.md`: The file you are currently reading. 現在読んでいるファイル。

このREADMEを使用することで、第三者の開発者が容易にセットアップ、使用、および貢献できるようになります。
