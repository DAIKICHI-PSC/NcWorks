import sys
#from tkinter import Scale #インタプリタや実行環境に関連した変数や関数がまとめられたライブラリの読込。
from PySide6 import QtCore, QtGui, QtWidgets #GUI処理ライブラリの読込。
import os
import collections
import operator
from Sub_MathPlus import RND

YEAR = "2025"
VERSION = "5.0.0[2025/10/29]"
#5.0.0[2025/10/29] PySide6のバージョンの問題で、シミュレーションの背景が灰色になる問題を修正（QtCore.Qt.white）
#4.0.3[2024/06/19] 工具フォルダーの選択で、キャンセル後のソフト再起動で、ファイルの読み込みエラーが発生するバグを修正
#4.0.2[2024/06/12] NC_MOVEMENT()で、M99 P_の実行していない行にあるUとWが加算されてしまうバグを修正
#4.0.1[2023/09/08] シミュレーターで拡大し過ぎると、オーバーフローのエラーが発生するバグを修正
#4.0.0[2023/09/08] シミュレーターで拡大縮小を行う際、マウスの位置からずれる問題を対策（マウスホイールでスクロールしている根本の問題は未解決）
#3.3.5[2023/09/08] ダミーの描画から、self.ui.graphicsView1.setSceneRectに変更
#3.3.4[2023/08/30] PySide6の仕様変更に対応　graphicsView1.AnchorUnderMouse→graphicsView1.ViewportAnchor.AnchorUnderMouse
#3.3.3[2023/06/15] シミュレーション実行時、「前へ」ボタンを押した後に表示が異常になるバグを修正（3.3.2と同じく大文字と小文字の問題）
#3.3.2[2023/04/07] シミュレーション実行時、画面の拡大縮小でプログラムテキストの拡大が有効にならないバグを修正（num_tool→NUM_TOOL num_line→NUM_LINE）
#3.3.1[2023/04/06] シフト　ジオメトリオ＋オフセットから、シフト＋オフセット　ジオメトリオへ組み合わせを変更
#3.3.0[2023/04/05] シミュレーションで、ジオメトリオ値とオフセット値が適用されるように改良
#3.2.4[2023/04/04] 工具形状選択時、数値入力処理に多くのバグがあったのを修整
#3.2.3[2023/04/04] エディタのサブ側でシミュレーションした場合の処理が無かったため修整
#3.2.2[2023/03/27] プログラムのフォルダを記憶可能に変更
#3.2.1[2023/03/27] 工具データのフォルダを記憶可能に変更　工具データ選択時にダイアログを表示する様に変更
#3.2.0[2023/03/24] 工具刃先Rの角度が90°未満の場合、正しく描画出来ないバグを修整
#3.1.0[2022/05/19] G2、G3でRの指定がない場合、送りのF値が0場合にエラーが発生するバグを修正
#3.0.9[2022/05/18] 四捨五入の計算を、RND関数で統一
#3.0.8[2022/05/17] マウスカーソルが移動中も、寸法測定用マーカーの脇に座標を表示
#3.0.7[2022/05/16] 寸法測定用マーカーの脇に座標を表示
#3.0.6[2022/05/16] 寸法測定の表示を変更
#3.0.5[2022/05/16] 寸法測定で、X軸の表示も計算もプラスとマイナスが反転する様に統一
#3.0.4[2022/05/15] 点群ではなく、端面と外径を検出する際の検出値を修正
#3.0.3[2022/05/15] 四捨五入の際、元値のプラスとマイナスで、0.005を足したり引いたりする様に変更
#3.0.2[2022/05/14] 寸法測定で、端面と外径を検出する機能を追加
#3.0.1[2022/05/13] NCで言うX軸の値をプラスとマイナス反転後、MIN XとMAX Xの値が逆になるバグを修正
#3.0.0[2022/05/13] 寸法測定機能を追加
#2.0.5[2022/04/28] プログラム軌跡とテキストを非表示可能に変更
#2.0.4[2022/04/28] フォントサイズを変更
#2.0.3[2022/04/27] シミュレーションのスクロールバーをオフに設定
#2.0.2[2022/04/27] シミュレーションの画像を保存する機能を追加
#2.0.1[2022/04/27] 読み込んだプログラムに対して、指定した材料径を保存
#2.0.0[2022/04/07] Nukitaに対応(PySide6へ変更、設定ファイルをホームディレクトリへ保存)
#1.9.0[2021/09/05] サブウィンドウがアクティブの間は、メインウィンドウを非アクティブにし終了出来ない様に変更
#1.8.5[2021/09/02] G50のZの動作が逆だったので修正
#1.8.4[2021/07/31] NCプログラムでG98からG99へ戻し忘れた時に、送り値が小さくなりすぎてフリーズを起こす為、送り値が0.001より小さい場合、送り値を0.001にする様に仕様を変更(Sub_NcTools.py CONVERT_G98_TO_G99)
#1.8.3[2021/07/29] DXFからプログラム変換で、一筆書きを選んだ場合に、円弧が正しく変換出来ない問題を修正("ARC"は反時計回りで始点と終点が決まるので)
#1.8.2[2021/07/29] 製品形状DXFファイルで、レイヤ名が0でなくてもデータを読込める様に変更
#1.8.1[2021/07/28] G92の挙動を変更（多条ネジは正確に描画出来ない）
#1.8.0[2021/07/24] DXFからプログラムへ変換する際、一筆書きで描かれたデータとした場合は、座標の重なりで処理を終了しないように処理を変更
#1.7.4[2021/07/22] 工具軌跡のレイヤ番号の始まりを0から1へ変更(CREATE_DXF_PATH PROGRAM_TO_DXF)
#1.7.3[2021/07/21] R_CENTER_DEGREE_2をR_CENTER_DEGREEへ統合(三角関数の精度を向上　出力の小数点丸めを廃止)
#1.7.2[2021/07/21] プログラムをDXFファイルへ変換する際、円弧の大きさが計算誤差で変わってしまう問題を、専用の関数を使用する事で修正(Sub_NcTools.py PROGRAM_TO_DXF RND_2 R_CENTER_DEGREE_2)
#1.7.1[2021/07/21] 工具軌跡をDXF出力する時の材料の色を白から黒へ変更
#1.7.0[2021/07/20] プログラムをDXFファイルへ変換する際、直線座標と円弧座標が正確に接続出来る様に修正(Sub_NcTools.py PROGRAM_TO_DXF)
#1.6.1[2021/07/20] Sub_NcTools.pyのPROGRAM_TO_DXF関数内のNC_PROGRAM = NC_SPLITTER(PROGRAM_TEXT)をret, NC_PROGRAM = NC_SPLITTER(PROGRAM_TEXT)へ変更（バグ修正）
#1.6.0[2021/07/13] DXF工具データのレイヤ名が0でなくても読込める様に変更
#1.5.0[2021/07/12] DXFからのプログラム変換で、線分が一本以上あり、かつスタートポイントを一つだけ含むレイヤのみ処理する様に変更
#1.4.1[2021/06/07] M99 P_のジャンプ先が無かった場合の挙動を変更（Sub_NcTools.py NC_MOVEMENT）
#1.4.0[2021/06/04] M99 P_のジャンプ命令に対応（Sub_NcTools.py NC_MOVEMENT）


##############################メインウィンドウ用の設定##############################
from GUI_EDITOR import Ui_MainWindow1 #QT Designerで作成し（GUI_EDITOR.ui）、PysideUicFrontEndでパイソンコードに変換したファイル（GUI_EDITOR.py）の読込
from Sub_NcTools import NC_SPLITTER, PROGRAM_TO_DXF
FLAG_TEXT1_CHANGED = 0
FLAG_TEXT2_CHANGED = 0
TEXT1_FILENAME = ""
TEXT2_FILENAME = ""
TEXT1_EX_LINE_NUM = 1
TEXT2_EX_LINE_NUM = 1
HOME_PATH = os.path.join(os.path.expanduser("~"), "NcWorks_SETTINGS") #設定ファイルを保存するフォルダへのパス（ホームディレクトリ）
if not os.path.isdir(HOME_PATH):
    os.makedirs(HOME_PATH, exist_ok=True)
SETTING_PATH_EDITOR = os.path.join(HOME_PATH, "SETTINGS_EDITOR.ini") #設定ファイルパス
MAIN_PRG_DIR = ""
SUB_PRG_DIR = ""
MAIN_SUB_FLAG = 0


##############################DXFファイルをプログラムへ変換するウィンドウ用の設定##############################
from GUI_DXFtoNC import Ui_MainWindow2 #QT Designerで作成し（GUI_DXFtoNC.ui）、PysideUicFrontEndでパイソンコードに変換したファイル（GUI_DXFtoNC.py）の読込
import ezdxf
from Sub_MathPlus import RND, ROTATION_DIRECTION_DETECTOR, INTERSECTION_DETECTOR
SETTING_PATH_DXFtoNC = os.path.join(HOME_PATH, "SETTINGS_DXFtoNC.ini") #設定ファイルパス


##############################シミュレーションを実行するウィンドウ用の設定##############################
from GUI_SIM import Ui_MainWindow3 #QT Designerで作成し変換したファイルの読込
from Sub_NcTools import NC_PROGRAM_TEXT, NC_MOVEMENT, NC_PATH, NC_REALTIME_MOVEMENT, CONVERT_CLOSED_DXF, NC_SIMPLE_PATH
EX_X = 0 #マウスの最後のX位置
EX_Y = 0 #マウスの最後のY位置
BUTTON_FLAG = 0 #マウスボタンが押されているか判定用フラグ
SCALE = 0.5 #graphicsViewの表示倍率
SELECTED_ITEM = None #マウスで選択されているアイテム
ITEMS = [] #graphicsViewのscene上にあるアイテム保持用配列
TOOL_PATH = [] #テスト用データ保存用配列

SELECTED_TOOL = None #選択されている工具
SELECTED_LINE = None #選択されている工具軌跡
PROGRAM_LINE_POS = None #リスト化されたプログラムの、配列位置と工具軌跡配列番号の対応表
TOOL_CHANGE_POS = None #リスト化されたプログラムの、工具交換を行う配列位置
MOVEMENT_DATA = None #配列化されたNCプログラムの移動データ
TOOLS = None #パス化された移動データ
TOOLS_LINE_NUM = None #各パスとプログラムとの対応表
TOOLS_TEXT = None #各工具のプログラムテキスト
TOOLS_POS = None #工具の位置データ
#TOOL_REGION = None
GUIDE_BUSH_U = None #ガイドブッシュの図形データ上
GUIDE_BUSH_L = None #ガイドブッシュの図形データ下
CENTER_LINE = None #センターラインの図形データ

#RUN_MODE = 0
FLAG_BEFORE = 0 #プログラムを一行戻すフラグ
FLAG_NEXT = 0 #プログラムを一行進めるフラグ
VIEW_SCALE = 50 #表示のスケール値
FLAG_SIMULATION_STARTED = 0 #シミュレーション開始の判定フラグ
SUB_WIN_ACTIVE = 0 #サブのウィンドウが表示中か判定するフラグ
NC_PROGRAM = "" #配列化したプログラム
RUN_SPEED = -1 #シミュレーションの実行スピード
FONT_SIZE = 1 #プログラムを表示する際のフォントサイズ
TOOLS_TEXT_SCALE = 1 #プログラムのスケール
MOUSE_R_CLICK_FIRST = ""
MOUSE_R_CLICK_SECOND = ""
MOUSE_R_CLICK_FLAG = 0
EX_MOUSE_R_CLICK_FIRST = ""
EX_MOUSE_R_CLICK_SECOND = ""
EX_MAX_X = 0
EX_MIN_X = 0
EX_MAX_Y = 0
EX_MAX_Y = 0
EX_PATH = ""
EX_MOUSE_R_CLICK_FIRST_X = 0
EX_MOUSE_R_CLICK_FIRST_Y = 0
EX_MAX_Z = 0
EX_MIN_Z = 0
EX_MAX_X = 0
EX_MIN_X = 0
FLAG_END = 0

Z1MIN_TEXT = ""
Z1MAX_TEXT = ""
X1MIN_TEXT = ""
X1MAX_TEXT = ""
Z2MIN_TEXT = ""
Z2MAX_TEXT = ""
X2MIN_TEXT = ""
X2MAX_TEXT = ""

MATERIAL_DIAMETER = -5 #10 / -2 材料径
MATERIAL = "" #材料の図形データ
MATERIAL_PATH = "" #材料径データのファイルパス

TOOL_DXF_PATH = {} #各工具図形データのファイルパス
TOOL_DXF_SHIFT = {} #各工具図形データのシフト量
TOOL_DXF_GEOMETRIO = {} #各工具図形データのジオメトリオ値
TOOL_DXF_OFFSET = {} #各工具図形データのオフセット値
TOOL_DXF_NOSE_R = {} #各工具図形データのノーズRパラメータ
TOOL_PAINTER_PATH = {} #各工具の図形データ
TOOL_PAINTER_PATH_REV = {} #各工具の反転した図形データ
TOOL_NAME= "" #各工具名
TOOL_TEXT_PARENTS = [] #プログラムの図形データ
SETTING_PATH_SIM = os.path.join(HOME_PATH, "SETTINGS_SIM.ini") #設定ファイルパス
SETTING_PATH_DIR = os.path.join(HOME_PATH, "SETTINGS_DIR.ini") #設定ファイルパス
TOOL_DATA_DIR_PATH = "" #ツールのフォルダ記憶用変数
MUM_TOOL = 0
NUM_LINE = 0




















'''
# 複数の座標のうちx, yに一番近い座標を求める
def nearPoint(x, y, points):
	result = {}
	if len(points) == 0:
		return result
	result["x"] = points[0]["x"]
	result["y"] = points[0]["y"]
	stdval = math.sqrt((points[0]["x"] - x) ** 2 + (points[0]["y"] - y) ** 2)
	for point in points:
		distance = math.sqrt((point["x"] - x) ** 2 + (point["y"] - y) ** 2)
		if stdval > distance:
			result["x"] = point["x"]
			result["y"] = point["y"]
			stdval = distance
	return result
'''




















#=====カスタムDialog　切削工具のシフト量入力用カスタムダイアログ========================================
class InputDialog(QtWidgets.QDialog):
    sx = ""
    sz = ""
    gx = ""
    gz = ""
    ox = ""
    oz = ""
    tool_edge_num = ""
    tool_edge_r = ""
    def __init__(self, parent=None, sx = "0", sz = "0", gx ="0", gz = "0", ox = "0", oz = "0", tool_edge_num = "0", tool_edge_r = "0"):
        super().__init__(parent)
        self.SX = QtWidgets.QLineEdit(self)
        self.SX.setText(sx)
        self.SZ = QtWidgets.QLineEdit(self)
        self.SZ.setText(sz)
        self.GX = QtWidgets.QLineEdit(self)
        self.GX.setText(gx)
        self.GZ = QtWidgets.QLineEdit(self)
        self.GZ.setText(gz)
        self.OX = QtWidgets.QLineEdit(self)
        self.OX.setText(ox)
        self.OZ = QtWidgets.QLineEdit(self)
        self.OZ.setText(oz)
        self.TOOL_EDGE_NUM = QtWidgets.QLineEdit(self)
        self.TOOL_EDGE_NUM.setText(tool_edge_num)
        self.TOOL_EDGE_R  = QtWidgets.QLineEdit(self)
        self.TOOL_EDGE_R.setText(tool_edge_r)
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok, self)# | QtWidgets.QDialogButtonBox.Cancel, self);

        layout = QtWidgets.QFormLayout(self)
        layout.addRow("工具取り付けシフト X（実寸）", self.SX)
        layout.addRow("工具取り付けシフト Z", self.SZ)
        layout.addRow("ジオメトリオ X（直径値）", self.GX)
        layout.addRow("ジオメトリオ Z", self.GZ)
        layout.addRow("オフセット X（直径値）", self.OX)
        layout.addRow("オフセット Z", self.OZ)
        layout.addRow("ノーズR補正刃先番号", self.TOOL_EDGE_NUM)
        layout.addRow("ノーズR補正R", self.TOOL_EDGE_R)
        layout.addWidget(buttonBox)
        self.setWindowTitle("工具パラメータ")
        self.setWindowFlags(QtCore.Qt.WindowTitleHint | QtCore.Qt.CustomizeWindowHint)
        buttonBox.accepted.connect(self.accept)
        #buttonBox.rejected.connect(self.reject)
        
    def getInputs(self):
        return (self.SX.text(), self.SZ.text(), self.GX.text(), self.GZ.text(), self.OX.text(), self.OZ.text(), self.TOOL_EDGE_NUM.text(), self.TOOL_EDGE_R.text())




















