以下に、結果を見渡しやすくするためのダッシュボードの実装例を示します。Dashを使用して、インタラクティブなダッシュボードを構築します。

### 必要なライブラリのインストール

まず、必要なライブラリをインストールします。

```bash
pip install dash pandas mlflow scikit-learn matplotlib
```

### Dashアプリケーションの実装

以下に、Dashを使用してモデルの性能比較結果を可視化するダッシュボードの実装例を示します。

#### ダッシュボードの構成要素
1. **モデルのメトリクス表示**: 初期モデルと新しいモデルのメトリクスを表示します。
2. **グラフ**: 各メトリクスのバーグラフとROC曲線を表示します。
3. **モデルの切り替え**: モデルのバージョンを選択して、過去のモデルにロールバックする機能を提供します。

#### ダッシュボードのコード

```python
import dash
from dash import dcc, html, Input, Output
import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
from sklearn.metrics import roc_curve, auc
import plotly.graph_objs as go

app = dash.Dash(__name__)

# MLflowから特定のモデルをロード
def load_model(run_id):
    return mlflow.sklearn.load_model(f"runs:/{run_id}/model")

# モデルの評価
def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)
    probas = model.predict_proba(X_test)
    fpr, tpr, _ = roc_curve(y_test, probas[:, 1])
    roc_auc = auc(fpr, tpr)
    
    metrics = {
        'accuracy': accuracy_score(y_test, predictions),
        'precision': precision_score(y_test, predictions),
        'recall': recall_score(y_test, predictions),
        'f1_score': f1_score(y_test, predictions),
        'roc_auc': roc_auc,
        'fpr': fpr,
        'tpr': tpr
    }
    return metrics

# データの読み込みと前処理
def load_and_preprocess_data(url):
    data = pd.read_csv(url)
    data = data[['Survived', 'Pclass', 'Sex', 'Age', 'Fare']]
    data['Sex'] = data['Sex'].map({'male': 0, 'female': 1})
    data = data.dropna()
    return data

url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
data = load_and_preprocess_data(url)
X, y = data.drop('Survived', axis=1), data['Survived']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 初期モデルと新しいモデルの評価結果
initial_run_id = "初期モデルのランID"
new_run_id = "新しいモデルのランID"

initial_model = load_model(initial_run_id)
new_model = load_model(new_run_id)

initial_metrics = evaluate_model(initial_model, X_test, y_test)
new_metrics = evaluate_model(new_model, X_test, y_test)

app.layout = html.Div([
    html.H1("モデルの性能比較ダッシュボード"),
    
    html.Div([
        dcc.Dropdown(
            id='model-dropdown',
            options=[
                {'label': 'Initial Model', 'value': initial_run_id},
                {'label': 'New Model', 'value': new_run_id}
            ],
            value=initial_run_id
        ),
    ]),
    
    html.Div(id='metrics-display'),
    
    dcc.Graph(id='metrics-graph'),
    
    dcc.Graph(id='roc-curve')
])

@app.callback(
    Output('metrics-display', 'children'),
    Output('metrics-graph', 'figure'),
    Output('roc-curve', 'figure'),
    Input('model-dropdown', 'value')
)
def update_dashboard(selected_run_id):
    model = load_model(selected_run_id)
    metrics = evaluate_model(model, X_test, y_test)
    
    # メトリクスの表示
    metrics_display = html.Div([
        html.H2("モデルのメトリクス"),
        html.P(f"Accuracy: {metrics['accuracy']:.2f}"),
        html.P(f"Precision: {metrics['precision']:.2f}"),
        html.P(f"Recall: {metrics['recall']:.2f}"),
        html.P(f"F1 Score: {metrics['f1_score']:.2f}"),
        html.P(f"ROC AUC: {metrics['roc_auc']:.2f}")
    ])
    
    # メトリクスのグラフ
    metrics_graph = {
        'data': [
            go.Bar(name='Initial Model', x=list(initial_metrics.keys())[:-2], y=list(initial_metrics.values())[:-2]),
            go.Bar(name='New Model', x=list(new_metrics.keys())[:-2], y=list(new_metrics.values())[:-2])
        ],
        'layout': go.Layout(title='モデルのメトリクス', barmode='group')
    }
    
    # ROC曲線
    roc_curve_fig = {
        'data': [
            go.Scatter(x=metrics['fpr'], y=metrics['tpr'], mode='lines', name='Selected Model ROC'),
            go.Scatter(x=[0, 1], y=[0, 1], mode='lines', name='Random', line=dict(dash='dash'))
        ],
        'layout': go.Layout(title='ROC Curve', xaxis={'title': 'False Positive Rate'}, yaxis={'title': 'True Positive Rate'})
    }
    
    return metrics_display, metrics_graph, roc_curve_fig

if __name__ == '__main__':
    app.run_server(debug=True)
```

### ダッシュボードの使い方
1. **モデルの選択**: ドロップダウンメニューから比較したいモデル（初期モデルまたは新しいモデル）を選択できます。
2. **メトリクスの表示**: 選択したモデルのメトリクスが表示されます。
3. **メトリクスのグラフ**: 各メトリクスのバーグラフで初期モデルと新しいモデルの比較を視覚的に確認できます。
4. **ROC曲線**: 選択したモデルのROC曲線が表示され、モデルの性能を視覚的に確認できます。

### 結果の解釈と有用性
- **メトリクスの比較**: ダッシュボードで表示されるメトリクス（精度、精密度、再現率、F1スコア、ROC AUC）は、初期モデルと新しいモデルの性能を直接比較するのに有用です。
- **ROC曲線**: ROC曲線は、モデルの識別能力を視覚的に評価するための有力なツールであり、モデルの改良の効果を確認するのに役立ちます。
- **インタラクティブなダッシュボード**: ユーザーがインタラクティブにモデルを選択し、異なるモデルの性能を比較することができるため、モデル管理と評価が容易になります。

このダッシュボードにより、モデルの性能を直感的に理解し、改善点を特定しやすくなります。また、モデルのバージョン管理やロールバックの機能も備えているため、運用環境でのモデル管理が効率的に行えます。
