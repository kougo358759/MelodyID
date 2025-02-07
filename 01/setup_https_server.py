import os
import subprocess

# 証明書関連のファイル名を定義
CERT_KEY = "server.key"
CERT_CSR = "server.csr"
CERT_CRT = "server.crt"
SAN_FILE = "SAN.txt"
NODE_SCRIPT = "index.js"

# SAN.txtファイルを作成
san_content = "subjectAltName = DNS:localhost"
with open(SAN_FILE, "w") as f:
    f.write(san_content)

# 証明書と秘密鍵の生成
print("Generating SSL certificate and key...")
subprocess.run(["openssl", "genrsa", "-out", CERT_KEY, "2048"])
subprocess.run(["openssl", "req", "-new", "-key", CERT_KEY, "-out", CERT_CSR, "-subj", "/C=JP/ST=Tokyo/L=Tokyo/O=MyOrg/OU=Dev/CN=localhost"])
subprocess.run(["openssl", "x509", "-req", "-days", "365", "-in", CERT_CSR, "-signkey", CERT_KEY, "-out", CERT_CRT, "-extfile", SAN_FILE])

# Node.js Expressサーバースクリプトを作成
node_script_content = """
const express = require('express');
const fs = require('fs');
const https = require('https');
const path = require('path');

const app = express();

const options = {
  key: fs.readFileSync('./server.key'),
  cert: fs.readFileSync('./server.crt'),
};

// 静的ファイルの提供設定
app.use(express.static(path.join(__dirname)));

// ルートにアクセスした際にindex.htmlを返す
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

https.createServer(options, app).listen(3000, () => {
  console.log('HTTPSサーバーがhttps://localhost:3000で起動しました');
});
"""


with open(NODE_SCRIPT, "w") as f:
    f.write(node_script_content)

# Node.jsの依存パッケージ（Express）をインストール
print("Installing Node.js packages...")
subprocess.run(["npm", "init", "-y"])
subprocess.run(["npm", "install", "express"])

# HTTPSサーバーを起動
print("Starting HTTPS server...")
subprocess.run(["node", NODE_SCRIPT])
