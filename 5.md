AIの推論結果をサマリとして表示する方法について、以下の情報を含めることが一般的です。具体的な表示形式や可視化手法も併せて説明します。

### 含める情報
1. **予測結果**:
   - 各データポイントに対する予測結果（例：生存、死亡）。
2. **確信度スコア**:
   - 各予測に対するモデルの確信度（確率）。
3. **入力データの概要**:
   - 予測対象となったデータの要約（例：年齢、性別、料金など）。
4. **集計結果**:
   - 全体の予測結果の集計（例：生存者の割合、死亡者の割合）。
5. **モデルのパフォーマンス指標**:
   - モデルの性能指標（例：正確性、精密度、再現率、F1スコア）。

### 表示形式
1. **テキスト形式**:
   - 簡潔なテキストでの概要表示。
2. **表形式**:
   - 入力データと対応する予測結果を表形式で表示。
3. **グラフ・チャート**:
   - バーチャート、パイチャート、ヒストグラムなどを使用して予測結果や集計結果を視覚的に表示。
4. **ダッシュボード**:
   - 上記の要素を統合したダッシュボード形式での表示。

### 可視化手法の例
- **Matplotlib**: 基本的なグラフを作成するためのPythonライブラリ。
- **Seaborn**: 統計データの可視化を行うためのライブラリ。
- **Plotly**: インタラクティブなグラフを作成するためのライブラリ。
- **Dash**: Plotlyと連携してインタラクティブなダッシュボードを作成するためのフレームワーク。

### サンプルコード
以下に、Flaskアプリケーション内で推論結果のサマリを表示する方法を示します。

```python
from flask import Flask, request, jsonify, render_template
import pandas as pd
import mlflow
import mlflow.sklearn
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

app = Flask(__name__)

# MLflowから最新モデルをロード
def load_latest_model():
    runs = mlflow.search_runs(order_by=["end_time DESC"], max_results=1)
    latest_run_id = runs.iloc[0].run_id
    model = mlflow.sklearn.load_model(f"runs:/{latest_run_id}/model")
    return model

model = load_latest_model()

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    new_data = pd.DataFrame(data)
    predictions = model.predict(new_data)
    probabilities = model.predict_proba(new_data)
    
    # サマリ情報の作成
    summary = create_summary(new_data, predictions, probabilities)
    
    # 可視化の作成
    chart = create_visualization(predictions)
    
    return render_template('summary.html', summary=summary, chart=chart)

def create_summary(data, predictions, probabilities):
    data['Prediction'] = predictions
    data['Probability'] = probabilities.max(axis=1)
    summary = {
        'total': len(data),
        'survived': data['Prediction'].sum(),
        'not_survived': len(data) - data['Prediction'].sum(),
        'details': data.to_dict(orient='records')
    }
    return summary

def create_visualization(predictions):
    sns.set(style="darkgrid")
    plt.figure(figsize=(10, 6))
    sns.countplot(predictions)
    plt.title('Prediction Summary')
    plt.xlabel('Survived')
    plt.ylabel('Count')
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    chart = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    return chart

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
```

### HTMLテンプレートの例
`templates/summary.html`:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Prediction Summary</title>
</head>
<body>
    <h1>Prediction Summary</h1>
    <p>Total Predictions: {{ summary.total }}</p>
    <p>Survived: {{ summary.survived }}</p>
    <p>Not Survived: {{ summary.not_survived }}</p>
    <h2>Details</h2>
    <table border="1">
        <tr>
            <th>Pclass</th>
            <th>Sex</th>
            <th>Age</th>
            <th>Fare</th>
            <th>Prediction</th>
            <th>Probability</th>
        </tr>
        {% for item in summary.details %}
        <tr>
            <td>{{ item.Pclass }}</td>
            <td>{{ item.Sex }}</td>
            <td>{{ item.Age }}</td>
            <td>{{ item.Fare }}</td>
            <td>{{ item.Prediction }}</td>
            <td>{{ item.Probability }}</td>
        </tr>
        {% endfor %}
    </table>
    <h2>Visualization</h2>
    <img src="data:image/png;base64,{{ chart }}">
</body>
</html>
```

### まとめ
- **テキスト形式**: 予測結果の概要を簡潔に表示。
- **表形式**: 入力データと対応する予測結果を詳細に表示。
- **グラフ・チャート**: 予測結果や集計結果を視覚的に表示。
- **ダッシュボード**: 上記の要素を統合したインタラクティブな表示。

このようなサマリ表示と可視化により、AIの推論結果を直感的に理解しやすくなります。
