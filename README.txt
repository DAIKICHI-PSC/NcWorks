NcWorks
NC PROGRAM EDITOR, 2D SIMULATOR AND 2D CADCAM FOR SWISS-TYPE LATHE



[概要]
本プログラムは、自動盤（スイス型旋盤）のエディター、二次元シミュレーター、二次元CADCAMを提供します。
視覚的にプログラムの作成、確認が出来るので、大幅な時間短縮（コスト削減）に貢献すると思います。
一般的に購入できるCADCAMは高額で、NCコードからのシミュレーションが出来ないので、本プログラムを作成しました。
XZ平面のみに対応します。
NCプログラムの標準化に活用して下さい。



[二次元シミュレーター]
視覚的にNCプログラムを確認出来るので、新人教育、作業者のポカヨケに最適です。
作業の流れは、下記となります。
１．プログラム作成
２．無ければ切削工具の作成（[sample_tools]にあるDXFファイルを参考にして下さい）
３．二次元シミュレーターで切削工具の登録（各プログラムに対して初回のみ）
４．二次元シミュレーターで材料径を指定（各プログラムに対して初回のみ）
５．必要に応じて[表示]や[実行スピード]を設定し、[開始]ボタンを押してシミュレーターを開始後、[次へ]ボタンを押してシミュレーターを実行します（[シングルブロック]チェックをはずすと、全自動で実行されます）
６．シミュレーション終了後は、簡易的に寸法測定が出来ます。
エディターで[sample]フォルダにあるプログラムを読み込んで、テストして下さい（上記は設定済み）。
ドリル等の内径加工工具は、X0を指定して下さい。
一般的な直線補間、R補間は実装しております。
G50も実装しております。
刃先R補正は未実装です。



[二次元CADCAM]
視覚的にNCプログラムを作成出来るので、新人教育、作業者のポカヨケに最適です。
工具軌跡をCAD上で描画したDXFファイルを、NCプログラムに変換します。
各工具の軌跡を、[レイヤー]毎に描画して下さい（レイヤー番号が必要となります）。
開始点に[CIRCLE]を描画して下さい（径は問いません）。
同一座標上の移動は変換出来ません（基本的に一筆書きで描画して下さい）。
通常は、[線分データは、一筆書きで描かれていますか？]の問いに対して、[No]を選択して下さい。
[頭脳CAD RAPID 2D]で確認済みです（未確認ですが、フリーソフトのJW_CADも使用可能だと思います）。



[各ファイルの説明]
sampleフォルダ        NCプログラム[sample_NC_program.m]と、設定ファイルが入っています
sample_camフォルダ    CADCAM用のサンプルCADデータ、[sample_CAM_file.dxf]が入ってます
sample_toolsフォルダ  二次元シミュレーター用の工具データ(DXF)が入ってます
GUI_DXFtoNC.py        二次元CADCAM用のGUIプログラム(Pythonプログラム)
GUI_DXFtoNC.ui        GUI作成用ファイル（QT Designer用）
GUI_EDITOR.py         エディター用のGUIプログラム(Pythonプログラム)
GUI_EDITOR.ui         GUI作成用ファイル（QT Designer用）
GUI_SIM.py            二次元シミュレーター用のGUIプログラム(Pythonプログラム)
GUI_SIM.ui            GUI作成用ファイル（QT Designer用）
NcWorks.py            メインプログラム
PLANET.ico            アイコンファイル
README.txt            本ファイル
SETTINGS_DXFtoNC.ini  CADCAM用の設定ファイル（本来は自動で生成されます）
SETTINGS_EDITOR.ini   エディター用の設定ファイル（本来は自動で生成されます）
SETTINGS_SIM.ini      二次元シミュレーター用の設定ファイル（本来は自動で生成されます）
Sub_MathPlus.py       演算用のモジュール
Sub_NcTools.py        演算用のモジュール



［LICENSE ライセンス］
This program(本プログラム)
MIT LISENCE
Distribution, modification, commercial use, etc. are all permitted.(配布、改変、商用利用等、全て自由です。)

Python
Python Software Foundation License
Distribution, modification, commercial use, etc. of the resulting work are all permitted.(成果物の配布、改変、商用利用等、全て自由です。)

PySide6
LGPLv3
Distribution and commercial use are permitted.(配布、商用利用が可能です。)

ezdxf
MIT LISENCE
Distribution, modification, commercial use, etc. are all permitted(配布、改変、商用利用等、全て自由です。)

pyinstaller
https://github.com/pyinstaller/pyinstaller/wiki/FAQ
Distribution, modification, commercial use, etc. of the resulting work are all permitted.(成果物の配布、改変、商用利用等、全て自由です。)



［appreciation 感謝］
Developer of Python(programming language)
Python Software Foundation and the community
https://www.python.org/

Developer of GUI module
The Qt Company
https://www.qt.io/ja-jp/

Developer of dxf handling module for Python
Manfred Moitzi and the community
https://github.com/mozman

Developer of software that converts Python programs to executable file
pyinstaller and the community
https://github.com/pyinstaller
