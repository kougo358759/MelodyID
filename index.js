
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
