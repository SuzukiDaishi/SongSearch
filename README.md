# SongSearch

## 動かし方
まず任意のディレクトリにクローンします

```
git clone https://github.com/SuzukiDaishi/SongSearch.git
```

まず，`data`ディレクトリの下にm4aファイルを置きます(他の拡張子の場合`build.py`に変更が必要)

```
例:
SongSearch/data
├── README.md
├── THE IDOLM@STER STARLIT SEASON 01
│   ├── 01 THE IDOLM@STER.m4a
│   ├── 02 お願い!シンデレラ.m4a
│   ├── 03 Thank You!.m4a
│   ├── 04 Spread the Wings!!.m4a
│   ├── 05 SESSION!.m4a
│   ├── 06 EVER RISING.m4a
│   ├── 07 SESSION! (Off Vocal).m4a
│   └── 08 EVER RISING (Off Vocal).m4a
├── THE IDOLM@STER STARLIT SEASON 02
│   ├── 01 READY!! (M@STER VERSION).m4a
│   ├── 02 Star!!.m4a
│   ├── 03 Brand New Theater!.m4a
│   ├── 04 Multicolored Sky.m4a
│   ├── 05 夏のBang!!.m4a
│   ├── 06 1st Call.m4a
│   ├── 07 夏のBang!! (オリジナル・カラオケ).m4a
│   └── 08 1st Call (オリジナル・カラオケ).m4a
├── THE IDOLM@STER STARLIT SEASON 03
│   ├── 01 M@STERPIECE.m4a
│   ├── 02 M@GIC☆.m4a
│   ├── 03 UNION!!.m4a
│   ├── 04 Ambitious Eve.m4a
│   ├── 05 アイシテの呪縛～Je vous aime～.m4a
│   ├── 06 全力★ドリーミングガールズ.m4a
│   ├── 07 アイシテの呪縛～Je vous aime～ (Off Vocal).m4a
│   ├── 08 全力★ドリーミングガールズ (Off Vocal).m4a
│   ├── 09 READY!!.m4a
│   └── 10 Spread the Wings!!.m4a
└── THE IDOLM@STER STARLIT SEASON 04
    ├── 01 MUSIC♪ (M@STER VERSION).m4a
    ├── 02 オーバーマスター (M@STER VERSION).m4a
    ├── 03 IDOL☆HEART.m4a
    ├── 04 KAWAII ウォーズ.m4a
    ├── 05 ダンス・ダンス・ダンス.m4a
    ├── 06 GR@TITUDE.m4a
    ├── 07 GR@TITUDE.m4a
    ├── 08 なんどでも笑おう.m4a
    ├── 09 KAWAII ウォーズ (オリジナル・カラオケ).m4a
    ├── 10 ダンス・ダンス・ダンス (オリジナル・カラオケ).m4a
    ├── 12 READY!! (M@STER VERSION).m4a
    └── 13 お願い! シンデレラ (M@STER VERSION).m4a
```

次に，音声データの解析を行います(その際にdockerが必要)
```
cd SongSearch
docker build ./ -t song_search_build
sudo docker run -it -v $(pwd):/workspace song_search_build:latest python build.py
```

次にサーバーを起動します
```
cd SongSearch
python -m http.server 8000
```

これで http://localhost:8000 にアクセスすることで，検索を行うことができます．

## 実装の説明

### 1. 楽曲のヒストグラムの作成

まず楽曲をPop2Pianoを用いて，Midiデータとして要約します  
![](web/img1.drawio.png)  
MIDIを時間でスライスし，ヒストグラムを作成する

### 2. モードを考慮した楽曲間の距離を測定

ヒストグラムを二つを引数にとる以下の関数で距離を算出できる

```js
modeSlideDistance(hist1, hist2) {
    let h1 = hist1.map(v=>v/Math.max(...hist1))
    let h2 = hist2.map(v=>v/Math.max(...hist2))
    let r = Infinity
    for (let x=0; x<12; x++) {
        h1 = [
            h1[(x+0)%12], h1[(x+1)%12], h1[(x+2)%12], h1[(x+3)%12], 
            h1[(x+4)%12], h1[(x+5)%12], h1[(x+6)%12], h1[(x+7)%12],
            h1[(x+8)%12], h1[(x+9)%12], h1[(x+10)%12], h1[(x+11)%12]
        ]
        let s = 0
        for (let i=0; i<12; i++) s += Math.pow(h1[i] - h2[i], 2)
        r = Math.min(s, r)
    }
    return r
}
```