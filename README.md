# Discord Bot with Flask Server

## 功能介紹
本程式是一個結合 Flask 伺服器與 Discord Bot 的應用，具備多種指令，提供文字回應與圖片搜尋功能。

---

## 主要功能

### 1. Flask 伺服器
- 啟動 Flask 伺服器，提供 `/` 路由，回應 `"Bot is active!"`
- 讓 Render 取得環境變數 `PORT`，確保伺服器可正常運行

### 2. Discord Bot
- 使用 `discord.py` 建立機器人，支援 `message_content` 和 `members` 權限。
- 透過 `commands.Bot` 設置前綴指令 `!`，同時支援 `app_commands` 斜線指令。
- 設有冷卻機制，避免機器人過度回應相同使用者的訊息。

### 3. 指令列表

#### 文字指令（`!` 前綴）
- `!吃啥`：隨機回應建議的食物。
- `!今日`：提供隨機的一句話（以隱藏文字方式顯示）。
- `!Labrat`：回應 `Labrat` 相關內容。
- `!研究生`：提供研究生的勵志語錄。

#### 斜線指令（`/` 指令）
- `/雞腿語錄`：根據使用者輸入的語錄名稱搜尋對應內容，支援 `隨機` 選項。
- `/圖`：根據使用者輸入的圖片名稱搜尋對應圖片，支援 `隨機` 選項。
- `/吃啥`：與 `!吃啥` 相同，隨機提供建議的食物。
- `/研究生`：與 `!研究生` 相同，提供勵志語錄。
- `/水豚`：回應隨機水豚療育內容。

### 4. 自動補全功能
- `雞腿語錄` 和 `圖` 指令提供輸入補全，會根據使用者輸入的部分文字顯示匹配的結果。

### 5. 同時運行 Flask 與 Discord Bot
- 透過 `threading.Thread` 讓 Flask 伺服器在背景運行，同時啟動 Discord Bot。

---

## 環境變數
- `DISCORD_TOKEN`：Discord Bot 的 Token，用於啟動機器人。
- `PORT`：Flask 伺服器運行的 Port，適用於 Render 部署。

---

## 執行方式
1. 安裝相依套件：
   ```bash
   pip install flask discord.py
   ```
2. 設定環境變數（Linux/Mac）：
   ```bash
   export DISCORD_TOKEN="your_token_here"
   export PORT=5000
   ```
3. 執行程式：
   ```bash
   python bot.py
   ```

---

## 版本需求
- Python 3.8+
- `discord.py` 2.0+
- `Flask` 最新版本

---

## 作者
此機器人由 **pvc** 開發，歡迎提供建議與回饋！

