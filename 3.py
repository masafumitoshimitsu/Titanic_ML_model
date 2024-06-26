#コード実装 リクエストを受け取ると学習したAIモデルを使って新たなデータに対して推論を行うWebサーバーを構築してください。

#新たなデータを取得、選択する方法は自由です。（リクエストに含める、クラウドからダウンロードする等）
#使用するモデルの更新を行うための機能を実装してください。

from flask import Flask, request, jsonify
import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report

app = Flask(__name__)

MODEL_PATH = 'titanic_model.pkl'
DATA_URL = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"

# モデルの読み込み
def load_model(file_path):
    return joblib.load(file_path)

# モデルの保存
def save_model(model, file_path):
    joblib.dump(model, file_path)

# データの読み込みと前処理
def load_and_preprocess_data(url):
    data = pd.read_csv(url)
    data = data[['Survived', 'Pclass', 'Sex', 'Age', 'Fare']]
    data['Sex'] = data['Sex'].map({'male': 0, 'female': 1})
    data = data.dropna()
    return data

# 特徴量とターゲットの分離
def split_features_and_target(data):
    X = data.drop('Survived', axis=1)
    y = data['Survived']
    return X, y

# モデルの訓練
def train_model(X_train, y_train):
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    return model

# モデルの評価
def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions)
    recall = recall_score(y_test, predictions)
    f1 = f1_score(y_test, predictions)
    roc_auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
    report = classification_report(y_test, predictions)
    return accuracy, precision, recall, f1, roc_auc, report

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    new_data = pd.DataFrame(data)
    model = load_model(MODEL_PATH)
    prediction = model.predict(new_data)
    return jsonify({'prediction': prediction.tolist()})

@app.route('/update_model', methods=['POST'])
def update_model():
    # データの読み込みと前処理
    data = load_and_preprocess_data(DATA_URL)
    
    # 特徴量とターゲットの分離
    X, y = split_features_and_target(data)
    
    # 訓練データとテストデータの分割
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 新しいモデルの訓練
    new_model = train_model(X_train, y_train)
    
    # 新しいモデルの評価
    new_metrics = evaluate_model(new_model, X_test, y_test)
    
    try:
        old_model = load_model(MODEL_PATH)
        old_metrics = evaluate_model(old_model, X_test, y_test)
    except FileNotFoundError:
        old_metrics = (0, 0, 0, 0, 0, '')  # 初回は古いモデルのメトリクスをゼロに設定
    
    # モデルの比較と更新
    new_accuracy, _, _, _, _, _ = new_metrics
    old_accuracy, _, _, _, _, _ = old_metrics
    
    if new_accuracy > old_accuracy:
        save_model(new_model, MODEL_PATH)
        return jsonify({'status': 'Model updated', 'new_accuracy': new_accuracy, 'old_accuracy': old_accuracy})
    else:
        return jsonify({'status': 'Old model retained', 'new_accuracy': new_accuracy, 'old_accuracy': old_accuracy})

if __name__ == '__main__':
    app.run(debug=True)