#=====メインウィンドウのイベント処理========================================
class MainWindow3(QtWidgets.QMainWindow): #QtWidgets.QMainWindowを継承。
    #-----初期化----------------------------------------
    def __init__(self, parent = None): #クラス初期化時にのみ実行される関数（コンストラクタと呼ばれる）。
        super().__init__(parent)  #親クラスのコンストラクタを呼び出す（親クラスのコンストラクタを再利用したい場合）。指定する引数は、親クラスのコンストラクタの引数からselfを除いた引数。
        self.ui = Ui_MainWindow3() #uiクラスの作成。Ui_MainWindowのMainWindowは、QT DesignerのobjectNameで設定した名前。
        self.ui.setupUi(self) #uiクラスの設定。
        #シグナルにメッソドを関連付け
        self.ui.listWidget2.doubleClicked.connect(self.listWidget2_doubleClicked)
        self.ui.listWidget2.clicked.connect(self.listWidget2_clicked)
        self.ui.action1_1.triggered.connect(self.action1_1_triggered)
        self.ui.action1_2.triggered.connect(self.action1_2_triggered)
        self.ui.action1_3.triggered.connect(self.action1_3_triggered)
        self.ui.action1_4.triggered.connect(self.action1_4_triggered)
        self.ui.action1_5.triggered.connect(self.action1_5_triggered)
        self.ui.action1_6.triggered.connect(self.action1_6_triggered)
        self.ui.action1_7.triggered.connect(self.action1_7_triggered)
        self.ui.action2_1.triggered.connect(self.action2_1_triggered)
        self.ui.action2_2.triggered.connect(self.action2_2_triggered)
        self.ui.action2_3.triggered.connect(self.action2_3_triggered)
        self.ui.action2_4.triggered.connect(self.action2_4_triggered)
        self.ui.action2_5.triggered.connect(self.action2_5_triggered)
        self.ui.action2_6.triggered.connect(self.action2_6_triggered)
        self.ui.action2_7.triggered.connect(self.action2_7_triggered)
        self.ui.action2_8.triggered.connect(self.action2_8_triggered)
        self.ui.action2_9.triggered.connect(self.action2_9_triggered)
        self.ui.action2_10.triggered.connect(self.action2_10_triggered)
        self.ui.action2_11.triggered.connect(self.action2_11_triggered)
        self.ui.action2_12.triggered.connect(self.action2_12_triggered)
        self.ui.action2_13.triggered.connect(self.action2_13_triggered)
        self.ui.action2_14.triggered.connect(self.action2_14_triggered)
        self.ui.action2_15.triggered.connect(self.action2_15_triggered)
        self.ui.action2_16.triggered.connect(self.action2_16_triggered)
        self.ui.action2_17.triggered.connect(self.action2_17_triggered)
        self.ui.action2_18.triggered.connect(self.action2_18_triggered)
        self.ui.action2_19.triggered.connect(self.action2_19_triggered)
        self.ui.action2_20.triggered.connect(self.action2_20_triggered)
        self.ui.action2_21.triggered.connect(self.action2_21_triggered)
        self.ui.action2_22.triggered.connect(self.action2_22_triggered)
        self.ui.action2_23.triggered.connect(self.action2_23_triggered)
        self.ui.action2_24.triggered.connect(self.action2_24_triggered)
        self.ui.action2_25.triggered.connect(self.action2_25_triggered)
        self.ui.action3_1.triggered.connect(self.action3_1_triggered)
        self.ui.action3_2.triggered.connect(self.action3_2_triggered)
        self.ui.action3_3.triggered.connect(self.action3_3_triggered)
        self.ui.action3_4.triggered.connect(self.action3_4_triggered)
        self.ui.action3_5.triggered.connect(self.action3_5_triggered)
        self.ui.action3_6.triggered.connect(self.action3_6_triggered)
        self.ui.action4_1.triggered.connect(self.action4_1_triggered)
        self.ui.pushButton1.clicked.connect(self.pushButton1_clicked)
        self.ui.pushButton2.clicked.connect(self.pushButton2_clicked)
        self.ui.pushButton3.clicked.connect(self.pushButton3_clicked)
        self.ui.pushButton4.clicked.connect(self.pushButton4_clicked)
        self.ui.pushButton5.clicked.connect(self.pushButton5_clicked)
        if os.path.exists(SETTING_PATH_SIM):
            self.SETTINGS_READ()
        else:
            self.SETTINGS_SAVE()
        if os.path.exists(SETTING_PATH_DIR):
            f = open(SETTING_PATH_DIR, "r")
            x = ""
            x = f.readlines() #テキストを一行ずつ配列として読込む（行の終わりの改行コードも含めて読込む）
            f.close()
            global TOOL_DATA_DIR_PATH
            TOOL_DATA_DIR_PATH = x[0]
        #graphicsviewの背景を白にする
        self.ui.graphicsView1.setBackgroundBrush((QtGui.QBrush(QtCore.Qt.white, QtCore.Qt.SolidPattern)))









    ##################################################インターフェイス　ボタン関連##################################################
    def pushButton1_clicked(self):
        global FLAG_SIMULATION_STARTED
        self.ui.pushButton2.setEnabled(True)
        self.ui.pushButton5.setEnabled(False)
        self.ui.menu_1.setEnabled(False)
        self.ui.listWidget1.setEnabled(False)
        self.ui.listWidget2.setEnabled(False)
        self.ui.action2_1.setEnabled(True)
        self.ui.action2_5.setEnabled(False)
        self.ui.action2_6.setEnabled(False)
        self.ui.action2_9.setEnabled(True)
        self.ui.action2_10.setEnabled(True)
        self.ui.action2_11.setEnabled(True)
        self.ui.action2_12.setEnabled(True)
        self.ui.action2_14.setEnabled(True)
        self.ui.action2_15.setEnabled(True)
        self.ui.action2_16.setEnabled(True)
        self.ui.action2_21.setEnabled(True)
        self.ui.action2_22.setEnabled(True)
        self.ui.action2_23.setEnabled(True)
        #self.ui.action2_9.setChecked(True)
        FLAG_SIMULATION_STARTED = 1
        self.RUN_SIMULATION()


    def pushButton2_clicked(self):
        global FLAG_SIMULATION_STARTED
        self.ui.pushButton2.setEnabled(False)
        self.ui.pushButton3.setEnabled(False)
        self.ui.pushButton4.setEnabled(False)
        self.ui.pushButton5.setEnabled(True)
        self.ui.menu_1.setEnabled(True)
        self.ui.listWidget1.setEnabled(True)
        self.ui.listWidget2.setEnabled(True)
        self.ui.action2_1.setEnabled(False)
        self.ui.action2_5.setEnabled(True)
        self.ui.action2_6.setEnabled(True)
        self.ui.action2_9.setEnabled(False)
        self.ui.action2_10.setEnabled(False)
        self.ui.action2_11.setEnabled(False)
        self.ui.action2_12.setEnabled(False)
        self.ui.action2_14.setEnabled(False)
        self.ui.action2_15.setEnabled(False)
        self.ui.action2_16.setEnabled(False)
        self.ui.action2_21.setEnabled(False)
        self.ui.action2_22.setEnabled(False)
        self.ui.action2_23.setEnabled(False)
        #self.ui.checkBox1.setChecked(False)
        FLAG_SIMULATION_STARTED = 0


    def pushButton3_clicked(self):
        global FLAG_BEFORE
        FLAG_BEFORE = 1


    def pushButton4_clicked(self):
        global FLAG_NEXT
        FLAG_NEXT = 1


    def pushButton5_clicked(self):
        global MATERIAL_DIAMETER
        input_diameter, buttonState = QtWidgets.QInputDialog().getDouble(self, "メッセージ", "材料径を入力して下さい。", MATERIAL_DIAMETER * -2, 1.0, 50.0, 3)
        if buttonState:
            MATERIAL_DIAMETER = input_diameter / -2
            self.SETTINGS_SAVE()
            f = open(MATERIAL_PATH, "w")
            f.write(str(input_diameter) + "\n") #Plaine Text Editの内容を書込む
            f.close()










    ##################################################インターフェイス　リストウィジット関連##################################################
    #-----リストウィジット２のアイテムをクリックした時の処理----------------------------------------
    def listWidget2_clicked(self):
        global TOOL_DXF_PATH
        global TOOL_DXF_SHIFT
        global TOOL_DXF_GEOMETRIO
        global TOOL_DXF_OFFSET
        global TOOL_DXF_NOSE_R
        global TOOL_NAME
        LT = self.ui.listWidget2.currentItem().text()
        if  "[" in LT:
            item = TOOL_NAME[self.ui.listWidget2.currentRow()]
            dialog = InputDialog(None, TOOL_DXF_SHIFT[item][0], TOOL_DXF_SHIFT[item][1], TOOL_DXF_GEOMETRIO[item][0], TOOL_DXF_GEOMETRIO[item][1], TOOL_DXF_OFFSET[item][0], TOOL_DXF_OFFSET[item][1], TOOL_DXF_NOSE_R[item][0], TOOL_DXF_NOSE_R[item][1])
            if dialog.exec():
                shift_xz = dialog.getInputs()
                if len(shift_xz) < 5:
                    shift_x = shift_xz[0]
                    shift_z = shift_xz[1]
                    chk_val = shift_x.replace(".", "")
                    chk_val = chk_val.replace("-", "")
                    if chk_val.isdigit() == False:
                        msgbox = QtWidgets.QMessageBox()
                        msgbox.setWindowTitle("Message")
                        msgbox.setText("工具取り付けシフト Xの値にエラーがあります。\r\n工具取り付けシフト Xの値を0に設定します。")
                        ret = msgbox.exec()
                        shift_x = "0"
                    chk_val = shift_z.replace(".", "")
                    chk_val = chk_val.replace("-", "")
                    if chk_val.isdigit() == False:
                        msgbox = QtWidgets.QMessageBox()
                        msgbox.setWindowTitle("Message")
                        msgbox.setText("工具取り付けシフト Zの値にエラーがあります。\r\n工具取り付けシフト Zの値を0に設定します。")
                        ret = msgbox.exec()
                        shift_z = "0"
                    geometrio_x = "0"
                    geometrio_z = "0"
                    offset_x = "0"
                    offset_z = "0"
                    nose_r_pos = "0"
                    nose_r = "0"
                else:
                    shift_x = shift_xz[0]
                    shift_z = shift_xz[1]
                    geometrio_x = shift_xz[2]
                    geometrio_z = shift_xz[3]
                    offset_x = shift_xz[4]
                    offset_z = shift_xz[5]
                    nose_r_pos = shift_xz[6]
                    nose_r = shift_xz[7]
                    chk_val = shift_x.replace(".", "")
                    chk_val = chk_val.replace("-", "")
                    if chk_val.isdigit() == False:
                        msgbox = QtWidgets.QMessageBox()
                        msgbox.setWindowTitle("Message")
                        msgbox.setText("工具取り付けシフト Xの値にエラーがあります。\r\n工具取り付けシフト Xの値を0に設定します。")
                        ret = msgbox.exec()
                        shift_x = "0"
                    chk_val = shift_z.replace(".", "")
                    chk_val = chk_val.replace("-", "")
                    if chk_val.isdigit() == False:
                        msgbox = QtWidgets.QMessageBox()
                        msgbox.setWindowTitle("Message")
                        msgbox.setText("工具取り付けシフト Zの値にエラーがあります。\r\n工具取り付けシフト Zの値を0に設定します。")
                        ret = msgbox.exec()
                        shift_z = "0"
                    chk_val = geometrio_x.replace(".", "")
                    chk_val = chk_val.replace("-", "")
                    if chk_val.isdigit() == False:
                        msgbox = QtWidgets.QMessageBox()
                        msgbox.setWindowTitle("Message")
                        msgbox.setText("ジオメトリオ Xの値にエラーがあります。\r\nジオメトリオ Xの値を0に設定します。")
                        ret = msgbox.exec()
                        geometrio_x = "0"
                    chk_val = geometrio_z.replace(".", "")
                    chk_val = chk_val.replace("-", "")
                    if chk_val.isdigit() == False:
                        msgbox = QtWidgets.QMessageBox()
                        msgbox.setWindowTitle("Message")
                        msgbox.setText("ジオメトリオ Zの値にエラーがあります。\r\nジオメトリオ Zの値を0に設定します。")
                        ret = msgbox.exec()
                        geometrio_z = "0"
                    chk_val = offset_x.replace(".", "")
                    chk_val = chk_val.replace("-", "")
                    if chk_val.isdigit() == False:
                        msgbox = QtWidgets.QMessageBox()
                        msgbox.setWindowTitle("Message")
                        msgbox.setText("オフセット Xの値にエラーがあります。\r\nオフセット Xの値を0に設定します。")
                        ret = msgbox.exec()
                        offset_x = "0"
                    chk_val = offset_z.replace(".", "")
                    chk_val = chk_val.replace("-", "")
                    if chk_val.isdigit() == False:
                        msgbox = QtWidgets.QMessageBox()
                        msgbox.setWindowTitle("Message")
                        msgbox.setText("オフセット Zの値にエラーがあります。\r\nオフセット Zの値を0に設定します。")
                        ret = msgbox.exec()
                        offset_z = "0"
                    chk_val = nose_r_pos.replace(".", "")
                    chk_val = chk_val.replace("-", "")
                    if chk_val.isdigit() == False:
                        msgbox = QtWidgets.QMessageBox()
                        msgbox.setWindowTitle("Message")
                        msgbox.setText("ノーズR補正刃先番号の値にエラーがあります。\r\nノーズR補正刃先番号の値を0に設定します。")
                        ret = msgbox.exec()
                        nose_r_pos = "0"
                    chk_val = nose_r.replace(".", "")
                    chk_val = chk_val.replace("-", "")
                    if chk_val.isdigit() == False:
                        msgbox = QtWidgets.QMessageBox()
                        msgbox.setWindowTitle("Message")
                        msgbox.setText("ノーズR補正Rの値にエラーがあります。\r\nノーズR補正Rの値を0に設定します。")
                        ret = msgbox.exec()
                        nose_r = "0"
                TOOL_DXF_SHIFT[item] = (shift_x, shift_z)
                TOOL_DXF_GEOMETRIO[item] = (geometrio_x, geometrio_z)
                TOOL_DXF_OFFSET[item] = (offset_x, offset_z)
                TOOL_DXF_NOSE_R[item] = (nose_r_pos, nose_r)

            if MAIN_SUB_FLAG == 0:
                f_name = TEXT1_FILENAME
            else:
                f_name = TEXT2_FILENAME
            if f_name:
                f_name = f_name.split(".")#ネットワークパスで問題が起こるので下記でワークアラウンド
                tool_dxf_path = ""
                list_length = len(f_name)
                i = 0
                while(True):
                    tool_dxf_path += f_name[i] + "."
                    i += 1
                    if i == list_length - 1:
                        break
                tool_dxf_path += "tdd"
                tool_text = ""
                for x in TOOL_DXF_PATH:
                    if TOOL_DXF_PATH[x] != "":
                        shift_xz = TOOL_DXF_SHIFT[x]
                        geometrio_xz = TOOL_DXF_GEOMETRIO[x]
                        offset_xz = TOOL_DXF_OFFSET[x]
                        nose_r_val = TOOL_DXF_NOSE_R[x]
                        tool_text += x + "," + TOOL_DXF_PATH[x] + "," + shift_xz[0] + "," + shift_xz[1] + "," + geometrio_xz[0] + "," + geometrio_xz[1] + "," + offset_xz[0] + "," + offset_xz[1] + "," + nose_r_val[0] + "," + nose_r_val[1] + "\n"
                f = open(tool_dxf_path, "w")
                f.writelines(tool_text) #Plaine Text Editの内容を書込む
                f.close()


    #-----リストウィジット２のアイテムをダブルクリックした時の処理----------------------------------------
    def listWidget2_doubleClicked(self):
        global TOOL_DXF_PATH
        global TOOL_DXF_SHIFT
        global TOOL_DXF_GEOMETRIO
        global TOOL_DXF_OFFSET
        global TOOL_DXF_NOSE_R
        global TOOL_NAME
        ex_pos = self.ui.listWidget2.currentRow()
        item = TOOL_NAME[self.ui.listWidget2.currentRow()]

        CFlag = 0
        LT = self.ui.listWidget2.currentItem().text()
        if  "[" in LT:
            msgbox = QtWidgets.QMessageBox(self)
            msgbox.setWindowTitle("Message")
            msgbox.setIcon(QtWidgets.QMessageBox.Question)
            msgbox.setText("工具を変更しますか？")
            #msgbox.setIconPixmap(QtGui.QPixmap("PLANET.ico"))
            msgbox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            msgbox.setDefaultButton(QtWidgets.QMessageBox.Cancel)
            ret = msgbox.exec()
            if ret == QtWidgets.QMessageBox.Ok:
                CFlag = 0
            else:
                CFlag = 1
        if CFlag == 0:
            QQG = QtWidgets.QFileDialog(self)
            if TOOL_DATA_DIR_PATH != "":
                QQG.setDirectory(TOOL_DATA_DIR_PATH)
            filepath, _ = QQG.getOpenFileName(self, "Open File", "",'dxf File (*.dxf)')
            if filepath:
                _, ret = CONVERT_CLOSED_DXF(filepath, 50, -1) #工具形状をQPainterPathとして取得
                if ret == 0:
                    TOOL_DXF_PATH[item] = filepath #DXFファイルが正常な場合、辞書に登録
                    dialog = InputDialog(None, TOOL_DXF_SHIFT[item][0], TOOL_DXF_SHIFT[item][1], TOOL_DXF_GEOMETRIO[item][0], TOOL_DXF_GEOMETRIO[item][1], TOOL_DXF_OFFSET[item][0], TOOL_DXF_OFFSET[item][1], TOOL_DXF_NOSE_R[item][0], TOOL_DXF_NOSE_R[item][1])
                    if dialog.exec():
                        shift_xz = dialog.getInputs()
                        if len(shift_xz) < 5:
                            shift_x = shift_xz[0]
                            shift_z = shift_xz[1]
                            chk_val = shift_x.replace(".", "")
                            chk_val = chk_val.replace("-", "")
                            if chk_val.isdigit() == False:
                                msgbox = QtWidgets.QMessageBox()
                                msgbox.setWindowTitle("Message")
                                msgbox.setText("工具取り付けシフト Xの値にエラーがあります。\r\n工具取り付けシフト Xの値を0に設定します。")
                                ret = msgbox.exec()
                                shift_x = "0"
                            chk_val = shift_z.replace(".", "")
                            chk_val = chk_val.replace("-", "")
                            if chk_val.isdigit() == False:
                                msgbox = QtWidgets.QMessageBox()
                                msgbox.setWindowTitle("Message")
                                msgbox.setText("工具取り付けシフト Zの値にエラーがあります。\r\n工具取り付けシフト Zの値を0に設定します。")
                                ret = msgbox.exec()
                                shift_z = "0"
                            geometrio_x = "0"
                            geometrio_z = "0"
                            offset_x = "0"
                            offset_z = "0"
                            nose_r_pos = "0"
                            nose_r = "0"
                        else:
                            shift_x = shift_xz[0]
                            shift_z = shift_xz[1]
                            geometrio_x = shift_xz[2]
                            geometrio_z = shift_xz[3]
                            offset_x = shift_xz[4]
                            offset_z = shift_xz[5]
                            nose_r_pos = shift_xz[6]
                            nose_r = shift_xz[7]
                            chk_val = shift_x.replace(".", "")
                            chk_val = chk_val.replace("-", "")
                            if chk_val.isdigit() == False:
                                msgbox = QtWidgets.QMessageBox()
                                msgbox.setWindowTitle("Message")
                                msgbox.setText("工具取り付けシフト Xの値にエラーがあります。\r\n工具取り付けシフト Xの値を0に設定します。")
                                ret = msgbox.exec()
                                shift_x = "0"
                            chk_val = shift_z.replace(".", "")
                            chk_val = chk_val.replace("-", "")
                            if chk_val.isdigit() == False:
                                msgbox = QtWidgets.QMessageBox()
                                msgbox.setWindowTitle("Message")
                                msgbox.setText("工具取り付けシフト Zの値にエラーがあります。\r\n工具取り付けシフト Zの値を0に設定します。")
                                ret = msgbox.exec()
                                shift_z = "0"
                            chk_val = geometrio_x.replace(".", "")
                            chk_val = chk_val.replace("-", "")
                            if chk_val.isdigit() == False:
                                msgbox = QtWidgets.QMessageBox()
                                msgbox.setWindowTitle("Message")
                                msgbox.setText("ジオメトリオ Xの値にエラーがあります。\r\nジオメトリオ Xの値を0に設定します。")
                                ret = msgbox.exec()
                                geometrio_x = "0"
                            chk_val = geometrio_z.replace(".", "")
                            chk_val = chk_val.replace("-", "")
                            if chk_val.isdigit() == False:
                                msgbox = QtWidgets.QMessageBox()
                                msgbox.setWindowTitle("Message")
                                msgbox.setText("ジオメトリオ Zの値にエラーがあります。\r\nジオメトリオ Zの値を0に設定します。")
                                ret = msgbox.exec()
                                geometrio_z = "0"
                            chk_val = offset_x.replace(".", "")
                            chk_val = chk_val.replace("-", "")
                            if chk_val.isdigit() == False:
                                msgbox = QtWidgets.QMessageBox()
                                msgbox.setWindowTitle("Message")
                                msgbox.setText("オフセット Xの値にエラーがあります。\r\nオフセット Xの値を0に設定します。")
                                ret = msgbox.exec()
                                offset_x = "0"
                            chk_val = offset_z.replace(".", "")
                            chk_val = chk_val.replace("-", "")
                            if chk_val.isdigit() == False:
                                msgbox = QtWidgets.QMessageBox()
                                msgbox.setWindowTitle("Message")
                                msgbox.setText("オフセット Zの値にエラーがあります。\r\nオフセット Zの値を0に設定します。")
                                ret = msgbox.exec()
                                offset_z = "0"
                            chk_val = nose_r_pos.replace(".", "")
                            chk_val = chk_val.replace("-", "")
                            if chk_val.isdigit() == False:
                                msgbox = QtWidgets.QMessageBox()
                                msgbox.setWindowTitle("Message")
                                msgbox.setText("ノーズR補正刃先番号の値にエラーがあります。\r\nノーズR補正刃先番号の値を0に設定します。")
                                ret = msgbox.exec()
                                nose_r_pos = "0"
                            chk_val = nose_r.replace(".", "")
                            chk_val = chk_val.replace("-", "")
                            if chk_val.isdigit() == False:
                                msgbox = QtWidgets.QMessageBox()
                                msgbox.setWindowTitle("Message")
                                msgbox.setText("ノーズR補正Rの値にエラーがあります。\r\nノーズR補正Rの値を0に設定します。")
                                ret = msgbox.exec()
                                nose_r = "0"
                        TOOL_DXF_SHIFT[item] = (shift_x, shift_z)
                        TOOL_DXF_GEOMETRIO[item] = (geometrio_x, geometrio_z)
                        TOOL_DXF_OFFSET[item] = (offset_x, offset_z)
                        TOOL_DXF_NOSE_R[item] = (nose_r_pos, nose_r)
                else:
                    msgbox = QtWidgets.QMessageBox()
                    msgbox.setWindowTitle("Message")
                    msgbox.setText("DXFデータにエラーがあります。\r\n" + filepath)
                    ret = msgbox.exec()
                self.ui.listWidget2.clear()
                for x in TOOL_NAME:
                    if TOOL_DXF_PATH[x] != "":
                        dxf_name = TOOL_DXF_PATH[x]
                        dxf_name = dxf_name.rsplit(".", 1)
                        dxf_name = dxf_name[0]
                        dxf_name = dxf_name.replace("\\", "/")
                        dxf_name = dxf_name.rsplit("/", 1)
                        dxf_name = dxf_name[1]
                        self.ui.listWidget2.addItem(x + "[" + dxf_name + "]")
                    else:
                        self.ui.listWidget2.addItem(x)
                self.ui.listWidget2.setCurrentRow(ex_pos)
            else:
                CFlag = 0
                LT = self.ui.listWidget2.currentItem().text()
                if  "T" in LT:
                    msgbox = QtWidgets.QMessageBox(self)
                    msgbox.setWindowTitle("Message")
                    msgbox.setIcon(QtWidgets.QMessageBox.Question)
                    msgbox.setText("現在の工具を解除しますか？")
                    #msgbox.setIconPixmap(QtGui.QPixmap("PLANET.ico"))
                    msgbox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
                    msgbox.setDefaultButton(QtWidgets.QMessageBox.Cancel)
                    ret = msgbox.exec()
                    if ret == QtWidgets.QMessageBox.Ok:
                        CFlag = 0
                    else:
                        CFlag = 1
                if CFlag == 0:
                    TOOL_DXF_PATH[item] = ""
                    TOOL_DXF_SHIFT[item] = ("0","0")
                    TOOL_DXF_GEOMETRIO[item] = ("0","0")
                    TOOL_DXF_OFFSET[item] = ("0","0")
                    TOOL_DXF_NOSE_R[item] = ("0","0")
                    self.ui.listWidget2.clear()
                    for x in TOOL_NAME:
                        if TOOL_DXF_PATH[x] != "":
                            dxf_name = TOOL_DXF_PATH[x]
                            dxf_name = dxf_name.rsplit(".", 1)
                            dxf_name = dxf_name[0]
                            dxf_name = dxf_name.replace("\\", "/")
                            dxf_name = dxf_name.rsplit("/", 1)
                            dxf_name = dxf_name[1]
                            self.ui.listWidget2.addItem(x + " [" + dxf_name + "]")
                        else:
                            self.ui.listWidget2.addItem(x)
                    self.ui.listWidget2.setCurrentRow(ex_pos)

            if MAIN_SUB_FLAG == 0:
                f_name = TEXT1_FILENAME
            else:
                f_name = TEXT2_FILENAME
            if f_name:
                f_name = f_name.split(".") #ネットワークパスで問題が起こるので下記でワークアラウンド
                tool_dxf_path = ""
                list_length = len(f_name)
                i = 0
                while(True):
                    tool_dxf_path += f_name[i] + "."
                    i += 1
                    if i == list_length - 1:
                        break
                tool_dxf_path += "tdd"
                tool_text = ""
                for x in TOOL_DXF_PATH:
                    if TOOL_DXF_PATH[x] != "":
                        shift_xz = TOOL_DXF_SHIFT[x]
                        geometrio_xz = TOOL_DXF_GEOMETRIO[x]
                        offset_xz = TOOL_DXF_OFFSET[x]
                        nose_r_val = TOOL_DXF_NOSE_R[x]
                        tool_text += x + "," + TOOL_DXF_PATH[x] + "," + shift_xz[0] + "," + shift_xz[1] + "," + geometrio_xz[0] + "," + geometrio_xz[1] + "," + offset_xz[0] + "," + offset_xz[1] + "," + nose_r_val[0] + "," + nose_r_val[1] + "\n"
                f = open(tool_dxf_path, "w")
                f.writelines(tool_text) #Plaine Text Editの内容を書込む
                f.close()


    ##################################################インターフェイス　メニュー関連##################################################
    #---------------------------------------------------------------------
    #---------------------------------------------------------------------
    #---------------------------------------------------------------------
    #---------------------------------------------------------------------
    #-----呼び出し用の関数として使用　シミュレーション実行で呼び出される--------
    #---------------------------------------------------------------------
    #---------------------------------------------------------------------
    #---------------------------------------------------------------------
    #---------------------------------------------------------------------
    def action1_1_triggered(self): #MainWindow1の「シミュレーション実行」で呼び出される
        global PROGRAM_LINE_POS
        global TOOL_CHANGE_POS
        global TOOL_DXF_PATH
        global TOOL_DXF_SHIFT
        global TOOL_DXF_GEOMETRIO
        global TOOL_DXF_OFFSET
        global TOOL_DXF_NOSE_R
        global TOOL_NAME
        global MOVEMENT_DATA
        global TOOLS
        global TOOLS_LINE_NUM
        global TOOLS_TEXT
        global TOOLS_POS
        global NC_PROGRAM
        global FONT_SIZE
        global MATERIAL_PATH
        global MATERIAL_DIAMETER

        if MAIN_SUB_FLAG == 0:
            f_name = TEXT1_FILENAME
        else:
            f_name = TEXT2_FILENAME
        if f_name:
            f = open(f_name, "r")
            original_program = ""
            original_program = f.read()
            f.close()

            _, NC_PROGRAM = NC_SPLITTER(original_program) #テキストのプログラムを解析し、命令と値をリスト配列に代入
            nc_text = NC_PROGRAM_TEXT(NC_PROGRAM) #配列化したプログラムを取得

            if self.ui.action2_6.isChecked() == True:
                MOVEMENT_DATA, PROGRAM_LINE_POS, TOOL_NAME, TOOL_CHANGE_POS = NC_MOVEMENT(NC_PROGRAM, 1) #append_G50はG50を適用するかのフラグ
            else:
                MOVEMENT_DATA, PROGRAM_LINE_POS, TOOL_NAME, TOOL_CHANGE_POS = NC_MOVEMENT(NC_PROGRAM, 0) #append_G50はG50を適用するかのフラグ

            #MOVEMENT_DATA = [G98かG99, 回転数, G012350, NC_X, NC_Z, NC_R, NC_F, 行番号, G50_U, G50_W, 移動距離X, 移動距離Z, 移動角度]
            spindleSpeed = 0
            G98_G99 = 0
            GCode = 0
            ncR = 0
            ncF = 0
            xL = 0
            zL = 0
            resultText = ""
            for i in MOVEMENT_DATA:
                for l in i:
                    G98_G99 = l[0]
                    GCode = l[2]
                    if l[1] != 0:
                        spindleSpeed = l[1]
                    if l[2] != 0:
                        GCode = l[2]
                    ncR = l[5]
                    if l[6] != 0:
                        ncF = l[6]
                    xL = l[10]
                    zL = l[11]
                    if GCode == "1" or GCode == "2" or GCode == "3":
                        if xL > 0 or zL > 0:
                            if spindleSpeed == 0 and G98_G99 == "99":
                                resultText += "LINE " + str(l[7]) + ":VALUE OF S IS 0.\r\n"
                            if ncF ==0:
                                resultText += "LINE " + str(l[7]) + ":VALUE OF F IS 0.\r\n"
                    if GCode == "2" or GCode == "3":
                        if xL == 0 or zL == 0:
                            resultText += "LINE " + str(l[7]) + ":NEED X AND Z VALUE.\r\n"
                        if ncR == 0:
                            resultText += "LINE " + str(l[7]) + ":NEED R VALUE.\r\n"
            if resultText != "":
                self.ui.plainTextEdit1.setPlainText(resultText + "ERROR!")
                return

            if self.ui.action2_6.isChecked() == True:
                APPEND_G50 = 1
            else:
                APPEND_G50 = 0
            if self.ui.action2_14.isChecked() == True:
                TOOLS, TOOLS_LINE_NUM, TOOLS_TEXT, TOOLS_POS = NC_PATH(MOVEMENT_DATA, 50, 1, FONT_SIZE, 1, APPEND_G50)
            else:
                TOOLS, TOOLS_LINE_NUM, TOOLS_TEXT, TOOLS_POS = NC_PATH(MOVEMENT_DATA, 50, 1, FONT_SIZE, 0, APPEND_G50)

            each_line = nc_text.split("\r\n")
            self.ui.listWidget1.clear()
            self.ui.listWidget2.clear()
            self.ui.listWidget1.addItems(each_line)
            #self.ui.listWidget2.addItems(TOOL_NAME)
            for x in TOOL_NAME:
                TOOL_DXF_PATH[x] = ""
                TOOL_DXF_SHIFT[x] = ("0","0")
                TOOL_DXF_GEOMETRIO[x] = ("0","0")
                TOOL_DXF_OFFSET[x] = ("0","0")
                TOOL_DXF_NOSE_R[x] = ("0","0")
            self.ui.listWidget2.clear()
            for x in TOOL_NAME:
                self.ui.listWidget2.addItem(x)
            
            self.ui.pushButton1.setEnabled(True)
            self.ui.listWidget2.setEnabled(True)
            self.ui.action1_2.setEnabled(True)
            self.ui.action1_3.setEnabled(True)

            f_name = f_name.split(".")
            #tool_dxf_path = f_name[0] + ".tdd" #ネットワークパスで問題が起こるので下記でワークアラウンド
            tool_dxf_path = ""
            list_length = len(f_name)
            i = 0
            while(True):
                tool_dxf_path += f_name[i] + "."
                i += 1
                if i == list_length - 1:
                    break
            MATERIAL_PATH = tool_dxf_path + "mdd"
            tool_dxf_path += "tdd"

            if os.path.exists(tool_dxf_path):
                self.action1_2_triggered(tool_dxf_path)

            if os.path.exists(MATERIAL_PATH):
                f = open(MATERIAL_PATH, "r")
                x = ""
                x = f.readlines() #テキストを一行ずつ配列として読込む（行の終わりの改行コードも含めて読込む）
                f.close()
                data = x[0].replace("\n", "")
                MATERIAL_DIAMETER = float(data)
                MATERIAL_DIAMETER = MATERIAL_DIAMETER / -2 #10 / -2 材料径


    #-----メニュー処理（工具データを開く）----------------------------------------
    def action1_2_triggered(self, filepath=""):
        global TOOL_DXF_PATH
        global TOOL_DXF_SHIFT
        global TOOL_DXF_GEOMETRIO
        global TOOL_DXF_OFFSET
        global TOOL_DXF_NOSE_R
        global TOOL_NAME

        if filepath == False: #action1_2_triggered(self, filepath="")のfilepath=""がFalseになる問題のworkaround
            filepath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "",'tdd File (*.tdd)')
        if filepath:
            for x in TOOL_NAME:
                TOOL_DXF_PATH[x] = ""
            f = open(filepath, "r")
            textList = ""
            textList = f.readlines() #テキストを一行ずつ配列として読込む（行の終わりの改行コードも含めて読込む）
            f.close()
            for x in textList:
                x = x.replace("\r\n", "")
                x = x.replace("\n", "")
                if x != "":
                    read_data = x.split(",")
                    if (read_data[0] in TOOL_DXF_PATH) == True:
                        if os.path.exists(read_data[1]):
                            TOOL_DXF_PATH[read_data[0]] = read_data[1]
                            TOOL_DXF_SHIFT[read_data[0]] = (read_data[2], read_data[3])
                            if len(read_data) > 4:
                                TOOL_DXF_GEOMETRIO[read_data[0]] = (read_data[4], read_data[5])
                                TOOL_DXF_OFFSET[read_data[0]] = (read_data[6], read_data[7])
                                TOOL_DXF_NOSE_R[read_data[0]] = (read_data[8], read_data[9])
                            else:
                                TOOL_DXF_GEOMETRIO[read_data[0]] = ("0", "0")
                                TOOL_DXF_OFFSET[read_data[0]] = ("0", "0")
                                TOOL_DXF_NOSE_R[read_data[0]] = ("0", "0")
                        else:
                            msgbox = QtWidgets.QMessageBox(self)
                            msgbox.setWindowTitle("Message")
                            #msgbox.setIconPixmap(QtGui.QPixmap("PLANET.ico"))
                            msgbox.setText("DXFファイル" + read_data[1] + "が存在しません。\r\n再度設定して下さい。")
                            ret = msgbox.exec()
                            self.ui.plainTextEdit1.setFocus()
                        
            ex_pos = self.ui.listWidget2.currentRow()
            self.ui.listWidget2.clear()
            for x in TOOL_NAME:
                if TOOL_DXF_PATH[x] != "":
                    dxf_name = TOOL_DXF_PATH[x]
                    dxf_name = dxf_name.rsplit(".", 1)
                    dxf_name = dxf_name[0]
                    dxf_name = dxf_name.replace("\\", "/")
                    dxf_name = dxf_name.rsplit("/", 1)
                    dxf_name = dxf_name[1]
                    self.ui.listWidget2.addItem(x + " [" + dxf_name + "]")
                else:
                    self.ui.listWidget2.addItem(x)
            self.ui.listWidget2.setCurrentRow(ex_pos)


    #-----メニュー処理（工具データを保存）----------------------------------------
    def action1_3_triggered(self):
        global TOOL_DXF_PATH
        global TOOL_DXF_SHIFT
        global TOOL_DXF_GEOMETRIO
        global TOOL_DXF_OFFSET
        global TOOL_DXF_NOSE_R
        filepath, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "",'tdd File (*.tdd)')
        if filepath:
            tool_text = ""
            for x in TOOL_DXF_PATH:
                if TOOL_DXF_PATH[x] != "":
                    shift_xz = TOOL_DXF_SHIFT[x]
                    geometrio_xz = TOOL_DXF_GEOMETRIO[x]
                    offset_xz = TOOL_DXF_OFFSET[x]
                    nose_r_val = TOOL_DXF_NOSE_R[x]
                    tool_text += x + "," + TOOL_DXF_PATH[x] + "," + shift_xz[0] + "," + shift_xz[1] + "," + geometrio_xz[0] + "," + geometrio_xz[1] + "," + offset_xz[0] + "," + offset_xz[1] + "," + nose_r_val[0] + "," + nose_r_val[1] + "\n"
            f = open(filepath, "w")
            f.writelines(tool_text) #Plaine Text Editの内容を書込む
            f.close()
            msgbox = QtWidgets.QMessageBox()
            msgbox.setWindowTitle("Massage")
            msgbox.setText("工具データを保存しました。")
            ret = msgbox.exec()


    #-----メニュー処理（工具軌跡を保存）----------------------------------------
    def action1_4_triggered(self):
        self.CREATE_DXF_PATH_1()


    #-----メニュー処理（工具軌跡を保存）----------------------------------------
    def action1_5_triggered(self):
        self.CREATE_DXF_PATH_2()


    #-----メニュー処理（工具軌跡を保存）----------------------------------------
    def action1_6_triggered(self):
        self.CREATE_DXF_PATH_3()


    #-----メニュー処理（工具フォルダを記憶）----------------------------------------
    def action1_7_triggered(self):
        global TOOL_DATA_DIR_PATH
        FolderPath = QtWidgets.QFileDialog.getExistingDirectory(self)
        if FolderPath:
            TOOL_DATA_DIR_PATH = FolderPath
            f = open(SETTING_PATH_DIR, "w")
            f.write(TOOL_DATA_DIR_PATH) #Plaine Text Editの内容を書込む
            f.close()


    #-----メニュー処理（表示の初期化）----------------------------------------
    def action2_1_triggered(self):
        global SCALE
        global TOOLS_TEXT
        global TOOL_TEXT_PARENTS
        global MATERIAL
        global MOVEMENT_DATA
        global FONT_SIZE
        global TOOLS_TEXT_SCALE
        #self.ui.graphicsView1.resetMatrix() #回転、拡大のマトリクスをリセット
        self.ui.graphicsView1.resetTransform()
        self.ui.graphicsView1.scale(0.5, 0.5)
        SCALE = 0.5
        self.ui.graphicsView1.centerOn(0, 0)
        for i, x in enumerate(TOOLS_TEXT):
            for l, y in enumerate(x):
                self.scene.removeItem(TOOLS_TEXT[i][l])
                TOOLS_TEXT[i][l] = ""
        if self.ui.action2_6.isChecked() == True:
            APPEND_G50 = 1
        else:
            APPEND_G50 = 0
        if self.ui.action2_14.isChecked() == True:
            _, _, TOOLS_TEXT, _ = NC_PATH(MOVEMENT_DATA, 50, 1, FONT_SIZE, 1, APPEND_G50, TOOL_NAME, TOOL_DXF_GEOMETRIO)
        else:
            _, _, TOOLS_TEXT, _ = NC_PATH(MOVEMENT_DATA, 50, 1, FONT_SIZE, 0, APPEND_G50, TOOL_NAME, TOOL_DXF_GEOMETRIO)
        TOOL_TEXT_PARENTS.clear()
        for i, x in enumerate(TOOLS_TEXT):
            TOOL_TEXT_PARENTS.append(QtWidgets.QGraphicsTextItem())
            for y in x:
                y.setParentItem(TOOL_TEXT_PARENTS[i])
                y.show()
            TOOL_TEXT_PARENTS[i].setParentItem(MATERIAL)
            TOOL_TEXT_PARENTS[i].hide()
        TOOLS_TEXT_SCALE = 1
        for i, x in enumerate(TOOLS_TEXT):
            for l, y in enumerate(x):
                TOOLS_TEXT[i][l].setScale(TOOLS_TEXT_SCALE)

    #-----メニュー処理（パスの移動初期化）----------------------------------------
    def action2_2_triggered(self):
        self.SETTINGS_SAVE()
        #if self.ui.action2_2.isChecked() == False:
            #COLOR_MODE = 0
        #else:
            #COLOR_MODE = 1

        #for x in ITEMS:
            #for y in x:
                #y.setPos(0, 0)


    def action2_3_triggered(self):
        self.ui.action2_3.setChecked(True)
        self.ui.action2_4.setChecked(False)
        self.ui.action2_25.setChecked(False)
        self.SETTINGS_SAVE()


    def action2_4_triggered(self):
        self.ui.action2_3.setChecked(False)
        self.ui.action2_4.setChecked(True)
        self.ui.action2_25.setChecked(False)
        self.SETTINGS_SAVE()


    def action2_5_triggered(self):
        self.SETTINGS_SAVE()


    def action2_6_triggered(self):
        global PROGRAM_LINE_POS
        global TOOL_CHANGE_POS
        global TOOL_NAME
        global MOVEMENT_DATA
        global TOOLS
        global NC_PROGRAM
        global FONT_SIZE
        if NC_PROGRAM != "":
            if self.ui.action2_6.isChecked() == True:
                MOVEMENT_DATA, PROGRAM_LINE_POS, TOOL_NAME, TOOL_CHANGE_POS = NC_MOVEMENT(NC_PROGRAM, 1) #append_G50はG50を適用するかのフラグ
            else:
                MOVEMENT_DATA, PROGRAM_LINE_POS, TOOL_NAME, TOOL_CHANGE_POS = NC_MOVEMENT(NC_PROGRAM, 0) #append_G50はG50を適用するかのフラグ
            if self.ui.action2_6.isChecked() == True:
                APPEND_G50 = 1
            else:
                APPEND_G50 = 0
            if self.ui.action2_14.isChecked() == True:
                TOOLS, _, _, _ = NC_PATH(MOVEMENT_DATA, 50, 1, FONT_SIZE, 1, APPEND_G50)
            else:
                TOOLS, _, _, _ = NC_PATH(MOVEMENT_DATA, 50, 1, FONT_SIZE, 0, APPEND_G50)
        self.SETTINGS_SAVE()


    def action2_7_triggered(self):
        self.ui.action2_7.setChecked(True)
        self.ui.action2_8.setChecked(False)
        self.ui.action2_24.setChecked(False)
        self.SETTINGS_SAVE()


    def action2_8_triggered(self):
        self.ui.action2_7.setChecked(False)
        self.ui.action2_8.setChecked(True)
        self.ui.action2_24.setChecked(False)
        self.SETTINGS_SAVE()


    def action2_9_triggered(self):
        global GUIDE_BUSH_U
        global GUIDE_BUSH_L
        if self.ui.action2_9.isChecked() == True:
            GUIDE_BUSH_U.show()
            GUIDE_BUSH_L.show()
        else:
            GUIDE_BUSH_U.hide()
            GUIDE_BUSH_L.hide()
        self.SETTINGS_SAVE()


    def action2_10_triggered(self):
        global FONT_SIZE
        self.ui.action2_10.setChecked(True)
        self.ui.action2_11.setChecked(False)
        self.ui.action2_12.setChecked(False)
        self.ui.action2_21.setChecked(False)
        self.ui.action2_22.setChecked(False)
        self.ui.action2_23.setChecked(False)
        for i, x in enumerate(TOOLS_TEXT):
            for l, y in enumerate(x):
                TOOLS_TEXT[i][l].setFont(QtGui.QFont('Times', 15))
        FONT_SIZE = 15
        self.SETTINGS_SAVE()


    def action2_11_triggered(self):
        global FONT_SIZE
        self.ui.action2_10.setChecked(False)
        self.ui.action2_11.setChecked(True)
        self.ui.action2_12.setChecked(False)
        self.ui.action2_21.setChecked(False)
        self.ui.action2_22.setChecked(False)
        self.ui.action2_23.setChecked(False)
        for i, x in enumerate(TOOLS_TEXT):
            for l, y in enumerate(x):
                TOOLS_TEXT[i][l].setFont(QtGui.QFont('Times', 20))
        FONT_SIZE = 20
        self.SETTINGS_SAVE()


    def action2_12_triggered(self):
        global FONT_SIZE
        self.ui.action2_10.setChecked(False)
        self.ui.action2_11.setChecked(False)
        self.ui.action2_12.setChecked(True)
        self.ui.action2_21.setChecked(False)
        self.ui.action2_22.setChecked(False)
        self.ui.action2_23.setChecked(False)
        for i, x in enumerate(TOOLS_TEXT):
            for l, y in enumerate(x):
                TOOLS_TEXT[i][l].setFont(QtGui.QFont('Times', 25))
        FONT_SIZE = 25
        self.SETTINGS_SAVE()


    def action2_13_triggered(self):
        self.SETTINGS_SAVE()


    def action2_14_triggered(self):
        global MOVEMENT_DATA
        global TOOLS
        global TOOL_TEXT_PARENTS
        global TOOLS_TEXT
        global MATERIAL
        global FONT_SIZE
        for i, x in enumerate(TOOLS_TEXT):
            for l, y in enumerate(x):
                self.scene.removeItem(TOOLS_TEXT[i][l])
                TOOLS_TEXT[i][l] = ""
        if self.ui.action2_6.isChecked() == True:
            APPEND_G50 = 1
        else:
            APPEND_G50 = 0
        if self.ui.action2_14.isChecked() == True:
            _, _, TOOLS_TEXT, _ = NC_PATH(MOVEMENT_DATA, 50, 1, FONT_SIZE, 1, APPEND_G50, TOOL_NAME, TOOL_DXF_GEOMETRIO)
        else:
            _, _, TOOLS_TEXT, _ = NC_PATH(MOVEMENT_DATA, 50, 1, FONT_SIZE, 0, APPEND_G50, TOOL_NAME, TOOL_DXF_GEOMETRIO)
        TOOL_TEXT_PARENTS.clear()
        for i, x in enumerate(TOOLS_TEXT):
            TOOL_TEXT_PARENTS.append(QtWidgets.QGraphicsTextItem())
            for y in x:
                y.setParentItem(TOOL_TEXT_PARENTS[i])
                y.show()
            TOOL_TEXT_PARENTS[i].setParentItem(MATERIAL)
            TOOL_TEXT_PARENTS[i].hide()
        self.SETTINGS_SAVE()


    def action2_15_triggered(self):
        global CENTER_LINE
        if self.ui.action2_15.isChecked() == False:
            CENTER_LINE.hide()
        else:
            CENTER_LINE.show()
        self.SETTINGS_SAVE()


    def action2_16_triggered(self):
        global MOVEMENT_DATA
        global TOOLS
        global TOOL_TEXT_PARENTS
        global TOOLS_TEXT
        global MATERIAL
        global FONT_SIZE
        for i, x in enumerate(TOOLS_TEXT):
            for l, y in enumerate(x):
                self.scene.removeItem(TOOLS_TEXT[i][l])
                TOOLS_TEXT[i][l] = ""
        if self.ui.action2_6.isChecked() == True:
            APPEND_G50 = 1
        else:
            APPEND_G50 = 0
        if self.ui.action2_14.isChecked() == True:
            _, _, TOOLS_TEXT, _ = NC_PATH(MOVEMENT_DATA, 50, 1, FONT_SIZE, 1, APPEND_G50, TOOL_NAME, TOOL_DXF_GEOMETRIO)
        else:
            _, _, TOOLS_TEXT, _ = NC_PATH(MOVEMENT_DATA, 50, 1, FONT_SIZE, 0, APPEND_G50, TOOL_NAME, TOOL_DXF_GEOMETRIO)
        TOOL_TEXT_PARENTS.clear()
        for i, x in enumerate(TOOLS_TEXT):
            TOOL_TEXT_PARENTS.append(QtWidgets.QGraphicsTextItem())
            for y in x:
                y.setParentItem(TOOL_TEXT_PARENTS[i])
                y.show()
            TOOL_TEXT_PARENTS[i].setParentItem(MATERIAL)
            TOOL_TEXT_PARENTS[i].hide()
        self.SETTINGS_SAVE()

    def action2_17_triggered(self):
        self.SETTINGS_SAVE()

    def action2_18_triggered(self):
        self.SETTINGS_SAVE()

    def action2_19_triggered(self):
        self.SETTINGS_SAVE()

    def action2_20_triggered(self):
        self.SETTINGS_SAVE()

    def action2_21_triggered(self):
        global FONT_SIZE
        self.ui.action2_10.setChecked(False)
        self.ui.action2_11.setChecked(False)
        self.ui.action2_12.setChecked(False)
        self.ui.action2_21.setChecked(True)
        self.ui.action2_22.setChecked(False)
        self.ui.action2_23.setChecked(False)
        for i, x in enumerate(TOOLS_TEXT):
            for l, y in enumerate(x):
                TOOLS_TEXT[i][l].setFont(QtGui.QFont('Times', 10))
        FONT_SIZE = 10
        self.SETTINGS_SAVE()

    def action2_22_triggered(self):
        global FONT_SIZE
        self.ui.action2_10.setChecked(False)
        self.ui.action2_11.setChecked(False)
        self.ui.action2_12.setChecked(False)
        self.ui.action2_21.setChecked(False)
        self.ui.action2_22.setChecked(True)
        self.ui.action2_23.setChecked(False)
        for i, x in enumerate(TOOLS_TEXT):
            for l, y in enumerate(x):
                TOOLS_TEXT[i][l].setFont(QtGui.QFont('Times', 5))
        FONT_SIZE = 5
        self.SETTINGS_SAVE()

    def action2_23_triggered(self):
        global FONT_SIZE
        self.ui.action2_10.setChecked(False)
        self.ui.action2_11.setChecked(False)
        self.ui.action2_12.setChecked(False)
        self.ui.action2_21.setChecked(False)
        self.ui.action2_22.setChecked(False)
        self.ui.action2_23.setChecked(True)
        for i, x in enumerate(TOOLS_TEXT):
            for l, y in enumerate(x):
                TOOLS_TEXT[i][l].setFont(QtGui.QFont('Times', 1))
        FONT_SIZE = 1
        self.SETTINGS_SAVE()

    def action2_24_triggered(self):
        self.ui.action2_7.setChecked(False)
        self.ui.action2_8.setChecked(False)
        self.ui.action2_24.setChecked(True)
        self.SETTINGS_SAVE()

    def action2_25_triggered(self):
        self.ui.action2_3.setChecked(False)
        self.ui.action2_4.setChecked(False)
        self.ui.action2_25.setChecked(True)
        self.SETTINGS_SAVE()

    def action3_1_triggered(self):
        global RUN_SPEED
        RUN_SPEED = 0
        self.ui.action3_1.setChecked(True)
        self.ui.action3_2.setChecked(False)
        self.ui.action3_3.setChecked(False)
        self.ui.action3_4.setChecked(False)
        self.ui.action3_5.setChecked(False)
        self.ui.action3_6.setChecked(False)
        self.SETTINGS_SAVE()


    def action3_2_triggered(self):
        global RUN_SPEED
        RUN_SPEED = 1
        self.ui.action3_1.setChecked(False)
        self.ui.action3_2.setChecked(True)
        self.ui.action3_3.setChecked(False)
        self.ui.action3_4.setChecked(False)
        self.ui.action3_5.setChecked(False)
        self.ui.action3_6.setChecked(False)
        self.SETTINGS_SAVE()


    def action3_3_triggered(self):
        global RUN_SPEED
        RUN_SPEED = 3
        self.ui.action3_1.setChecked(False)
        self.ui.action3_2.setChecked(False)
        self.ui.action3_3.setChecked(True)
        self.ui.action3_4.setChecked(False)
        self.ui.action3_5.setChecked(False)
        self.ui.action3_6.setChecked(False)
        self.SETTINGS_SAVE()


    def action3_4_triggered(self):
        global RUN_SPEED
        RUN_SPEED = 7
        self.ui.action3_1.setChecked(False)
        self.ui.action3_2.setChecked(False)
        self.ui.action3_3.setChecked(False)
        self.ui.action3_4.setChecked(True)
        self.ui.action3_5.setChecked(False)
        self.ui.action3_6.setChecked(False)
        self.SETTINGS_SAVE()


    def action3_5_triggered(self):
        global RUN_SPEED
        RUN_SPEED = 15
        self.ui.action3_1.setChecked(False)
        self.ui.action3_2.setChecked(False)
        self.ui.action3_3.setChecked(False)
        self.ui.action3_4.setChecked(False)
        self.ui.action3_5.setChecked(True)
        self.ui.action3_6.setChecked(False)
        self.SETTINGS_SAVE()


    def action3_6_triggered(self):
        global RUN_SPEED
        RUN_SPEED = -1
        self.ui.action3_1.setChecked(False)
        self.ui.action3_2.setChecked(False)
        self.ui.action3_3.setChecked(False)
        self.ui.action3_4.setChecked(False)
        self.ui.action3_5.setChecked(False)
        self.ui.action3_6.setChecked(True)
        self.SETTINGS_SAVE()


    #-----メニュー処理（画像を保存）----------------------------------------
    def action4_1_triggered(self):
        filepath, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "",'png File (*.png)')
        if filepath:
            self.ui.graphicsView1.grab().save(filepath)










    ##################################################イベント関連##################################################
    #-----マウスのイベント処理----------------------------------------
    def eventFilter(self, obj, event):
        global EX_X
        global EX_Y
        global BUTTON_FLAG
        global SCALE
        global SELECTED_ITEM
        global MATERIAL
        #global TOOL_REGION
        global TOOLS_TEXT
        global TOOLS_TEXT_SCALE
        global MOUSE_R_CLICK_FIRST
        global MOUSE_R_CLICK_SECOND
        global MOUSE_R_CLICK_FLAG
        global EX_MOUSE_R_CLICK_FIRST
        global EX_MOUSE_R_CLICK_SECOND
        global EX_MOUSE_R_CLICK_FIRST_X
        global EX_MOUSE_R_CLICK_FIRST_Y
        global EX_PATH
        global EX_MAX_Z
        global EX_MIN_Z
        global EX_MAX_X
        global EX_MIN_X
        global Z1MIN_TEXT
        global Z1MAX_TEXT
        global X1MIN_TEXT
        global X1MAX_TEXT
        global Z2MIN_TEXT
        global Z2MAX_TEXT
        global X2MIN_TEXT
        global X2MAX_TEXT

        #graphicsView1.viewport()上でボタンが押された場合の処理
        if (event.type() == QtGui.QPaintEvent.MouseButtonPress and obj is self.ui.graphicsView1.viewport()) or (event.type() == QtGui.QPaintEvent.MouseButtonDblClick and obj is self.ui.graphicsView1.viewport()):
            SELECTED_ITEM = self.ui.graphicsView1.itemAt(event.position().x(), event.position().y())#, QtGui.QTransform())
            if event.button() == QtCore.Qt.LeftButton:
                BUTTON_FLAG = 1
                EX_X = event.position().x() #マウスカーソルのX位置を記憶
                EX_Y = event.position().y() #マウスカーソルのY位置を記憶
            elif event.button() == QtCore.Qt.RightButton and FLAG_END == 1:
                if MOUSE_R_CLICK_FLAG == 0:
                    if MOUSE_R_CLICK_SECOND != "":
                        self.scene.removeItem(MOUSE_R_CLICK_SECOND)
                        MOUSE_R_CLICK_SECOND = ""
                    EX_MOUSE_R_CLICK_FIRST.hide()
                    if EX_MOUSE_R_CLICK_SECOND != "":
                        self.scene.removeItem(EX_MOUSE_R_CLICK_SECOND)
                        EX_MOUSE_R_CLICK_SECOND = ""
                    Z1MIN_TEXT.hide()
                    Z1MAX_TEXT.hide()
                    X1MIN_TEXT.hide()
                    X1MAX_TEXT.hide()
                    Z2MIN_TEXT.hide()
                    Z2MAX_TEXT.hide()
                    X2MIN_TEXT.hide()
                    X2MAX_TEXT.hide()
                elif MOUSE_R_CLICK_FLAG == 1:
                    self.scene.removeItem(MOUSE_R_CLICK_SECOND)
                    MOUSE_R_CLICK_SECOND = ""
                    EX_MOUSE_R_CLICK_FIRST.setPos(EX_MOUSE_R_CLICK_FIRST_X, EX_MOUSE_R_CLICK_FIRST_Y)
                    EX_MOUSE_R_CLICK_FIRST.show()
                    #if EX_MOUSE_R_CLICK_SECOND != "":
                        #self.scene.removeItem(EX_MOUSE_R_CLICK_SECOND)
                    pen = QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.SolidLine)
                    pen.setCosmetic(True)
                    EX_MOUSE_R_CLICK_SECOND = self.scene.addPath(EX_PATH, pen)
                scenePos =self.ui.graphicsView1.mapToScene(event.position().x(), event.position().y())
                MOUSE_R_CLICK_FIRST.setPos(scenePos.x() - 15, scenePos.y() - 15)
                MOUSE_R_CLICK_FIRST.show()
                xyListX = []
                xyListY = []
                for i in self.scene.collidingItems(MOUSE_R_CLICK_FIRST, QtCore.Qt.ItemSelectionMode.IntersectsItemShape):
                    tmp = i.shape().toFillPolygon().toList()
                    #print(i.shape().toFillPolygon().toPolygon().toList())
                    for l in tmp:
                        inPos = QtCore.QPointF(l.x() - MOUSE_R_CLICK_FIRST.x() + MATERIAL.x(), l.y() - MOUSE_R_CLICK_FIRST.y())
                        if MOUSE_R_CLICK_FIRST.contains(inPos):
                            pX = l.x()
                            pY = l.y()
                            if "999999999999" in str(pX):
                                pX = pX + 0.001
                                pX = str(pX)
                                sp = pX.split(".")
                                lp = sp[1]
                                lp = lp[:3]
                                pX = float(sp[0] + "." + lp)
                            elif "000000000001" in str(pX):
                                pX = str(pX)
                                sp = pX.split(".")
                                lp = sp[1]
                                lp = lp[:3]
                                pX = float(sp[0] + "." + lp)
                            if "999999999999" in str(pY):
                                pY = pY + 0.001
                                pY = str(pY)
                                sp = pY.split(".")
                                lp = sp[1]
                                lp = lp[:3]
                                pY = float(sp[0] + "." + lp)
                            elif "000000000001" in str(pY):
                                pY = str(pY)
                                sp = pY.split(".")
                                lp = sp[1]
                                lp = lp[:3]
                                pY = float(sp[0] + "." + lp)
                            stX = str(pX)
                            stY = str(pY)
                            tmpX = stX.split(".")
                            stX = tmpX[1]
                            tmpY = stY.split(".")
                            stY = tmpY[1]
                            stX = stX.replace('-', "")
                            stX = stX.replace('+', "")
                            stY = stY.replace('-', "")
                            stY = stY.replace('+', "")
                            pX = RND(pX / VIEW_SCALE)
                            pY = RND(pY / VIEW_SCALE)
                            if len(stX) < 4:
                                xyListX.append(pX)
                                xyListY.append(pY)
                            if len(stY) < 4:
                                xyListX.append(pX)
                                xyListY.append(pY)
                cX = collections.Counter(xyListX)
                cY = collections.Counter(xyListY)
                if len(cX) > 0 and len(cY)> 0:
                    maxKeyX = max(cX.items(), key=operator.itemgetter(1))[0]
                    cXnum = cX[maxKeyX]
                    maxKeyY = max(cY.items(), key=operator.itemgetter(1))[0]
                    cYnum = cY[maxKeyY]
                    if cXnum > cYnum:
                        idx = -1
                        result = []
                        for cnt in range(xyListX.count(maxKeyX)):
                            idx = xyListX.index(maxKeyX, idx+1)
                            result.append(idx)
                        searchList = []
                        for x in result:
                            searchList.append(xyListY[x])
                        path = QtGui.QPainterPath()
                        path.moveTo(maxKeyX * VIEW_SCALE + MATERIAL.x(), max(searchList) * VIEW_SCALE)
                        path.lineTo(maxKeyX * VIEW_SCALE + MATERIAL.x(), min(searchList) * VIEW_SCALE)
                        pen = QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.SolidLine)
                        pen.setCosmetic(True)
                        MOUSE_R_CLICK_SECOND = self.scene.addPath(path, pen)
                        if MOUSE_R_CLICK_FLAG == 0:
                            Z1MIN_TEXT.setPlainText("Z1min=" + str(maxKeyX))
                            Z1MIN_TEXT.setPos(scenePos.x() - 15 - Z1MIN_TEXT.boundingRect().width(), scenePos.y() - int(Z1MIN_TEXT.boundingRect().height() / 2))
                            Z1MIN_TEXT.show()
                            Z1MAX_TEXT.setPlainText("Z1max=" + str(maxKeyX))
                            Z1MAX_TEXT.setPos(scenePos.x() + 15, scenePos.y() - int(Z1MAX_TEXT.boundingRect().height() / 2))
                            Z1MAX_TEXT.show()
                            X1MIN_TEXT.setPlainText("X1min=" + str(max(searchList) * -1))
                            X1MIN_TEXT.setPos(scenePos.x() - int(X1MIN_TEXT.boundingRect().width() / 2), scenePos.y() + 15)
                            X1MIN_TEXT.show()
                            X1MAX_TEXT.setPlainText("X1max=" + str(min(searchList) * -1))
                            X1MAX_TEXT.setPos(scenePos.x() - int(X1MAX_TEXT.boundingRect().width() / 2), scenePos.y() - 15 - X1MAX_TEXT.boundingRect().height())
                            X1MAX_TEXT.show()
                        else:
                            Z2MIN_TEXT.setPlainText("Z2min=" + str(maxKeyX))
                            Z2MIN_TEXT.setPos(scenePos.x() - 15 - Z2MIN_TEXT.boundingRect().width(), scenePos.y() - int(Z2MIN_TEXT.boundingRect().height() / 2))
                            Z2MIN_TEXT.show()
                            Z2MAX_TEXT.setPlainText("Z2max=" + str(maxKeyX))
                            Z2MAX_TEXT.setPos(scenePos.x() + 15, scenePos.y() - int(Z2MAX_TEXT.boundingRect().height() / 2))
                            Z2MAX_TEXT.show()
                            X2MIN_TEXT.setPlainText("X2min=" + str(max(searchList) * -1))
                            X2MIN_TEXT.setPos(scenePos.x() - int(X2MIN_TEXT.boundingRect().width() / 2), scenePos.y() + 15)
                            X2MIN_TEXT.show()
                            X2MAX_TEXT.setPlainText("X2max=" + str(min(searchList) * -1))
                            X2MAX_TEXT.setPos(scenePos.x() - int(X2MAX_TEXT.boundingRect().width() / 2), scenePos.y() - 15 - X2MAX_TEXT.boundingRect().height())
                            X2MAX_TEXT.show()
                    elif cXnum < cYnum:
                        idx = -1
                        result = []
                        for cnt in range(xyListY.count(maxKeyY)):
                            idx = xyListY.index(maxKeyY, idx+1)
                            result.append(idx)
                        searchList = []
                        for x in result:
                            searchList.append(xyListX[x])
                        path = QtGui.QPainterPath()
                        path.moveTo(max(searchList) * VIEW_SCALE + MATERIAL.x(), maxKeyY * VIEW_SCALE)
                        path.lineTo(min(searchList) * VIEW_SCALE + MATERIAL.x(), maxKeyY * VIEW_SCALE)
                        pen = QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.SolidLine)
                        pen.setCosmetic(True)
                        MOUSE_R_CLICK_SECOND = self.scene.addPath(path, pen)
                        if MOUSE_R_CLICK_FLAG == 0:
                            Z1MIN_TEXT.setPlainText("Z1min=" + str(min(searchList)))
                            Z1MIN_TEXT.setPos(scenePos.x() - 15 - Z1MIN_TEXT.boundingRect().width(), scenePos.y() - int(Z1MIN_TEXT.boundingRect().height() / 2))
                            Z1MIN_TEXT.show()
                            Z1MAX_TEXT.setPlainText("Z1max=" + str(max(searchList)))
                            Z1MAX_TEXT.setPos(scenePos.x() + 15, scenePos.y() - int(Z1MAX_TEXT.boundingRect().height() / 2))
                            Z1MAX_TEXT.show()
                            X1MIN_TEXT.setPlainText("X1min=" + str(maxKeyY * -1))
                            X1MIN_TEXT.setPos(scenePos.x() - int(X1MIN_TEXT.boundingRect().width() / 2), scenePos.y() + 15)
                            X1MIN_TEXT.show()
                            X1MAX_TEXT.setPlainText("X1max=" + str(maxKeyY * -1))
                            X1MAX_TEXT.setPos(scenePos.x() - int(X1MAX_TEXT.boundingRect().width() / 2), scenePos.y() - 15 - X1MAX_TEXT.boundingRect().height())
                            X1MAX_TEXT.show()
                        else:
                            Z2MIN_TEXT.setPlainText("Z2min=" + str(min(searchList)))
                            Z2MIN_TEXT.setPos(scenePos.x() - 15 - Z2MIN_TEXT.boundingRect().width(), scenePos.y() - int(Z2MIN_TEXT.boundingRect().height() / 2))
                            Z2MIN_TEXT.show()
                            Z2MAX_TEXT.setPlainText("Z2max=" + str(max(searchList)))
                            Z2MAX_TEXT.setPos(scenePos.x() + 15, scenePos.y() - int(Z2MAX_TEXT.boundingRect().height() / 2))
                            Z2MAX_TEXT.show()
                            X2MIN_TEXT.setPlainText("X2min=" + str(maxKeyY * -1))
                            X2MIN_TEXT.setPos(scenePos.x() - int(X2MIN_TEXT.boundingRect().width() / 2), scenePos.y() + 15)
                            X2MIN_TEXT.show()
                            X2MAX_TEXT.setPlainText("X2max=" + str(maxKeyY * -1))
                            X2MAX_TEXT.setPos(scenePos.x() - int(X2MAX_TEXT.boundingRect().width() / 2), scenePos.y() - 15 - X2MAX_TEXT.boundingRect().height())
                            X2MAX_TEXT.show()
                else:
                    if scenePos.x() -15 < MATERIAL.x() and scenePos.x() + 15 > MATERIAL.x():
                        path = QtGui.QPainterPath()
                        path.moveTo(MATERIAL.x(), scenePos.y() - 15)
                        path.lineTo(MATERIAL.x(), scenePos.y() + 15)
                        pen = QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.SolidLine)
                        pen.setCosmetic(True)
                        MOUSE_R_CLICK_SECOND = self.scene.addPath(path, pen)
                        if MOUSE_R_CLICK_FLAG == 0:
                            Z1MIN_TEXT.setPlainText("Z1min=0")
                            Z1MIN_TEXT.setPos(scenePos.x() - 15 - Z1MIN_TEXT.boundingRect().width(), scenePos.y() - int(Z1MIN_TEXT.boundingRect().height() / 2))
                            Z1MIN_TEXT.show()
                            Z1MAX_TEXT.setPlainText("Z1max=0")
                            Z1MAX_TEXT.setPos(scenePos.x() + 15, scenePos.y() - int(Z1MAX_TEXT.boundingRect().height() / 2))
                            Z1MAX_TEXT.show()
                            X1MIN_TEXT.setPlainText("X1min=" + str((scenePos.y() + 15) / VIEW_SCALE * -1))
                            X1MIN_TEXT.setPos(scenePos.x() - int(X1MIN_TEXT.boundingRect().width() / 2), scenePos.y() + 15)
                            X1MIN_TEXT.show()
                            X1MAX_TEXT.setPlainText("X1max=" + str((scenePos.y() - 15) / VIEW_SCALE * -1))
                            X1MAX_TEXT.setPos(scenePos.x() - int(X1MAX_TEXT.boundingRect().width() / 2), scenePos.y() - 15 - X1MAX_TEXT.boundingRect().height())
                            X1MAX_TEXT.show()
                        else:
                            Z2MIN_TEXT.setPlainText("Z2min=0")
                            Z2MIN_TEXT.setPos(scenePos.x() - 15 - Z2MIN_TEXT.boundingRect().width(), scenePos.y() - int(Z2MIN_TEXT.boundingRect().height() / 2))
                            Z2MIN_TEXT.show()
                            Z2MAX_TEXT.setPlainText("Z2max=0")
                            Z2MAX_TEXT.setPos(scenePos.x() + 15, scenePos.y() - int(Z2MAX_TEXT.boundingRect().height() / 2))
                            Z2MAX_TEXT.show()
                            X2MIN_TEXT.setPlainText("X2min=" + str((scenePos.y() + 15) / VIEW_SCALE* -1))
                            X2MIN_TEXT.setPos(scenePos.x() - int(X2MIN_TEXT.boundingRect().width() / 2), scenePos.y() + 15)
                            X2MIN_TEXT.show()
                            X2MAX_TEXT.setPlainText("X2max=" + str((scenePos.y() - 15) / VIEW_SCALE* -1))
                            X2MAX_TEXT.setPos(scenePos.x() - int(X2MAX_TEXT.boundingRect().width() / 2), scenePos.y() - 15 - X2MAX_TEXT.boundingRect().height())
                            X2MAX_TEXT.show()
                    elif scenePos.y() -15 < MATERIAL_DIAMETER * VIEW_SCALE and scenePos.y() + 15 > MATERIAL_DIAMETER * VIEW_SCALE:
                        path = QtGui.QPainterPath()
                        path.moveTo(scenePos.x() - 15, MATERIAL_DIAMETER * VIEW_SCALE)
                        path.lineTo(scenePos.x() + 15, MATERIAL_DIAMETER * VIEW_SCALE)
                        pen = QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.SolidLine)
                        pen.setCosmetic(True)
                        MOUSE_R_CLICK_SECOND = self.scene.addPath(path, pen)
                        scenePosX_m_15 = str(RND((scenePos.x() - 15) / VIEW_SCALE - MATERIAL.x() / VIEW_SCALE))
                        scenePosX_p_15 = str(RND((scenePos.x() + 15) / VIEW_SCALE - MATERIAL.x() / VIEW_SCALE))
                        if MOUSE_R_CLICK_FLAG == 0:
                            Z1MIN_TEXT.setPlainText("Z1min=" + scenePosX_m_15)
                            Z1MIN_TEXT.setPos(scenePos.x() - 15 - Z1MIN_TEXT.boundingRect().width(), scenePos.y() - int(Z1MIN_TEXT.boundingRect().height() / 2))
                            Z1MIN_TEXT.show()
                            Z1MAX_TEXT.setPlainText("Z1max=" + scenePosX_p_15)
                            Z1MAX_TEXT.setPos(scenePos.x() + 15, scenePos.y() - int(Z1MAX_TEXT.boundingRect().height() / 2))
                            Z1MAX_TEXT.show()
                            X1MIN_TEXT.setPlainText("X1min=" + str(MATERIAL_DIAMETER * -1))
                            X1MIN_TEXT.setPos(scenePos.x() - int(X1MIN_TEXT.boundingRect().width() / 2), scenePos.y() + 15)
                            X1MIN_TEXT.show()
                            X1MAX_TEXT.setPlainText("X1max=" + str(MATERIAL_DIAMETER * -1))
                            X1MAX_TEXT.setPos(scenePos.x() - int(X1MAX_TEXT.boundingRect().width() / 2), scenePos.y() - 15 - X1MAX_TEXT.boundingRect().height())
                            X1MAX_TEXT.show()
                        else:
                            Z2MIN_TEXT.setPlainText("Z2min=" + scenePosX_m_15)
                            Z2MIN_TEXT.setPos(scenePos.x() - 15 - Z2MIN_TEXT.boundingRect().width(), scenePos.y() - int(Z2MIN_TEXT.boundingRect().height() / 2))
                            Z2MIN_TEXT.show()
                            Z2MAX_TEXT.setPlainText("Z2max=" + scenePosX_p_15)
                            Z2MAX_TEXT.setPos(scenePos.x() + 15, scenePos.y() - int(Z2MAX_TEXT.boundingRect().height() / 2))
                            Z2MAX_TEXT.show()
                            X2MIN_TEXT.setPlainText("X2min=" + str(MATERIAL_DIAMETER * -1))
                            X2MIN_TEXT.setPos(scenePos.x() - int(X2MIN_TEXT.boundingRect().width() / 2), scenePos.y() + 15)
                            X2MIN_TEXT.show()
                            X2MAX_TEXT.setPlainText("X2max=" + str(MATERIAL_DIAMETER * -1))
                            X2MAX_TEXT.setPos(scenePos.x() - int(X2MAX_TEXT.boundingRect().width() / 2), scenePos.y() - 15 - X2MAX_TEXT.boundingRect().height())
                            X2MAX_TEXT.show()
                    elif scenePos.y() -15 < MATERIAL_DIAMETER * VIEW_SCALE * -1 and scenePos.y() + 15 > MATERIAL_DIAMETER * VIEW_SCALE * -1:
                        path = QtGui.QPainterPath()
                        path.moveTo(scenePos.x() - 15, MATERIAL_DIAMETER * VIEW_SCALE * -1)
                        path.lineTo(scenePos.x() + 15, MATERIAL_DIAMETER * VIEW_SCALE * -1)
                        pen = QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.SolidLine)
                        pen.setCosmetic(True)
                        MOUSE_R_CLICK_SECOND = self.scene.addPath(path, pen)
                        scenePosX_m_15 = str(RND((scenePos.x() - 15) / VIEW_SCALE - MATERIAL.x() / VIEW_SCALE))
                        scenePosX_p_15 = str(RND((scenePos.x() + 15) / VIEW_SCALE - MATERIAL.x() / VIEW_SCALE))
                        if MOUSE_R_CLICK_FLAG == 0:
                            Z1MIN_TEXT.setPlainText("Z1min=" + scenePosX_m_15)
                            Z1MIN_TEXT.setPos(scenePos.x() - 15 - Z1MIN_TEXT.boundingRect().width(), scenePos.y() - int(Z1MIN_TEXT.boundingRect().height() / 2))
                            Z1MIN_TEXT.show()
                            Z1MAX_TEXT.setPlainText("Z1max=" + scenePosX_p_15)
                            Z1MAX_TEXT.setPos(scenePos.x() + 15, scenePos.y() - int(Z1MAX_TEXT.boundingRect().height() / 2))
                            Z1MAX_TEXT.show()
                            X1MIN_TEXT.setPlainText("X1min=" + str(MATERIAL_DIAMETER)) # * -1 *-1
                            X1MIN_TEXT.setPos(scenePos.x() - int(X1MIN_TEXT.boundingRect().width() / 2), scenePos.y() + 15)
                            X1MIN_TEXT.show()
                            X1MAX_TEXT.setPlainText("X1max=" + str(MATERIAL_DIAMETER)) # * -1 *-1
                            X1MAX_TEXT.setPos(scenePos.x() - int(X1MAX_TEXT.boundingRect().width() / 2), scenePos.y() - 15 - X1MAX_TEXT.boundingRect().height())
                            X1MAX_TEXT.show()
                        else:
                            Z2MIN_TEXT.setPlainText("Z2min=" + scenePosX_m_15)
                            Z2MIN_TEXT.setPos(scenePos.x() - 15 - Z2MIN_TEXT.boundingRect().width(), scenePos.y() - int(Z2MIN_TEXT.boundingRect().height() / 2))
                            Z2MIN_TEXT.show()
                            Z2MAX_TEXT.setPlainText("Z2max=" + scenePosX_p_15)
                            Z2MAX_TEXT.setPos(scenePos.x() + 15, scenePos.y() - int(Z2MAX_TEXT.boundingRect().height() / 2))
                            Z2MAX_TEXT.show()
                            X2MIN_TEXT.setPlainText("X2min=" + str(MATERIAL_DIAMETER)) # * -1 *-1
                            X2MIN_TEXT.setPos(scenePos.x() - int(X2MIN_TEXT.boundingRect().width() / 2), scenePos.y() + 15)
                            X2MIN_TEXT.show()
                            X2MAX_TEXT.setPlainText("X2max=" + str(MATERIAL_DIAMETER )) # * -1 *-1
                            X2MAX_TEXT.setPos(scenePos.x() - int(X2MAX_TEXT.boundingRect().width() / 2), scenePos.y() - 15 - X2MAX_TEXT.boundingRect().height())
                            X2MAX_TEXT.show()
                BUTTON_FLAG = 2
    
        #graphicsView1.viewport()上でボタンがリリースされた場合の処理
        elif (event.type() == QtGui.QMouseEvent.MouseButtonRelease and obj is self.ui.graphicsView1.viewport()):
            if event.button() == QtCore.Qt.LeftButton:
                BUTTON_FLAG = 0
                SELECTED_ITEM = None
            elif event.button() == QtCore.Qt.RightButton and FLAG_END == 1:
                scenePos =self.ui.graphicsView1.mapToScene(event.position().x(), event.position().y())
                BUTTON_FLAG = 0
                xyListX = []
                xyListY = []
                for i in self.scene.collidingItems(MOUSE_R_CLICK_FIRST, QtCore.Qt.ItemSelectionMode.IntersectsItemShape):
                    tmp = i.shape().toFillPolygon().toList()
                    for l in tmp:
                        inPos = QtCore.QPointF(l.x() - MOUSE_R_CLICK_FIRST.x() + MATERIAL.x(), l.y() - MOUSE_R_CLICK_FIRST.y())
                        if MOUSE_R_CLICK_FIRST.contains(inPos):
                            pX = l.x()
                            pY = l.y()
                            if "999999999999" in str(pX):
                                pX = pX + 0.001
                                pX = str(pX)
                                sp = pX.split(".")
                                lp = sp[1]
                                lp = lp[:3]
                                pX = float(sp[0] + "." + lp)
                            elif "000000000001" in str(pX):
                                pX = str(pX)
                                sp = pX.split(".")
                                lp = sp[1]
                                lp = lp[:3]
                                pX = float(sp[0] + "." + lp)
                            if "999999999999" in str(pY):
                                pY = pY + 0.001
                                pY = str(pY)
                                sp = pY.split(".")
                                lp = sp[1]
                                lp = lp[:3]
                                pY = float(sp[0] + "." + lp)
                            elif "000000000001" in str(pY):
                                pY = str(pY)
                                sp = pY.split(".")
                                lp = sp[1]
                                lp = lp[:3]
                                pY = float(sp[0] + "." + lp)

                            stX = str(pX)
                            stY = str(pY)
                            tmpX = stX.split(".")
                            stX = tmpX[1]
                            tmpY = stY.split(".")
                            stY = tmpY[1]
                            stX = stX.replace('-', "")
                            stX = stX.replace('+', "")
                            stY = stY.replace('-', "")
                            stY = stY.replace('+', "")
                            pX = RND(pX / VIEW_SCALE)
                            pY = RND(pY / VIEW_SCALE)
                            if len(stX) < 4:
                                #xList.append(pX)
                                xyListX.append(pX)
                                xyListY.append(pY)
                            if len(stY) < 4:
                                #yList.append(pY)
                                xyListX.append(pX)
                                xyListY.append(pY)
                cX = collections.Counter(xyListX)
                cY = collections.Counter(xyListY)
                if len(cX) > 0 and len(cY)> 0:
                    maxKeyX = max(cX.items(), key=operator.itemgetter(1))[0]
                    cXnum = cX[maxKeyX]
                    maxKeyY = max(cY.items(), key=operator.itemgetter(1))[0]
                    cYnum = cY[maxKeyY]
                    if cXnum > cYnum:
                        idx = -1
                        result = []
                        for cnt in range(xyListX.count(maxKeyX)):
                            idx = xyListX.index(maxKeyX, idx+1)
                            result.append(idx)
                        searchList = []
                        for x in result:
                            searchList.append(xyListY[x])
                        self.scene.removeItem(MOUSE_R_CLICK_SECOND)
                        MOUSE_R_CLICK_SECOND = ""
                        path = QtGui.QPainterPath()
                        path.moveTo(maxKeyX * VIEW_SCALE + MATERIAL.x(), max(searchList) * VIEW_SCALE)
                        path.lineTo(maxKeyX * VIEW_SCALE + MATERIAL.x(), min(searchList) * VIEW_SCALE)
                        pen = QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.SolidLine)
                        pen.setCosmetic(True)
                        MOUSE_R_CLICK_SECOND = self.scene.addPath(path, pen)
                        rev_max_x = min(searchList) * -1
                        rev_min_x = max(searchList) * -1
                        if MOUSE_R_CLICK_FLAG == 0:
                            MOUSE_R_CLICK_FLAG = 1
                            cursor = self.ui.plainTextEdit1.textCursor()
                            cursor.movePosition(QtGui.QTextCursor.End)
                            cursor.insertText("Z1min and Z1max=" + str(maxKeyX) + "\r\n")
                            cursor.insertText("X1min=" + str(rev_min_x) + " X1max=" + str(rev_max_x) + "\r\n\r\n")
                            self.ui.plainTextEdit1.setTextCursor(cursor)
                            EX_PATH = path
                            EX_MOUSE_R_CLICK_FIRST_X = MOUSE_R_CLICK_FIRST.x()
                            EX_MOUSE_R_CLICK_FIRST_Y = MOUSE_R_CLICK_FIRST.y()
                            EX_MAX_Z = maxKeyX
                            EX_MIN_Z = maxKeyX
                            EX_MAX_X = rev_max_x
                            EX_MIN_X = rev_min_x
                            Z1MIN_TEXT.setPlainText("Z1min=" + str(EX_MIN_Z))
                            Z1MIN_TEXT.setPos(scenePos.x() - 15 - Z1MIN_TEXT.boundingRect().width(), scenePos.y() - int(Z1MIN_TEXT.boundingRect().height() / 2))
                            Z1MIN_TEXT.show()
                            Z1MAX_TEXT.setPlainText("Z1max=" + str(EX_MAX_Z))
                            Z1MAX_TEXT.setPos(scenePos.x() + 15, scenePos.y() - int(Z1MAX_TEXT.boundingRect().height() / 2))
                            Z1MAX_TEXT.show()
                            X1MIN_TEXT.setPlainText("X1min=" + str(EX_MIN_X))
                            X1MIN_TEXT.setPos(scenePos.x() - int(X1MIN_TEXT.boundingRect().width() / 2), scenePos.y() + 15)
                            X1MIN_TEXT.show()
                            X1MAX_TEXT.setPlainText("X1max=" + str(EX_MAX_X))
                            X1MAX_TEXT.setPos(scenePos.x() - int(X1MAX_TEXT.boundingRect().width() / 2), scenePos.y() - 15 - X1MAX_TEXT.boundingRect().height())
                            X1MAX_TEXT.show()
                        else:
                            MOUSE_R_CLICK_FLAG = 0
                            z_length_min_min = RND(abs(EX_MIN_Z - maxKeyX))
                            z_length_min_max = RND(abs(EX_MIN_Z - maxKeyX))
                            z_length_max_min = RND(abs(EX_MAX_Z - maxKeyX))
                            z_length_max_max = RND(abs(EX_MAX_Z - maxKeyX))
                            x_length_min_min = RND(abs(EX_MIN_X - rev_min_x))
                            x_length_min_max = RND(abs(EX_MIN_X - rev_max_x))
                            x_length_max_min = RND(abs(EX_MAX_X - rev_min_x))
                            x_length_max_max = RND(abs(EX_MAX_X - rev_max_x))
                            Z2MIN_TEXT.setPlainText("Z2min=" + str(maxKeyX))
                            Z2MIN_TEXT.setPos(scenePos.x() - 15 - Z2MIN_TEXT.boundingRect().width(), scenePos.y() - int(Z2MIN_TEXT.boundingRect().height() / 2))
                            Z2MIN_TEXT.show()
                            Z2MAX_TEXT.setPlainText("Z2max=" + str(maxKeyX))
                            Z2MAX_TEXT.setPos(scenePos.x() + 15, scenePos.y() - int(Z2MAX_TEXT.boundingRect().height() / 2))
                            Z2MAX_TEXT.show()
                            X2MIN_TEXT.setPlainText("X2min=" + str(rev_min_x))
                            X2MIN_TEXT.setPos(scenePos.x() - int(X2MIN_TEXT.boundingRect().width() / 2), scenePos.y() + 15)
                            X2MIN_TEXT.show()
                            X2MAX_TEXT.setPlainText("X2max=" + str(rev_max_x))
                            X2MAX_TEXT.setPos(scenePos.x() - int(X2MAX_TEXT.boundingRect().width() / 2), scenePos.y() - 15 - X2MAX_TEXT.boundingRect().height())
                            X2MAX_TEXT.show()
                            cursor = self.ui.plainTextEdit1.textCursor()
                            cursor.movePosition(QtGui.QTextCursor.End)
                            cursor.insertText("Z2min and Z2max=" + str(maxKeyX) + "\r\n")
                            cursor.insertText("X2min =" + str(rev_min_x) + " X2max =" + str(rev_max_x) + "\r\n\r\n")
                            cursor.insertText("Z1min to Z2min=" + str(z_length_min_min) + "\r\n")
                            cursor.insertText("Z1min to Z2max=" + str(z_length_min_max) + "\r\n")
                            cursor.insertText("Z1max to Z2min=" + str(z_length_max_min) + "\r\n")
                            cursor.insertText("Z1max to Z2max=" + str(z_length_max_max) + "\r\n\r\n")
                            cursor.insertText("X1min to X2min=" + str(x_length_min_min) + "\r\n")
                            cursor.insertText("X1min to X2max=" + str(x_length_min_max) + "\r\n")
                            cursor.insertText("X1max to X2min=" + str(x_length_max_min) + "\r\n")
                            cursor.insertText("X1max to X2max=" + str(x_length_max_max) + "\r\n\r\n")
                            self.ui.plainTextEdit1.setTextCursor(cursor)
                    elif cXnum < cYnum:
                        idx = -1
                        result = []
                        for cnt in range(xyListY.count(maxKeyY)):
                            idx = xyListY.index(maxKeyY, idx+1)
                            result.append(idx)
                        searchList = []
                        for x in result:
                            searchList.append(xyListX[x])
                        self.scene.removeItem(MOUSE_R_CLICK_SECOND)
                        MOUSE_R_CLICK_SECOND = ""
                        path = QtGui.QPainterPath()
                        path.moveTo(max(searchList) * VIEW_SCALE + MATERIAL.x(), maxKeyY * VIEW_SCALE)
                        path.lineTo(min(searchList) * VIEW_SCALE + MATERIAL.x(), maxKeyY * VIEW_SCALE)
                        pen = QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.SolidLine)
                        pen.setCosmetic(True)
                        MOUSE_R_CLICK_SECOND = self.scene.addPath(path, pen)
                        if MOUSE_R_CLICK_FLAG == 0:
                            MOUSE_R_CLICK_FLAG = 1
                            cursor = self.ui.plainTextEdit1.textCursor()
                            cursor.movePosition(QtGui.QTextCursor.End)
                            cursor.insertText("Z1min=" + str(min(searchList)) + " Z1max=" + str(max(searchList)) + "\r\n")
                            cursor.insertText("X1min and X1max=" + str(maxKeyY * -1) + "\r\n\r\n")
                            self.ui.plainTextEdit1.setTextCursor(cursor)
                            EX_PATH = path
                            EX_MOUSE_R_CLICK_FIRST_X = MOUSE_R_CLICK_FIRST.x()
                            EX_MOUSE_R_CLICK_FIRST_Y = MOUSE_R_CLICK_FIRST.y()
                            EX_MAX_Z = max(searchList)
                            EX_MIN_Z = min(searchList)
                            EX_MAX_X = maxKeyY * -1
                            EX_MIN_X = maxKeyY * -1
                            Z1MIN_TEXT.setPlainText("Z1min=" + str(EX_MIN_Z))
                            Z1MIN_TEXT.setPos(scenePos.x() - 15 - Z1MIN_TEXT.boundingRect().width(), scenePos.y() - int(Z1MIN_TEXT.boundingRect().height() / 2))
                            Z1MIN_TEXT.show()
                            Z1MAX_TEXT.setPlainText("Z1max=" + str(EX_MAX_Z))
                            Z1MAX_TEXT.setPos(scenePos.x() + 15, scenePos.y() - int(Z1MAX_TEXT.boundingRect().height() / 2))
                            Z1MAX_TEXT.show()
                            X1MIN_TEXT.setPlainText("X1min=" + str(EX_MIN_X))
                            X1MIN_TEXT.setPos(scenePos.x() - int(X1MIN_TEXT.boundingRect().width() / 2), scenePos.y() + 15)
                            X1MIN_TEXT.show()
                            X1MAX_TEXT.setPlainText("X1max=" + str(EX_MAX_X))
                            X1MAX_TEXT.setPos(scenePos.x() - int(X1MAX_TEXT.boundingRect().width() / 2), scenePos.y() - 15 - X1MAX_TEXT.boundingRect().height())
                            X1MAX_TEXT.show()
                        else:
                            MOUSE_R_CLICK_FLAG = 0
                            z_length_min_min = RND(abs(EX_MIN_Z - min(searchList)))
                            z_length_min_max = RND(abs(EX_MIN_Z - max(searchList)))
                            z_length_max_min = RND(abs(EX_MAX_Z - min(searchList)))
                            z_length_max_max = RND(abs(EX_MAX_Z - max(searchList)))
                            x_length_min_min = RND(abs(EX_MIN_X - maxKeyY * -1))
                            x_length_min_max = RND(abs(EX_MIN_X - maxKeyY * -1))
                            x_length_max_min = RND(abs(EX_MAX_X - maxKeyY * -1))
                            x_length_max_max = RND(abs(EX_MAX_X - maxKeyY * -1))
                            Z2MIN_TEXT.setPlainText("Z2min=" + str(min(searchList)))
                            Z2MIN_TEXT.setPos(scenePos.x() - 15 - Z2MIN_TEXT.boundingRect().width(), scenePos.y() - int(Z2MIN_TEXT.boundingRect().height() / 2))
                            Z2MIN_TEXT.show()
                            Z2MAX_TEXT.setPlainText("Z2max=" + str(max(searchList)))
                            Z2MAX_TEXT.setPos(scenePos.x() + 15, scenePos.y() - int(Z2MAX_TEXT.boundingRect().height() / 2))
                            Z2MAX_TEXT.show()
                            X2MIN_TEXT.setPlainText("X2min=" + str(maxKeyY * -1))
                            X2MIN_TEXT.setPos(scenePos.x() - int(X2MIN_TEXT.boundingRect().width() / 2), scenePos.y() + 15)
                            X2MIN_TEXT.show()
                            X2MAX_TEXT.setPlainText("X2max=" + str(maxKeyY * -1))
                            X2MAX_TEXT.setPos(scenePos.x() - int(X2MAX_TEXT.boundingRect().width() / 2), scenePos.y() - 15 - X2MAX_TEXT.boundingRect().height())
                            X2MAX_TEXT.show()
                            cursor = self.ui.plainTextEdit1.textCursor()
                            cursor.movePosition(QtGui.QTextCursor.End)
                            cursor.insertText("Z2min =" + str(min(searchList)) + " Z2max=" + str(max(searchList)) + "\r\n")
                            cursor.insertText("X2min and X2max=" + str(maxKeyY *-1) + "\r\n\r\n")
                            cursor.insertText("Z1min to Z2min=" + str(z_length_min_min) + "\r\n")
                            cursor.insertText("Z1min to Z2max=" + str(z_length_min_max) + "\r\n")
                            cursor.insertText("Z1max to Z2min=" + str(z_length_max_min) + "\r\n")
                            cursor.insertText("Z1max to Z2max=" + str(z_length_max_max) + "\r\n\r\n")
                            cursor.insertText("X1min to X2min=" + str(x_length_min_min) + "\r\n")
                            cursor.insertText("X1min to X2max=" + str(x_length_min_max) + "\r\n")
                            cursor.insertText("X1max to X2min=" + str(x_length_max_min) + "\r\n")
                            cursor.insertText("X1max to X2max=" + str(x_length_max_max) + "\r\n\r\n")
                            self.ui.plainTextEdit1.setTextCursor(cursor)
                    else:
                        if MOUSE_R_CLICK_FLAG == 0:
                            MOUSE_R_CLICK_FIRST.hide()
                            if MOUSE_R_CLICK_SECOND != "":
                                self.scene.removeItem(MOUSE_R_CLICK_SECOND)
                        else:
                            MOUSE_R_CLICK_FIRST.hide()
                            if MOUSE_R_CLICK_SECOND != "":
                                self.scene.removeItem(MOUSE_R_CLICK_SECOND)
                                MOUSE_R_CLICK_SECOND = ""
                            EX_MOUSE_R_CLICK_FIRST.hide()
                            if EX_MOUSE_R_CLICK_SECOND != "":
                                self.scene.removeItem(EX_MOUSE_R_CLICK_SECOND)
                                EX_MOUSE_R_CLICK_SECOND = ""
                            MOUSE_R_CLICK_FLAG = 0
                            Z1MIN_TEXT.hide()
                            Z1MAX_TEXT.hide()
                            X1MIN_TEXT.hide()
                            X1MAX_TEXT.hide()
                            Z2MIN_TEXT.hide()
                            Z2MAX_TEXT.hide()
                            X2MIN_TEXT.hide()
                            X2MAX_TEXT.hide()
                else:
                    if scenePos.x() -15 < MATERIAL.x() and scenePos.x() + 15 > MATERIAL.x():
                        self.scene.removeItem(MOUSE_R_CLICK_SECOND)
                        MOUSE_R_CLICK_SECOND = ""
                        path = QtGui.QPainterPath()
                        path.moveTo(MATERIAL.x(), scenePos.y() - 15)
                        path.lineTo(MATERIAL.x(), scenePos.y() + 15)
                        pen = QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.SolidLine)
                        pen.setCosmetic(True)
                        MOUSE_R_CLICK_SECOND = self.scene.addPath(path, pen)
                        rev_max_x = RND((scenePos.y() - 15) / VIEW_SCALE) * -1
                        rev_min_x = RND((scenePos.y() + 15) / VIEW_SCALE) * -1
                        if MOUSE_R_CLICK_FLAG == 0:
                            MOUSE_R_CLICK_FLAG = 1
                            cursor = self.ui.plainTextEdit1.textCursor()
                            cursor.movePosition(QtGui.QTextCursor.End)
                            cursor.insertText("Z1min and Z1max=0\r\n")
                            cursor.insertText("X1min=" + str(rev_min_x) + " X1max=" + str(rev_max_x) + "\r\n\r\n")
                            self.ui.plainTextEdit1.setTextCursor(cursor)
                            EX_PATH = path
                            EX_MOUSE_R_CLICK_FIRST_X = MOUSE_R_CLICK_FIRST.x()
                            EX_MOUSE_R_CLICK_FIRST_Y = MOUSE_R_CLICK_FIRST.y()
                            EX_MAX_Z = 0
                            EX_MIN_Z = 0
                            EX_MAX_X = rev_max_x
                            EX_MIN_X = rev_min_x
                            Z1MIN_TEXT.setPlainText("Z1min=" + str(EX_MIN_Z))
                            Z1MIN_TEXT.setPos(scenePos.x() - 15 - Z1MIN_TEXT.boundingRect().width(), scenePos.y() - int(Z1MIN_TEXT.boundingRect().height() / 2))
                            Z1MIN_TEXT.show()
                            Z1MAX_TEXT.setPlainText("Z1max=" + str(EX_MAX_Z))
                            Z1MAX_TEXT.setPos(scenePos.x() + 15, scenePos.y() - int(Z1MAX_TEXT.boundingRect().height() / 2))
                            Z1MAX_TEXT.show()
                            X1MIN_TEXT.setPlainText("X1min=" + str(EX_MIN_X))
                            X1MIN_TEXT.setPos(scenePos.x() - int(X1MIN_TEXT.boundingRect().width() / 2), scenePos.y() + 15)
                            X1MIN_TEXT.show()
                            X1MAX_TEXT.setPlainText("X1max=" + str(EX_MAX_X))
                            X1MAX_TEXT.setPos(scenePos.x() - int(X1MAX_TEXT.boundingRect().width() / 2), scenePos.y() - 15 - X1MAX_TEXT.boundingRect().height())
                            X1MAX_TEXT.show()
                        else:
                            MOUSE_R_CLICK_FLAG = 0
                            z_length_min_min = RND(abs(EX_MIN_Z - 0))
                            z_length_min_max = RND(abs(EX_MIN_Z - 0))
                            z_length_max_min = RND(abs(EX_MAX_Z - 0))
                            z_length_max_max = RND(abs(EX_MAX_Z - 0))
                            x_length_min_min = RND(abs(EX_MIN_X - rev_min_x))
                            x_length_min_max = RND(abs(EX_MIN_X - rev_max_x))
                            x_length_max_min = RND(abs(EX_MAX_X - rev_min_x))
                            x_length_max_max = RND(abs(EX_MAX_X - rev_max_x))
                            Z2MIN_TEXT.setPlainText("Z2min=" + str("0"))
                            Z2MIN_TEXT.setPos(scenePos.x() - 15 - Z2MIN_TEXT.boundingRect().width(), scenePos.y() - int(Z2MIN_TEXT.boundingRect().height() / 2))
                            Z2MIN_TEXT.show()
                            Z2MAX_TEXT.setPlainText("Z2max=" + str("0"))
                            Z2MAX_TEXT.setPos(scenePos.x() + 15, scenePos.y() - int(Z2MAX_TEXT.boundingRect().height() / 2))
                            Z2MAX_TEXT.show()
                            X2MIN_TEXT.setPlainText("X2min=" + str(rev_min_x))
                            X2MIN_TEXT.setPos(scenePos.x() - int(X2MIN_TEXT.boundingRect().width() / 2), scenePos.y() + 15)
                            X2MIN_TEXT.show()
                            X2MAX_TEXT.setPlainText("X2max=" + str(rev_max_x))
                            X2MAX_TEXT.setPos(scenePos.x() - int(X2MAX_TEXT.boundingRect().width() / 2), scenePos.y() - 15 - X2MAX_TEXT.boundingRect().height())
                            X2MAX_TEXT.show()
                            cursor = self.ui.plainTextEdit1.textCursor()
                            cursor.movePosition(QtGui.QTextCursor.End)
                            cursor.insertText("Z2min and Z2max=0\r\n")
                            cursor.insertText("X2min =" + str(rev_min_x) + " X2max=" + str(rev_max_x) + "\r\n\r\n")
                            cursor.insertText("Z1min to Z2min=" + str(z_length_min_min) + "\r\n")
                            cursor.insertText("Z1min to Z2max=" + str(z_length_min_max) + "\r\n")
                            cursor.insertText("Z1max to Z2min=" + str(z_length_max_min) + "\r\n")
                            cursor.insertText("Z1max to Z2max=" + str(z_length_max_max) + "\r\n\r\n")
                            cursor.insertText("X1min to X2min=" + str(x_length_min_min) + "\r\n")
                            cursor.insertText("X1min to X2max=" + str(x_length_min_max) + "\r\n")
                            cursor.insertText("X1max to X2min=" + str(x_length_max_min) + "\r\n")
                            cursor.insertText("X1max to X2max=" + str(x_length_max_max) + "\r\n\r\n")
                            self.ui.plainTextEdit1.setTextCursor(cursor)
                    elif scenePos.y() -15 < MATERIAL_DIAMETER * VIEW_SCALE and scenePos.y() + 15 > MATERIAL_DIAMETER * VIEW_SCALE:
                        self.scene.removeItem(MOUSE_R_CLICK_SECOND)
                        MOUSE_R_CLICK_SECOND = ""
                        path = QtGui.QPainterPath()
                        path.moveTo(scenePos.x() - 15, MATERIAL_DIAMETER * VIEW_SCALE)
                        path.lineTo(scenePos.x() + 15, MATERIAL_DIAMETER * VIEW_SCALE)
                        pen = QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.SolidLine)
                        pen.setCosmetic(True)
                        MOUSE_R_CLICK_SECOND = self.scene.addPath(path, pen)
                        realX_min = RND((scenePos.x() - 15) / VIEW_SCALE -  MATERIAL.x() / VIEW_SCALE)
                        realX_max = RND((scenePos.x() + 15) / VIEW_SCALE - MATERIAL.x() / VIEW_SCALE)
                        calc_diameter = RND(MATERIAL_DIAMETER * -1)
                        if MOUSE_R_CLICK_FLAG == 0:
                            MOUSE_R_CLICK_FLAG = 1
                            cursor = self.ui.plainTextEdit1.textCursor()
                            cursor.movePosition(QtGui.QTextCursor.End)
                            cursor.insertText("Z1min=" + str(realX_min) + " Z1max=" + str(realX_max) + "\r\n")
                            cursor.insertText("X1min and X1 max=" + str(calc_diameter) + "\r\n\r\n")
                            self.ui.plainTextEdit1.setTextCursor(cursor)
                            EX_PATH = path
                            EX_MOUSE_R_CLICK_FIRST_X = MOUSE_R_CLICK_FIRST.x()
                            EX_MOUSE_R_CLICK_FIRST_Y = MOUSE_R_CLICK_FIRST.y()
                            EX_MAX_Z = realX_max
                            EX_MIN_Z = realX_min
                            EX_MAX_X = MATERIAL_DIAMETER * -1
                            EX_MIN_X = MATERIAL_DIAMETER * -1
                            Z1MIN_TEXT.setPlainText("Z1min=" + str(EX_MIN_Z))
                            Z1MIN_TEXT.setPos(scenePos.x() - 15 - Z1MIN_TEXT.boundingRect().width(), scenePos.y() - int(Z1MIN_TEXT.boundingRect().height() / 2))
                            Z1MIN_TEXT.show()
                            Z1MAX_TEXT.setPlainText("Z1max=" + str(EX_MAX_Z))
                            Z1MAX_TEXT.setPos(scenePos.x() + 15, scenePos.y() - int(Z1MAX_TEXT.boundingRect().height() / 2))
                            Z1MAX_TEXT.show()
                            X1MIN_TEXT.setPlainText("X1min=" + str(EX_MIN_X))
                            X1MIN_TEXT.setPos(scenePos.x() - int(X1MIN_TEXT.boundingRect().width() / 2), scenePos.y() + 15)
                            X1MIN_TEXT.show()
                            X1MAX_TEXT.setPlainText("X1max=" + str(EX_MAX_X))
                            X1MAX_TEXT.setPos(scenePos.x() - int(X1MAX_TEXT.boundingRect().width() / 2), scenePos.y() - 15 - X1MAX_TEXT.boundingRect().height())
                            X1MAX_TEXT.show()
                        else:
                            MOUSE_R_CLICK_FLAG = 0
                            z_length_min_min = RND(abs(EX_MIN_Z - realX_min))
                            z_length_min_max = RND(abs(EX_MIN_Z - realX_max))
                            z_length_max_min = RND(abs(EX_MAX_Z - realX_min))
                            z_length_max_max = RND(abs(EX_MAX_Z - realX_max))
                            x_length_min_min = RND(abs(EX_MIN_X - MATERIAL_DIAMETER * -1))
                            x_length_min_max = RND(abs(EX_MIN_X - MATERIAL_DIAMETER * -1))
                            x_length_max_min = RND(abs(EX_MAX_X - MATERIAL_DIAMETER * -1))
                            x_length_max_max = RND(abs(EX_MAX_X - MATERIAL_DIAMETER * -1))
                            Z2MIN_TEXT.setPlainText("Z2min=" + str(realX_min))
                            Z2MIN_TEXT.setPos(scenePos.x() - 15 - Z2MIN_TEXT.boundingRect().width(), scenePos.y() - int(Z2MIN_TEXT.boundingRect().height() / 2))
                            Z2MIN_TEXT.show()
                            Z2MAX_TEXT.setPlainText("Z2max=" + str(realX_min))
                            Z2MAX_TEXT.setPos(scenePos.x() + 15, scenePos.y() - int(Z2MAX_TEXT.boundingRect().height() / 2))
                            Z2MAX_TEXT.show()
                            X2MIN_TEXT.setPlainText("X2min=" + str(MATERIAL_DIAMETER * -1))
                            X2MIN_TEXT.setPos(scenePos.x() - int(X2MIN_TEXT.boundingRect().width() / 2), scenePos.y() + 15)
                            X2MIN_TEXT.show()
                            X2MAX_TEXT.setPlainText("X2max=" + str(MATERIAL_DIAMETER * -1))
                            X2MAX_TEXT.setPos(scenePos.x() - int(X2MAX_TEXT.boundingRect().width() / 2), scenePos.y() - 15 - X2MAX_TEXT.boundingRect().height())
                            X2MAX_TEXT.show()
                            cursor = self.ui.plainTextEdit1.textCursor()
                            cursor.movePosition(QtGui.QTextCursor.End)
                            cursor.insertText("Z2min=" + str(realX_min) + " Z2 max=" + str(realX_max) + "\r\n")
                            cursor.insertText("X2min and X2max=" + str(MATERIAL_DIAMETER *-1) + "\r\n\r\n")
                            cursor.insertText("Z1min to Z2min=" + str(z_length_min_min) + "\r\n")
                            cursor.insertText("Z1min to Z2max=" + str(z_length_min_max) + "\r\n")
                            cursor.insertText("Z1max to Z2min=" + str(z_length_max_min) + "\r\n")
                            cursor.insertText("Z1max to Z2max=" + str(z_length_max_max) + "\r\n\r\n")
                            cursor.insertText("X1min to X2min=" + str(x_length_min_min) + "\r\n")
                            cursor.insertText("X1min to X2max=" + str(x_length_min_max) + "\r\n")
                            cursor.insertText("X1max to X2min=" + str(x_length_max_min) + "\r\n")
                            cursor.insertText("X1max to X2max=" + str(x_length_max_max) + "\r\n\r\n")
                            self.ui.plainTextEdit1.setTextCursor(cursor)
                    elif scenePos.y() -15 < MATERIAL_DIAMETER * VIEW_SCALE * -1 and scenePos.y() + 15 > MATERIAL_DIAMETER * VIEW_SCALE * -1:
                        self.scene.removeItem(MOUSE_R_CLICK_SECOND)
                        MOUSE_R_CLICK_SECOND = ""
                        path = QtGui.QPainterPath()
                        path.moveTo(scenePos.x() - 15, MATERIAL_DIAMETER * VIEW_SCALE * -1)
                        path.lineTo(scenePos.x() + 15, MATERIAL_DIAMETER * VIEW_SCALE * -1)
                        pen = QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.SolidLine)
                        pen.setCosmetic(True)
                        MOUSE_R_CLICK_SECOND = self.scene.addPath(path, pen)
                        realX_min = RND(((scenePos.x() - 15) / VIEW_SCALE - MATERIAL.x() / VIEW_SCALE))
                        realX_max = RND(((scenePos.x() + 15) / VIEW_SCALE - MATERIAL.x() / VIEW_SCALE))
                        calc_diameter = RND(MATERIAL_DIAMETER) # *-1 *-1
                        if MOUSE_R_CLICK_FLAG == 0:
                            MOUSE_R_CLICK_FLAG = 1
                            cursor = self.ui.plainTextEdit1.textCursor()
                            cursor.movePosition(QtGui.QTextCursor.End)
                            cursor.insertText("Z1min=" + str(realX_min) + " Z1max=" + str(realX_max) + "\r\n")
                            cursor.insertText("X1min and X1max=" + str(calc_diameter) + "\r\n\r\n")
                            self.ui.plainTextEdit1.setTextCursor(cursor)
                            EX_PATH = path
                            EX_MOUSE_R_CLICK_FIRST_X = MOUSE_R_CLICK_FIRST.x()
                            EX_MOUSE_R_CLICK_FIRST_Y = MOUSE_R_CLICK_FIRST.y()
                            EX_MAX_Z = realX_max
                            EX_MIN_Z = realX_min
                            EX_MAX_X = MATERIAL_DIAMETER # *-1 *-1
                            EX_MIN_X = MATERIAL_DIAMETER # *-1 *-1
                            Z1MIN_TEXT.setPlainText("Z1min=" + str(EX_MIN_Z))
                            Z1MIN_TEXT.setPos(scenePos.x() - 15 - Z1MIN_TEXT.boundingRect().width(), scenePos.y() - int(Z1MIN_TEXT.boundingRect().height() / 2))
                            Z1MIN_TEXT.show()
                            Z1MAX_TEXT.setPlainText("Z1max=" + str(EX_MAX_Z))
                            Z1MAX_TEXT.setPos(scenePos.x() + 15, scenePos.y() - int(Z1MAX_TEXT.boundingRect().height() / 2))
                            Z1MAX_TEXT.show()
                            X1MIN_TEXT.setPlainText("X1min=" + str(EX_MIN_X))
                            X1MIN_TEXT.setPos(scenePos.x() - int(X1MIN_TEXT.boundingRect().width() / 2), scenePos.y() + 15)
                            X1MIN_TEXT.show()
                            X1MAX_TEXT.setPlainText("X1max=" + str(EX_MAX_X))
                            X1MAX_TEXT.setPos(scenePos.x() - int(X1MAX_TEXT.boundingRect().width() / 2), scenePos.y() - 15 - X1MAX_TEXT.boundingRect().height())
                            X1MAX_TEXT.show()
                        else:
                            MOUSE_R_CLICK_FLAG = 0
                            z_length_min_min = RND(abs(EX_MIN_Z - realX_min))
                            z_length_min_max = RND(abs(EX_MIN_Z - realX_max))
                            z_length_max_min = RND(abs(EX_MAX_Z - realX_min))
                            z_length_max_max = RND(abs(EX_MAX_Z - realX_max))
                            x_length_min_min = RND(abs(EX_MIN_X - MATERIAL_DIAMETER)) # *-1 *-1
                            x_length_min_max = RND(abs(EX_MIN_X - MATERIAL_DIAMETER)) # *-1 *-1
                            x_length_max_min = RND(abs(EX_MAX_X - MATERIAL_DIAMETER)) # *-1 *-1
                            x_length_max_max = RND(abs(EX_MAX_X - MATERIAL_DIAMETER)) # *-1 *-1
                            Z2MIN_TEXT.setPlainText("Z2min=" + str(realX_min))
                            Z2MIN_TEXT.setPos(scenePos.x() - 15 - Z2MIN_TEXT.boundingRect().width(), scenePos.y() - int(Z2MIN_TEXT.boundingRect().height() / 2))
                            Z2MIN_TEXT.show()
                            Z2MAX_TEXT.setPlainText("Z2max=" + str(realX_min))
                            Z2MAX_TEXT.setPos(scenePos.x() + 15, scenePos.y() - int(Z2MAX_TEXT.boundingRect().height() / 2))
                            Z2MAX_TEXT.show()
                            X2MIN_TEXT.setPlainText("X2min=" + str(MATERIAL_DIAMETER)) # *-1 *-1
                            X2MIN_TEXT.setPos(scenePos.x() - int(X2MIN_TEXT.boundingRect().width() / 2), scenePos.y() + 15)
                            X2MIN_TEXT.show()
                            X2MAX_TEXT.setPlainText("X2max=" + str(MATERIAL_DIAMETER)) # *-1 *-1
                            X2MAX_TEXT.setPos(scenePos.x() - int(X2MAX_TEXT.boundingRect().width() / 2), scenePos.y() - 15 - X2MAX_TEXT.boundingRect().height())
                            X2MAX_TEXT.show()
                            cursor = self.ui.plainTextEdit1.textCursor()
                            cursor.movePosition(QtGui.QTextCursor.End)
                            cursor.insertText("Z2min=" + str(realX_min) + " Z2max=" + str(realX_max) + "\r\n")
                            cursor.insertText("X2min and X2max=" + str(MATERIAL_DIAMETER * -1 * -1) + "\r\n\r\n")
                            cursor.insertText("Z1min to Z2min=" + str(z_length_min_min) + "\r\n")
                            cursor.insertText("Z1min to Z2max=" + str(z_length_min_max) + "\r\n")
                            cursor.insertText("Z1max to Z2min=" + str(z_length_max_min) + "\r\n")
                            cursor.insertText("Z1max to Z2max=" + str(z_length_max_max) + "\r\n\r\n")
                            cursor.insertText("X1min to X2min=" + str(x_length_min_min) + "\r\n")
                            cursor.insertText("X1min to X2max=" + str(x_length_min_max) + "\r\n")
                            cursor.insertText("X1max to X2min=" + str(x_length_max_min) + "\r\n")
                            cursor.insertText("X1max to X2max=" + str(x_length_max_max) + "\r\n\r\n")
                            self.ui.plainTextEdit1.setTextCursor(cursor)
                    else:
                        if MOUSE_R_CLICK_FLAG == 0:
                            MOUSE_R_CLICK_FIRST.hide()
                            if MOUSE_R_CLICK_SECOND != "":
                                self.scene.removeItem(MOUSE_R_CLICK_SECOND)
                                MOUSE_R_CLICK_SECOND = ""
                        else:
                            MOUSE_R_CLICK_FIRST.hide()
                            if MOUSE_R_CLICK_SECOND != "":
                                self.scene.removeItem(MOUSE_R_CLICK_SECOND)
                                MOUSE_R_CLICK_SECOND = ""
                            EX_MOUSE_R_CLICK_FIRST.hide()
                            if EX_MOUSE_R_CLICK_SECOND != "":
                                self.scene.removeItem(EX_MOUSE_R_CLICK_SECOND)
                                EX_MOUSE_R_CLICK_SECOND = ""
                            MOUSE_R_CLICK_FLAG = 0
                        Z1MIN_TEXT.hide()
                        Z1MAX_TEXT.hide()
                        X1MIN_TEXT.hide()
                        X1MAX_TEXT.hide()
                        Z2MIN_TEXT.hide()
                        Z2MAX_TEXT.hide()
                        X2MIN_TEXT.hide()
                        X2MAX_TEXT.hide()

        #graphicsView1.viewport()上でマウスが移動した際の処理
        elif (event.type() == QtGui.QMouseEvent.MouseMove and obj is self.ui.graphicsView1.viewport()):
            if BUTTON_FLAG == 1:
                #if SELECTED_ITEM == None or SELECTED_ITEM == MATERIAL: #アイテムが選択されていない場合
                no_item = 0
                if self.ui.action2_20.isChecked() == True:
                    for x in TOOLS_TEXT:
                        for y in x:
                            if SELECTED_ITEM == y:
                                length = event.position().x() - EX_X
                                height = event.position().y() - EX_Y
                                SELECTED_ITEM.moveBy(length / SCALE, height / SCALE)
                                no_item = 1
                if no_item == 0:
                    length = EX_X - event.position().x()
                    height = EX_Y - event.position().y()
                    bar_x = self.ui.graphicsView1.horizontalScrollBar().value()
                    bar_y = self.ui.graphicsView1.verticalScrollBar().value()
                    self.ui.graphicsView1.horizontalScrollBar().setValue(bar_x + length)
                    self.ui.graphicsView1.verticalScrollBar().setValue(bar_y + height)
                '''
                else: #アイテムが選択されている場合
                    length = event.pos().x() - EX_X
                    height = event.pos().y() - EX_Y
                    SELECTED_ITEM.moveBy(length / SCALE, height / SCALE)
                '''
                EX_X = event.position().x() #マウスカーソルのX位置を記憶
                EX_Y = event.position().y() #マウスカーソルのY位置を記憶
            elif BUTTON_FLAG == 2 and FLAG_END == 1:
                if MOUSE_R_CLICK_SECOND != "":
                    self.scene.removeItem(MOUSE_R_CLICK_SECOND)
                    MOUSE_R_CLICK_SECOND = ""
                scenePos =self.ui.graphicsView1.mapToScene(event.position().x(), event.position().y())
                MOUSE_R_CLICK_FIRST.setPos(scenePos.x() - 15, scenePos.y() - 15)
                MOUSE_R_CLICK_FIRST.show()
                #xList = []
                #yList = []
                xyListX = []
                xyListY = []
                for i in self.scene.collidingItems(MOUSE_R_CLICK_FIRST, QtCore.Qt.ItemSelectionMode.IntersectsItemShape):
                    tmp = i.shape().toFillPolygon().toList()
                    for l in tmp:
                        inPos = QtCore.QPointF(l.x() - MOUSE_R_CLICK_FIRST.x() + MATERIAL.x(), l.y() - MOUSE_R_CLICK_FIRST.y())
                        if MOUSE_R_CLICK_FIRST.contains(inPos):
                            pX = l.x()
                            pY = l.y()
                            if "999999999999" in str(pX):
                                pX = pX + 0.001
                                pX = str(pX)
                                sp = pX.split(".")
                                lp = sp[1]
                                lp = lp[:3]
                                pX = float(sp[0] + "." + lp)
                            elif "000000000001" in str(pX):
                                pX = str(pX)
                                sp = pX.split(".")
                                lp = sp[1]
                                lp = lp[:3]
                                pX = float(sp[0] + "." + lp)
                            if "999999999999" in str(pY):
                                pY = pY + 0.001
                                pY = str(pY)
                                sp = pY.split(".")
                                lp = sp[1]
                                lp = lp[:3]
                                pY = float(sp[0] + "." + lp)
                            elif "000000000001" in str(pY):
                                pY = str(pY)
                                sp = pY.split(".")
                                lp = sp[1]
                                lp = lp[:3]
                                pY = float(sp[0] + "." + lp)
                            stX = str(pX)
                            stY = str(pY)
                            tmpX = stX.split(".")
                            stX = tmpX[1]
                            tmpY = stY.split(".")
                            stY = tmpY[1]
                            stX = stX.replace('-', "")
                            stX = stX.replace('+', "")
                            stY = stY.replace('-', "")
                            stY = stY.replace('+', "")
                            pX = RND(pX / VIEW_SCALE)
                            pY = RND(pY / VIEW_SCALE)
                            if len(stX) < 4:
                                #xList.append(pX)
                                xyListX.append(pX)
                                xyListY.append(pY)
                            if len(stY) < 4:
                                #yList.append(pY)
                                xyListX.append(pX)
                                xyListY.append(pY)
                cX = collections.Counter(xyListX)
                cY = collections.Counter(xyListY)
                if len(cX) > 0 and len(cY)> 0:
                    maxKeyX = max(cX.items(), key=operator.itemgetter(1))[0]
                    cXnum = cX[maxKeyX]
                    maxKeyY = max(cY.items(), key=operator.itemgetter(1))[0]
                    cYnum = cY[maxKeyY]
                    if cXnum > cYnum:
                        idx = -1
                        result = []
                        for cnt in range(xyListX.count(maxKeyX)):
                            idx = xyListX.index(maxKeyX, idx+1)
                            result.append(idx)
                        searchList = []
                        for x in result:
                            searchList.append(xyListY[x])
                        path = QtGui.QPainterPath()
                        path.moveTo(maxKeyX * VIEW_SCALE + MATERIAL.x(), max(searchList) * VIEW_SCALE)
                        path.lineTo(maxKeyX * VIEW_SCALE + MATERIAL.x(), min(searchList) * VIEW_SCALE)
                        pen = QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.SolidLine)
                        pen.setCosmetic(True)
                        MOUSE_R_CLICK_SECOND = self.scene.addPath(path, pen)
                        if MOUSE_R_CLICK_FLAG == 0:
                            Z1MIN_TEXT.setPlainText("Z1min=" + str(maxKeyX))
                            Z1MIN_TEXT.setPos(scenePos.x() - 15 - Z1MIN_TEXT.boundingRect().width(), scenePos.y() - int(Z1MIN_TEXT.boundingRect().height() / 2))
                            Z1MIN_TEXT.show()
                            Z1MAX_TEXT.setPlainText("Z1max=" + str(maxKeyX))
                            Z1MAX_TEXT.setPos(scenePos.x() + 15, scenePos.y() - int(Z1MAX_TEXT.boundingRect().height() / 2))
                            Z1MAX_TEXT.show()
                            X1MIN_TEXT.setPlainText("X1min=" + str(max(searchList) * -1))
                            X1MIN_TEXT.setPos(scenePos.x() - int(X1MIN_TEXT.boundingRect().width() / 2), scenePos.y() + 15)
                            X1MIN_TEXT.show()
                            X1MAX_TEXT.setPlainText("X1max=" + str(min(searchList) * -1))
                            X1MAX_TEXT.setPos(scenePos.x() - int(X1MAX_TEXT.boundingRect().width() / 2), scenePos.y() - 15 - X1MAX_TEXT.boundingRect().height())
                            X1MAX_TEXT.show()
                        else:
                            Z2MIN_TEXT.setPlainText("Z2min=" + str(maxKeyX))
                            Z2MIN_TEXT.setPos(scenePos.x() - 15 - Z2MIN_TEXT.boundingRect().width(), scenePos.y() - int(Z2MIN_TEXT.boundingRect().height() / 2))
                            Z2MIN_TEXT.show()
                            Z2MAX_TEXT.setPlainText("Z2max=" + str(maxKeyX))
                            Z2MAX_TEXT.setPos(scenePos.x() + 15, scenePos.y() - int(Z2MAX_TEXT.boundingRect().height() / 2))
                            Z2MAX_TEXT.show()
                            X2MIN_TEXT.setPlainText("X2min=" + str(max(searchList) * -1))
                            X2MIN_TEXT.setPos(scenePos.x() - int(X2MIN_TEXT.boundingRect().width() / 2), scenePos.y() + 15)
                            X2MIN_TEXT.show()
                            X2MAX_TEXT.setPlainText("X2max=" + str(min(searchList) * -1))
                            X2MAX_TEXT.setPos(scenePos.x() - int(X2MAX_TEXT.boundingRect().width() / 2), scenePos.y() - 15 - X2MAX_TEXT.boundingRect().height())
                            X2MAX_TEXT.show()
                    elif cXnum < cYnum:
                        idx = -1
                        result = []
                        for cnt in range(xyListY.count(maxKeyY)):
                            idx = xyListY.index(maxKeyY, idx+1)
                            result.append(idx)
                        searchList = []
                        for x in result:
                            searchList.append(xyListX[x])
                        path = QtGui.QPainterPath()
                        path.moveTo(max(searchList) * VIEW_SCALE + MATERIAL.x(), maxKeyY * VIEW_SCALE)
                        path.lineTo(min(searchList) * VIEW_SCALE + MATERIAL.x(), maxKeyY * VIEW_SCALE)
                        pen = QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.SolidLine)
                        pen.setCosmetic(True)
                        MOUSE_R_CLICK_SECOND = self.scene.addPath(path, pen)
                        if MOUSE_R_CLICK_FLAG == 0:
                            Z1MIN_TEXT.setPlainText("Z1min=" + str(min(searchList)))
                            Z1MIN_TEXT.setPos(scenePos.x() - 15 - Z1MIN_TEXT.boundingRect().width(), scenePos.y() - int(Z1MIN_TEXT.boundingRect().height() / 2))
                            Z1MIN_TEXT.show()
                            Z1MAX_TEXT.setPlainText("Z1max=" + str(max(searchList)))
                            Z1MAX_TEXT.setPos(scenePos.x() + 15, scenePos.y() - int(Z1MAX_TEXT.boundingRect().height() / 2))
                            Z1MAX_TEXT.show()
                            X1MIN_TEXT.setPlainText("X1min=" + str(maxKeyY * -1))
                            X1MIN_TEXT.setPos(scenePos.x() - int(X1MIN_TEXT.boundingRect().width() / 2), scenePos.y() + 15)
                            X1MIN_TEXT.show()
                            X1MAX_TEXT.setPlainText("X1max=" + str(maxKeyY * -1))
                            X1MAX_TEXT.setPos(scenePos.x() - int(X1MAX_TEXT.boundingRect().width() / 2), scenePos.y() - 15 - X1MAX_TEXT.boundingRect().height())
                            X1MAX_TEXT.show()
                        else:
                            Z2MIN_TEXT.setPlainText("Z2min=" + str(min(searchList)))
                            Z2MIN_TEXT.setPos(scenePos.x() - 15 - Z2MIN_TEXT.boundingRect().width(), scenePos.y() - int(Z2MIN_TEXT.boundingRect().height() / 2))
                            Z2MIN_TEXT.show()
                            Z2MAX_TEXT.setPlainText("Z2max=" + str(max(searchList)))
                            Z2MAX_TEXT.setPos(scenePos.x() + 15, scenePos.y() - int(Z2MAX_TEXT.boundingRect().height() / 2))
                            Z2MAX_TEXT.show()
                            X2MIN_TEXT.setPlainText("X2min=" + str(maxKeyY * -1))
                            X2MIN_TEXT.setPos(scenePos.x() - int(X2MIN_TEXT.boundingRect().width() / 2), scenePos.y() + 15)
                            X2MIN_TEXT.show()
                            X2MAX_TEXT.setPlainText("X2max=" + str(maxKeyY * -1))
                            X2MAX_TEXT.setPos(scenePos.x() - int(X2MAX_TEXT.boundingRect().width() / 2), scenePos.y() - 15 - X2MAX_TEXT.boundingRect().height())
                            X2MAX_TEXT.show()
                    else:
                        if MOUSE_R_CLICK_FLAG == 0:
                            Z1MIN_TEXT.hide()
                            Z1MAX_TEXT.hide()
                            X1MIN_TEXT.hide()
                            X1MAX_TEXT.hide()
                        else:
                            Z2MIN_TEXT.hide()
                            Z2MAX_TEXT.hide()
                            X2MIN_TEXT.hide()
                            X2MAX_TEXT.hide()
                else:
                    if scenePos.x() -15 < MATERIAL.x() and scenePos.x() + 15 > MATERIAL.x():
                        path = QtGui.QPainterPath()
                        path.moveTo(MATERIAL.x(), scenePos.y() - 15)
                        path.lineTo(MATERIAL.x(), scenePos.y() + 15)
                        pen = QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.SolidLine)
                        pen.setCosmetic(True)
                        MOUSE_R_CLICK_SECOND = self.scene.addPath(path, pen)
                        if MOUSE_R_CLICK_FLAG == 0:
                            Z1MIN_TEXT.setPlainText("Z1min=0")
                            Z1MIN_TEXT.setPos(scenePos.x() - 15 - Z1MIN_TEXT.boundingRect().width(), scenePos.y() - int(Z1MIN_TEXT.boundingRect().height() / 2))
                            Z1MIN_TEXT.show()
                            Z1MAX_TEXT.setPlainText("Z1max=0")
                            Z1MAX_TEXT.setPos(scenePos.x() + 15, scenePos.y() - int(Z1MAX_TEXT.boundingRect().height() / 2))
                            Z1MAX_TEXT.show()
                            X1MIN_TEXT.setPlainText("X1min=" + str((scenePos.y() + 15) / VIEW_SCALE * -1))
                            X1MIN_TEXT.setPos(scenePos.x() - int(X1MIN_TEXT.boundingRect().width() / 2), scenePos.y() + 15)
                            X1MIN_TEXT.show()
                            X1MAX_TEXT.setPlainText("X1max=" + str((scenePos.y() - 15) / VIEW_SCALE * -1))
                            X1MAX_TEXT.setPos(scenePos.x() - int(X1MAX_TEXT.boundingRect().width() / 2), scenePos.y() - 15 - X1MAX_TEXT.boundingRect().height())
                            X1MAX_TEXT.show()
                        else:
                            Z2MIN_TEXT.setPlainText("Z2min=0")
                            Z2MIN_TEXT.setPos(scenePos.x() - 15 - Z2MIN_TEXT.boundingRect().width(), scenePos.y() - int(Z2MIN_TEXT.boundingRect().height() / 2))
                            Z2MIN_TEXT.show()
                            Z2MAX_TEXT.setPlainText("Z2max=0")
                            Z2MAX_TEXT.setPos(scenePos.x() + 15, scenePos.y() - int(Z2MAX_TEXT.boundingRect().height() / 2))
                            Z2MAX_TEXT.show()
                            X2MIN_TEXT.setPlainText("X2min=" + str((scenePos.y() + 15) / VIEW_SCALE* -1))
                            X2MIN_TEXT.setPos(scenePos.x() - int(X2MIN_TEXT.boundingRect().width() / 2), scenePos.y() + 15)
                            X2MIN_TEXT.show()
                            X2MAX_TEXT.setPlainText("X2max=" + str((scenePos.y() - 15) / VIEW_SCALE* -1))
                            X2MAX_TEXT.setPos(scenePos.x() - int(X2MAX_TEXT.boundingRect().width() / 2), scenePos.y() - 15 - X2MAX_TEXT.boundingRect().height())
                            X2MAX_TEXT.show()
                    elif scenePos.y() -15 < MATERIAL_DIAMETER * VIEW_SCALE and scenePos.y() + 15 > MATERIAL_DIAMETER * VIEW_SCALE:
                        path = QtGui.QPainterPath()
                        path.moveTo(scenePos.x() - 15, MATERIAL_DIAMETER * VIEW_SCALE)
                        path.lineTo(scenePos.x() + 15, MATERIAL_DIAMETER * VIEW_SCALE)
                        pen = QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.SolidLine)
                        pen.setCosmetic(True)
                        MOUSE_R_CLICK_SECOND = self.scene.addPath(path, pen)
                        scenePosX_m_15 = str(RND((scenePos.x() - 15) / VIEW_SCALE - MATERIAL.x() / VIEW_SCALE))
                        scenePosX_p_15 = str(RND((scenePos.x() + 15) / VIEW_SCALE - MATERIAL.x() / VIEW_SCALE))
                        if MOUSE_R_CLICK_FLAG == 0:
                            Z1MIN_TEXT.setPlainText("Z1min=" + scenePosX_m_15)
                            Z1MIN_TEXT.setPos(scenePos.x() - 15 - Z1MIN_TEXT.boundingRect().width(), scenePos.y() - int(Z1MIN_TEXT.boundingRect().height() / 2))
                            Z1MIN_TEXT.show()
                            Z1MAX_TEXT.setPlainText("Z1max=" + scenePosX_p_15)
                            Z1MAX_TEXT.setPos(scenePos.x() + 15, scenePos.y() - int(Z1MAX_TEXT.boundingRect().height() / 2))
                            Z1MAX_TEXT.show()
                            X1MIN_TEXT.setPlainText("X1min=" + str(MATERIAL_DIAMETER * -1))
                            X1MIN_TEXT.setPos(scenePos.x() - int(X1MIN_TEXT.boundingRect().width() / 2), scenePos.y() + 15)
                            X1MIN_TEXT.show()
                            X1MAX_TEXT.setPlainText("X1max=" + str(MATERIAL_DIAMETER * -1))
                            X1MAX_TEXT.setPos(scenePos.x() - int(X1MAX_TEXT.boundingRect().width() / 2), scenePos.y() - 15 - X1MAX_TEXT.boundingRect().height())
                            X1MAX_TEXT.show()
                        else:
                            Z2MIN_TEXT.setPlainText("Z2min=" + scenePosX_m_15)
                            Z2MIN_TEXT.setPos(scenePos.x() - 15 - Z2MIN_TEXT.boundingRect().width(), scenePos.y() - int(Z2MIN_TEXT.boundingRect().height() / 2))
                            Z2MIN_TEXT.show()
                            Z2MAX_TEXT.setPlainText("Z2max=" + scenePosX_p_15)
                            Z2MAX_TEXT.setPos(scenePos.x() + 15, scenePos.y() - int(Z2MAX_TEXT.boundingRect().height() / 2))
                            Z2MAX_TEXT.show()
                            X2MIN_TEXT.setPlainText("X2min=" + str(MATERIAL_DIAMETER * -1))
                            X2MIN_TEXT.setPos(scenePos.x() - int(X2MIN_TEXT.boundingRect().width() / 2), scenePos.y() + 15)
                            X2MIN_TEXT.show()
                            X2MAX_TEXT.setPlainText("X2max=" + str(MATERIAL_DIAMETER * -1))
                            X2MAX_TEXT.setPos(scenePos.x() - int(X2MAX_TEXT.boundingRect().width() / 2), scenePos.y() - 15 - X2MAX_TEXT.boundingRect().height())
                            X2MAX_TEXT.show()
                    elif scenePos.y() -15 < MATERIAL_DIAMETER * VIEW_SCALE * -1 and scenePos.y() + 15 > MATERIAL_DIAMETER * VIEW_SCALE * -1:
                        path = QtGui.QPainterPath()
                        path.moveTo(scenePos.x() - 15, MATERIAL_DIAMETER * VIEW_SCALE * -1)
                        path.lineTo(scenePos.x() + 15, MATERIAL_DIAMETER * VIEW_SCALE * -1)
                        pen = QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.SolidLine)
                        pen.setCosmetic(True)
                        MOUSE_R_CLICK_SECOND = self.scene.addPath(path, pen)
                        scenePosX_m_15 = str(RND((scenePos.x() - 15) / VIEW_SCALE - MATERIAL.x() / VIEW_SCALE))
                        scenePosX_p_15 = str(RND((scenePos.x() + 15) / VIEW_SCALE - MATERIAL.x() / VIEW_SCALE))
                        if MOUSE_R_CLICK_FLAG == 0:
                            Z1MIN_TEXT.setPlainText("Z1min=" + scenePosX_m_15)
                            Z1MIN_TEXT.setPos(scenePos.x() - 15 - Z1MIN_TEXT.boundingRect().width(), scenePos.y() - int(Z1MIN_TEXT.boundingRect().height() / 2))
                            Z1MIN_TEXT.show()
                            Z1MAX_TEXT.setPlainText("Z1max=" + scenePosX_p_15)
                            Z1MAX_TEXT.setPos(scenePos.x() + 15, scenePos.y() - int(Z1MAX_TEXT.boundingRect().height() / 2))
                            Z1MAX_TEXT.show()
                            X1MIN_TEXT.setPlainText("X1min=" + str(MATERIAL_DIAMETER)) # * -1 *-1
                            X1MIN_TEXT.setPos(scenePos.x() - int(X1MIN_TEXT.boundingRect().width() / 2), scenePos.y() + 15)
                            X1MIN_TEXT.show()
                            X1MAX_TEXT.setPlainText("X1max=" + str(MATERIAL_DIAMETER)) # * -1 *-1
                            X1MAX_TEXT.setPos(scenePos.x() - int(X1MAX_TEXT.boundingRect().width() / 2), scenePos.y() - 15 - X1MAX_TEXT.boundingRect().height())
                            X1MAX_TEXT.show()
                        else:
                            Z2MIN_TEXT.setPlainText("Z2min=" + scenePosX_m_15)
                            Z2MIN_TEXT.setPos(scenePos.x() - 15 - Z2MIN_TEXT.boundingRect().width(), scenePos.y() - int(Z2MIN_TEXT.boundingRect().height() / 2))
                            Z2MIN_TEXT.show()
                            Z2MAX_TEXT.setPlainText("Z2max=" + scenePosX_p_15)
                            Z2MAX_TEXT.setPos(scenePos.x() + 15, scenePos.y() - int(Z2MAX_TEXT.boundingRect().height() / 2))
                            Z2MAX_TEXT.show()
                            X2MIN_TEXT.setPlainText("X2min=" + str(MATERIAL_DIAMETER)) # * -1 *-1
                            X2MIN_TEXT.setPos(scenePos.x() - int(X2MIN_TEXT.boundingRect().width() / 2), scenePos.y() + 15)
                            X2MIN_TEXT.show()
                            X2MAX_TEXT.setPlainText("X2max=" + str(MATERIAL_DIAMETER )) # * -1 *-1
                            X2MAX_TEXT.setPos(scenePos.x() - int(X2MAX_TEXT.boundingRect().width() / 2), scenePos.y() - 15 - X2MAX_TEXT.boundingRect().height())
                            X2MAX_TEXT.show()
                    else:
                        if MOUSE_R_CLICK_FLAG == 0:
                            Z1MIN_TEXT.hide()
                            Z1MAX_TEXT.hide()
                            X1MIN_TEXT.hide()
                            X1MAX_TEXT.hide()
                        else:
                            Z2MIN_TEXT.hide()
                            Z2MAX_TEXT.hide()
                            X2MIN_TEXT.hide()
                            X2MAX_TEXT.hide()

        #graphicsView1.viewport()上でマウスホイールが回転した場合の処理
        elif (event.type() == QtGui.QMouseEvent.Wheel and obj is self.ui.graphicsView1.viewport()):
            if event.angleDelta().y() > 0:
                tf = 0
                SCALE =  SCALE *  2
                if SCALE > 32:
                    SCALE =32
                    tf = 1

                '''
                self.ui.graphicsView1.resetTransform()
                self.ui.graphicsView1.setTransformationAnchor(self.ui.graphicsView1.ViewportAnchor.AnchorUnderMouse)
                self.ui.graphicsView1.setResizeAnchor(self.ui.graphicsView1.ViewportAnchor.AnchorUnderMouse)
                self.ui.graphicsView1.scale(SCALE, SCALE)
                '''

                EX_POS = self.ui.graphicsView1.mapToScene(event.position().x(), event.position().y())
                EX_X = EX_POS.x()
                EX_Y = EX_POS.y()
                self.ui.graphicsView1.resetTransform()
                self.ui.graphicsView1.scale(SCALE, SCALE)
                CU_POS = self.ui.graphicsView1.mapToScene(event.position().x(), event.position().y())
                CU_X = CU_POS.x()
                CU_Y = CU_POS.y()
                length = (EX_X - CU_X) * SCALE
                height = (EX_Y - CU_Y) * SCALE + 139
                bar_x = self.ui.graphicsView1.horizontalScrollBar().value()
                bar_y = self.ui.graphicsView1.verticalScrollBar().value()
                self.ui.graphicsView1.horizontalScrollBar().setValue(bar_x + length)
                self.ui.graphicsView1.verticalScrollBar().setValue(bar_y + height)

                if tf == 0:
                    TOOLS_TEXT_SCALE = TOOLS_TEXT_SCALE / 2
                    for i, x in enumerate(TOOLS_TEXT):
                        for l, y in enumerate(x):
                            TOOLS_TEXT[i][l].setScale(TOOLS_TEXT_SCALE)
                    #移動先のプログラムを拡大表示
                    if self.ui.action2_16.isChecked() == True:
                        TOOLS_TEXT[NUM_TOOL][NUM_LINE-1].setScale(TOOLS_TEXT_SCALE)
                        TOOLS_TEXT[NUM_TOOL][NUM_LINE].setScale(TOOLS_TEXT_SCALE * 4.0)
            else:
                SCALE =  SCALE / 2
                tf = 0
                if SCALE < 0.015625:
                    SCALE =0.015625
                    tf = 1

                '''
                self.ui.graphicsView1.resetTransform()
                self.ui.graphicsView1.setTransformationAnchor(self.ui.graphicsView1.ViewportAnchor.AnchorUnderMouse)
                self.ui.graphicsView1.setResizeAnchor(self.ui.graphicsView1.ViewportAnchor.AnchorUnderMouse)
                self.ui.graphicsView1.scale(SCALE, SCALE)
                '''

                EX_POS = self.ui.graphicsView1.mapToScene(event.position().x(), event.position().y())
                EX_X = EX_POS.x()
                EX_Y = EX_POS.y()
                self.ui.graphicsView1.resetTransform()
                self.ui.graphicsView1.scale(SCALE, SCALE)
                CU_POS = self.ui.graphicsView1.mapToScene(event.position().x(), event.position().y())
                CU_X = CU_POS.x()
                CU_Y = CU_POS.y()
                length = (EX_X - CU_X) * SCALE
                height = (EX_Y - CU_Y) * SCALE - 139
                bar_x = self.ui.graphicsView1.horizontalScrollBar().value()
                bar_y = self.ui.graphicsView1.verticalScrollBar().value()
                self.ui.graphicsView1.horizontalScrollBar().setValue(bar_x + length)
                self.ui.graphicsView1.verticalScrollBar().setValue(bar_y + height)

                if tf == 0:
                    TOOLS_TEXT_SCALE = TOOLS_TEXT_SCALE * 2
                    for i, x in enumerate(TOOLS_TEXT):
                        for l, y in enumerate(x):
                            TOOLS_TEXT[i][l].setScale(TOOLS_TEXT_SCALE)
                    #移動先のプログラムを拡大表示
                    if self.ui.action2_16.isChecked() == True:
                        TOOLS_TEXT[NUM_TOOL][NUM_LINE-1].setScale(TOOLS_TEXT_SCALE)
                        TOOLS_TEXT[NUM_TOOL][NUM_LINE].setScale(TOOLS_TEXT_SCALE * 4.0)
        return QtWidgets.QMainWindow.eventFilter(self, obj, event)


    #-----キー入力処理----------------------------------------
    def keyPressEvent(self, event):
        if event.isAutoRepeat():
            return
        pressed = QtGui.QKeySequence(event.key()).toString()
        if pressed == "Z" and self.ui.pushButton3.isEnabled() == True:
            self.pushButton3_clicked()
        elif pressed == "X" and self.ui.pushButton4.isEnabled() == True:
            self.pushButton4_clicked()


    #-----ウィンドウ終了イベントのフック----------------------------------------
    def closeEvent(self, event): #event.accept() event.ignore()で処理を選択可能
        global FLAG_SIMULATION_STARTED
        global SUB_WIN_ACTIVE
        if FLAG_SIMULATION_STARTED == 1: #ループ実行中の場合
            event.ignore() #メインウィンドウの終了イベントをキャンセル
        else: #ループが実行中でない場合
            win.setEnabled(True)
            SUB_WIN_ACTIVE = 0
            event.accept() #メインウィンドウの終了イベントを実行










    ##################################################独自関数##################################################
    #-----設定ファイル読み込み処理----------------------------------------
    def SETTINGS_READ(self):
        global SETTING_PATH_SIM
        f = open(SETTING_PATH_SIM, "r")
        x = ""
        x = f.readlines() #テキストを一行ずつ配列として読込む（行の終わりの改行コードも含めて読込む）
        f.close()

        #材料径の設定
        global MATERIAL_DIAMETER
        data = x[0].replace("\n", "")
        MATERIAL_DIAMETER = float(data)

        #工具基準位置マーカーの設定（加工領域を色分けの設定）
        data = x[1].replace("\n", "")
        if data == "0":
            self.ui.action2_2.setChecked(False)
        else:
            self.ui.action2_2.setChecked(True)
        
        #プログラム軌跡の設定
        data = x[2].replace("\n", "")
        if data == "0":
            self.ui.action2_25.setChecked(True)
            self.ui.action2_3.setChecked(False)
            self.ui.action2_4.setChecked(False)
        elif data == "1":
            self.ui.action2_25.setChecked(False)
            self.ui.action2_3.setChecked(True)
            self.ui.action2_4.setChecked(False)
        else:
            self.ui.action2_25.setChecked(False)
            self.ui.action2_3.setChecked(False)
            self.ui.action2_4.setChecked(True)

        #両側表示の設定
        data = x[3].replace("\n", "")
        if data == "0":
            self.ui.action2_5.setChecked(False)
        else:
            self.ui.action2_5.setChecked(True)

        #G50の設定
        data = x[4].replace("\n", "")
        if data == "0":
            self.ui.action2_6.setChecked(False)
        else:
            self.ui.action2_6.setChecked(True)

        #プログラム表示の設定
        data = x[5].replace("\n", "")
        if data == "0":
            self.ui.action2_24.setChecked(True)
            self.ui.action2_7.setChecked(False)
            self.ui.action2_8.setChecked(False)
        elif data == "1":
            self.ui.action2_24.setChecked(False)
            self.ui.action2_7.setChecked(True)
            self.ui.action2_8.setChecked(False)
        else:
            self.ui.action2_24.setChecked(False)
            self.ui.action2_7.setChecked(False)
            self.ui.action2_8.setChecked(True)

        #ガイドブッシュ表示の設定
        data = x[6].replace("\n", "")
        if data == "0":
            self.ui.action2_9.setChecked(False)
        else:
            self.ui.action2_9.setChecked(True)

        #フォントサイズの設定
        data = x[7].replace("\n", "")
        global FONT_SIZE
        if data == "0":
            self.ui.action2_21.setChecked(False)
            self.ui.action2_22.setChecked(False)
            self.ui.action2_23.setChecked(True)
            self.ui.action2_10.setChecked(False)
            self.ui.action2_11.setChecked(False)
            self.ui.action2_12.setChecked(False)
            FONT_SIZE = 1
        elif data == "1":
            self.ui.action2_21.setChecked(False)
            self.ui.action2_22.setChecked(True)
            self.ui.action2_23.setChecked(False)
            self.ui.action2_10.setChecked(False)
            self.ui.action2_11.setChecked(False)
            self.ui.action2_12.setChecked(False)
            FONT_SIZE = 5
        elif data == "2":
            self.ui.action2_21.setChecked(True)
            self.ui.action2_22.setChecked(False)
            self.ui.action2_23.setChecked(False)
            self.ui.action2_10.setChecked(False)
            self.ui.action2_11.setChecked(False)
            self.ui.action2_12.setChecked(False)
            FONT_SIZE = 10
        elif data == "3":
            self.ui.action2_21.setChecked(False)
            self.ui.action2_22.setChecked(False)
            self.ui.action2_23.setChecked(False)
            self.ui.action2_10.setChecked(True)
            self.ui.action2_11.setChecked(False)
            self.ui.action2_12.setChecked(False)
            FONT_SIZE = 15
        elif data == "4":
            self.ui.action2_21.setChecked(False)
            self.ui.action2_22.setChecked(False)
            self.ui.action2_23.setChecked(False)
            self.ui.action2_10.setChecked(False)
            self.ui.action2_11.setChecked(True)
            self.ui.action2_12.setChecked(False)
            FONT_SIZE = 20
        else:
            self.ui.action2_21.setChecked(False)
            self.ui.action2_22.setChecked(False)
            self.ui.action2_23.setChecked(False)
            self.ui.action2_10.setChecked(False)
            self.ui.action2_11.setChecked(False)
            self.ui.action2_12.setChecked(True)
            FONT_SIZE = 25

        #加工工具原点を基準に移動の設定
        data = x[8].replace("\n", "")
        if data == "0":
            self.ui.action2_13.setChecked(False)
        else:
            self.ui.action2_13.setChecked(True)

        #プログラムの詳細を表示の設定
        data = x[9].replace("\n", "")
        if data == "0":
            self.ui.action2_14.setChecked(False)
        else:
            self.ui.action2_14.setChecked(True)

        #中心線表示の設定
        data = x[10].replace("\n", "")
        if data == "0":
            self.ui.action2_15.setChecked(False)
        else:
            self.ui.action2_15.setChecked(True)

        #移動先のプログラムを拡大表示の設定
        data = x[11].replace("\n", "")
        if data == "0":
            self.ui.action2_16.setChecked(False)
        else:
            self.ui.action2_16.setChecked(True)

        #プログラム座標マーカー表示の設定
        data = x[12].replace("\n", "")
        if data == "0":
            self.ui.action2_17.setChecked(False)
        else:
            self.ui.action2_17.setChecked(True)

        #ガイドブッシュ半透明表示の設定
        data = x[13].replace("\n", "")
        if data == "0":
            self.ui.action2_18.setChecked(False)
        else:
            self.ui.action2_18.setChecked(True)

        #切削工具半透明表示の設定
        data = x[14].replace("\n", "")
        if data == "0":
            self.ui.action2_19.setChecked(False)
        else:
            self.ui.action2_19.setChecked(True)

        #プログラム移動の設定
        data = x[15].replace("\n", "")
        if data == "0":
            self.ui.action2_20.setChecked(False)
        else:
            self.ui.action2_20.setChecked(True)

        #実行スピードの設定
        data = x[16].replace("\n", "")
        global RUN_SPEED
        if data == "0":
            self.ui.action3_1.setChecked(True)
            self.ui.action3_2.setChecked(False)
            self.ui.action3_3.setChecked(False)
            self.ui.action3_4.setChecked(False)
            self.ui.action3_5.setChecked(False)
            self.ui.action3_6.setChecked(False)
            RUN_SPEED = 0
        elif data == "1":
            self.ui.action3_1.setChecked(False)
            self.ui.action3_2.setChecked(True)
            self.ui.action3_3.setChecked(False)
            self.ui.action3_4.setChecked(False)
            self.ui.action3_5.setChecked(False)
            self.ui.action3_6.setChecked(False)
            RUN_SPEED = 1
        elif data == "2":
            self.ui.action3_1.setChecked(False)
            self.ui.action3_2.setChecked(False)
            self.ui.action3_3.setChecked(True)
            self.ui.action3_4.setChecked(False)
            self.ui.action3_5.setChecked(False)
            self.ui.action3_6.setChecked(False)
            RUN_SPEED = 3
        elif data == "3":
            self.ui.action3_1.setChecked(False)
            self.ui.action3_2.setChecked(False)
            self.ui.action3_3.setChecked(False)
            self.ui.action3_4.setChecked(True)
            self.ui.action3_5.setChecked(False)
            self.ui.action3_6.setChecked(False)
            RUN_SPEED = 7
        elif data == "4":
            self.ui.action3_1.setChecked(False)
            self.ui.action3_2.setChecked(False)
            self.ui.action3_3.setChecked(False)
            self.ui.action3_4.setChecked(False)
            self.ui.action3_5.setChecked(True)
            self.ui.action3_6.setChecked(False)
            RUN_SPEED = 15
        else:
            self.ui.action3_1.setChecked(False)
            self.ui.action3_2.setChecked(False)
            self.ui.action3_3.setChecked(False)
            self.ui.action3_4.setChecked(False)
            self.ui.action3_5.setChecked(False)
            self.ui.action3_6.setChecked(True)
            RUN_SPEED = -1


    #-----設定ファイルの保存処理----------------------------------------
    def SETTINGS_SAVE(self):
        global MATERIAL_DIAMETER
        global SETTING_PATH_SIM
        data = ""

        #材料径の設定
        data = str(MATERIAL_DIAMETER)+"\n"

        #工具基準位置マーカーの設定（加工領域を色分けの設定）
        if self.ui.action2_2.isChecked() == False:
            data += "0\n"
        else:
            data += "1\n"

        #プログラム軌跡の設定
        if self.ui.action2_25.isChecked() == True:
            data += "0\n"
        elif self.ui.action2_3.isChecked() == True:
            data += "1\n"
        elif self.ui.action2_4.isChecked() == True:
            data += "2\n"

        #両側表示の設定
        if self.ui.action2_5.isChecked() == False:
            data += "0\n"
        else:
            data += "1\n"

        #G50の設定
        if self.ui.action2_6.isChecked() == False:
            data += "0\n"
        else:
            data += "1\n"

        #プログラム表示の設定
        if self.ui.action2_24.isChecked() == True:
            data += "0\n"
        elif self.ui.action2_7.isChecked() == True:
            data += "1\n"
        elif self.ui.action2_8.isChecked() == True:
            data += "2\n"

        #ガイドブッシュ表示の設定
        if self.ui.action2_9.isChecked() == False:
            data += "0\n"
        else:
            data += "1\n"

        #フォントサイズの設定
        if self.ui.action2_21.isChecked() == True:
            data += "3\n"
        elif self.ui.action2_22.isChecked() == True:
            data += "1\n"
        elif self.ui.action2_23.isChecked() == True:
            data += "0\n"
        if self.ui.action2_10.isChecked() == True:
            data += "3\n"
        elif self.ui.action2_11.isChecked() == True:
            data += "4\n"
        elif self.ui.action2_12.isChecked() == True:
            data += "5\n"

        #加工工具原点を基準に移動の設定
        if self.ui.action2_13.isChecked() == False:
            data += "0\n"
        else:
            data += "1\n"

        #プログラムの詳細を表示の設定
        if self.ui.action2_14.isChecked() == False:
            data += "0\n"
        else:
            data += "1\n"

        #中心線表示の設定
        if self.ui.action2_15.isChecked() == False:
            data += "0\n"
        else:
            data += "1\n"

        #移動先のプログラムを拡大表示の設定
        if self.ui.action2_16.isChecked() == False:
            data += "0\n"
        else:
            data += "1\n"

        #プログラム座標マーカー表示の設定
        if self.ui.action2_17.isChecked() == False:
            data += "0\n"
        else:
            data += "1\n"

        #ガイドブッシュ半透明表示の設定
        if self.ui.action2_18.isChecked() == False:
            data += "0\n"
        else:
            data += "1\n"

        #切削工具半透明表示の設定
        if self.ui.action2_19.isChecked() == False:
            data += "0\n"
        else:
            data += "1\n"

        #プログラム移動の設定
        if self.ui.action2_20.isChecked() == False:
            data += "0\n"
        else:
            data += "1\n"

        #実行スピードの設定
        if self.ui.action3_1.isChecked() == True:
            data += "0\n"
        elif self.ui.action3_2.isChecked() == True:
            data += "1\n"
        elif self.ui.action3_3.isChecked() == True:
            data += "2\n"
        elif self.ui.action3_4.isChecked() == True:
            data += "3\n"
        elif self.ui.action3_5.isChecked() == True:
            data += "4\n"
        elif self.ui.action3_6.isChecked() == True:
            data += "5\n"

        f = open(SETTING_PATH_SIM, "w")
        f.write(data) #Plaine Text Editの内容を書込む
        f.close()

    ################################################################################################################################################################
    ################################################################################################################################################################
    ################################################################################################################################################################
    ################################################################################################################################################################
    ################################################################################################################################################################
    #-----シミュレーション実行用関数----------------------------------------
    ################################################################################################################################################################
    ################################################################################################################################################################
    ################################################################################################################################################################
    ################################################################################################################################################################
    ################################################################################################################################################################
    def RUN_SIMULATION(self):
        global SCALE
        global PROGRAM_LINE_POS
        global TOOL_CHANGE_POS
        global MATERIAL_DIAMETER
        global MATERIAL
        global TOOL_DXF_PATH
        global TOOL_PAINTER_PATH
        global TOOL_PAINTER_PATH_REV
        global TOOL_NAME
        global MOVEMENT_DATA
        global TOOLS
        global TOOLS_TEXT
        global TOOLS_POS
        global TOOLS_LINE_NUM
        global FLAG_BEFORE
        global FLAG_NEXT
        global FLAG_SIMULATION_STARTED
        global RUN_SPEED
        global TOOL_TEXT_PARENTS
        global GUIDE_BUSH_U
        global GUIDE_BUSH_L
        global CENTER_LINE
        global TOOLS_TEXT_SCALE
        global MOUSE_R_CLICK_FIRST
        global MOUSE_R_CLICK_SECOND
        global EX_MOUSE_R_CLICK_FIRST
        global EX_MOUSE_R_CLICK_SECOND
        global MOUSE_R_CLICK_FLAG
        global FLAG_END
        global Z1MIN_TEXT
        global Z1MAX_TEXT
        global X1MIN_TEXT
        global X1MAX_TEXT
        global Z2MIN_TEXT
        global Z2MAX_TEXT
        global X2MIN_TEXT
        global X2MAX_TEXT
        global NUM_TOOL
        global NUM_LINE
        #self.ui.graphicsView1.resetMatrix() #回転、拡大のマトリクスをリセット
        self.ui.graphicsView1.resetTransform()
        self.ui.graphicsView1.scale(0.5, 0.5)
        SCALE = 0.5
        self.ui.graphicsView1.centerOn(0, 0)
        self.ui.graphicsView1.viewport().installEventFilter(self) #イベントの取得はviewport()に対して行う！
        self.scene = QtWidgets.QGraphicsScene() #シーンを定義
        self.ui.graphicsView1.setScene(self.scene) #ビューにシーンをセット
        #self.ui.graphicsView1.setViewportUpdateMode(self.ui.graphicsView1.SmartViewportUpdate)

        self.ui.graphicsView1.setSceneRect (-100000,-100000,200000, 200000)
        #####ダミーの描画
        '''
        path = QtGui.QPainterPath()
        path.moveTo(-100000,-100000)
        path.lineTo(-99999, -99999)
        pen = QtGui.QPen(QtGui.QColor(255, 255, 255, 255), 1, QtCore.Qt.SolidLine)
        item1 = self.scene.addPath(path, pen)
        path = QtGui.QPainterPath()
        path.moveTo(100000,100000)
        path.lineTo(99999, 99999)
        item2 = self.scene.addPath(path, pen)
        '''

        #####材料の描画
        path = QtGui.QPainterPath()
        path.moveTo(0, MATERIAL_DIAMETER * VIEW_SCALE)
        path.lineTo(3000 * VIEW_SCALE, MATERIAL_DIAMETER * VIEW_SCALE)
        path.lineTo(3000 * VIEW_SCALE, MATERIAL_DIAMETER * -1 * VIEW_SCALE)
        path.lineTo(0, MATERIAL_DIAMETER * -1 * VIEW_SCALE)
        path.lineTo(0, MATERIAL_DIAMETER * VIEW_SCALE)
        #pen = QtGui.QPen(QtCore.Qt.lightGray, 1, QtCore.Qt.SolidLine)
        pen = QtGui.QPen(QtCore.Qt.darkGray, 1, QtCore.Qt.SolidLine)
        pen.setCosmetic(True)
        MATERIAL = self.scene.addPath(path, pen)
        MATERIAL.setBrush(QtGui.QBrush(QtCore.Qt.darkGray, QtCore.Qt.SolidPattern))
        
        #####ガイドブッシュの描画
        path = QtGui.QPainterPath()
        path.moveTo(0.5 * VIEW_SCALE, MATERIAL_DIAMETER * VIEW_SCALE * -1)
        path.lineTo(0.5 * VIEW_SCALE, (3 - MATERIAL_DIAMETER) * VIEW_SCALE)
        path.lineTo(1 * VIEW_SCALE, (9 - MATERIAL_DIAMETER) * VIEW_SCALE)
        path.lineTo(9.4 * VIEW_SCALE, (7.1 - MATERIAL_DIAMETER) * VIEW_SCALE)
        path.lineTo(10.5 * VIEW_SCALE, (6 - MATERIAL_DIAMETER) * VIEW_SCALE)
        path.lineTo(29.5 * VIEW_SCALE, (6 - MATERIAL_DIAMETER) * VIEW_SCALE)
        path.lineTo(30.2 * VIEW_SCALE, (6.7 - MATERIAL_DIAMETER) * VIEW_SCALE)
        path.lineTo(51.3 * VIEW_SCALE, (6.7 - MATERIAL_DIAMETER) * VIEW_SCALE)
        path.lineTo(52.3 * VIEW_SCALE, (5.7 - MATERIAL_DIAMETER) * VIEW_SCALE)
        path.lineTo(52.3 * VIEW_SCALE, (3.8 - MATERIAL_DIAMETER) * VIEW_SCALE)
        path.lineTo(24.3 * VIEW_SCALE, (3.8 - MATERIAL_DIAMETER) * VIEW_SCALE)
        path.lineTo(22.1 * VIEW_SCALE, (1.6 - MATERIAL_DIAMETER) * VIEW_SCALE)
        path.lineTo(17.1 * VIEW_SCALE, (1.6 - MATERIAL_DIAMETER) * VIEW_SCALE)
        path.lineTo(15.5 * VIEW_SCALE, MATERIAL_DIAMETER * VIEW_SCALE * -1)
        path.lineTo(0.5 * VIEW_SCALE, MATERIAL_DIAMETER * VIEW_SCALE * -1)
        pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 255), 1, QtCore.Qt.SolidLine)
        pen.setCosmetic(True)
        GUIDE_BUSH_U = self.scene.addPath(path, pen)
        #GUIDE_BUSH_U.setBrush(QtGui.QBrush(QtCore.Qt.lightGray , QtCore.Qt.SolidPattern))
        GUIDE_BUSH_U.setBrush(QtGui.QBrush(QtGui.QColor(211, 211, 211, 255), QtCore.Qt.SolidPattern))
        path = QtGui.QPainterPath()
        path.moveTo(0.5 * VIEW_SCALE, MATERIAL_DIAMETER * VIEW_SCALE)
        path.lineTo(0.5 * VIEW_SCALE, (3 - MATERIAL_DIAMETER) * VIEW_SCALE * -1)
        path.lineTo(1 * VIEW_SCALE, (9 - MATERIAL_DIAMETER) * VIEW_SCALE * -1)
        path.lineTo(9.4 * VIEW_SCALE, (7.1 - MATERIAL_DIAMETER) * VIEW_SCALE * -1)
        path.lineTo(10.5 * VIEW_SCALE, (6 - MATERIAL_DIAMETER) * VIEW_SCALE * -1)
        path.lineTo(29.5 * VIEW_SCALE, (6 - MATERIAL_DIAMETER) * VIEW_SCALE * -1)
        path.lineTo(30.2 * VIEW_SCALE, (6.7 - MATERIAL_DIAMETER) * VIEW_SCALE * -1)
        path.lineTo(51.3 * VIEW_SCALE, (6.7 - MATERIAL_DIAMETER) * VIEW_SCALE * -1)
        path.lineTo(52.3 * VIEW_SCALE, (5.7 - MATERIAL_DIAMETER) * VIEW_SCALE * -1)
        path.lineTo(52.3 * VIEW_SCALE, (3.8 - MATERIAL_DIAMETER) * VIEW_SCALE * -1)
        path.lineTo(24.3 * VIEW_SCALE, (3.8 - MATERIAL_DIAMETER) * VIEW_SCALE * -1)
        path.lineTo(22.1 * VIEW_SCALE, (1.6 - MATERIAL_DIAMETER) * VIEW_SCALE * -1)
        path.lineTo(17.1 * VIEW_SCALE, (1.6 - MATERIAL_DIAMETER) * VIEW_SCALE * -1)
        path.lineTo(15.5 * VIEW_SCALE, MATERIAL_DIAMETER * VIEW_SCALE)
        path.lineTo(0.5 * VIEW_SCALE, MATERIAL_DIAMETER * VIEW_SCALE)
        pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 255), 1, QtCore.Qt.SolidLine)
        pen.setCosmetic(True)
        GUIDE_BUSH_L = self.scene.addPath(path, pen)
        #GUIDE_BUSH_L.setBrush(QtGui.QBrush(QtCore.Qt.lightGray, QtCore.Qt.SolidPattern))
        GUIDE_BUSH_L.setBrush(QtGui.QBrush(QtGui.QColor(211, 211, 211, 255), QtCore.Qt.SolidPattern))
        if self.ui.action2_9.isChecked() == False:
            GUIDE_BUSH_U.hide()
            GUIDE_BUSH_L.hide()
        else:
            GUIDE_BUSH_U.show()
            GUIDE_BUSH_L.show()

        #####中心線を描画
        pen = QtGui.QPen(QtGui.QColor(0, 0, 200, 100), 1, QtCore.Qt.DashDotLine)
        pen.setCosmetic(True)
        path = QtGui.QPainterPath()
        path.moveTo(-3001 * VIEW_SCALE, 0)
        path.lineTo(3001 * VIEW_SCALE, 0)
        CENTER_LINE = self.scene.addPath(path, pen)
        if self.ui.action2_15.isChecked() == False:
            CENTER_LINE.hide()
        else:
            CENTER_LINE.show()
        #####各工具の工具軌跡を取得
        pen = QtGui.QPen(QtGui.QColor(255, 255, 255, 255), 1, QtCore.Qt.SolidLine) #線分のスタイル設定
        pen.setCosmetic(True) #線分のスタイル設定を適用
        tools = NC_SIMPLE_PATH(MOVEMENT_DATA, 50 , 1, TOOL_NAME, TOOL_DXF_GEOMETRIO)
        TOOLS.clear()
        color = 50
        for i in tools:
            tool = QtWidgets.QGraphicsPathItem(i)
            pen = QtGui.QPen(QtGui.QColor(0, 0, color, 255), 1, QtCore.Qt.SolidLine) #線分のスタイル設定
            pen.setCosmetic(True) #線分のスタイル設定を適用
            tool.setPen(pen)
            TOOLS.append(tool)
            color += 40
            if color >= 250:
                color = 50
        #####プログラムのテキストを配列化
        if self.ui.action2_6.isChecked() == True:
            APPEND_G50 = 1
        else:
            APPEND_G50 = 0
        if self.ui.action2_14.isChecked() == True:
            _, _, TOOLS_TEXT, _ = NC_PATH(MOVEMENT_DATA, 50, 1, FONT_SIZE, 1, APPEND_G50, TOOL_NAME, TOOL_DXF_GEOMETRIO,)
        else:
            _, _, TOOLS_TEXT, _ = NC_PATH(MOVEMENT_DATA, 50, 1, FONT_SIZE, 0, APPEND_G50, TOOL_NAME, TOOL_DXF_GEOMETRIO)
        TOOL_TEXT_PARENTS = []
        for i, x in enumerate(TOOLS_TEXT):
            TOOL_TEXT_PARENTS.append(QtWidgets.QGraphicsTextItem())
            for y in x:
                y.setParentItem(TOOL_TEXT_PARENTS[i])
                y.show()
            TOOL_TEXT_PARENTS[i].setParentItem(MATERIAL)
            TOOL_TEXT_PARENTS[i].hide()
        #####プログラム座標マーカーを配列化
        if self.ui.action2_6.isChecked() == True:
            APPEND_G50 = 1
        else:
            APPEND_G50 = 0
        if self.ui.action2_14.isChecked() == True:
            _, _, _, TOOLS_POS = NC_PATH(MOVEMENT_DATA, 50, 1, FONT_SIZE, 1, APPEND_G50, TOOL_NAME, TOOL_DXF_GEOMETRIO)
        else:
            _, _, _, TOOLS_POS = NC_PATH(MOVEMENT_DATA, 50, 1, FONT_SIZE, 0, APPEND_G50, TOOL_NAME, TOOL_DXF_GEOMETRIO)
        TOOL_POS_PARENTS = []
        for i, x in enumerate(TOOLS_POS):
            TOOL_POS_PARENTS.append(QtWidgets.QGraphicsTextItem())
            for y in x:
                y.setParentItem(TOOL_POS_PARENTS[i])
                y.show()
            TOOL_POS_PARENTS[i].setParentItem(MATERIAL)
            TOOL_POS_PARENTS[i].hide()
        #####切削工具の準備
        #工具形状を、工具名をキーとして辞書に登録
        TOOL_PAINTER_PATH.clear() #工具に対するDXFファイルパスをクリア
        for x in TOOL_DXF_PATH: #辞書の工具名をxへ代入
            file_path = TOOL_DXF_PATH[x] #工具名に対するDXFファイルパスを取得
            if file_path != "":
                if os.path.exists(file_path):
                    shift_xz = TOOL_DXF_SHIFT[x]
                    offset_xz = TOOL_DXF_OFFSET[x]
                    offset_x = offset_xz[0]
                    offset_z = offset_xz[1]
                    shift_x = shift_xz[0]
                    shift_z = shift_xz[1]
                    painter_path, ret = CONVERT_CLOSED_DXF(file_path, 50, -1, shift_x, shift_z, offset_x, offset_z) #工具形状をQPainterPathとして取得
                    if ret == 0:
                        TOOL_PAINTER_PATH[x] = painter_path #工具名に対するQpainterPathをディクショナリへ保存
                    else:
                        TOOL_PAINTER_PATH[x] = ""
                else:
                    TOOL_PAINTER_PATH[x] = ""
            else:
                TOOL_PAINTER_PATH[x] = ""
        #反転した工具形状を、工具名をキーとして辞書に登録
        TOOL_PAINTER_PATH_REV.clear() #工具に対するDXFファイルパスをクリア
        for x in TOOL_DXF_PATH: #辞書の工具名をxへ代入
            file_path = TOOL_DXF_PATH[x] #工具名に対するDXFファイルパスを取得
            if file_path != "":
                if os.path.exists(file_path):
                    shift_xz = TOOL_DXF_SHIFT[x]
                    offset_xz = TOOL_DXF_OFFSET[x]
                    offset_x = offset_xz[0]
                    offset_z = offset_xz[1]
                    shift_x = shift_xz[0]
                    shift_z = shift_xz[1]
                    painter_path, ret = CONVERT_CLOSED_DXF(file_path, 50, 1,  shift_x, shift_z, offset_x, offset_z) #工具形状をQPainterPathとして取得
                    if ret == 0:
                        TOOL_PAINTER_PATH_REV[x] = painter_path #工具名に対するQpainterPathをディクショナリへ保存
                    else:
                        TOOL_PAINTER_PATH_REV[x] = ""
            else:
                TOOL_PAINTER_PATH_REV[x] = ""
        #表示用の工具形状を、工具名をキーとして辞書に登録
        pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 255), 1, QtCore.Qt.SolidLine) #線分のスタイル設定
        pen.setCosmetic(True) #線分のスタイル設定を適用
        tool_visible = {} #表示用工具パス格納用辞書
        for x in TOOL_NAME: #工具一覧から、各工具名を取得
            if TOOL_PAINTER_PATH[x] != "": #ディクショナリに形状データがあった場合
                tool_visible[x] = self.scene.addPath(TOOL_PAINTER_PATH[x], pen)
                tool_visible[x].hide()
                #tool_visible[x].setBrush(QtGui.QBrush(QtGui.QColor(230, 170, 50, 255), QtCore.Qt.SolidPattern))
                tool_visible[x].setBrush(QtGui.QBrush(QtGui.QColor(230, 170, 50, 255), QtCore.Qt.SolidPattern))
                tool_visible[x].setPos(0, 0)
        #工具基準位置マーカーの描画
        pen = QtGui.QPen(QtGui.QColor(255, 69, 0, 255), 1, QtCore.Qt.SolidLine)
        pen.setCosmetic(True)
        path = QtGui.QPainterPath()
        path.moveTo(0.1 * VIEW_SCALE, 0)
        path.lineTo(-0.1 * VIEW_SCALE, 0)
        CROSS_V = QtWidgets.QGraphicsPathItem(path)
        CROSS_V.setPen(pen)
        path.moveTo(0, 0.1 * VIEW_SCALE)
        path.lineTo(0, -0.1 * VIEW_SCALE)
        CROSS_H = QtWidgets.QGraphicsPathItem(path)
        CROSS_H.setPen(pen)
        #####工具軌跡保存用配列
        qgi_program = []
        qgi_program_rev = []
        qgi_tool = []
        qgi_line = []
        qgi_pos = []
        realtime_tools, realtime_tools_g50 = NC_REALTIME_MOVEMENT(MOVEMENT_DATA) #工具の詳細移動データを取得
        for x in realtime_tools:
            qgi_tool.clear()
            for y in x:
                qgi_line.clear()
                for z in y:
                    qgi_line.append(qgi_pos)
                qgi_tool.append(qgi_line[:])
            qgi_program.append(qgi_tool[:])
            #qgi_program_rev.append(qgi_tool[:])
        for x in realtime_tools:
            qgi_tool.clear()
            for y in x:
                qgi_line.clear()
                for z in y:
                    qgi_line.append(qgi_pos)
                qgi_tool.append(qgi_line[:])
            qgi_program_rev.append(qgi_tool[:])

        path = QtGui.QPainterPath()
        path.moveTo(0, 0)
        path.lineTo(30, 0)
        path.lineTo(30, 30)
        path.lineTo(0, 30)
        path.lineTo(0, 0)
        pen = QtGui.QPen(QtCore.Qt.blue, 1, QtCore.Qt.SolidLine)
        pen.setCosmetic(True)
        MOUSE_R_CLICK_FIRST = self.scene.addPath(path, pen)
        MOUSE_R_CLICK_FIRST.hide()

        path = QtGui.QPainterPath()
        path.moveTo(0, 0)
        path.lineTo(30, 0)
        path.lineTo(30, 30)
        path.lineTo(0, 30)
        path.lineTo(0, 0)
        pen = QtGui.QPen(QtCore.Qt.green, 1, QtCore.Qt.SolidLine)
        pen.setCosmetic(True)
        MOUSE_R_CLICK_SECOND = self.scene.addPath(path, pen)
        MOUSE_R_CLICK_SECOND.hide()

        path = QtGui.QPainterPath()
        path.moveTo(0, 0)
        path.lineTo(30, 0)
        path.lineTo(30, 30)
        path.lineTo(0, 30)
        path.lineTo(0, 0)
        pen = QtGui.QPen(QtCore.Qt.blue, 1, QtCore.Qt.SolidLine)
        pen.setCosmetic(True)
        EX_MOUSE_R_CLICK_FIRST = self.scene.addPath(path, pen)
        EX_MOUSE_R_CLICK_FIRST.hide()

        Z1MIN_TEXT = QtWidgets.QGraphicsTextItem()
        Z1MIN_TEXT.setFont(QtGui.QFont('Times', 10))
        Z1MIN_TEXT.setDefaultTextColor(QtGui.QColor(0, 0, 126, 255))
        Z1MIN_TEXT.setPlainText("Z1min")
        self.scene.addItem(Z1MIN_TEXT)
        Z1MIN_TEXT.setPos(0, 0)
        Z1MIN_TEXT.hide()

        Z1MAX_TEXT = QtWidgets.QGraphicsTextItem()
        Z1MAX_TEXT.setFont(QtGui.QFont('Times', 10))
        Z1MAX_TEXT.setDefaultTextColor(QtGui.QColor(0, 0, 126, 255))
        Z1MAX_TEXT.setPlainText("Z1max")
        self.scene.addItem(Z1MAX_TEXT)
        Z1MAX_TEXT.setPos(0, 0)
        Z1MAX_TEXT.hide()

        X1MIN_TEXT = QtWidgets.QGraphicsTextItem()
        X1MIN_TEXT.setFont(QtGui.QFont('Times', 10))
        X1MIN_TEXT.setDefaultTextColor(QtGui.QColor(0, 0, 126, 255))
        X1MIN_TEXT.setPlainText("X1min")
        self.scene.addItem(X1MIN_TEXT)
        X1MIN_TEXT.setPos(0, 0)
        X1MIN_TEXT.hide()

        X1MAX_TEXT = QtWidgets.QGraphicsTextItem()
        X1MAX_TEXT.setFont(QtGui.QFont('Times', 10))
        X1MAX_TEXT.setDefaultTextColor(QtGui.QColor(0, 0, 126, 255))
        X1MAX_TEXT.setPlainText("X1max")
        self.scene.addItem(X1MAX_TEXT)
        X1MAX_TEXT.setPos(0, 0)
        X1MAX_TEXT.hide()

        Z2MIN_TEXT = QtWidgets.QGraphicsTextItem()
        Z2MIN_TEXT.setFont(QtGui.QFont('Times', 10))
        Z2MIN_TEXT.setDefaultTextColor(QtGui.QColor(126, 0, 0, 255))
        Z2MIN_TEXT.setPlainText("Z2min")
        self.scene.addItem(Z2MIN_TEXT)
        Z2MIN_TEXT.setPos(0, 0)
        Z2MIN_TEXT.hide()

        Z2MAX_TEXT = QtWidgets.QGraphicsTextItem()
        Z2MAX_TEXT.setFont(QtGui.QFont('Times', 10))
        Z2MAX_TEXT.setDefaultTextColor(QtGui.QColor(126, 0, 0, 255))
        Z2MAX_TEXT.setPlainText("Z2max")
        self.scene.addItem(Z2MAX_TEXT)
        Z2MAX_TEXT.setPos(0, 0)
        Z2MAX_TEXT.hide()

        X2MIN_TEXT = QtWidgets.QGraphicsTextItem()
        X2MIN_TEXT.setFont(QtGui.QFont('Times', 10))
        X2MIN_TEXT.setDefaultTextColor(QtGui.QColor(126, 0, 0, 255))
        X2MIN_TEXT.setPlainText("X2min")
        self.scene.addItem(X2MIN_TEXT)
        X2MIN_TEXT.setPos(0, 0)
        X2MIN_TEXT.hide()

        X2MAX_TEXT = QtWidgets.QGraphicsTextItem()
        X2MAX_TEXT.setFont(QtGui.QFont('Times', 10))
        X2MAX_TEXT.setDefaultTextColor(QtGui.QColor(126, 0, 0, 255))
        X2MAX_TEXT.setPlainText("X2max")
        self.scene.addItem(X2MAX_TEXT)
        X2MAX_TEXT.setPos(0, 0)
        X2MAX_TEXT.hide()

        MOUSE_R_CLICK_SECOND = ""
        EX_MOUSE_R_CLICK_SECOND = ""
        MOUSE_R_CLICK_FLAG = 0

        '''#実験用コード
        path = QtGui.QPainterPath()
        path.moveTo(0, 0)
        path.lineTo(100, 0)
        path.lineTo(100, 100)
        path.lineTo(0, 100)
        path.lineTo(0, 0)
        pen = QtGui.QPen(QtCore.Qt.red, 1, QtCore.Qt.SolidLine)
        pen.setCosmetic(True)
        test = self.scene.addPath(path, pen)
        
        for i in self.scene.collidingItems(test, QtCore.Qt.ItemSelectionMode.IntersectsItemShape):
            print(i)
            print(i.pos().x())
            print(i.pos().y())
            tmp = i.shape().toSubpathPolygons()
            for x in tmp:
                x = x.toList()
                for y in x:
                    if test.contains(y):
                        print("INSIDE : X=" + str(y.x()) + " Y=" + str(y.y()))
                    else:
                        print("OUTSIDE : X=" + str(y.x()) + " Y=" + str(y.y()))
        self.scene.removeItem(test)
        '''

        ####################################################################################################
        ####################################################################################################
        ####################################################################################################
        ########################################シミュレーションを実行########################################
        ####################################################################################################
        ####################################################################################################
        ####################################################################################################
        color = 30
        ex_x = 0
        NUM_TOOL = 0
        num_tool_len = len(TOOL_NAME)
        flag_start = 1
        FLAG_END = 0
        run_timer = 0
        self.action2_1_triggered() #centerOn work around
        while(True):########################################プログラム全体のループ処理########################################
            app.processEvents()
            if FLAG_SIMULATION_STARTED == 0:
                break
            #self.ui.listWidget2.setCurrentRow(num_tool)
            ########################################各工具の処理########################################
            name_tool = TOOL_NAME[NUM_TOOL] #各工具を取得
            if TOOL_PAINTER_PATH[name_tool] != "": #ディクショナリに工具形状データがあった場合
                geometrio = TOOL_DXF_GEOMETRIO[name_tool]
                go_x = float(geometrio[1])
                go_y = float(geometrio[0])
                go_x = RND(go_x * VIEW_SCALE)
                go_y = RND(go_y / -2 * VIEW_SCALE)
                MATERIAL.moveBy(go_x * -1, 0)
                tool_visible[name_tool].moveBy(0, go_y)
                self.ui.listWidget2.setCurrentRow(NUM_TOOL)
                each_tool = realtime_tools[NUM_TOOL] #現在の工具の移動座標を取得
                num_line_len = len(each_tool) #各工具の移動数（配列数）
                NUM_LINE = 0 #現在の工具の移動配列番号
                ex_y = 0
                ########################################各工具のループ処理########################################
                while(True):
                    app.processEvents()
                    if FLAG_SIMULATION_STARTED == 0:
                        break
                    #加工開始ならステップを有効にする
                    if flag_start == 1:
                        self.ui.checkBox1.setChecked(True)
                        flag_start = 0

                    #加工終了ならステップを有効にする
                    if NUM_LINE + 1 == num_line_len:
                        tmp_num_tool = NUM_TOOL
                        while(True):
                            app.processEvents()
                            tmp_num_tool += 1
                            if tmp_num_tool < num_tool_len:
                                tmp_name_tool = TOOL_NAME[tmp_num_tool]
                                if TOOL_PAINTER_PATH[tmp_name_tool] != "":
                                    break
                            else:
                                self.ui.checkBox1.setChecked(True)
                                FLAG_END = 1
                                break

                    self.ui.listWidget1.setCurrentRow(TOOLS_LINE_NUM[NUM_TOOL][NUM_LINE])

                    #移動先のプログラムを拡大表示
                    if self.ui.action2_16.isChecked() == True:
                        TOOLS_TEXT[NUM_TOOL][NUM_LINE-1].setScale(TOOLS_TEXT_SCALE)
                        TOOLS_TEXT[NUM_TOOL][NUM_LINE].setScale(TOOLS_TEXT_SCALE * 4.0)

                    #移動先のプログラム座標マーカーを表示
                    if self.ui.action2_16.isChecked() == True:
                        pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 0), 1, QtCore.Qt.SolidLine) #線分のスタイル設定
                        pen.setCosmetic(True) #線分のスタイル設定を適用
                        TOOLS_POS[NUM_TOOL][NUM_LINE-1].setPen(pen)
                        TOOLS_POS[NUM_TOOL][NUM_LINE-1].setBrush(QtGui.QBrush(QtGui.QColor(0, 255, 0, 0), QtCore.Qt.SolidPattern))
                        pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 100), 1, QtCore.Qt.SolidLine) #線分のスタイル設定
                        pen.setCosmetic(True) #線分のスタイル設定を適用
                        TOOLS_POS[NUM_TOOL][NUM_LINE].setPen(pen)
                        TOOLS_POS[NUM_TOOL][NUM_LINE].setBrush(QtGui.QBrush(QtGui.QColor(0, 255, 0, 100), QtCore.Qt.SolidPattern))

                    each_line = each_tool[NUM_LINE] #各行を取得
                    ########################################各工具の各行の移動ループ処理########################################
                    for num_pos, each_pos in enumerate(each_line): #各行の移動座標を取得
                        if FLAG_SIMULATION_STARTED == 0:
                            break

                        if RUN_SPEED > -1:
                            if run_timer >= RUN_SPEED:
                                app.processEvents()
                            run_timer += 1
                            if run_timer > RUN_SPEED:
                                run_timer = 0

                        cur_x = RND((each_pos[0]) * VIEW_SCALE)
                        cur_y = RND((each_pos[1]) * VIEW_SCALE)
                        #材料を移動
                        MATERIAL.moveBy(RND(ex_x - cur_x), 0)
                        #工具軌跡を材料に対して描画
                        tool = TOOL_PAINTER_PATH[name_tool].translated(cur_x + go_x, cur_y +go_y) #NCプログラム座標cur_x、cur_yに工具の原点を移動
                        tool_rev = TOOL_PAINTER_PATH_REV[name_tool].translated(cur_x + go_x, RND((cur_y + go_y)* -1)) #NCプログラム座標cur_x、cur_yに工具の原点を移動
                        qgi = QtWidgets.QGraphicsPathItem(tool) #工具をパスに変換
                        qgi_rev = QtWidgets.QGraphicsPathItem(tool_rev) #工具をパスに変換
                        #if self.ui.action2_2.isChecked() == False:
                        pen = QtGui.QPen(QtGui.QColor(255, 255, 255, 255), 1, QtCore.Qt.SolidLine) #線分のスタイル設定
                        pen.setCosmetic(True) #線分のスタイル設定を適用
                        qgi.setPen(pen)
                        qgi.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255, 255), QtCore.Qt.SolidPattern))
                        qgi_rev.setPen(pen)
                        qgi_rev.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255, 255), QtCore.Qt.SolidPattern))
                        '''
                        else:
                            pen = QtGui.QPen(QtGui.QColor(0, color, 0, 255), 1, QtCore.Qt.SolidLine) #線分のスタイル設定
                            pen.setCosmetic(True) #線分のスタイル設定を適用
                            qgi.setPen(pen)
                            qgi.setBrush(QtGui.QBrush(QtGui.QColor(0, color, 0, 255), QtCore.Qt.SolidPattern))
                            qgi_rev.setPen(pen)
                            qgi_rev.setBrush(QtGui.QBrush(QtGui.QColor(0, color, 0, 255), QtCore.Qt.SolidPattern))
                        '''
                        qgi.setParentItem(MATERIAL) #材料を、工具の親アイテムとする
                        qgi_program[NUM_TOOL][NUM_LINE][num_pos]=qgi
                        if self.ui.action2_5.isChecked() == True:
                            qgi_rev.setParentItem(MATERIAL) #材料を、工具の親アイテムとする
                            qgi_program_rev[NUM_TOOL][NUM_LINE][num_pos]=qgi_rev

                        #工具軌跡線を材料に対して描画
                        if self.ui.action2_3.isChecked() == True:
                            for i, x in enumerate(TOOLS):
                                tmp_name_tool = TOOL_NAME[i]
                                if TOOL_PAINTER_PATH[tmp_name_tool] != "": #ディクショナリに形状データがあった場合
                                    x.show()
                                    x.setParentItem(None)
                                    x.setParentItem(MATERIAL)
                        elif self.ui.action2_4.isChecked() == True:
                            for i, x in enumerate(TOOLS):
                                if i == NUM_TOOL:
                                    x.show()
                                else:
                                    x.hide()
                                x.setParentItem(None)
                                x.setParentItem(MATERIAL)
                        else:
                            for x in TOOLS:
                                x.hide()

                        #プログラムを材料に対して描画
                        if self.ui.action2_7.isChecked() == True:
                            for i, x in enumerate(TOOL_TEXT_PARENTS):
                                tmp_name_tool = TOOL_NAME[i]
                                if TOOL_PAINTER_PATH[tmp_name_tool] != "": #ディクショナリに形状データがあった場合
                                    x.show()
                                    x.setParentItem(None)
                                    x.setParentItem(MATERIAL)
                        elif self.ui.action2_8.isChecked() == True:
                            for i, x in enumerate(TOOL_TEXT_PARENTS):
                                if i == NUM_TOOL:
                                    x.show()
                                else:
                                    x.hide()
                                x.setParentItem(None)
                                x.setParentItem(MATERIAL)
                        else:
                            for x in TOOL_TEXT_PARENTS:
                                x.hide()

                        #プログラム座標マーカーを描画
                        if self.ui.action2_17.isChecked() == True:
                            for i, x in enumerate(TOOL_POS_PARENTS):
                                if i == NUM_TOOL:
                                    x.show()
                                else:
                                    x.hide()
                                x.setParentItem(None)
                                x.setParentItem(MATERIAL)
                        else:
                            for x in TOOL_POS_PARENTS:
                                x.hide()

                        #工具を材料に対して描画
                        if self.ui.action2_19.isChecked() == True:
                            pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 100), 1, QtCore.Qt.SolidLine) #線分のスタイル設定
                            pen.setCosmetic(True) #線分のスタイル設定を適用
                            tool_visible[name_tool].setPen(pen)
                            tool_visible[name_tool].setBrush(QtGui.QBrush(QtGui.QColor(230, 170, 50, 100), QtCore.Qt.SolidPattern))
                        else:
                            pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 255), 1, QtCore.Qt.SolidLine) #線分のスタイル設定
                            pen.setCosmetic(True) #線分のスタイル設定を適用
                            tool_visible[name_tool].setPen(pen)
                            tool_visible[name_tool].setBrush(QtGui.QBrush(QtGui.QColor(230, 170, 50, 255), QtCore.Qt.SolidPattern))
                        tool_visible[name_tool].show()
                        tool_visible[name_tool].moveBy(0, cur_y - ex_y)

                        #工具基準位置マーカーの描画
                        if self.ui.action2_2.isChecked() == False:
                            CROSS_H.hide()
                            CROSS_V.hide()
                        else:
                            CROSS_H.show()
                            CROSS_V.show()
                        CROSS_H.setParentItem(tool_visible[name_tool])
                        CROSS_V.setParentItem(tool_visible[name_tool])

                        ex_x = cur_x
                        ex_y = cur_y

                        #工具原点を画面中心へ移動（指示があった場合）
                        if self.ui.action2_13.isChecked() == True:
                            g50_x = realtime_tools_g50[NUM_TOOL][NUM_LINE][num_pos][0] * VIEW_SCALE
                            g50_y = realtime_tools_g50[NUM_TOOL][NUM_LINE][num_pos][1] * VIEW_SCALE
                            xx = 0
                            yy = 0
                            point = QtCore.QPointF(xx, yy)
                            point_item = tool_visible[name_tool].mapFromScene(point) #シーンに対するアイテムの座標を取得
                            self.ui.graphicsView1.centerOn(point_item.x() - g50_x, point_item.y() * -1 - g50_y)
                        
                        #ガイドブッシュの透明度を変更
                        if self.ui.action2_18.isChecked() == True:
                            pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 100), 1, QtCore.Qt.SolidLine)
                            pen.setCosmetic(True)
                            GUIDE_BUSH_U.setPen(pen)
                            GUIDE_BUSH_L.setPen(pen)
                            GUIDE_BUSH_U.setBrush(QtGui.QBrush(QtGui.QColor(211, 211, 211, 100), QtCore.Qt.SolidPattern))
                            GUIDE_BUSH_L.setBrush(QtGui.QBrush(QtGui.QColor(211, 211, 211, 100), QtCore.Qt.SolidPattern))
                        else:
                            pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 255), 1, QtCore.Qt.SolidLine)
                            pen.setCosmetic(True)
                            GUIDE_BUSH_U.setPen(pen)
                            GUIDE_BUSH_L.setPen(pen)
                            GUIDE_BUSH_U.setBrush(QtGui.QBrush(QtCore.Qt.lightGray , QtCore.Qt.SolidPattern))
                            GUIDE_BUSH_L.setBrush(QtGui.QBrush(QtCore.Qt.lightGray , QtCore.Qt.SolidPattern))
                    #========================================各工具の各行の移動ループ処理　終了========================================
                    ########################################ステップ動作の処理########################################
                    if self.ui.checkBox1.isChecked() == True:
                        self.ui.pushButton3.setEnabled(True)
                        self.ui.pushButton4.setEnabled(True)
                        while(True): #一時停止
                            app.processEvents()
                            if FLAG_SIMULATION_STARTED == 0:
                                break
                            ########################################前の行に戻る########################################
                            if FLAG_BEFORE == 1:
                                MOUSE_R_CLICK_FIRST.hide()
                                if MOUSE_R_CLICK_SECOND != "":
                                    self.scene.removeItem(MOUSE_R_CLICK_SECOND)
                                    MOUSE_R_CLICK_SECOND = ""
                                EX_MOUSE_R_CLICK_FIRST.hide()
                                if EX_MOUSE_R_CLICK_SECOND != "":
                                    self.scene.removeItem(EX_MOUSE_R_CLICK_SECOND)
                                    EX_MOUSE_R_CLICK_SECOND = ""
                                MOUSE_R_CLICK_FLAG = 0
                                Z1MIN_TEXT.hide()
                                Z1MAX_TEXT.hide()
                                X1MIN_TEXT.hide()
                                X1MAX_TEXT.hide()
                                Z2MIN_TEXT.hide()
                                Z2MAX_TEXT.hide()
                                X2MIN_TEXT.hide()
                                X2MAX_TEXT.hide()
                                self.ui.pushButton3.setEnabled(False)
                                self.ui.pushButton4.setEnabled(False)
                                if NUM_LINE -1 >= 0: ####################同一工具内での後退動作####################
                                    for x in qgi_program[NUM_TOOL][NUM_LINE]:
                                        self.scene.removeItem(x)
                                        x = ""
                                    if self.ui.action2_5.isChecked() == True:
                                        for x in qgi_program_rev[NUM_TOOL][NUM_LINE]:
                                            self.scene.removeItem(x)
                                            x = ""
                                    NUM_LINE -= 1
                                    ex_x = MOVEMENT_DATA[NUM_TOOL][NUM_LINE][4] * VIEW_SCALE
                                    ex_y = MOVEMENT_DATA[NUM_TOOL][NUM_LINE][3] * VIEW_SCALE / -2
                                    future_x = MOVEMENT_DATA[NUM_TOOL][NUM_LINE + 1][4] * VIEW_SCALE
                                    future_y = MOVEMENT_DATA[NUM_TOOL][NUM_LINE + 1][3] * VIEW_SCALE / -2
                                    MATERIAL.moveBy(future_x - ex_x, 0) #材料を以前の位置へ移動
                                    tool_visible[name_tool].moveBy(0, ex_y - future_y) #工具を以前の位置へ移動
                                    FLAG_END = 0
                                    self.ui.listWidget1.setCurrentRow(TOOLS_LINE_NUM[NUM_TOOL][NUM_LINE])
                                    #移動先のプログラムを拡大表示
                                    if self.ui.action2_16.isChecked() == True:
                                        TOOLS_TEXT[NUM_TOOL][NUM_LINE + 1].setScale(TOOLS_TEXT_SCALE)
                                        TOOLS_TEXT[NUM_TOOL][NUM_LINE].setScale(TOOLS_TEXT_SCALE * 4.0)
                                    #移動先のプログラム座標マーカーを表示
                                    if self.ui.action2_16.isChecked() == True:
                                        pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 0), 1, QtCore.Qt.SolidLine) #線分のスタイル設定
                                        pen.setCosmetic(True) #線分のスタイル設定を適用
                                        TOOLS_POS[NUM_TOOL][NUM_LINE + 1].setPen(pen)
                                        TOOLS_POS[NUM_TOOL][NUM_LINE + 1].setBrush(QtGui.QBrush(QtGui.QColor(0, 255, 0, 0), QtCore.Qt.SolidPattern))
                                        pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 100), 1, QtCore.Qt.SolidLine) #線分のスタイル設定
                                        pen.setCosmetic(True) #線分のスタイル設定を適用
                                        TOOLS_POS[NUM_TOOL][NUM_LINE].setPen(pen)
                                        TOOLS_POS[NUM_TOOL][NUM_LINE].setBrush(QtGui.QBrush(QtGui.QColor(0, 255, 0, 100), QtCore.Qt.SolidPattern))
                                    #工具原点を画面中心へ移動（指示があった場合）
                                    if self.ui.action2_13.isChecked() == True:
                                        g50_x = MOVEMENT_DATA[NUM_TOOL][NUM_LINE][9] * VIEW_SCALE
                                        g50_y = MOVEMENT_DATA[NUM_TOOL][NUM_LINE][8] * VIEW_SCALE / -2
                                        xx = 0
                                        yy = 0
                                        point = QtCore.QPointF(xx, yy)
                                        point_item = tool_visible[name_tool].mapFromScene(point) #シーンに対するアイテムの座標を取得
                                        self.ui.graphicsView1.centerOn(point_item.x() - g50_x, point_item.y() * -1 - g50_y)
                                else: ####################前の工具への後退動作####################
                                    #移動先のプログラムを拡大表示
                                    TOOLS_TEXT[NUM_TOOL][NUM_LINE].setScale(TOOLS_TEXT_SCALE)
                                    #DXFが設定されている前の工具名を検索
                                    exist_tool = 0
                                    tmp_num_tool = NUM_TOOL
                                    while(True): #前に形状が登録された工具があるか確認
                                        tmp_num_tool -= 1
                                        if tmp_num_tool >= 0:
                                            tmp_name_tool = TOOL_NAME[tmp_num_tool]
                                            if TOOL_PAINTER_PATH[tmp_name_tool] != "":
                                                exist_tool = 1
                                                break
                                        else:
                                            break
                                    if exist_tool == 1: #工具配列番号が0以上場合（前の工具に戻る場合）
                                        #工具軌跡を削除
                                        for x in qgi_program[NUM_TOOL][NUM_LINE]:
                                            self.scene.removeItem(x)
                                            x = ""
                                        if self.ui.action2_5.isChecked() == True:
                                            for x in qgi_program_rev[NUM_TOOL][NUM_LINE]:
                                                self.scene.removeItem(x)
                                                x = ""
                                        future_x = MOVEMENT_DATA[NUM_TOOL][NUM_LINE][4] * VIEW_SCALE
                                        future_y = MOVEMENT_DATA[NUM_TOOL][NUM_LINE][3] * VIEW_SCALE / -2
                                        tool_visible[name_tool].hide() #表示用工具を隠す
                                        tool_visible[name_tool].setPos(0, 0) #表示用工具を初期位置へ戻す
                                        MATERIAL.moveBy(go_x, 0) #材料に適用されたジオメトリオとオフセットをキャンセルする
                                        NUM_TOOL = tmp_num_tool #####工具番号を前に戻す#####
                                        each_tool = realtime_tools[NUM_TOOL]
                                        num_line_len = len(each_tool) #移動行数を取得
                                        NUM_LINE = len(qgi_program[NUM_TOOL]) -1 #ライン番号を前の工具の最終行にする
                                        ex_x = (MOVEMENT_DATA[NUM_TOOL][NUM_LINE][4]) * VIEW_SCALE 
                                        ex_y = MOVEMENT_DATA[NUM_TOOL][NUM_LINE][3] * VIEW_SCALE / -2
                                        name_tool = TOOL_NAME[NUM_TOOL] #各工具を取得
                                        geometrio = TOOL_DXF_GEOMETRIO[name_tool] ############################################################
                                        go_x = float(geometrio[1])
                                        go_y = float(geometrio[0])
                                        go_x = RND(go_x * VIEW_SCALE)
                                        go_y = RND(go_y / -2 * VIEW_SCALE)
                                        MATERIAL.moveBy(go_x * -1, 0) #再度ジオメトリオとオフセットオフセットを有効にする
                                        tool_visible[name_tool].moveBy(0, go_y) #再度ジオメトリオとオフセットオフセットを有効にする
                                        tool_visible[name_tool].moveBy(0, ex_y)# - future_y) #工具を以前の位置へ移動
                                        tool_visible[name_tool].show() #表示用工具を表示
                                        MATERIAL.moveBy(future_x - ex_x, 0) #材料を以前の位置へ移動
                                        color -= 20
                                        self.ui.listWidget1.setCurrentRow(TOOLS_LINE_NUM[NUM_TOOL][NUM_LINE])
                                        self.ui.listWidget2.setCurrentRow(NUM_TOOL)
                                        #工具原点を画面中心へ移動
                                        if self.ui.action2_13.isChecked() == True:
                                            g50_x = MOVEMENT_DATA[NUM_TOOL][NUM_LINE][9] * VIEW_SCALE
                                            g50_y = MOVEMENT_DATA[NUM_TOOL][NUM_LINE][8] * VIEW_SCALE / -2
                                            xx = 0
                                            yy = 0
                                            point = QtCore.QPointF(xx, yy)
                                            point_item = tool_visible[name_tool].mapFromScene(point) #シーンに対するアイテムの座標を取得
                                            self.ui.graphicsView1.centerOn(point_item.x() - g50_x, point_item.y() * -1 - g50_y)
                                self.ui.pushButton3.setEnabled(True)
                                self.ui.pushButton4.setEnabled(True)
                                FLAG_BEFORE = 0
                            ########################################次の行に進む########################################
                            if FLAG_NEXT == 1:
                                FLAG_NEXT = 0
                                if FLAG_END == 0:
                                    self.ui.pushButton3.setEnabled(False)
                                    self.ui.pushButton4.setEnabled(False)
                                    break

                            ########################################ステップ動作のループ処理中の描画処理########################################
                            #工具軌跡線を材料に対して描画
                            if self.ui.action2_3.isChecked() == True:
                                for i, x in enumerate(TOOLS):
                                    tmp_name_tool = TOOL_NAME[i]
                                    if TOOL_PAINTER_PATH[tmp_name_tool] != "": #ディクショナリに形状データがあった場合
                                        x.show()
                                        x.setParentItem(None)
                                        x.setParentItem(MATERIAL)
                            elif self.ui.action2_4.isChecked() == True:
                                for i, x in enumerate(TOOLS):
                                    if i == NUM_TOOL:
                                        x.show()
                                    else:
                                        x.hide()
                                    x.setParentItem(None)
                                    x.setParentItem(MATERIAL)
                            else:
                                for x in TOOLS:
                                    x.hide()

                            #プログラムを材料に対して描画
                            if self.ui.action2_7.isChecked() == True:
                                for i, x in enumerate(TOOL_TEXT_PARENTS):
                                    tmp_name_tool = TOOL_NAME[i]
                                    if TOOL_PAINTER_PATH[tmp_name_tool] != "": #ディクショナリに形状データがあった場合
                                        x.show()
                                        x.setParentItem(None)
                                        x.setParentItem(MATERIAL)
                            elif self.ui.action2_8.isChecked() == True:
                                for i, x in enumerate(TOOL_TEXT_PARENTS):
                                    if i == NUM_TOOL:
                                        x.show()
                                    else:
                                        x.hide()
                                    x.setParentItem(None)
                                    x.setParentItem(MATERIAL)
                            else:
                                for x in TOOL_TEXT_PARENTS:
                                    x.hide()

                            #プログラム座標マーカーを描画
                            if self.ui.action2_17.isChecked() == True:
                                for i, x in enumerate(TOOL_POS_PARENTS):
                                    if i == NUM_TOOL:
                                        x.show()
                                    else:
                                        x.hide()
                                    x.setParentItem(None)
                                    x.setParentItem(MATERIAL)
                            else:
                                for x in TOOL_POS_PARENTS:
                                    x.hide()

                            #工具を材料に対して描画
                            if self.ui.action2_19.isChecked() == True:
                                pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 100), 1, QtCore.Qt.SolidLine) #線分のスタイル設定
                                pen.setCosmetic(True) #線分のスタイル設定を適用
                                tool_visible[name_tool].setPen(pen)
                                tool_visible[name_tool].setBrush(QtGui.QBrush(QtGui.QColor(230, 170, 50, 100), QtCore.Qt.SolidPattern))
                            else:
                                pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 255), 1, QtCore.Qt.SolidLine) #線分のスタイル設定
                                pen.setCosmetic(True) #線分のスタイル設定を適用
                                tool_visible[name_tool].setPen(pen)
                                tool_visible[name_tool].setBrush(QtGui.QBrush(QtGui.QColor(230, 170, 50, 255), QtCore.Qt.SolidPattern))
                            tool_visible[name_tool].show()

                            #工具基準位置マーカーの描画
                            if self.ui.action2_2.isChecked() == False:
                                CROSS_H.hide()
                                CROSS_V.hide()
                            else:
                                CROSS_H.show()
                                CROSS_V.show()
                            CROSS_H.setParentItem(tool_visible[name_tool])
                            CROSS_V.setParentItem(tool_visible[name_tool])

                            #移動先のプログラムを拡大表示
                            if self.ui.action2_16.isChecked() == True:
                                TOOLS_TEXT[NUM_TOOL][NUM_LINE-1].setScale(TOOLS_TEXT_SCALE)
                                TOOLS_TEXT[NUM_TOOL][NUM_LINE].setScale(TOOLS_TEXT_SCALE * 4.0)

                            #ガイドブッシュの透明度を変更
                            if self.ui.action2_18.isChecked() == True:
                                pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 100), 1, QtCore.Qt.SolidLine)
                                pen.setCosmetic(True)
                                GUIDE_BUSH_U.setPen(pen)
                                GUIDE_BUSH_L.setPen(pen)
                                GUIDE_BUSH_U.setBrush(QtGui.QBrush(QtGui.QColor(211, 211, 211, 100), QtCore.Qt.SolidPattern))
                                GUIDE_BUSH_L.setBrush(QtGui.QBrush(QtGui.QColor(211, 211, 211, 100), QtCore.Qt.SolidPattern))
                            else:
                                pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 255), 1, QtCore.Qt.SolidLine)
                                pen.setCosmetic(True)
                                GUIDE_BUSH_U.setPen(pen)
                                GUIDE_BUSH_L.setPen(pen)
                                GUIDE_BUSH_U.setBrush(QtGui.QBrush(QtCore.Qt.lightGray , QtCore.Qt.SolidPattern))
                                GUIDE_BUSH_L.setBrush(QtGui.QBrush(QtCore.Qt.lightGray , QtCore.Qt.SolidPattern))
                    NUM_LINE += 1
                    if NUM_LINE == num_line_len: #現在の工具の移動が終わったか確認
                        break
                    #========================================ステップ動作の処理　終了========================================
                #========================================各工具のループ処理　終了========================================
                if FLAG_SIMULATION_STARTED == 1:
                    tool_visible[name_tool].hide() #移動が終わったので、工具を非表示にする
                    tool_visible[name_tool].setPos(0,0)
                    MATERIAL.moveBy(go_x, 0) #材料に適用されたジオメトリオとオフセットをキャンセルする
                    color += 20
                    if color >= 210:
                        color = 30
                    #移動先のプログラムを拡大表示
                    TOOLS_TEXT[NUM_TOOL][NUM_LINE-1].setScale(TOOLS_TEXT_SCALE)
                    NUM_TOOL += 1
            else: #工具形状が辞書になかった場合
                NUM_TOOL += 1
            if NUM_TOOL == num_tool_len:
                break
            #========================================各工具の処理 終了========================================
        #========================================プログラム全体のループ処理　終了========================================
        self.scene = QtWidgets.QGraphicsScene() #シーンを定義
        self.ui.graphicsView1.setScene(self.scene) #ビューにシーンをセット
        self.ui.pushButton2.setEnabled(False)
        self.ui.pushButton3.setEnabled(False)
        self.ui.pushButton4.setEnabled(False)
        self.ui.pushButton5.setEnabled(True)
        self.ui.menu_1.setEnabled(True)
        self.ui.listWidget1.setEnabled(True)
        self.ui.listWidget2.setEnabled(True)
        self.ui.action2_1.setEnabled(False)
        self.ui.action2_5.setEnabled(True)
        self.ui.action2_6.setEnabled(True)
        self.ui.action2_9.setEnabled(False)
        self.ui.action2_10.setEnabled(False)
        self.ui.action2_11.setEnabled(False)
        self.ui.action2_12.setEnabled(False)
        self.ui.action2_14.setEnabled(False)
        #self.ui.checkBox1.setChecked(False)
        self.ui.plainTextEdit1.setPlainText("")
        FLAG_SIMULATION_STARTED = 0


    #-----工具軌跡のDXFファイル作成用関数----------------------------------------
    def CREATE_DXF_PATH_1(self):
        global MATERIAL_DIAMETER
        global TOOL_DXF_PATH
        global TOOL_NAME
        global MOVEMENT_DATA
        if MAIN_SUB_FLAG == 0:
            f_name = TEXT1_FILENAME
        else:
            f_name = TEXT2_FILENAME
        if f_name:
            f_name = f_name.split(".")
            tool_dxf_path = ""
            list_length = len(f_name)
            i = 0
            while(True):
                tool_dxf_path += f_name[i] + "."
                i += 1
                if i == list_length - 1:
                    break
            tool_dxf_path += "dxf"

        #####切削工具の準備
        #工具形状を、工具名をキーとして辞書に登録
        tool_path = []
        tool_path.clear()
        for x in TOOL_NAME: #辞書の工具名をxへ代入
            file_path = TOOL_DXF_PATH[x] #工具名に対するDXFファイルパスを取得
            if file_path != "":
                if os.path.exists(file_path):
                    dxf_data = ezdxf.readfile(file_path)
                    msp = dxf_data.modelspace()
                    detect = 0
                    tool_layer = ""
                    for x in dxf_data.layers:
                        Layer_name = str(x.dxf.name)
                        if Layer_name.isdigit() == True:
                            n_one = msp.query('*[layer=="' + Layer_name + '"]')
                            CL = 0
                            for i, y in enumerate(n_one.entities):
                                Line_Type = y.dxf.dxftype #線種
                                if Line_Type == "LINE": #線種が直線の場合
                                    CL += 1
                            if CL > 0 and detect == 0:
                                tool_layer = Layer_name
                                detect = 1
                    n_one = msp.query('*[layer=="' + tool_layer + '"]')
                    tool_path.append(n_one) #工具名に対するQpainterPathをディクショナリへ保存
                else:
                    tool_path.append("")
                    msgbox = QtWidgets.QMessageBox()
                    msgbox.setWindowTitle("Massage")
                    msgbox.setText("指定した工具形状ファイルが存在しません。")
                    ret = msgbox.exec()
            else:
                tool_path.append("")

        realtime_tools, _ = NC_REALTIME_MOVEMENT(MOVEMENT_DATA) #工具の詳細移動データを取得

        dwg = ezdxf.new('R2018')
        dwg.layers.remove('0')
        dwg.layers.remove('Defpoints')
        dwg.header['$INSUNITS'] = 4
        dwg.header['$MEASUREMENT'] = 1
        dwg.header['$LUNITS'] = 2
        dwg.header['$AUNITS'] = 0
        msp = dwg.modelspace()

        #####実行

        layer_num = 1
        color = 12

        num_tool = 0
        num_tool_len = len(TOOL_NAME)
        while(True):
            name_tool = TOOL_NAME[num_tool] #各工具を取得
            if tool_path[num_tool] != "": #ディクショナリに形状データがあった場合
                shift_xz = TOOL_DXF_SHIFT[name_tool]
                shift_x = RND(float(shift_xz[0]))
                shift_z = RND(float(shift_xz[1]))
                geometrio_xz = TOOL_DXF_GEOMETRIO[name_tool]
                geometrio_x = RND(float(geometrio_xz[0]) / -2)
                geometrio_z = RND(float(geometrio_xz[1]))
                offset_xz = TOOL_DXF_OFFSET[name_tool]
                offset_x = RND(float(offset_xz[0]) / -2)
                offset_z = RND(float(offset_xz[1]))
                dwg.layers.new(str(layer_num) + '-' + name_tool, dxfattribs={'color': color})
                each_tool = realtime_tools[num_tool] #現在の工具の移動座標を取得
                num_line_len = len(each_tool) #各工具の移動数（配列数）
                num_line = 0 #現在の工具の移動配列番号
                while(True):
                    each_line = each_tool[num_line] #各行を取得
                    for each_pos in each_line: #各行の移動座標を取得
                        cur_x = each_pos[0]
                        cur_y = each_pos[1]
                        for x in tool_path[num_tool]:
                            Line_Type = x.dxf.dxftype #線種
                            if Line_Type == "LINE": #線種が直線の場合
                                cx0 = RND(x.dxf.start[0] + cur_x + shift_z + geometrio_z + offset_z)
                                cy0 = RND(x.dxf.start[1] - cur_y - shift_x - geometrio_x - offset_x)
                                cx1 = RND(x.dxf.end[0] + cur_x + shift_z + geometrio_z + offset_z)
                                cy1 = RND(x.dxf.end[1] - cur_y - shift_x - geometrio_x - offset_x)
                                msp.add_line((cx0, cy0), (cx1, cy1), dxfattribs={'layer': str(layer_num) + '-' + name_tool})
                            elif Line_Type == "ARC": #線種が円弧の場合
                                cx0 = RND(x.dxf.center[0] + cur_x + shift_z + geometrio_z + offset_z)
                                cy0 = RND(x.dxf.center[1] - cur_y - shift_x - geometrio_x - offset_x)
                                R = RND(x.dxf.radius)
                                F = RND(x.dxf.start_angle)
                                N = RND(x.dxf.end_angle)
                                msp.add_arc(center=[cx0, cy0], radius = R, start_angle = F, end_angle = N, dxfattribs = {'layer': str(layer_num) + '-' + name_tool})
                    num_line += 1
                    if num_line == num_line_len: #現在の工具の移動が終わったか確認
                        num_tool += 1
                        layer_num += 1
                        color += 10
                        if color > 255:
                            color = 12
                        break
            else: #工具形状が辞書になかった場合
                num_tool += 1
            if num_tool == num_tool_len:
                break

        dwg.layers.new('MATERIAL', dxfattribs={'color': 0})
        msp.add_line((0, MATERIAL_DIAMETER), (3000, MATERIAL_DIAMETER), dxfattribs={'layer': 'MATERIAL'})
        msp.add_line((3000, MATERIAL_DIAMETER), (3000, MATERIAL_DIAMETER * -1), dxfattribs={'layer': 'MATERIAL'})
        msp.add_line((3000, MATERIAL_DIAMETER * -1), (0, MATERIAL_DIAMETER * -1), dxfattribs={'layer': 'MATERIAL'})
        msp.add_line((0, MATERIAL_DIAMETER * -1), (0, MATERIAL_DIAMETER), dxfattribs={'layer': 'MATERIAL'})

        dwg.layers.new('CENTER LINE', dxfattribs={'color': 150})
        msp.add_line((-3000, 0), (3000, 0), dxfattribs={'layer': 'CENTER LINE'})

        dwg.set_modelspace_vport(0, (0,0))
        dwg.saveas(tool_dxf_path)

        msgbox = QtWidgets.QMessageBox()
        msgbox.setWindowTitle("Massage")
        msgbox.setText("DXFファイルを保存しました。")
        ret = msgbox.exec()


    #-----工具軌跡のDXFファイル作成用関数----------------------------------------
    def CREATE_DXF_PATH_2(self):
        global MATERIAL_DIAMETER
        global TOOL_DXF_PATH
        global TOOL_NAME
        global MOVEMENT_DATA
        if MAIN_SUB_FLAG == 0:
            f_name = TEXT1_FILENAME
        else:
            f_name = TEXT2_FILENAME
        if f_name:
            f_name = f_name.split(".")
            tool_dxf_path = ""
            list_length = len(f_name)
            i = 0
            while(True):
                tool_dxf_path += f_name[i] + "."
                i += 1
                if i == list_length - 1:
                    break
            tool_dxf_path += "dxf"

        #####切削工具の準備
        #工具形状を、工具名をキーとして辞書に登録
        tool_path = []
        tool_path.clear()
        for x in TOOL_NAME: #辞書の工具名をxへ代入
            file_path = TOOL_DXF_PATH[x] #工具名に対するDXFファイルパスを取得
            if file_path != "":
                if os.path.exists(file_path):
                    dxf_data = ezdxf.readfile(file_path)
                    msp = dxf_data.modelspace()
                    detect = 0
                    tool_layer = ""
                    for x in dxf_data.layers:
                        Layer_name = str(x.dxf.name)
                        if Layer_name.isdigit() == True:
                            n_one = msp.query('*[layer=="' + Layer_name + '"]')
                            CL = 0
                            for i, y in enumerate(n_one.entities):
                                Line_Type = y.dxf.dxftype #線種
                                if Line_Type == "LINE": #線種が直線の場合
                                    CL += 1
                            if CL > 0 and detect == 0:
                                tool_layer = Layer_name
                                detect = 1
                    n_one = msp.query('*[layer=="' + tool_layer + '"]')
                    tool_path.append(n_one) #工具名に対するQpainterPathをディクショナリへ保存
                else:
                    tool_path.append("")
                    msgbox = QtWidgets.QMessageBox()
                    msgbox.setWindowTitle("Massage")
                    msgbox.setText("指定した工具形状ファイルが存在しません。")
                    ret = msgbox.exec()
            else:
                tool_path.append("")

        realtime_tools, _ = NC_REALTIME_MOVEMENT(MOVEMENT_DATA) #工具の詳細移動データを取得

        dwg = ezdxf.new('R2018')
        dwg.layers.remove('0')
        dwg.layers.remove('Defpoints')
        dwg.header['$INSUNITS'] = 4
        dwg.header['$MEASUREMENT'] = 1
        dwg.header['$LUNITS'] = 2
        dwg.header['$AUNITS'] = 0
        msp = dwg.modelspace()

        #####実行

        layer_num = 1
        color = 12

        num_tool = 0
        num_tool_len = len(TOOL_NAME)
        while(True):
            name_tool = TOOL_NAME[num_tool] #各工具を取得
            if tool_path[num_tool] != "": #ディクショナリに形状データがあった場合
                shift_xz = TOOL_DXF_SHIFT[name_tool]
                shift_x = RND(float(shift_xz[0]))
                shift_z = RND(float(shift_xz[1]))
                geometrio_xz = TOOL_DXF_GEOMETRIO[name_tool]
                geometrio_x = RND(float(geometrio_xz[0])/ -2)
                geometrio_z = RND(float(geometrio_xz[1]))
                offset_xz = TOOL_DXF_OFFSET[name_tool]
                offset_x = RND(float(offset_xz[0]) / -2)
                offset_z = RND(float(offset_xz[1]))
                dwg.layers.new(str(layer_num) + '-' + name_tool, dxfattribs={'color': color})
                each_tool = realtime_tools[num_tool] #現在の工具の移動座標を取得
                num_line_len = len(each_tool) #各工具の移動数（配列数）
                num_line = 0 #現在の工具の移動配列番号
                while(True):
                    each_line = each_tool[num_line] #各行を取得
                    for each_pos in each_line: #各行の移動座標を取得
                        cur_x = each_pos[0]
                        cur_y = each_pos[1]
                        for x in tool_path[num_tool]:
                            Line_Type = x.dxf.dxftype #線種
                            if Line_Type == "LINE": #線種が直線の場合
                                cx0 = RND(x.dxf.start[0] + cur_x + shift_z + geometrio_z + offset_z)
                                cy0 = RND(x.dxf.start[1] - cur_y - shift_x - geometrio_x - offset_x)
                                cx1 = RND(x.dxf.end[0] + cur_x + shift_z + geometrio_z + offset_z)
                                cy1 = RND(x.dxf.end[1] - cur_y - shift_x - geometrio_x - offset_x)
                                msp.add_line((cx0, cy0), (cx1, cy1), dxfattribs={'layer': str(layer_num) + '-' + name_tool})
                                cx0 = RND(x.dxf.start[0] + cur_x + shift_z + geometrio_z + offset_z)
                                cy0 = RND(x.dxf.start[1] * -1 + cur_y + shift_x + geometrio_x + offset_x)
                                cx1 = RND(x.dxf.end[0] + cur_x + shift_z + geometrio_z + offset_z)
                                cy1 = RND(x.dxf.end[1] * -1 + cur_y + shift_x + geometrio_x + offset_x)
                                msp.add_line((cx0, cy0), (cx1, cy1), dxfattribs={'layer': str(layer_num) + '-' + name_tool})
                            elif Line_Type == "ARC": #線種が円弧の場合
                                cx0 = RND(x.dxf.center[0] + cur_x + shift_z + geometrio_z + offset_z)
                                cy0 = RND(x.dxf.center[1] - cur_y - shift_x - geometrio_x - offset_x)
                                R = RND(x.dxf.radius)
                                F = RND(x.dxf.start_angle)
                                N = RND(x.dxf.end_angle)
                                msp.add_arc(center=[cx0, cy0], radius = R, start_angle = F, end_angle = N, dxfattribs = {'layer': str(layer_num) + '-' + name_tool})
                                cx0 = RND(x.dxf.center[0] + cur_x + shift_z)
                                cy0 = RND(x.dxf.center[1] * -1 + cur_y + shift_x)
                                R = RND(x.dxf.radius)
                                F = RND(x.dxf.start_angle * -1)
                                N = RND(x.dxf.end_angle * -1)
                                msp.add_arc(center=[cx0, cy0], radius = R, start_angle = N, end_angle = F, dxfattribs = {'layer': str(layer_num) + '-' + name_tool})
                    num_line += 1
                    if num_line == num_line_len: #現在の工具の移動が終わったか確認
                        num_tool += 1
                        layer_num += 1
                        color += 10
                        if color > 255:
                            color = 12
                        break
            else: #工具形状が辞書になかった場合
                num_tool += 1
            if num_tool == num_tool_len:
                break

        dwg.layers.new('MATERIAL', dxfattribs={'color': 0})
        msp.add_line((0, MATERIAL_DIAMETER), (3000, MATERIAL_DIAMETER), dxfattribs={'layer': 'MATERIAL'})
        msp.add_line((3000, MATERIAL_DIAMETER), (3000, MATERIAL_DIAMETER * -1), dxfattribs={'layer': 'MATERIAL'})
        msp.add_line((3000, MATERIAL_DIAMETER * -1), (0, MATERIAL_DIAMETER * -1), dxfattribs={'layer': 'MATERIAL'})
        msp.add_line((0, MATERIAL_DIAMETER * -1), (0, MATERIAL_DIAMETER), dxfattribs={'layer': 'MATERIAL'})

        dwg.layers.new('CENTER LINE', dxfattribs={'color': 150})
        msp.add_line((-3000, 0), (3000, 0), dxfattribs={'layer': 'CENTER LINE'})

        dwg.set_modelspace_vport(0, (0,0))
        dwg.saveas(tool_dxf_path)

        msgbox = QtWidgets.QMessageBox()
        msgbox.setWindowTitle("Massage")
        msgbox.setText("DXFファイルを保存しました。")
        ret = msgbox.exec()


    #-----工具軌跡のDXFファイル作成用関数----------------------------------------
    def CREATE_DXF_PATH_3(self):
        global MATERIAL_DIAMETER
        global TOOL_DXF_PATH
        global TOOL_NAME
        global MOVEMENT_DATA
        if MAIN_SUB_FLAG == 0:
            f_name = TEXT1_FILENAME
        else:
            f_name = TEXT2_FILENAME
        if f_name:
            f_name = f_name.split(".")
            tool_dxf_path = ""
            list_length = len(f_name)
            i = 0
            while(True):
                tool_dxf_path += f_name[i] + "."
                i += 1
                if i == list_length - 1:
                    break
            tool_dxf_path += "dxf"

        #####切削工具の準備
        #工具形状を、工具名をキーとして辞書に登録
        tool_path = []
        tool_path.clear()
        for x in TOOL_NAME: #辞書の工具名をxへ代入
            file_path = TOOL_DXF_PATH[x] #工具名に対するDXFファイルパスを取得
            if file_path != "":
                if os.path.exists(file_path):
                    dxf_data = ezdxf.readfile(file_path)
                    msp = dxf_data.modelspace()
                    detect = 0
                    tool_layer = ""
                    for x in dxf_data.layers:
                        Layer_name = str(x.dxf.name)
                        if Layer_name.isdigit() == True:
                            n_one = msp.query('*[layer=="' + Layer_name + '"]')
                            CL = 0
                            for i, y in enumerate(n_one.entities):
                                Line_Type = y.dxf.dxftype #線種
                                if Line_Type == "LINE": #線種が直線の場合
                                    CL += 1
                            if CL > 0 and detect == 0:
                                tool_layer = Layer_name
                                detect = 1
                    n_one = msp.query('*[layer=="' + tool_layer + '"]')
                    tool_path.append(n_one) #工具名に対するQpainterPathをディクショナリへ保存
                else:
                    tool_path.append("")
                    msgbox = QtWidgets.QMessageBox()
                    msgbox.setWindowTitle("Massage")
                    msgbox.setText("指定した工具形状ファイルが存在しません。")
                    ret = msgbox.exec()
            else:
                tool_path.append("")

        realtime_tools, _ = NC_REALTIME_MOVEMENT(MOVEMENT_DATA) #工具の詳細移動データを取得

        dwg = ezdxf.new('R2018')
        dwg.layers.remove('0')
        dwg.layers.remove('Defpoints')
        dwg.header['$INSUNITS'] = 4
        dwg.header['$MEASUREMENT'] = 1
        dwg.header['$LUNITS'] = 2
        dwg.header['$AUNITS'] = 0
        msp = dwg.modelspace()

        #####実行

        layer_num = 1
        color = 12

        num_tool = 0
        num_tool_len = len(TOOL_NAME)
        while(True):
            name_tool = TOOL_NAME[num_tool] #各工具を取得
            if tool_path[num_tool] != "": #ディクショナリに形状データがあった場合
                shift_xz = TOOL_DXF_SHIFT[name_tool]
                shift_x = RND(float(shift_xz[0]))
                shift_z = RND(float(shift_xz[1]))
                geometrio_xz = TOOL_DXF_GEOMETRIO[name_tool]
                geometrio_x = RND(float(geometrio_xz[0]) / -2)
                geometrio_z = RND(float(geometrio_xz[1]))
                offset_xz = TOOL_DXF_OFFSET[name_tool]
                offset_x = RND(float(offset_xz[0]) / -2)
                offset_z = RND(float(offset_xz[1]))
                dwg.layers.new(str(layer_num) + '-' + name_tool, dxfattribs={'color': color})
                each_tool = realtime_tools[num_tool] #現在の工具の移動座標を取得
                num_line_len = len(each_tool) #各工具の移動数（配列数）
                num_line = 0 #現在の工具の移動配列番号
                while(True):
                    each_line = each_tool[num_line] #各行を取得
                    for each_pos in each_line: #各行の移動座標を取得
                        cur_x = each_pos[0]
                        cur_y = each_pos[1]
                        for x in tool_path[num_tool]:
                            Line_Type = x.dxf.dxftype #線種
                            if Line_Type == "LINE": #線種が直線の場合
                                cx0 = RND(x.dxf.start[0] + cur_x + shift_z + geometrio_z + offset_z)
                                cy0 = RND(x.dxf.start[1] - cur_y - shift_x - geometrio_x - offset_x)
                                cx1 = RND(x.dxf.end[0] + cur_x + shift_z + geometrio_z + offset_z)
                                cy1 = RND(x.dxf.end[1] - cur_y - shift_x - geometrio_x - offset_x)
                                msp.add_line((cx0, cy0), (cx1, cy1), dxfattribs={'layer': str(layer_num) + '-' + name_tool})
                            elif Line_Type == "ARC": #線種が円弧の場合
                                cx0 = RND(x.dxf.center[0] + cur_x + shift_z + geometrio_z + offset_z)
                                cy0 = RND(x.dxf.center[1] - cur_y - shift_x - geometrio_x - offset_x)
                                R = RND(x.dxf.radius)
                                F = RND(x.dxf.start_angle)
                                N = RND(x.dxf.end_angle)
                                msp.add_arc(center=[cx0, cy0], radius = R, start_angle = F, end_angle = N, dxfattribs = {'layer': str(layer_num) + '-' + name_tool})
                    num_line += 1
                    if num_line == num_line_len: #現在の工具の移動が終わったか確認
                        layer_num += 1
                        color += 10
                        if color > 255:
                            color = 12
                        break
                dwg.layers.new(str(layer_num) + '-' + name_tool + 'rev', dxfattribs={'color': color})
                each_tool = realtime_tools[num_tool] #現在の工具の移動座標を取得
                num_line_len = len(each_tool) #各工具の移動数（配列数）
                num_line = 0 #現在の工具の移動配列番号
                while(True):
                    each_line = each_tool[num_line] #各行を取得
                    for each_pos in each_line: #各行の移動座標を取得
                        cur_x = each_pos[0]
                        cur_y = each_pos[1]
                        for x in tool_path[num_tool]:
                            Line_Type = x.dxf.dxftype #線種
                            if Line_Type == "LINE": #線種が直線の場合
                                cx0 = RND(x.dxf.start[0] + cur_x + shift_z + geometrio_z + offset_z)
                                cy0 = RND(x.dxf.start[1] * -1 + cur_y + shift_x + geometrio_x + offset_x)
                                cx1 = RND(x.dxf.end[0] + cur_x + shift_z + geometrio_z + offset_z)
                                cy1 = RND(x.dxf.end[1] * -1 + cur_y + shift_x + geometrio_x + offset_x)
                                msp.add_line((cx0, cy0), (cx1, cy1), dxfattribs={'layer': str(layer_num) + '-' + name_tool + 'rev'})
                            elif Line_Type == "ARC": #線種が円弧の場合
                                cx0 = RND(x.dxf.center[0] + cur_x + shift_z + geometrio_z + offset_z)
                                cy0 = RND(x.dxf.center[1] * -1 + cur_y + shift_x + geometrio_x + offset_x)
                                R = RND(x.dxf.radius)
                                F = RND(x.dxf.start_angle * -1)
                                N = RND(x.dxf.end_angle * -1)
                                msp.add_arc(center=[cx0, cy0], radius = R, start_angle = N, end_angle = F, dxfattribs = {'layer': str(layer_num) + '-' + name_tool + 'rev'})
                    num_line += 1
                    if num_line == num_line_len: #現在の工具の移動が終わったか確認
                        num_tool += 1
                        layer_num += 1
                        color += 1
                        break
            else: #工具形状が辞書になかった場合
                num_tool += 1
            if num_tool == num_tool_len:
                break

        dwg.layers.new('MATERIAL', dxfattribs={'color': 0})
        msp.add_line((0, MATERIAL_DIAMETER), (3000, MATERIAL_DIAMETER), dxfattribs={'layer': 'MATERIAL'})
        msp.add_line((3000, MATERIAL_DIAMETER), (3000, MATERIAL_DIAMETER * -1), dxfattribs={'layer': 'MATERIAL'})
        msp.add_line((3000, MATERIAL_DIAMETER * -1), (0, MATERIAL_DIAMETER * -1), dxfattribs={'layer': 'MATERIAL'})
        msp.add_line((0, MATERIAL_DIAMETER * -1), (0, MATERIAL_DIAMETER), dxfattribs={'layer': 'MATERIAL'})

        dwg.layers.new('CENTER LINE', dxfattribs={'color': 150})
        msp.add_line((-3000, 0), (3000, 0), dxfattribs={'layer': 'CENTER LINE'})

        dwg.set_modelspace_vport(0, (0,0))
        dwg.saveas(tool_dxf_path)

        msgbox = QtWidgets.QMessageBox()
        msgbox.setWindowTitle("Massage")
        msgbox.setText("DXFファイルを保存しました。")
        ret = msgbox.exec()






























