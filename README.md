# HRC_powder_data_proc
processing INS data of powder samples measured at HRC

## How to use
HANAを使って２つのcvsファイルを出力します。

1. Vanadium補正をかけたもの：HRCXXXXXwqp_128_383_0_1023_c.csv
2. 補正なしで生の中性子カウントをbinningしたもの：HRCXXXXXwqp_128_383_0_1023_r.csv

バックグラウンド測定も行なった場合は、同様のcsvファイルを補正あり、無しともに用意しておきます。

initファイルに以下のように書きます。

```
HRC024695wqp_128_383_0_1023_c.csv     # measurement with sample
HRC024695wqp_128_383_0_1023_r.csv     # measurement with sample (raw)
1      # Proton number for measurement
nan    # background measurement
nan    # background measurement (raw)
1     # Proton number for background
./intensity_map_Ei10meV.txt   # output filename for intensity map.
1.9   # lower limit of E for const-E cut (meV)
3.1   # Upper limit of E for const-E cut (meV)
./constE_cut_Ei10meV.txt    # output filename for const-E cut.
1.20   # lower limit of Q for const-Q cut (A^-1)
1.5   # Upper limit of Q for const-Q cut (A^-1)
./constQ_cut_Ei10meV.txt    # output filename for const-E cut.
```
バックグラウンドファイルが無い時には適当に「0」とか「nan」とか書いておきます。


Python3, numpyが入っている環境で以下のように実行します。
```
python HRC_powder_data_proc.py [init file]
```
