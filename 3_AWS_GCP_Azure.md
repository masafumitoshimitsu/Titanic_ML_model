
### AWSでのデプロイ手順
#### 使用するAWSのサービス
- **Amazon EC2**: Webサーバーをホスティングする仮想マシン
- **Amazon S3**: モデルファイルの保存
- **Amazon RDS**: 必要に応じてデータベースの使用

#### 手順
1. **EC2インスタンスのセットアップ**
   - AWSマネジメントコンソールにログイン
   - EC2ダッシュボードから新しいインスタンスを起動
   - Amazon Linux 2またはUbuntuを選択
   - セキュリティグループでHTTP（ポート80）とSSH（ポート22）を許可
   - インスタンスに接続し、以下のコマンドを実行して環境をセットアップ
     ```bash
     sudo yum update -y  # Ubuntuの場合はsudo apt-get update -y
     sudo yum install python3 -y  # Ubuntuの場合はsudo apt-get install python3 -y
     sudo pip3 install virtualenv
     virtualenv venv
     source venv/bin/activate
     git clone https://github.com/yourusername/titanic-survival-prediction.git
     cd titanic-survival-prediction
     pip install -r requirements.txt
     ```

2. **Flaskアプリケーションの起動**
   - `app.py`ファイルを実行
     ```bash
     python app.py
     ```

3. **EC2インスタンスにパブリックIPアドレスが割り当てられていることを確認し、Webブラウザからアクセス**

#### アーキテクチャ図
```plaintext
+-------------------+      +------------------+      +----------------+
|   Amazon S3       | ---> |  Amazon EC2      | ---> |  Client        |
| (Model Storage)   |      | (Web Server)     |      | (Web Browser)  |
+-------------------+      +------------------+      +----------------+
```

### GCPでのデプロイ手順
#### 使用するGCPのサービス
- **Google Compute Engine**: Webサーバーをホスティングする仮想マシン
- **Google Cloud Storage**: モデルファイルの保存
- **Google Cloud SQL**: 必要に応じてデータベースの使用

#### 手順
1. **Compute Engineインスタンスのセットアップ**
   - GCPコンソールにログイン
   - Compute Engineダッシュボードから新しいインスタンスを作成
   - マシンタイプとイメージ（Debian、Ubuntuなど）を選択
   - ファイアウォールでHTTPとSSHトラフィックを許可
   - インスタンスに接続し、以下のコマンドを実行して環境をセットアップ
     ```bash
     sudo apt-get update -y
     sudo apt-get install python3 -y
     sudo apt-get install python3-pip -y
     pip3 install virtualenv
     virtualenv venv
     source venv/bin/activate
     git clone https://github.com/yourusername/titanic-survival-prediction.git
     cd titanic-survival-prediction
     pip install -r requirements.txt
     ```

2. **Flaskアプリケーションの起動**
   - `app.py`ファイルを実行
     ```bash
     python app.py
     ```

3. **Compute Engineインスタンスの外部IPアドレスを確認し、Webブラウザからアクセス**

#### アーキテクチャ図
```plaintext
+-----------------------+      +-----------------------+      +----------------+
| Google Cloud Storage  | ---> |  Google Compute Engine| ---> |  Client        |
| (Model Storage)       |      |  (Web Server)         |      | (Web Browser)  |
+-----------------------+      +-----------------------+      +----------------+
```

### Azureでのデプロイ手順
#### 使用するAzureのサービス
- **Azure Virtual Machines**: Webサーバーをホスティングする仮想マシン
- **Azure Blob Storage**: モデルファイルの保存
- **Azure SQL Database**: 必要に応じてデータベースの使用

#### 手順
1. **Virtual Machineのセットアップ**
   - Azureポータルにログイン
   - 仮想マシンを作成し、Ubuntu Serverまたは他のLinuxディストリビューションを選択
   - ネットワークセキュリティグループでHTTP（ポート80）とSSH（ポート22）を許可
   - インスタンスに接続し、以下のコマンドを実行して環境をセットアップ
     ```bash
     sudo apt-get update -y
     sudo apt-get install python3 -y
     sudo apt-get install python3-pip -y
     pip3 install virtualenv
     virtualenv venv
     source venv/bin/activate
     git clone https://github.com/yourusername/titanic-survival-prediction.git
     cd titanic-survival-prediction
     pip install -r requirements.txt
     ```

2. **Flaskアプリケーションの起動**
   - `app.py`ファイルを実行
     ```bash
     python app.py
     ```

3. **仮想マシンのパブリックIPアドレスを確認し、Webブラウザからアクセス**

#### アーキテクチャ図
```plaintext
+----------------------+      +----------------------+      +----------------+
|  Azure Blob Storage  | ---> |  Azure Virtual       | ---> |  Client        |
| (Model Storage)      |      |  Machines            |      | (Web Browser)  |
+----------------------+      +----------------------+      +----------------+
```

### まとめ
この手順を使用することで、AWS、GCP、Azureなどのクラウドサービス上でWebサーバーを実行し、新しいデータに対する推論とモデル更新機能を提供することができます。クラウド環境を利用することで、高い可用性とスケーラビリティを確保できます。