########################################定型文########################################
#####Pysideのウィンドウ処理クラス
class MainWindow2(QtWidgets.QMainWindow): #QtWidgets.QMainWindowを継承。
    def __init__(self, parent = None): #クラス初期化時にのみ実行される関数（コンストラクタと呼ばれる）。
        super().__init__(parent) #親クラスのコンストラクタを呼び出す（親クラスのコンストラクタを再利用したい場合）。指定する引数は、親クラスのコンストラクタの引数からselfを除いた引数。
        self.ui = Ui_MainWindow2() #uiクラスの作成。Ui_MainWindowのMainWindowは、QT DesignerのobjectNameで設定した名前。
        self.ui.setupUi(self) #uiクラスの設定。
######################################################################################

        self.ui.comboBox1.addItems(["0.01", "0.015", "0.02", "0.03", "0.035", "0.04", "0.045", "0.05", "0.055", "0.06", "0.065", "0.07", "0.075", "0.08", "0.085", "0.09", "0.095", "0.1"]) #####コンボボックスにアイテムを追加
        self.ui.comboBox1.setCurrentIndex(1) #####コンボボックスのアイテムを選択
        self.ui.comboBox2.addItems(["0.01", "0.015", "0.02", "0.03", "0.035", "0.04", "0.045", "0.05", "0.055", "0.06", "0.065", "0.07", "0.075", "0.08", "0.085", "0.09", "0.095", "0.1"]) #####コンボボックスにアイテムを追加
        self.ui.comboBox2.setCurrentIndex(3) #####コンボボックスのアイテムを選択
        self.ui.comboBox3.addItems(["500", "1000", "1500", "2000","2500", "3000", "3500", "4000", "4500", "5000", "5500", "6000", "6500", "7000", "7500", "8000", "8500", "9000", "9500", "10000"]) #####コンボボックスにアイテムを追加
        self.ui.comboBox3.setCurrentIndex(8) #####コンボボックスのアイテムを選択
        self.ui.comboBox4.addItems(["0.05", "0.1", "0.15", "0.2", "0.25", "0.3", "0.35", "0.4", "0.45", "0.5"]) #####コンボボックスにアイテムを追加
        self.ui.comboBox4.setCurrentIndex(3) #####コンボボックスのアイテムを選択
        #-----シグナルにメッソドを関連付け----------------------------------------
        self.ui.pushButton1.clicked.connect(self.pushButton1_clicked) #pushButton1は、QT DesignerのobjectNameで設定した名前で、pushButton1_clickedは任意の関数名
        self.ui.pushButton2.clicked.connect(self.pushButton2_clicked) #pushButton2は、QT DesignerのobjectNameで設定した名前で、pushButton2_clickedは任意の関数名
        self.ui.comboBox1.currentIndexChanged.connect(self.comboBox1_currentIndexChanged)
        self.ui.comboBox2.currentIndexChanged.connect(self.comboBox2_currentIndexChanged)
        self.ui.comboBox3.currentIndexChanged.connect(self.comboBox3_currentIndexChanged)
        self.ui.comboBox4.currentIndexChanged.connect(self.comboBox4_currentIndexChanged)
        self.ui.checkBox1.clicked.connect(self.checkBox1_clicked)
        global SETTING_PATH_DXFtoNC
        if os.path.exists(SETTING_PATH_DXFtoNC):
            self.SETTINGS_READ()
        else:
            self.SETTINGS_SAVE()

    def comboBox1_currentIndexChanged(self):
        self.SETTINGS_SAVE()
    def comboBox2_currentIndexChanged(self):
        self.SETTINGS_SAVE()
    def comboBox3_currentIndexChanged(self):
        self.SETTINGS_SAVE()
    def comboBox4_currentIndexChanged(self):
        self.SETTINGS_SAVE()
    def checkBox1_clicked(self):
        self.SETTINGS_SAVE()


    #-----pushButton1用イベント処理----------------------------------------
    def pushButton1_clicked(self):
    #####ファイル読込み
        dxf_data = ""
    
        filepath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "",'dxf File (*.dxf)')
        if filepath:
            f = open(filepath, "r")

            dxf_data = ezdxf.readfile(filepath)
            msp = dxf_data.modelspace()

            #####番号のレイヤー名のみ摘出
            Layer_num = []
            for x in dxf_data.layers:
                Layer_name = str(x.dxf.name)
                if Layer_name.isdigit() == True:
                    n_one = msp.query('*[layer=="' + Layer_name + '"]')
                    CL = 0
                    CC = 0
                    for i, y in enumerate(n_one.entities):
                        Line_Type = y.dxf.dxftype #線種
                        if Line_Type == "LINE": #線種が直線の場合
                            CL += 1
                        elif Line_Type == "CIRCLE": #線種が円の場合（移動線の開始点とする）
                            CC += 1
                    if CL > 0 and CC == 1:
                        Layer_num.append(Layer_name)

            line_flag = 0
            ret = QtWidgets.QMessageBox.information(None, "Message", "線分データは、一筆書きで描かれていますか？", QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
            if ret == QtWidgets.QMessageBox.Yes:
                line_flag = 1

            line = {}
            NC_line = []
            PROGRAM = []
            StartPointFlag = 0
            #####レイヤー毎の処理
            for x in Layer_num:
                line.clear()
                n_one = msp.query('*[layer=="' + x + '"]')
                #####レイヤー内にあるアイテム毎の処理
                for i, y in enumerate(n_one.entities):
                    Line_Type = y.dxf.dxftype #線種
                    if Line_Type == "LINE": #線種が直線の場合
                        if y.dxf.start != y.dxf.end: #始点と終点が同一点ではない場合
                            cx0 = RND(y.dxf.start[0])
                            cy0 = RND(y.dxf.start[1])
                            cx1 = RND(y.dxf.end[0])
                            cy1 = RND(y.dxf.end[1])
                            line[str(i) + "_T"] = Line_Type
                            line[str(i) + "_S"] = [cx0, cy0] #始点
                            line[str(i) + "_E"] = [cx1, cy1] #終点
                    elif Line_Type == "ARC": #線種が円弧の場合
                        cx0 = RND(y.start_point[0]) #反時計回りの始まりのX
                        cy0 = RND(y.start_point[1]) #反時計回りの始まりのY
                        cx1 = RND(y.end_point[0]) #反時計周りの終わりのX
                        cy1 = RND(y.end_point[1]) #反時計周りの終わりのY
                        cx2 = RND(y.dxf.center[0])
                        cy2 = RND(y.dxf.center[1])
                        line[str(i) + "_T"] = Line_Type
                        line[str(i) + "_S"] = [cx0, cy0] #始点
                        line[str(i) + "_E"] = [cx1, cy1] #終点
                        line[str(i) + "_C"] = [cx2, cy2] #円弧の中心位置
                        line[str(i) + "_R"] = RND(y.dxf.radius)
                        #print(y.dxf.start_angle) #反時計回りの始まりの角度
                        #print(y.dxf.end_angle) #反時計周りの終わりの角度
                        #print(y.dxf.radius) #円の半径
                    elif Line_Type == "CIRCLE": #線種が円の場合（移動線の開始点とする）
                        cx0 = RND(y.dxf.center[0])
                        cy0 = RND(y.dxf.center[1])
                        line_start_point = [cx0, cy0] #円の中心点
                        StartPointFlag = 1 #移動線の開始点有りとする
                NC_line.clear()
                if StartPointFlag == 0: #移動線の開始点が無い場合
                    msgbox = QtWidgets.QMessageBox()
                    msgbox.setWindowTitle("Message")
                    msgbox.setText("Need to plot starting point(circle).")
                    ret = msgbox.exec()
                    break
                else:
                    keys = [k for k, v in line.items() if v == line_start_point] #移動線の開始点を有する辞書キーを検索
                    if len(keys) == 0: #移動線の開始点を有する辞書キーが無い場合はエラーとする
                        msgbox = QtWidgets.QMessageBox()
                        msgbox.setWindowTitle("Message")
                        msgbox.setText("Starting point exist but it does not match to any line.")
                        ret = msgbox.exec()
                        break
                    elif len(keys) > 1: #移動線の開始点を有する辞書キーが２つ以上あった場合はエラーとする
                        msgbox = QtWidgets.QMessageBox()
                        msgbox.setWindowTitle("Message")
                        msgbox.setText("Starting point must be only one point on a line.")
                        ret = msgbox.exec()
                        break
                    else:
                        #####開始点の処理
                        NC_line.append([line_start_point, "L", "", ""]) #移動線の開始点を配列化
                        start_point = line_start_point #次の線分の開始座標とする
                    if line_flag == 0:
                        loop_num = 0
                        while(True):
                            #####以後の座標の処理
                            keys = [k for k, v in line.items() if v == start_point] #前の座標を有する辞書キーを検索
                            if len(keys) == 0: #該当する座標が無い場合は、移動線の終端迄来たとし、処理を終了する
                                break
                            elif len(keys) > 1 and loop_num > 0: #開始座標を有する辞書キーが２つ以上あった場合はエラーとする（2線目以降）
                                msgbox = QtWidgets.QMessageBox()
                                msgbox.setWindowTitle("Message")
                                msgbox.setText("Point must be only one on a line.")
                                ret = msgbox.exec()
                                break
                            else:
                                p_num, p_com = keys[0].split("_") #辞書キーを番号とコマンドに分離する
                                if p_com == "S":
                                    dist_point = line[p_num + "_E"] #検索したキーにSが含まれた場合、Eを有するキーの座標を線分の終点とする
                                elif p_com == "E":
                                    dist_point = line[p_num + "_S"] #検索したキーにEが含まれた場合、Sを有するキーの座標を線分の終点とする
                                line[p_num + "_S"] = ["*", "*"] #座標を*で埋め、検索に掛からないようにする（使用済みにする）
                                line[p_num + "_E"] = ["*", "*"] #座標を*で埋め、検索に掛からないようにする（使用済みにする）
                                if line[p_num + "_T"] == "LINE":
                                    NC_line.append([dist_point, "L", "", ""]) #終点を線分として配列化
                                elif line[p_num + "_T"] == "ARC":
                                    cnt = line[p_num + "_C"]
                                    ret = ROTATION_DIRECTION_DETECTOR(start_point[0], start_point[1], dist_point[0], dist_point[1], cnt[0], cnt[1]) #円弧がG2とG3の何れか判定
                                    r = str(line[p_num + "_R"])
                                    NC_line.append([dist_point, "R", ret, r]) #終点を円弧として配列化
                                start_point = dist_point #次の線分の開始座標とする
                            loop_num += 1
                    else:
                        key_num = 1
                        while(True):
                            if (str(key_num) + "_T" in line.keys()) == True:
                                #####以後の座標の処理
                                #start_point = line[str(key_num) + "_S"] #検索したキーにSが含まれた場合、Eを有するキーの座標を線分の終点とする
                                dist_point = line[str(key_num) + "_E"] #検索したキーにEが含まれた場合、Sを有するキーの座標を線分の終点とする
                                if start_point[0] == dist_point[0] and start_point[1] == dist_point[1]: #ARCは反時計回りで始点と終点が決まるので
                                    dist_point = line[str(key_num) + "_S"]
                                if line[str(key_num) + "_T"] == "LINE":
                                    NC_line.append([dist_point, "L", "", ""]) #終点を線分として配列化
                                elif line[str(key_num)+ "_T"] == "ARC":
                                    cnt = line[str(key_num) + "_C"]
                                    ret = ROTATION_DIRECTION_DETECTOR(start_point[0], start_point[1], dist_point[0], dist_point[1], cnt[0], cnt[1]) #円弧がG2とG3の何れか判定
                                    r = str(line[str(key_num) + "_R"])
                                    NC_line.append([dist_point, "R", ret, r]) #終点を円弧として配列化
                                start_point = dist_point #次の線分の開始座標とする
                            else:
                                break
                            key_num += 1
                PROGRAM.append(NC_line[:]) #####内容を、参照ではなく、コピーする

            PROGRAM_TEXT = ""
            #####レイヤー毎の処理
            for i, x in enumerate(PROGRAM): #iは各レイヤーの番号　xは軌跡
                PROGRAM_TEXT += "G25\r\n"
                PROGRAM_TEXT += "M3 S" + self.ui.comboBox3.currentText() + "\r\n"
                PROGRAM_TEXT += "G26\r\n"
                TOOL_NUM = "T" + str(i + 1) +"00" #工具番号
                TOOL_OFFSET = "T" + str(i + 1) #オフセット番号
                PROGRAM_TEXT += TOOL_NUM + "\r\n"
                POINT_COUNT = len(x)
                #####レイヤー内にあるアイテム毎の処理
                for j, y in enumerate(x): #jは軌跡上の座標番号　yは座標と種類
                    POS = y[0] #座標
                    G_TYPE = y[1] #線種
                    R_DIRECTION = y[2] # G2かG3
                    R_LENGTH = y[3] #半径値
                    #####開始点の処理
                    if j == 0:
                        PROGRAM_TEXT += "G0 X" + str(POS[1] * 2) + " Z" + str(POS[0]) + " " + TOOL_OFFSET + "\r\n"
                        OUTSIDE_DIAMETER = POS[1] - 0.5 #材料外径
                        EX_POS = POS
                    ######座標が終点の場合
                    elif j == POINT_COUNT - 1:
                        G_CODE , F_CODE = self.LINE_CHECK(EX_POS, POS, OUTSIDE_DIAMETER)
                        if G_TYPE == "L":
                            #####G1の場合
                            if G_CODE == "G1":
                                if EX_POS[0] == POS[0]: #Zが直線の場合
                                    PROGRAM_TEXT += "G1 X" + str(POS[1] * 2) + " " + F_CODE + "\r\n"
                                    if POS[0] >= 0 and POS[1] <= OUTSIDE_DIAMETER and self.ui.checkBox1.isChecked() == True:
                                        PROGRAM_TEXT += "G4 U" + self.ui.comboBox4.currentText() + "\r\n"
                                elif EX_POS[1] == POS[1]: #Xが直線の場合
                                    PROGRAM_TEXT += "G1 Z" + str(POS[0]) + " " + F_CODE + "\r\n"
                                    if POS[0] >= 0 and POS[1] <= OUTSIDE_DIAMETER and self.ui.checkBox1.isChecked() == True:
                                        PROGRAM_TEXT += "G4 U" + self.ui.comboBox4.currentText() + "\r\n"
                                else: #テーパーの場合
                                    PROGRAM_TEXT += "G1 X" + str(POS[1] * 2) + " Z" + str(POS[0]) + " " + F_CODE + "\r\n"
                            #####G1の場合
                            else:
                                if EX_POS[0] == POS[0]: #Zが直線の場合
                                    PROGRAM_TEXT += "G0 X" + str(POS[1] * 2) + "\r\n"
                                    if POS[0] >= 0 and POS[1] <= OUTSIDE_DIAMETER and self.ui.checkBox1.isChecked() == True:
                                        PROGRAM_TEXT += "G4 U" + self.ui.comboBox4.currentText() + "\r\n"
                                elif EX_POS[1] == POS[1]: #Xが直線の場合
                                    PROGRAM_TEXT += "G0 Z" + str(POS[0]) + "\r\n"
                                    if POS[0] >= 0 and POS[1] <= OUTSIDE_DIAMETER and self.ui.checkBox1.isChecked() == True:
                                        PROGRAM_TEXT += "G4 U" + self.ui.comboBox4.currentText() + "\r\n"
                                else: #テーパーの場合
                                    PROGRAM_TEXT += "G0 X" + str(POS[1] * 2) + " Z" + str(POS[0]) + "\r\n"
                        #####G2、G3の場合
                        elif G_TYPE == "R":
                            PROGRAM_TEXT += R_DIRECTION + " X" + str(POS[1] * 2) + " Z" + str(POS[0]) + " R" + str(R_LENGTH) + " F" +  self.ui.comboBox1.currentText() + "\r\n"
                        PROGRAM_TEXT += "T0\r\n\r\n"
                    ######座標が工具軌跡上に有る場合
                    else:
                        G_CODE , F_CODE = self.LINE_CHECK(EX_POS, POS, OUTSIDE_DIAMETER)
                        if G_TYPE == "L":
                            #####G1の場合
                            if G_CODE == "G1":
                                if EX_POS[0] == POS[0]:  #Zが直線の場合
                                    PROGRAM_TEXT += "G1 X" + str(POS[1] * 2) + " " + F_CODE + "\r\n"
                                    if POS[0] >= 0 and POS[1] <= OUTSIDE_DIAMETER and self.ui.checkBox1.isChecked() == True:
                                        PROGRAM_TEXT += "G4 U" + self.ui.comboBox4.currentText() + "\r\n"
                                elif EX_POS[1] == POS[1]: #Xが直線の場合
                                    PROGRAM_TEXT += "G1 Z" + str(POS[0]) + " " + F_CODE + "\r\n"
                                    if POS[0] >= 0 and POS[1] <= OUTSIDE_DIAMETER and self.ui.checkBox1.isChecked() == True:
                                        PROGRAM_TEXT += "G4 U" + self.ui.comboBox4.currentText() + "\r\n"
                                else: #テーパーの場合
                                    PROGRAM_TEXT += "G1 X" + str(POS[1] * 2) + " Z" + str(POS[0]) + " " + F_CODE + "\r\n"
                            #####G0の場合
                            else:
                                if EX_POS[0] == POS[0]: #Zが直線の場合
                                    PROGRAM_TEXT += "G0 X" + str(POS[1] * 2) + "\r\n"
                                    if POS[0] >= 0 and POS[1] <= OUTSIDE_DIAMETER and self.ui.checkBox1.isChecked() == True:
                                        PROGRAM_TEXT += "G4 U" + self.ui.comboBox4.currentText() + "\r\n"
                                elif EX_POS[1] == POS[1]: #Xが直線の場合
                                    PROGRAM_TEXT += "G0 Z" + str(POS[0]) + "\r\n"
                                    if POS[0] >= 0 and POS[1] <= OUTSIDE_DIAMETER and self.ui.checkBox1.isChecked() == True:
                                        PROGRAM_TEXT += "G4 U" + self.ui.comboBox4.currentText() + "\r\n"
                                else: #テーパーの場合
                                    PROGRAM_TEXT += "G0 X" + str(POS[1] * 2) + " Z" + str(POS[0]) + "\r\n"
                        #####G2、G3の場合
                        elif G_TYPE == "R":
                            PROGRAM_TEXT += R_DIRECTION + " X" + str(POS[1] * 2) + " Z" + str(POS[0]) + " R" + str(R_LENGTH) + " F" +  self.ui.comboBox1.currentText() + "\r\n"
                        EX_POS = POS
            self.ui.plainTextEdit.setPlainText(PROGRAM_TEXT)
            self.ui.plainTextEdit.setFocus()


    #-----pushButton2用イベント処理----------------------------------------
    def pushButton2_clicked(self):
        filepath, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "",'m File (*.m)')
        if filepath:
            f = open(filepath, "w")
            f.writelines(self.ui.plainTextEdit.toPlainText())
            f.close()
            msgbox = QtWidgets.QMessageBox(self)
            msgbox.setWindowTitle("TEST")
            #msgbox.setIconPixmap(QtGui.QPixmap("PLANET.ico"))
            msgbox.setText("プログラムを保存しました。")
            ret = msgbox.exec()
            self.ui.plainTextEdit.setFocus()


    #-----ウィンドウ終了イベントのフック----------------------------------------
    def closeEvent(self, event): #event.accept() event.ignore()で処理を選択可能
        global SUB_WIN_ACTIVE
        win.setEnabled(True)
        SUB_WIN_ACTIVE = 0
        event.accept() #メインウィンドウの終了イベントを実行


    #####ファイル書込み
    def LINE_CHECK(self, EX_POS, POS, OUTSIDE_DIAMETER):
        if EX_POS[0] == POS[0] or EX_POS[1] == POS[1]:
            f_val = "F" + self.ui.comboBox2.currentText()
        else:
            f_val = "F" + self.ui.comboBox1.currentText()

        vertical_0 = [[0, 0], [0, OUTSIDE_DIAMETER]]
        horizontal_0 = [[0, OUTSIDE_DIAMETER], [3000, OUTSIDE_DIAMETER]]

        if EX_POS[0] >= 0 and EX_POS[1] <= OUTSIDE_DIAMETER:
            return "G1", f_val
        elif POS[0] >= 0 and POS[1] <= OUTSIDE_DIAMETER:
            return "G1", f_val
        elif INTERSECTION_DETECTOR(EX_POS, POS, vertical_0[0], vertical_0[1]) == True:
            return "G1", f_val
        elif INTERSECTION_DETECTOR(EX_POS, POS, horizontal_0[0], horizontal_0[1]) == True:
            return "G1", f_val

        elif POS[0] >= -0.05 and POS[1] <= OUTSIDE_DIAMETER + 0.05:
            return "G1", "F0.05"
        elif POS[0] >= -0.2 and POS[1] <= OUTSIDE_DIAMETER + 0.2:
            return "G1", "F0.2"
        else:
            return "G0", ""


    #-----設定ファイル読み込み処理----------------------------------------
    def SETTINGS_READ(self):
        global SETTING_PATH_DXFtoNC
        f = open(SETTING_PATH_DXFtoNC, "r")
        x = ""
        x = f.readlines() #テキストを一行ずつ配列として読込む（行の終わりの改行コードも含めて読込む）
        f.close()
        data = x[0].replace("\n", "")
        self.ui.comboBox1.setCurrentIndex(int(data))
        data = x[1].replace("\n", "")
        self.ui.comboBox2.setCurrentIndex(int(data))
        data = x[2].replace("\n", "")
        self.ui.comboBox3.setCurrentIndex(int(data))
        data = x[3].replace("\n", "")
        self.ui.comboBox4.setCurrentIndex(int(data))
        data = x[4].replace("\n", "")
        if data == "0":
            self.ui.checkBox1.setChecked(False)
        else:
            self.ui.checkBox1.setChecked(True)


    #-----設定ファイルの保存処理----------------------------------------
    def SETTINGS_SAVE(self):
        data = ""
        #材料径の設定
        global SETTING_PATH_DXFtoNC
        data += str(self.ui.comboBox1.currentIndex())+"\n"
        data += str(self.ui.comboBox2.currentIndex())+"\n"
        data += str(self.ui.comboBox3.currentIndex())+"\n"
        data += str(self.ui.comboBox4.currentIndex())+"\n"
        if self.ui.checkBox1.isChecked() == False:
            data += "0\n"
        else:
            data += "1\n"
        f = open(SETTING_PATH_DXFtoNC, "w")
        f.write(data) #Plaine Text Editの内容を書込む
        f.close()






























