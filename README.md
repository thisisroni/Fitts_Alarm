# Fitts Alarm：防賴床鬧鐘點擊實驗

Fitts Alarm 是一個結合「防賴床鬧鐘」情境與 Fitts’ Law 資料收集的互動式網頁實驗。使用者不能在固定位置一鍵關閉鬧鐘，而必須依序點擊 36 個位置與尺寸隨機變化的圓形目標，藉此打破肌肉記憶並記錄移動時間（Movement Time, MT）。

整個專案只有一個 `index.html`，不需要框架、套件或 build step，可直接在瀏覽器執行或部署至 GitHub Pages。

## 快速開始

1. 直接用桌機瀏覽器開啟 `index.html`。
2. 視需要填寫 Session 標籤，例如 `sleepy_01` 或 `awake_01`。
3. 閱讀頁面上方的操作說明，點擊「起床／開始解除鬧鐘」。
4. 依序點擊畫面中的 36 個圓形目標。
5. 完成後點擊「下載 CSV 實驗資料」。
6. 如需進行下一輪，點擊「再測一次」、調整標籤後重新開始。

建議使用桌機與滑鼠，並在不同實驗條件間保持相同的瀏覽器縮放比例、視窗大小、輸入裝置與坐姿。

## Session 標籤怎麼用？

Session 標籤是選填的實驗條件識別文字，不會影響 trial 內容或計時。建議使用一致的命名規則：

| 標籤範例 | 意義 |
|---|---|
| `sleepy_01` | 剛睡醒狀態，第 1 次測量 |
| `awake_01` | 清醒狀態，第 1 次測量 |
| `p03_sleepy` | 受試者 3，剛睡醒狀態 |

標籤會寫入 CSV 的 `session` 欄位，也會加入下載檔名，例如 `fitts_alarm_results_sleepy_01.csv`。開始實驗後標籤會暫時鎖定；選擇「再測一次」後會重新開放編輯並保留原文字。

## 實驗設計

| 因子 | 水準 |
|---|---|
| Target Distance A | 150、300、450 px |
| Target Width W（圓形直徑） | 40、70、100 px |
| 每組重複次數 | 4 |
| Trial 總數 | 3 × 3 × 4 = 36 |

- 九種 `(A, W)` 組合各出現四次，開始時使用 Fisher–Yates shuffle 隨機排列。
- 第一個目標從開始按鈕的實際點擊位置計算；之後從上一個成功命中的實際位置計算。
- 目標中心與起點的距離會精確等於該 trial 的 A，且整個圓都會保留在 900×700 canvas 內。
- 點擊圓外會增加該 trial 的 `misses`，不會前進到下一個目標，也不會重設計時。

## 計時方式

App 使用 `performance.now()` 計時：

- 第一筆 MT：從點擊開始按鈕到成功命中第一個目標。
- 後續 MT：從成功命中上一個目標到成功命中目前目標。
- 若發生 miss，MT 會包含重新嘗試所花費的時間。
- MT 單位為毫秒，記錄至小數點後一位。

## CSV 資料

CSV 每一列代表一個 trial：

```csv
trial,A,W,MT,misses,session
1,300,70,612.4,0,sleepy_01
2,150,40,845.1,1,sleepy_01
```

| 欄位 | 說明 |
|---|---|
| `trial` | Trial 編號，從 1 開始 |
| `A` | 目標距離（px） |
| `W` | 目標直徑（px） |
| `MT` | Movement Time（ms） |
| `misses` | 成功命中前的錯誤點擊次數 |
| `session` | 使用者輸入的 Session 標籤 |

資料在實驗期間只保存在目前分頁的記憶體中。完成後請先下載 CSV；若尚未下載就選擇重測，App 會顯示警告。重新整理或關閉分頁也會清除尚未下載的結果。

## GitHub Pages 部署

1. 將 `index.html` 與本 README 放在 GitHub repository 根目錄。
2. 在 repository 開啟 **Settings → Pages**。
3. 將 Source 設為 **Deploy from a branch**。
4. 選擇要部署的 branch（通常是 `main`）及 `/ (root)`。
5. 儲存後等待 GitHub 提供網站網址。

本專案不需要後端；CSV 由瀏覽器使用 `Blob` 與暫時下載連結在本機產生。

## 調整實驗參數

可在 `index.html` 的 JavaScript 區段修改以下常數：

```js
const DISTANCES = [150, 300, 450];
const WIDTHS = [40, 70, 100];
const REPETITIONS = 4;
```

若增加最大距離或目標尺寸，必須同步確認 900×700 canvas 是否仍能在所有起點放置完整目標，否則會影響指定 A 的正確性。

## 專案結構

```text
Fitts_Alarm/
├── index.html   # 完整 App：版面、canvas、實驗邏輯與 CSV 匯出
└── README.md    # 使用、資料與部署說明
```
