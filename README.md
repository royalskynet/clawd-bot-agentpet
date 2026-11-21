# Clawd Bot — AgentPet pet

![Clawd Bot](preview.gif)

Clawd Bot 是一支短影音頻道的智能機械蟹吉祥物：陶土橘機甲、LED 面罩、星芒天線。這個 repo 把它做成 [AgentPet](https://github.com/ntd4996/agentpet) 桌面寵物，格式跟 Codex pet 一樣（`pet.json`，加一張 8×9 格、每格 192×208 的透明 `spritesheet.webp`）。

## 安裝

```bash
git clone https://github.com/royalskynet/clawd-bot-agentpet ~/.agentpet/pets/clawd-bot
```

重開 AgentPet，在寵物清單選 **Clawd Bot**。也可以在 AgentPet 裡用 Choose Spritesheet 直接匯入 `spritesheet.webp`。

## 動作

| 列 | 狀態 | 格數 | 動作 |
|---|---|---|---|
| 1 | idle | 6 | 待機浮動 |
| 2 | running-right | 8 | 往右跑 |
| 3 | running-left | 8 | 往左跑 |
| 4 | waving | 4 | 笑眼揮螯 |
| 5 | jumping | 5 | 蹲下彈跳 |
| 6 | failed | 8 | 紅色一字眼，垮下來趴著 |
| 7 | waiting | 6 | 抬頭等，頭上冒「?」 |
| 8 | running | 6 | 工作中，雙螯敲鍵盤 |
| 9 | review | 6 | 托腮，眼睛左右掃 |

每一格都由角色的向量原檔加決定性姿態函式渲染，不是 AI 生圖。

## 檢查寵物素材

修改素材後，可以在專案目錄用 Python 和 Pillow 檢查設定檔、圖片格式和每列格數：

```bash
python3 -m pip install Pillow
python3 scripts/validate_pack.py
python3 -m unittest discover -s tests
```

固定格線檢查會確認圖片仍是 8×9 格且每列動作格數正確。要另外檢查 [AgentPet v1.17.5](https://github.com/ntd4996/agentpet/releases/tag/v1.17.5) 的透明切圖方式，請執行：

```bash
python3 scripts/validate_pack.py --agentpet
```

目前這項相容性檢查預期會回報不符：原圖有 9 列動作，但 AgentPet v1.17.5 的切法會把動作內的透明空隙也當成分隔線，切成 14 列。若在該版本看到動作偏移或角色分成數塊，並不代表安裝步驟做錯。此處未改動原圖。