########################################定型文########################################
#####Pysideのウィンドウ処理クラス
class MainWindow1(QtWidgets.QMainWindow): #QtWidgets.QMainWindowを継承。
    def __init__(self, parent = None): #クラス初期化時にのみ実行される関数（コンストラクタと呼ばれる）。
        super().__init__(parent)  #親クラスのコンストラクタを呼び出す（親クラスのコンストラクタを再利用したい場合）。指定する引数は、親クラスのコンストラクタの引数からselfを除いた引数。
        self.ui = Ui_MainWindow1() #uiクラスの作成。Ui_MainWindowのMainWindowは、QT DesignerのobjectNameで設定した名前。
        self.ui.setupUi(self) #uiクラスの設定。
######################################################################################

        #-----シグナルにメッソドを関連付け----------------------------------------
        self.ui.action1_1.triggered.connect(self.action1_1_triggered)
        self.ui.action1_2.triggered.connect(self.action1_2_triggered)
        self.ui.action1_3.triggered.connect(self.action1_3_triggered)
        self.ui.action1_4.triggered.connect(self.action1_4_triggered)
        self.ui.action1_5.triggered.connect(self.action1_5_triggered)
        self.ui.action1_6.triggered.connect(self.action1_6_triggered)
        self.ui.action1_7.triggered.connect(self.action1_7_triggered)
        self.ui.action2_1.triggered.connect(self.action2_1_triggered)
        self.ui.action2_2.triggered.connect(self.action2_2_triggered)
        self.ui.action2_3.triggered.connect(self.action2_3_triggered)
        self.ui.action2_4.triggered.connect(self.action2_4_triggered)
        self.ui.action2_5.triggered.connect(self.action2_5_triggered)
        self.ui.action2_6.triggered.connect(self.action2_6_triggered)
        self.ui.action2_7.triggered.connect(self.action2_7_triggered)
        self.ui.action3_1.triggered.connect(self.action3_1_triggered)
        self.ui.action4_1.triggered.connect(self.action4_1_triggered)
        self.ui.plainTextEdit1.textChanged.connect(self.plainTextEdit1_textChanged)
        self.ui.plainTextEdit2.textChanged.connect(self.plainTextEdit2_textChanged)
        self.win2 = MainWindow2()
        self.win3 = MainWindow3()
        if os.path.exists(SETTING_PATH_EDITOR):
            self.SETTINGS_READ()
        else:
            self.SETTINGS_SAVE()
        self.ui.plainTextEdit1.setFocus()

    def action1_1_triggered(self):
    #####ファイルの読込み
        global TEXT1_FILENAME
        global FLAG_TEXT1_CHANGED
        global MAIN_PRG_DIR
        flag_tmp = 1
        if FLAG_TEXT1_CHANGED == 1:
            ret = QtWidgets.QMessageBox.information(None, "Message", "メイン側のプログラムには保存されていない変更箇所があります。\r\nプログラムを新たに読み込みますか？", QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
            if ret == QtWidgets.QMessageBox.No:
                flag_tmp = 0
        if flag_tmp == 1:
            QQG = QtWidgets.QFileDialog(self)
            if MAIN_PRG_DIR != "":
                QQG.setDirectory(MAIN_PRG_DIR)
            tmp_filename, _ = QQG.getOpenFileName(self, "Open File", "",'NC File (*.txt *.m *.s *.nc *.dnc)')
            if tmp_filename:
                TEXT1_FILENAME = tmp_filename
                f = open(TEXT1_FILENAME, "r")
                original_program_text = ""
                original_program_text = f.read()
                f.close()
                _, nc_program = NC_SPLITTER(original_program_text)
                new_program_text = ""
                for program_line in nc_program:
                    commands = program_line[0]
                    values = program_line[1]
                    for (a_command, a_value) in zip(commands, values):
                        new_program_text += a_command + a_value + " "
                    new_program_text = new_program_text.replace(" ; ", "\r\n") #プログラムのある行用
                    new_program_text = new_program_text.replace("; ", "\r\n") #空の行用
                self.ui.plainTextEdit1.setPlainText(new_program_text) #Plain Text Editにテキストを表示
                FLAG_TEXT1_CHANGED = 0
                tmp_dir = TEXT1_FILENAME.rsplit("\\", 1)
                MAIN_PRG_DIR = tmp_dir[0]
            self.ui.plainTextEdit1.setFocus()


    def action1_2_triggered(self):
    #####ファイルの上書き保存
        global TEXT1_FILENAME
        global FLAG_TEXT1_CHANGED
        global MAIN_PRG_DIR
        if TEXT1_FILENAME == "":
            QQG = QtWidgets.QFileDialog(self)
            if MAIN_PRG_DIR != "":
                QQG.setDirectory(MAIN_PRG_DIR)
            TEXT1_FILENAME, _ = QQG.getSaveFileName(self, "Save File", "",'NC File (*.txt *.m *.s *.nc *.dnc)')
        if TEXT1_FILENAME:
            f = open(TEXT1_FILENAME, "w")
            f.writelines(self.ui.plainTextEdit1.toPlainText()) #Plaine Text Editの内容を書込む
            f.close()
            FLAG_TEXT1_CHANGED = 0
            tmp_dir = TEXT1_FILENAME.rsplit("\\", 1)
            MAIN_PRG_DIR = tmp_dir[0]
        self.ui.plainTextEdit1.setFocus()


    def action1_3_triggered(self):
    #####ファイルを名前を付けて保存
        global TEXT1_FILENAME
        global FLAG_TEXT1_CHANGED
        global MAIN_PRG_DIR
        tmp_filename = TEXT1_FILENAME
        QQG = QtWidgets.QFileDialog(self)
        if MAIN_PRG_DIR != "":
            QQG.setDirectory(MAIN_PRG_DIR)
        TEXT1_FILENAME, _ = QQG.getSaveFileName(self, "Save File", "",'NC File (*.txt *.m *.s *.nc *.dnc)')
        if TEXT1_FILENAME:
            f = open(TEXT1_FILENAME, "w")
            f.writelines(self.ui.plainTextEdit1.toPlainText()) #Plaine Text Editの内容を書込む
            f.close()
            FLAG_TEXT1_CHANGED = 0
            tmp_dir = TEXT1_FILENAME.rsplit("\\", 1)
            MAIN_PRG_DIR = tmp_dir[0]
        else:
            TEXT1_FILENAME = tmp_filename
        self.ui.plainTextEdit1.setFocus()


    def action1_4_triggered(self):
    #####プログラムをDXFとして保存
        program_text = self.ui.plainTextEdit1.toPlainText()
        if program_text != "":
            ret, _ = NC_SPLITTER(program_text)
            if ret == 1:
                msgbox = QtWidgets.QMessageBox(self)
                msgbox.setWindowTitle("Massage")
                #msgbox.setIconPixmap(QtGui.QPixmap("PLANET.ico"))
                msgbox.setText("コマンドに続く数値が有りません。")
                ret = msgbox.exec()
            else:
                QQG = QtWidgets.QFileDialog(self)
                if MAIN_PRG_DIR != "":
                    QQG.setDirectory(MAIN_PRG_DIR)
                filepath, _ = QQG.getSaveFileName(self, "Save File", "",'DXF File (*.dxf)')
                if filepath:
                    PROGRAM_TO_DXF(program_text, filepath)
        else:
            msgbox = QtWidgets.QMessageBox(self)
            msgbox.setWindowTitle("Massage")
            #msgbox.setIconPixmap(QtGui.QPixmap("PLANET.ico"))
            msgbox.setText("プログラムが有りません。")
            ret = msgbox.exec()
            self.ui.plainTextEdit1.setFocus()


    def action1_5_triggered(self):
        program_text = self.ui.plainTextEdit1.toPlainText()
        if program_text != "":
            _, nc_program = NC_SPLITTER(program_text)
            new_program_text = ""
            for program_line in nc_program:
                commands = program_line[0]
                values = program_line[1]
                for (a_command, a_value) in zip(commands, values):
                    new_program_text += a_command + a_value + " "
                new_program_text = new_program_text.replace(" ; ", "\r\n") #プログラムのある行用
                new_program_text = new_program_text.replace("; ", "\r\n") #空の行用
            self.ui.plainTextEdit1.setPlainText(new_program_text) #Plain Text Editにテキストを表示
            self.ui.plainTextEdit1.setFocus()
        else:
            msgbox = QtWidgets.QMessageBox(self)
            msgbox.setWindowTitle("Massage")
            #msgbox.setIconPixmap(QtGui.QPixmap("PLANET.ico"))
            msgbox.setText("プログラムが有りません。")
            ret = msgbox.exec()
            self.ui.plainTextEdit1.setFocus()


    def action1_6_triggered(self):
        global TEXT1_FILENAME
        global FLAG_TEXT1_CHANGED
        global SUB_WIN_ACTIVE
        global MAIN_PRG_DIR
        global MAIN_SUB_FLAG
        program_text = self.ui.plainTextEdit1.toPlainText()
        if program_text != "":
            ret, _ = NC_SPLITTER(program_text)
            if ret == 1:
                msgbox = QtWidgets.QMessageBox(self)
                msgbox.setWindowTitle("Massage")
                #msgbox.setIconPixmap(QtGui.QPixmap("PLANET.ico"))
                msgbox.setText("コマンドに続く数値が有りません。")
                ret = msgbox.exec()
            else:
                if TEXT1_FILENAME == "" or self.ui.action1_7.isChecked() == False:
                    tmp = TEXT1_FILENAME
                    QQG = QtWidgets.QFileDialog(self)
                    if MAIN_PRG_DIR != "":
                        QQG.setDirectory(MAIN_PRG_DIR)
                    TEXT1_FILENAME, _ = QQG.getSaveFileName(self, "Save File", "",'NC File (*.txt *.m *.s *.nc *.dnc)')
                if TEXT1_FILENAME:
                    f = open(TEXT1_FILENAME, "w")
                    f.writelines(self.ui.plainTextEdit1.toPlainText()) #Plaine Text Editの内容を書込む
                    f.close()
                    FLAG_TEXT1_CHANGED = 0
                    tmp_dir = TEXT1_FILENAME.rsplit("\\", 1)
                    MAIN_PRG_DIR = tmp_dir[0]
                    MAIN_SUB_FLAG = 0
                    self.ui.plainTextEdit1.setFocus()
                    self.win3 = MainWindow3()
                    self.win3.setWindowState(QtCore.Qt.WindowMaximized)
                    self.win3.show()
                    self.win3.action1_1_triggered()
                    SUB_WIN_ACTIVE = 1
                    win.setEnabled(False)
                else:
                    TEXT1_FILENAME = tmp
        else:
            msgbox = QtWidgets.QMessageBox(self)
            msgbox.setWindowTitle("Massage")
            #msgbox.setIconPixmap(QtGui.QPixmap("PLANET.ico"))
            msgbox.setText("プログラムが有りません。")
            ret = msgbox.exec()
            self.ui.plainTextEdit1.setFocus()


    def action1_7_triggered(self):
        self.SETTINGS_SAVE()


    def action2_1_triggered(self):
    #####ファイルの読込み
        global TEXT2_FILENAME
        global FLAG_TEXT2_CHANGED
        global SUB_PRG_DIR
        flag_tmp = 1
        if FLAG_TEXT2_CHANGED == 1:
            ret = QtWidgets.QMessageBox.information(None, "Message", "サブ側のプログラムには保存されていない変更箇所があります。\r\nプログラムを新たに読み込みますか？", QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
            if ret == QtWidgets.QMessageBox.No:
                flag_tmp = 0
        if flag_tmp == 1:
            QQG = QtWidgets.QFileDialog(self)
            if SUB_PRG_DIR != "":
                QQG.setDirectory(SUB_PRG_DIR)
            tmp_filename, _ = QQG.getOpenFileName(self, "Open File", "",'NC File (*.txt *.m *.s *.nc *.dnc)')
            if tmp_filename:
                TEXT2_FILENAME = tmp_filename
                f = open(TEXT2_FILENAME, "r")
                original_program_text = ""
                original_program_text = f.read()
                f.close()
                _, nc_program = NC_SPLITTER(original_program_text)
                new_program_text = ""
                for program_line in nc_program:
                    commands = program_line[0]
                    values = program_line[1]
                    for (a_command, a_value) in zip(commands, values):
                        new_program_text += a_command + a_value + " "
                    new_program_text = new_program_text.replace(" ; ", "\r\n") #プログラムのある行用
                    new_program_text = new_program_text.replace("; ", "\r\n") #空の行用
                self.ui.plainTextEdit2.setPlainText(new_program_text) #Plain Text Editにテキストを表示
                FLAG_TEXT2_CHANGED = 0
                tmp_dir = TEXT2_FILENAME.rsplit("\\", 1)
                SUB_PRG_DIR = tmp_dir[0]
            self.ui.plainTextEdit2.setFocus()


    def action2_2_triggered(self):
    #####ファイルの上書き保存
        global TEXT2_FILENAME
        global FLAG_TEXT2_CHANGED
        global SUB_PRG_DIR
        if TEXT2_FILENAME == "":
            QQG = QtWidgets.QFileDialog(self)
            if SUB_PRG_DIR != "":
                QQG.setDirectory(SUB_PRG_DIR)
            TEXT2_FILENAME, _ = QQG.getSaveFileName(self, "Save File", "",'NC File (*.txt *.m *.s *.nc *.dnc)')
        if TEXT2_FILENAME:
            f = open(TEXT2_FILENAME, "w")
            f.writelines(self.ui.plainTextEdit2.toPlainText()) #Plaine Text Editの内容を書込む
            f.close()
            FLAG_TEXT2_CHANGED = 0
            tmp_dir = TEXT2_FILENAME.rsplit("\\", 1)
            SUB_PRG_DIR = tmp_dir[0]
        self.ui.plainTextEdit2.setFocus()


    def action2_3_triggered(self):
    #####ファイルを名前を付けて保存
        global TEXT2_FILENAME
        global FLAG_TEXT2_CHANGED
        global SUB_PRG_DIR
        tmp_filename = TEXT2_FILENAME
        QQG = QtWidgets.QFileDialog(self)
        if SUB_PRG_DIR != "":
            QQG.setDirectory(SUB_PRG_DIR)
        TEXT2_FILENAME, _ = QQG.getSaveFileName(self, "Save File", "",'NC File (*.txt *.m *.s *.nc *.dnc)')
        if TEXT2_FILENAME:
            f = open(TEXT2_FILENAME, "w")
            f.writelines(self.ui.plainTextEdit2.toPlainText()) #Plaine Text Editの内容を書込む
            f.close()
            FLAG_TEXT2_CHANGED = 0
            tmp_dir = TEXT2_FILENAME.rsplit("\\", 1)
            SUB_PRG_DIR = tmp_dir[0]
        else:
            TEXT2_FILENAME = tmp_filename
        self.ui.plainTextEdit2.setFocus()


    def action2_4_triggered(self):
    #####プログラムをDXFとして保存
        program_text = self.ui.plainTextEdit2.toPlainText()
        if program_text != "":
            ret, _ = NC_SPLITTER(program_text)
            if ret == 1:
                msgbox = QtWidgets.QMessageBox(self)
                msgbox.setWindowTitle("Massage")
                #msgbox.setIconPixmap(QtGui.QPixmap("PLANET.ico"))
                msgbox.setText("コマンドに続く数値が有りません。")
                ret = msgbox.exec()
            else:
                QQG = QtWidgets.QFileDialog(self)
                if SUB_PRG_DIR != "":
                    QQG.setDirectory(SUB_PRG_DIR)
                filepath, _ = QQG.getSaveFileName(self, "Save File", "",'DXF File (*.dxf)')
                if filepath:
                    PROGRAM_TO_DXF(program_text, filepath)
        else:
            msgbox = QtWidgets.QMessageBox(self)
            msgbox.setWindowTitle("Massage")
            #msgbox.setIconPixmap(QtGui.QPixmap("PLANET.ico"))
            msgbox.setText("プログラムが有りません。")
            ret = msgbox.exec()
            self.ui.plainTextEdit2.setFocus()


    def action2_5_triggered(self):
        program_text = self.ui.plainTextEdit2.toPlainText()
        if program_text != "":
            _, nc_program = NC_SPLITTER(program_text)
            new_program_text = ""
            for program_line in nc_program:
                commands = program_line[0]
                values = program_line[1]
                for (a_command, a_value) in zip(commands, values):
                    new_program_text += a_command + a_value + " "
                new_program_text = new_program_text.replace(" ; ", "\r\n") #プログラムのある行用
                new_program_text = new_program_text.replace("; ", "\r\n") #空の行用
            self.ui.plainTextEdit2.setPlainText(new_program_text) #Plain Text Editにテキストを表示
            self.ui.plainTextEdit2.setFocus()
        else:
            msgbox = QtWidgets.QMessageBox(self)
            msgbox.setWindowTitle("Massage")
            #msgbox.setIconPixmap(QtGui.QPixmap("PLANET.ico"))
            msgbox.setText("プログラムが有りません。")
            ret = msgbox.exec()
            self.ui.plainTextEdit2.setFocus()


    def action2_6_triggered(self):
        global TEXT2_FILENAME
        global FLAG_TEXT2_CHANGED
        global SUB_WIN_ACTIVE
        global SUB_PRG_DIR
        global MAIN_SUB_FLAG
        program_text = self.ui.plainTextEdit2.toPlainText()
        if program_text != "":
            ret, _ = NC_SPLITTER(program_text)
            if ret == 1:
                msgbox = QtWidgets.QMessageBox(self)
                msgbox.setWindowTitle("Massage")
                #msgbox.setIconPixmap(QtGui.QPixmap("PLANET.ico"))
                msgbox.setText("コマンドに続く数値が有りません。")
                ret = msgbox.exec()
            else:
                if TEXT2_FILENAME == "" or self.ui.action2_7.isChecked() == False:
                    tmp = TEXT2_FILENAME
                    QQG = QtWidgets.QFileDialog(self)
                    if SUB_PRG_DIR != "":
                        QQG.setDirectory(SUB_PRG_DIR)
                    TEXT2_FILENAME, _ = QQG.getSaveFileName(self, "Save File", "",'NC File (*.txt *.m *.s *.nc *.dnc)')
                if TEXT2_FILENAME:
                    f = open(TEXT2_FILENAME, "w")
                    f.writelines(self.ui.plainTextEdit2.toPlainText()) #Plaine Text Editの内容を書込む
                    f.close()
                    FLAG_TEXT2_CHANGED = 0
                    tmp_dir = TEXT2_FILENAME.rsplit("\\", 1)
                    SUB_PRG_DIR = tmp_dir[0]
                    MAIN_SUB_FLAG = 1
                    self.ui.plainTextEdit2.setFocus()
                    self.win3 = MainWindow3()
                    self.win3.setWindowState(QtCore.Qt.WindowMaximized)
                    self.win3.show()
                    self.win3.action1_1_triggered()
                    SUB_WIN_ACTIVE = 1
                    win.setEnabled(False)
                else:
                    TEXT2_FILENAME = tmp
        else:
            msgbox = QtWidgets.QMessageBox(self)
            msgbox.setWindowTitle("Massage")
            #msgbox.setIconPixmap(QtGui.QPixmap("PLANET.ico"))
            msgbox.setText("プログラムが有りません。")
            ret = msgbox.exec()
            self.ui.plainTextEdit1.setFocus()


    def action2_7_triggered(self):
        self.SETTINGS_SAVE()


    def action3_1_triggered(self):
        global SUB_WIN_ACTIVE
        self.win2 = MainWindow2()
        self.win2.show()
        SUB_WIN_ACTIVE = 1
        win.setEnabled(False)


    def action4_1_triggered(self):
        global VERSION
        global YEAR
        msgbox = QtWidgets.QMessageBox(self)
        msgbox.setWindowTitle("NcWorksについて")
        msgbox.setIconPixmap(QtGui.QPixmap("PLANET.ico"))
        msgbox.setText("NcWorks\r\n\r\nバージョン " + VERSION + "\r\nNcWorksは、NC自動盤プログラムの作成と確認を支援するツールです。\r\nCAD/CAM機能、シミュレータ機能を提供します。\r\n\r\nCopyright(C) " + YEAR + " Daiya Seimitsu Co., Ltd.")
        ret = msgbox.exec()
        self.ui.plainTextEdit1.setFocus()

    def plainTextEdit1_textChanged(self):
        global FLAG_TEXT1_CHANGED
        FLAG_TEXT1_CHANGED = 1


    def plainTextEdit2_textChanged(self):
        global FLAG_TEXT2_CHANGED
        FLAG_TEXT2_CHANGED = 1


    #-----ウィンドウ終了イベントのフック----------------------------------------
    def closeEvent(self, event): #event.accept() event.ignore()で処理を選択可能
        global FLAG_TEXT1_CHANGED
        global FLAG_TEXT2_CHANGED
        global SUB_WIN_ACTIVE
        if SUB_WIN_ACTIVE == 0:
            if FLAG_TEXT1_CHANGED == 1:
                ret = QtWidgets.QMessageBox.information(None, "Message", "メイン側のプログラムには保存されていない変更箇所があります。\r\n終了しますか？", QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
                if ret == QtWidgets.QMessageBox.Yes:
                        self.win2.close()
                        self.win3.close()
                        event.accept() 
                elif ret == QtWidgets.QMessageBox.No:
                        event.ignore()
            elif FLAG_TEXT2_CHANGED == 1:
                ret = QtWidgets.QMessageBox.information(None, "Message", "サブ側のプログラムには保存されていない変更箇所があります。\r\n終了しますか？", QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
                if ret == QtWidgets.QMessageBox.Yes:
                        self.win2.close()
                        self.win3.close()
                        event.accept() 
                elif ret == QtWidgets.QMessageBox.No:
                        event.ignore()
            else:
                self.win2.close()
                self.win3.close()
                event.accept()
        else:
            event.ignore()

    #-----設定ファイル読み込み処理----------------------------------------
    def SETTINGS_READ(self):
        global SETTING_PATH_EDITOR
        f = open(SETTING_PATH_EDITOR, "r")
        x = ""
        x = f.readlines() #テキストを一行ずつ配列として読込む（行の終わりの改行コードも含めて読込む）
        f.close()
        data = x[0].replace("\n", "")
        if data == "0":
            self.ui.action1_7.setChecked(False)
        else:
            self.ui.action1_7.setChecked(True)
        data = x[1].replace("\n", "")
        if data == "0":
            self.ui.action2_7.setChecked(False)
        else:
            self.ui.action2_7.setChecked(True)


    #-----設定ファイルの保存処理----------------------------------------
    def SETTINGS_SAVE(self):
        data = ""
        global SETTING_PATH_EDITOR
        if self.ui.action1_7.isChecked() == False:
            data += "0\n"
        else:
            data += "1\n"
        if self.ui.action2_7.isChecked() == False:
            data += "0\n"
        else:
            data += "1\n"
        f = open(SETTING_PATH_EDITOR, "w")
        f.write(data) #Plaine Text Editの内容を書込む
        f.close()


########################################定型文########################################
#####メイン処理（グローバル）
if __name__ == '__main__': #C言語のmain()に相当。このファイルが実行された場合、以下の行が実行される（モジュールとして読込まれた場合は、実行されない）。
    app = QtWidgets.QApplication(sys.argv) #アプリケーションオブジェクト作成（sys.argvはコマンドライン引数のリスト）。
    win = MainWindow1() #MainWindow1クラスのインスタンスを作成。
    win.setWindowState(QtCore.Qt.WindowMaximized)
    win.show() #ウィンドウを表示。win.showFullScreen()やwin.showEvent()を指定する事でウィンドウの状態を変える事が出来る。
    sys.exit(app.exec()) #引数が関数の場合は、関数が終了するまで待ち、その関数の返値を上位プロセスに返す。
######################################################################################
