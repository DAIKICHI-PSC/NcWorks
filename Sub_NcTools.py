# -*- coding: utf-8 -*-
from Sub_MathPlus import RND, ROTATION_DIRECTION_DETECTOR, INTERSECTION_DETECTOR, R_CENTER_DEGREE, R_CENTER_DEGREE2, R_POSITION, CALCULATE_DEGREE
from PySide6 import QtCore, QtGui, QtWidgets
import ezdxf
from ezdxf.math import ConstructionArc
import math





#-----NCのプログラムからコマンドと値を個々に取り出すための関数
def NC_SPLITTER(ORIGINAL_PROGRAM_TEXT):
    ret = 0
    NC_PROGRAM = [] #NCプログラムを格納するリスト
    commands = [] #各行のコマンドを取得する為のリスト
    values = [] #各行のコマンドの値を取得する為のリスト
    lineCounter = 0 #何行目かを示す変数
    ncCommand ="" #取り出したNCのコマンドを一時的に格納する変数
    ncCommandValue ="" #取り出したNCのコマンドの値を一時的に格納する変数
    tmpStr = "" #NCのコマンドの値を一文字ずつ一時的に格納する変数
    currentPosition = 0 #各行の何文字目を処理しているかを示す変数
    #テキストの前処理
    if ORIGINAL_PROGRAM_TEXT == "":
        return(None)
    ORIGINAL_PROGRAM_TEXT = ORIGINAL_PROGRAM_TEXT.replace(";", "")
    if ORIGINAL_PROGRAM_TEXT.endswith("\n") == False:
        ORIGINAL_PROGRAM_TEXT += "\n"
    ORIGINAL_PROGRAM_TEXT = ORIGINAL_PROGRAM_TEXT.replace("\r", "")
    ORIGINAL_PROGRAM_TEXT = ORIGINAL_PROGRAM_TEXT.replace("\n", ";\n") #;を行の終わりとする
    ORIGINAL_PROGRAM_TEXT = ORIGINAL_PROGRAM_TEXT.upper()

    contentsTOOL = [] #テキストの各行を分割して格納するリスト
    contentsTOOL = ORIGINAL_PROGRAM_TEXT.split("\n")
    for IndivisualLine in contentsTOOL: #各行を摘出
        currentPosition = 0
        commands.clear()
        values.clear()
        while True: #行内の走査
            ncCommand = IndivisualLine[currentPosition : currentPosition + 1] #コマンド文字を取得
            if ncCommand == ";": #行の終わりを検出
                commands.append(";") #コマンドをリストに追加
                values.append("") #値をリストに追加
                break
            elif ncCommand == "": #念の為、空を検出
                break
            elif (ord(ncCommand) > 64 and ord(ncCommand) < 91) or ncCommand == "," or ncCommand == "#" or ncCommand == "(" or ncCommand == "/": #コマンドを検出
                ncCommandValue = ""
                if ncCommand == "(": #コマンドが(の場合の値の走査
                    while True:
                        currentPosition += 1
                        tmpStr = IndivisualLine[currentPosition : currentPosition + 1] #コマンドに続くの文字列から一文字ずつ順次取得
                        if tmpStr == ";":
                            currentPosition = currentPosition - 1 #ループ先頭のコマンド確認で行の走査を終了させる
                            break
                        elif tmpStr == ")":
                            ncCommandValue = ncCommandValue + tmpStr
                            break
                        ncCommandValue = ncCommandValue + tmpStr
                else: #コマンドが(以外の場合の値の走査
                    while True:
                        currentPosition = currentPosition + 1
                        tmpStr = IndivisualLine[currentPosition : currentPosition + 1] #コマンドに続くの文字列から一文字ずつ順次取得
                        if (ord(tmpStr) > 64 and ord(tmpStr) < 91) or tmpStr == "," or tmpStr == "(" or ncCommand == "/" or tmpStr == ";":
                            currentPosition = currentPosition - 1 #コマンドを検出したので、値の走査を終了する
                            break
                        elif tmpStr == " ": #スペースを検出したら、値の走査を終了する
                            break
                        ncCommandValue = ncCommandValue + tmpStr
                if ncCommand.isalpha()==True and ncCommandValue == "":
                    ret = 1
                commands.append(ncCommand) #コマンドをリストに追加
                values.append(ncCommandValue) #値をリストに追加
            currentPosition = currentPosition + 1
        NC_PROGRAM.append([commands[:], values[:]]) #プログラムに一行分のコマンドと値を追加　NC[[commands[], values[]], [commands[], values[]], ...]
        lineCounter = lineCounter + 1
    return ret, NC_PROGRAM





#-----NC_SPLITTERで配列化されたデータをテキストデータへ戻す為の関数("\r\n"でsplitするとリスト配列へ変換可能)
def NC_PROGRAM_TEXT(NC_PROGRAM):
    NC_TEXT = ""
    for program_line in NC_PROGRAM:
        commands = program_line[0]
        values = program_line[1]
        for (a_command, a_value) in zip(commands, values):
            NC_TEXT += a_command + a_value + " "
        NC_TEXT = NC_TEXT.replace(" ; ", "\r\n") #プログラムのある行用
        NC_TEXT = NC_TEXT.replace("; ", "\r\n") #空の行用
    return NC_TEXT





#-----NC_SPLITTERで配列化されたデータから、移動データを取り出すための関数
def NC_MOVEMENT(NC_PROGRAM, APPEND_G50): #append_G50はG50を適用するかのフラグ
    #NC_T = ""
    NC_G9899 = "99" #現在の送りのモード
    NC_S = 0 #現在の回転数
    NC_G012350 = "0" #現在の加工モード
    NC_exX = 0 #最後に工具移動した際のX
    NC_exZ = 0 #最後に工具移動した際のZ
    NC_X = 0 #工具の移動先のX
    NC_Z = 0 #工具の移動先のZ
    NC_R = 0 #加工Rの大きさ
    NC_F = 0 #送り値
    G50_U = 0 #G50のインクリメンタルU
    G50_W = 0 #G50のインクリメンタルW
    G50_U_val = 0
    G50_W_val = 0
    NC_U = 0 #工具移動のインクリメンタルU
    NC_W = 0 #工具移動のインクリメンタルW
    x_move_flag = 0
    z_move_flag = 0
    u_move_flag = 0
    w_move_flag = 0
    x_length = 0
    z_length = 0
    move_degree = 0
    G92_STARTED = 0
    G92_START_X = 0
    G92_END_X = 0
    G92_START_Z = 0
    G92_END_Z = 0
    G92_Z_LENGTH = 0
    move_flag = 0 #現在の行に移動命令があるかのフラグ
    start_flag = 0 #最初の工具が選択されたかのフラグ
    end_flag = 0 #プログラムが終了したかのフラグ
    TOOL_LINE_PATH = [] #工具毎の移動データ
    MOVEMENT_DATA = [] #解析後の移動データ
    PROGRAM_LINE_POS = [] #プログラムの移動行がどのパスに対応するかを記憶
    TOOL_NAME = [] #工具番号を記憶
    TOOL_CHANGE_POS = [] #工具交換が何行目か記憶
    ex_tool_change_pos = 0
    tool_num =0 #加工を行う工具の番号
    line_num = -1 #移動したかを確認する為の変数（一番最初の移動行はカウントしない）
    first_move = 1 #加工開始したか確認するフラグ
    first_move_line = 0 #工具が移動する最初の行を記憶
    ex_tool_name = ""
    tool_selected = 0 #工具が選択されたかを確認するフラグ
    JUMP_COMMAND = ""
    JUMP_FLAG = 0

    for i, program_line in enumerate(NC_PROGRAM): #プログラムの一行分を取得
        PROGRAM_LINE_POS.append(None)
        commands = program_line[0]
        values = program_line[1]
        for (a_command, a_value) in zip(commands, values): #各命令と値を取得
            if a_command == "T": #命令がTの場合
                if int(a_value) >= 100: #Tコマンドに続く値が100以上の場合は工具交換命令とする

                    G50_U = 0
                    G50_W = 0
                    if len(TOOL_LINE_PATH) > 1 and tool_selected == 1: #####移動した場合のみデータとして追加
                        MOVEMENT_DATA.append(TOOL_LINE_PATH[:])
                        TOOL_NAME.append(ex_tool_name)
                        TOOL_CHANGE_POS.append(ex_tool_change_pos)
                        while(True): #工具交換から、最初に移動を開始する迄のPROGRAM_LINE_POSの値をNONEにする
                            PROGRAM_LINE_POS[ex_tool_change_pos] = str(tool_num) + ",NONE" #プログラムの何行目がどのパスに対応するかを示すリスト配列を作成
                            ex_tool_change_pos += 1
                            if ex_tool_change_pos == first_move_line:
                                break
                        TOOL_LINE_PATH.clear()
                        tool_num += 1

                    #NC_T = a_value
                    #if int(a_value) >= 1000:
                    #    NC_exX = 0
                    #else:
                    #    NC_exX = 40
                    NC_exX = 50
                    TOOL_LINE_PATH.clear()
                    line_num = 0
                    start_flag = 1 #最初の工具が選択されたかのフラグ
                    ex_tool_name = "T" + str(a_value)  #工具名を記憶
                    ex_tool_change_pos = i #工具が交換された行を記憶
                    first_move = 1 #加工開始したか確認するフラグ
                    tool_selected = 1 #工具が選択されたかを確認するフラグ

                elif a_value == "0": #補正キャンセルコマンドの場合、G50をオフにする

                    G50_U = 0
                    G50_W = 0
                    if len(TOOL_LINE_PATH) > 1 and tool_selected == 1: #####移動した場合のみデータとして追加
                        MOVEMENT_DATA.append(TOOL_LINE_PATH[:])
                        TOOL_NAME.append(ex_tool_name)
                        TOOL_CHANGE_POS.append(ex_tool_change_pos)
                        while(True): #工具交換から、最初に移動を開始する迄のPROGRAM_LINE_POSの値をNONEにする
                            PROGRAM_LINE_POS[ex_tool_change_pos] = str(tool_num) + ",NONE" #プログラムの何行目がどのパスに対応するかを示すリスト配列を作成
                            ex_tool_change_pos += 1
                            if ex_tool_change_pos == first_move_line:
                                break
                        TOOL_LINE_PATH.clear()
                        tool_num += 1
                    line_num = -1
                    tool_selected = 0
                    #G50_U = 0
                    #G50_W = 0

            elif a_command == "G":
                if a_value == "98" or a_value =="99":
                    NC_G9899 = a_value
                elif a_value == "92":
                    NC_G012350 = a_value
                    G92_STARTED = 0
                elif a_value == "32":
                    NC_G012350 = "998"
                elif a_value == "84" or a_value == "184":
                    NC_G012350 = "999"
                    G92_STARTED = 0
                else:
                    NC_G012350 = a_value
            elif a_command == "S":
                NC_S = float(a_value)
            elif a_command == "X":
                NC_X = float(a_value)
                x_move_flag = 1
                move_flag = 1
            elif a_command == "Z":
                NC_Z = float(a_value)
                z_move_flag = 1
                move_flag = 1
            elif a_command == "R":
                NC_R = float(a_value)
            elif a_command == "F":
                NC_F = float(a_value)
            elif a_command == "U":
                NC_U = float(a_value)
                u_move_flag = 1
                move_flag = 1
            elif a_command == "W":
                NC_W = float(a_value)
                w_move_flag = 1
                move_flag = 1
            elif a_command == "M":
                if a_value == "80" or a_value == "99":
                    if not "P" in commands: #ジャンプ命令でない場合
                        G50_U = 0
                        G50_W = 0
                        if len(TOOL_LINE_PATH) > 1 and tool_selected == 1: #####移動した場合のみデータとして追加
                            MOVEMENT_DATA.append(TOOL_LINE_PATH[:])
                            TOOL_NAME.append(ex_tool_name)
                            TOOL_CHANGE_POS.append(ex_tool_change_pos)
                            while(True): #工具交換から、最初に移動を開始する迄のPROGRAM_LINE_POSの値をNONEにする
                                PROGRAM_LINE_POS[ex_tool_change_pos] = str(tool_num) + ",NONE" #プログラムの何行目がどのパスに対応するかを示すリスト配列を作成
                                ex_tool_change_pos += 1
                                if ex_tool_change_pos == first_move_line:
                                    break
                        TOOL_LINE_PATH.clear()
                        line_num = -1
                        end_flag = 1
                    else:
                        JUMP_FLAG = 1
            elif a_command == "P":
                if JUMP_FLAG == 1 and JUMP_COMMAND == "":
                    JUMP_COMMAND = "N" + a_value
                    NC_exX = NC_X
                    NC_exZ = NC_Z
            elif a_command == "N":
                if JUMP_FLAG == 1 and a_command + a_value == JUMP_COMMAND:
                    JUMP_COMMAND = ""
                    JUMP_FLAG = 0
                    move_flag = 0
                    NC_X = NC_exX
                    NC_Z = NC_exZ
                    NC_U = 0
                    NC_W = 0

        #==================================================移動した場合==================================================
        if move_flag == 1 and JUMP_FLAG == 0:
            ##################################################G50の処理##################################################
            if NC_G012350 == "50" and APPEND_G50 == 1:

                if x_move_flag == 1:
                    G50_U_val = (NC_X - NC_exX + G50_U) * -1
                elif u_move_flag == 1:
                    G50_U_val = NC_U * -1
                else:
                    G50_U_val = 0

                if z_move_flag == 1:
                    #G50_W_val = NC_Z - NC_exZ - G50_W
                    G50_W_val = (NC_Z - NC_exZ + G50_W) * -1
                elif w_move_flag == 1:
                    G50_W_val = NC_W
                else:
                    G50_W_val = 0

                G50_U += G50_U_val
                G50_W += G50_W_val

            ##################################################G0 G1 G2 G3の処理##################################################
            elif int(NC_G012350) <= 3 and start_flag ==1 and end_flag == 0:
                #多条ネジ
                #if G92_STARTED == 1:
                    #if x_move_flag == 0:
                        #NC_X = NC_exX
                    #if z_move_flag == 0:
                        #NC_Z = NC_exZ
                    #G92_STARTED = 0
                if G92_STARTED == 1:
                    NC_X = NC_exX
                    NC_Z = NC_exZ
                    G92_STARTED = 0
                #NC_exX = NC_X
                #NC_exZ = 
                if APPEND_G50 == 1:
                    if x_move_flag == 1:
                        NC_X = RND(NC_X + G50_U)
                    elif u_move_flag == 1:
                        NC_X = RND(NC_X + NC_U)
                    
                    if z_move_flag == 1:
                        NC_Z = RND(NC_Z + NC_W + G50_W)
                    elif w_move_flag == 1:
                        NC_Z = RND(NC_Z + NC_W)
                else:
                    NC_X = RND(NC_X + NC_U)
                    NC_Z = RND(NC_Z + NC_W)
                if x_move_flag == 1 or u_move_flag == 1:
                    x_length = NC_X - NC_exX
                if z_move_flag == 1 or w_move_flag == 1:
                    z_length = NC_Z - NC_exZ
                if abs(x_length) > 0 and abs(z_length) > 0:
                    move_degree = RND(CALCULATE_DEGREE(RND(abs(x_length) / 2), RND(abs(z_length))))
                TOOL_LINE_PATH.append([NC_G9899, NC_S, NC_G012350, NC_X, NC_Z, NC_R, NC_F, i, G50_U, G50_W, RND(x_length), RND(z_length), move_degree]) #MOVEMENT_DATA[TOOL_LINE_PATH[], ...] iは実際のNCプログラムの何行目かを示す
                if len(TOOL_LINE_PATH) > 1 and line_num >= 0: #####移動した場合のみデータとして追加
                    PROGRAM_LINE_POS[i] = str(tool_num) + "," + str(line_num) #プログラムの何行目がどのパスに対応するかを示すリスト配列
                    line_num += 1
                    if first_move == 1:
                        first_move_line = i #工具が移動する最初の行を記憶
                        first_move = 0
                NC_exX = NC_X
                NC_exZ = NC_Z
                #else:
                    #PROGRAM_LINE_POS[i] = str(tool_num) + ",NONE"

            ##################################################ねじ切りサイクルの処理##################################################
            elif NC_G012350 =="92" and start_flag ==1 and end_flag == 0:
                if G92_STARTED == 0:
                    G92_START_X = NC_exX
                    G92_START_Z = NC_exZ
                    if w_move_flag == 1:
                        G92_END_Z = NC_exZ + NC_W
                    else:
                        G92_END_Z = NC_Z
                    if APPEND_G50 == 1:
                        G92_END_Z += G50_W
                    G92_Z_LENGTH = G92_END_Z - G92_START_Z
                    G92_Z_LENGTH = int(G92_Z_LENGTH / NC_F) * NC_F
                    G92_END_Z = G92_START_Z + G92_Z_LENGTH
                    G92_Z_LENGTH = abs(G92_Z_LENGTH)
                    taper = NC_R * 2
                    G92_STARTED = 1
                if u_move_flag == 1:
                    G92_END_X = NC_exX + NC_U
                else:
                    G92_END_X = NC_X
                if APPEND_G50 == 1:
                    G92_END_X += G50_U
                x_length = abs(G92_END_X - G92_START_X)
                TOOL_LINE_PATH.append([NC_G9899, NC_S, "0", G92_END_X, G92_START_Z, NC_R, NC_F, i, G50_U, G50_W, RND(x_length), 0, 0])
                TOOL_LINE_PATH.append([NC_G9899, NC_S, "1", G92_END_X - taper, G92_END_Z, NC_R, NC_F, i, G50_U, G50_W, 0, RND(G92_Z_LENGTH), 0])
                TOOL_LINE_PATH.append([NC_G9899, NC_S, "0", G92_START_X, G92_END_Z, NC_R, NC_F, i, G50_U, G50_W, RND(x_length), 0, 0])
                TOOL_LINE_PATH.append([NC_G9899, NC_S, "0", G92_START_X, G92_START_Z, NC_R, NC_F, i, G50_U, G50_W, 0, RND(G92_Z_LENGTH), 0])
                if len(TOOL_LINE_PATH) > 1 and line_num >= 0: #####移動した場合のみデータとして追加
                    PROGRAM_LINE_POS[i] = str(tool_num) + "," + str(line_num) #プログラムの何行目がどのパスに対応するかを示すリスト配列
                    line_num += 1

            ##################################################テーパーねじ切りの処理##################################################
            elif NC_G012350 =="998" and start_flag ==1 and end_flag == 0:
                G92_START_X = NC_exX
                G92_START_Z = NC_exZ
                if w_move_flag == 1:
                    G92_END_Z = NC_exZ + NC_W
                else:
                    G92_END_Z = NC_Z
                if APPEND_G50 == 1:
                    G92_END_Z += G50_W
                G92_Z_LENGTH = G92_END_Z - G92_START_Z
                G92_Z_LENGTH = int(G92_Z_LENGTH / NC_F) * NC_F
                G92_END_Z = G92_START_Z + G92_Z_LENGTH
                G92_Z_LENGTH = abs(G92_Z_LENGTH)
                if u_move_flag == 1:
                    G92_END_X = NC_exX + NC_U
                else:
                    G92_END_X = NC_X
                if APPEND_G50 == 1:
                    G92_END_X += G50_U
                x_length = abs(G92_END_X - G92_START_X)
                TOOL_LINE_PATH.append([NC_G9899, NC_S, "1", G92_START_X, G92_END_Z, NC_R, NC_F, i, G50_U, G50_W, RND(x_length), RND(G92_Z_LENGTH), 0])
                if len(TOOL_LINE_PATH) > 1 and line_num >= 0: #####移動した場合のみデータとして追加
                    PROGRAM_LINE_POS[i] = str(tool_num) + "," + str(line_num) #プログラムの何行目がどのパスに対応するかを示すリスト配列
                    line_num += 1
                NC_exX = G92_END_X
                NC_exZ = G92_END_Z

            ##################################################タップの処理##################################################
            elif NC_G012350 =="999" and start_flag ==1 and end_flag == 0:
                G92_START_X = NC_exX
                G92_START_Z = NC_exZ
                if w_move_flag == 1:
                    G92_END_Z = NC_exZ + NC_W
                else:
                    G92_END_Z = NC_Z
                if APPEND_G50 == 1:
                    G92_END_Z += G50_W
                G92_Z_LENGTH = G92_END_Z - G92_START_Z
                G92_Z_LENGTH = int(G92_Z_LENGTH / NC_F) * NC_F
                G92_END_Z = G92_START_Z + G92_Z_LENGTH
                G92_Z_LENGTH = abs(G92_Z_LENGTH)
                if u_move_flag == 1:
                    G92_END_X = NC_exX + NC_U
                else:
                    G92_END_X = NC_X
                if APPEND_G50 == 1:
                    G92_END_X += G50_U
                x_length = abs(G92_END_X - G92_START_X)
                TOOL_LINE_PATH.append([NC_G9899, NC_S, "1", G92_START_X, G92_END_Z, NC_R, NC_F, i, G50_U, G50_W, RND(x_length), RND(G92_Z_LENGTH), 0])
                TOOL_LINE_PATH.append([NC_G9899, NC_S, "1", G92_START_X, G92_START_Z, NC_R, NC_F, i, G50_U, G50_W, RND(x_length), RND(G92_Z_LENGTH), 0])
                if len(TOOL_LINE_PATH) > 1 and line_num >= 0: #####移動した場合のみデータとして追加
                    PROGRAM_LINE_POS[i] = str(tool_num) + "," + str(line_num) #プログラムの何行目がどのパスに対応するかを示すリスト配列
                    line_num += 1

            ##################################################それ以外の処理##################################################
            else:
                if len(TOOL_LINE_PATH) > 1 and line_num >= 0: #####移動した場合のみデータとして追加
                    PROGRAM_LINE_POS[i] = str(tool_num) + ",NONE"
            NC_R = 0
            NC_U = 0
            NC_W = 0
            x_move_flag = 0
            z_move_flag = 0
            u_move_flag = 0
            w_move_flag = 0
            move_flag = 0
            x_length = 0
            z_length = 0
            move_degree = 0
        #==================================================移動しない場合==================================================
        else:
            if len(TOOL_LINE_PATH) > 1 and line_num >= 0: #####移動した場合のみデータとして追加
                PROGRAM_LINE_POS[i] = str(tool_num) + ",NONE"
    return MOVEMENT_DATA, PROGRAM_LINE_POS, TOOL_NAME, TOOL_CHANGE_POS #MOVEMENT_DATA(移動データ配列) PROGRAM_LINE_POS(移動線がプログラムの何行目に該当するか記憶) TOOL_NAME(工具名リスト) TOOL_CHANGE_POS(工具名リストの工具がプログラムの何行目かを記憶)
    #MOVEMENT_DATA = [G98かG99, 回転数, G012350, NC_X, NC_Z, NC_R, NC_F, 行番号, G50_U, G50_W, 移動距離X, 移動距離Z, 移動角度]





#-----NC_MOVEMENTで配列化されたデータを、工具毎にシンプルなパスへ変換する関数
def NC_SIMPLE_PATH(MOVEMENT_DATA, SCALE, APPEND_G50, TOOL_NAME, TOOL_DXF_GEOMETRIO):
    TOOLS = []
    for i, x in enumerate(MOVEMENT_DATA): #工具毎のデータを取得
        name_tool = TOOL_NAME[i] #各工具を取得
        geometrio = TOOL_DXF_GEOMETRIO[name_tool]
        go_x = float(geometrio[1])
        go_y = float(geometrio[0])
        go_x = RND(go_x)
        go_y = RND(go_y)
        fst_data = 1
        tool_path = QtGui.QPainterPath()
        for y in x: #各移動行を取得
            cX = y[4] + go_x
            cY = (y[3] + go_y) / -2
            nc_g = y[2]
            nc_r = y[5]
            if nc_g == "0" or nc_g == "1":
                if fst_data == 1: #起点の場合の処理
                    if APPEND_G50 == 0:
                        tool_path.moveTo(cX * SCALE, cY * SCALE)
                    else:
                        tool_path.moveTo((cX - y[9]) * SCALE, (cY - y[8] / -2) * SCALE)
                    fst_data = 0
                else: #座標データの処理
                    if APPEND_G50 == 0:
                        tool_path.lineTo(cX * SCALE, cY * SCALE)
                    else:
                        tool_path.lineTo((cX - y[9]) * SCALE, (cY - y[8] / -2) * SCALE)
                eX = cX
                eY = cY
            elif nc_g == "2" or nc_g == "3":
                cntX, cntY, d1, d2 = R_CENTER_DEGREE(eX, eY, cX, cY, nc_r, nc_g)
                cntX = RND(cntX)
                cntY = RND(cntY)
                d1 = RND(d1)
                d2 = RND(d2)
                if APPEND_G50 == 0:
                    tool_path.arcTo((cntX - nc_r) * SCALE, (cntY + nc_r) * SCALE, nc_r * 2 * SCALE, nc_r * -2  * SCALE, d1, d2 - d1)
                else:
                    tool_path.arcTo((cntX - nc_r - y[9]) * SCALE, (cntY + nc_r - y[8] / -2) * SCALE, nc_r * 2 * SCALE, nc_r * -2  * SCALE, d1, d2 - d1)
                eX = cX
                eY = cY
        TOOLS.append(tool_path)
    return TOOLS #工具毎に一本の工具軌跡を保持





#-----NC_MOVEMENTで配列化されたデータを工具毎、移動毎でパスへ変換する関数
def NC_PATH(MOVEMENT_DATA, SCALE, INCLUDE_FIRST_POSITION, FONT_SIZE, FLAG_PROG, APPEND_G50, TOOL_NAME = "", TOOL_DXF_GEOMETRIO = ""):
    TOOLS = []
    TOOLS_TEXT = []
    TOOLS_POS = []
    tool_path = []
    tool_path_text = []
    tool_path_pos = []
    PROGRAM_LINE_POS = []

    current_pos = []
    for i, x in enumerate(MOVEMENT_DATA): #工具毎のデータを取得
        if TOOL_NAME == "":
            go_x = 0
            go_y = 0
        else:
            name_tool = TOOL_NAME[i] #各工具を取得
            geometrio = TOOL_DXF_GEOMETRIO[name_tool]
            go_x = float(geometrio[1])
            go_y = float(geometrio[0])
            go_x = RND(go_x)
            go_y = RND(go_y)
        fst_data = 1
        current_pos.clear()
        tool_path.clear()
        tool_path_text.clear()
        tool_path_pos.clear()
        
        movement = QtGui.QPainterPath()
        movement_text = QtWidgets.QGraphicsTextItem()
        movement_pos = QtWidgets.QGraphicsEllipseItem()
        
        #textItem = QtGui.QGraphicsTextItem('QGraphicsTextItem')
        #textItem.setFont(QtGui.QFont('Arial Black', 9))

        for y in x: #各移動行を取得
            cX = RND(y[4] + go_x)
            cY = RND((y[3] + go_y) / -2)
            nc_g = y[2]
            nc_r = y[5]
            x_length = abs(y[10])
            z_length = abs(y[11])
            if nc_g == "0" or nc_g == "1":
                if fst_data == 1: #起点の場合の処理
                    if INCLUDE_FIRST_POSITION == 1:
                        current_pos.append(y[7])
                        movement_text.setFont(QtGui.QFont('Times', FONT_SIZE))
                        if y[2] == "0":
                            movement_text.setDefaultTextColor(QtGui.QColor(120, 0, 0, 255))
                        else:
                            movement_text.setDefaultTextColor(QtGui.QColor(0, 0, 100, 255))
                        if APPEND_G50 == 0:
                            PX = str(RND((cY - go_y) * -2))
                            PZ = str(RND(cX - go_x))
                        else:
                            PX = str(RND((cY - go_y) * -2  - y[8]))
                            PZ = str(RND(cX -go_x - y[9]))
                        if FLAG_PROG == 1:
                            if x_length > 0 and z_length > 0:
                                if y[2] == "0":
                                    tmp_text = "G" + y[2] + " X" + PX + " Z" + PZ
                                else:
                                    tmp_text = "G" + y[2] + " X" + PX + " Z" + PZ + " F" + str(y[6]) + "\n[U" + str(y[10]) +" W" + str(y[11]) + " D" + str(y[12]) + "]"
                                movement_text.setPlainText(tmp_text)
                            elif x_length > 0:
                                if y[2] == "0":
                                    tmp_text = "G" + y[2] + " X" + PX
                                else:
                                    tmp_text = "G" + y[2] + " X" + PX + " F" + str(y[6]) + "\n[U" + str(y[10]) + "]"
                                movement_text.setPlainText(tmp_text)
                            elif z_length > 0:
                                if y[2] == "0":
                                    tmp_text = "G" + y[2] + " Z" + PZ
                                else:
                                    tmp_text = "G" + y[2] + " Z" + PZ + " F" + str(y[6]) + "\n[W" + str(y[11]) + "]"
                                movement_text.setPlainText(tmp_text)
                            else:
                                movement_text.setPlainText("NO MOVEMENT")
                        else:
                            if x_length > 0 and z_length > 0:
                                tmp_text = "X" + PX + " Z" + PZ
                                movement_text.setPlainText(tmp_text)
                            elif x_length > 0:
                                tmp_text = "X" + PX
                                movement_text.setPlainText(tmp_text)
                            elif z_length > 0:
                                tmp_text = "Z" + PZ
                                movement_text.setPlainText(tmp_text)
                            else:
                                movement_text.setPlainText("NO MOVEMENT")
                        if APPEND_G50 == 0:
                            movement_text.setPos((cX - 0.075) * SCALE, (cY - 0.09) * SCALE)
                        else:
                            movement_text.setPos((cX - 0.075 - y[9]) * SCALE, (cY - 0.09 - y[8] / -2) * SCALE)
                        tool_path_text.append(movement_text)

                        movement_pos = QtWidgets.QGraphicsEllipseItem(RND(cX - 0.1) * SCALE, RND(cY - 0.1) * SCALE, 0.2 * SCALE, 0.2 * SCALE)
                        pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 0), 1, QtCore.Qt.SolidLine) #線分のスタイル設定
                        pen.setCosmetic(True) #線分のスタイル設定を適用
                        movement_pos.setPen(pen)
                        tool_path_pos.append(movement_pos)

                        movement = QtGui.QPainterPath()
                        movement_text = QtWidgets.QGraphicsTextItem()
                        movement_pos = QtWidgets.QGraphicsEllipseItem()

                    eX = cX
                    eY = cY
                    fst_data = 0
                else: #座標データの処理
                    movement.moveTo(eX * SCALE, eY * SCALE)
                    movement.lineTo(cX  * SCALE, cY * SCALE)
                    tool_path.append(movement)

                    movement_pos = QtWidgets.QGraphicsEllipseItem(RND(cX - 0.1) * SCALE, RND(cY - 0.1) * SCALE, 0.2 * SCALE, 0.2 * SCALE)
                    pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 0), 1, QtCore.Qt.SolidLine) #線分のスタイル設定
                    pen.setCosmetic(True) #線分のスタイル設定を適用
                    movement_pos.setPen(pen)
                    tool_path_pos.append(movement_pos)

                    movement_text.setFont(QtGui.QFont('Times', FONT_SIZE))
                    if y[2] == "0":
                        movement_text.setDefaultTextColor(QtGui.QColor(120, 0, 0, 255))
                    else:
                        movement_text.setDefaultTextColor(QtGui.QColor(0, 0, 100, 255))
                    if APPEND_G50 == 0:
                        PX = str(RND((cY - go_y) * -2))
                        PZ = str(RND(cX - go_x))
                    else:
                        PX = str(RND((cY - go_y) * -2  - y[8]))
                        PZ = str(RND(cX - go_x - y[9]))
                    if FLAG_PROG == 1:
                        if x_length > 0 and z_length > 0:
                            if y[2] == "0":
                                tmp_text = "G" + y[2] + " X" + PX + " Z" + PZ
                            else:
                                tmp_text = "G" + y[2] + " X" + PX + " Z" + PZ + " F" + str(y[6]) + "\n[U" + str(y[10]) +" W" + str(y[11]) + " D" + str(y[12]) + "]"
                            movement_text.setPlainText(tmp_text)
                        elif x_length > 0:
                            if y[2] == "0":
                                tmp_text = "G" + y[2] + " X" + PX
                            else:
                                tmp_text = "G" + y[2] + " X" + PX + " F" + str(y[6]) + "\n[U" + str(y[10]) + "]"
                            movement_text.setPlainText(tmp_text)
                        elif z_length > 0:
                            if y[2] == "0":
                                tmp_text = "G" + y[2] + " Z" + PZ
                            else:
                                tmp_text = "G" + y[2] + " Z" + PZ + " F" + str(y[6]) + "\n[W" + str(y[11]) + "]"
                            movement_text.setPlainText(tmp_text)
                        else:
                            movement_text.setPlainText("NO MOVEMENT")
                    else:
                        if x_length > 0 and z_length > 0:
                            tmp_text = "X" + PX + " Z" + PZ
                            movement_text.setPlainText(tmp_text)
                        elif x_length > 0:
                            tmp_text = "X" + PX
                            movement_text.setPlainText(tmp_text)
                        elif z_length > 0:
                            tmp_text = "Z" + PZ
                            movement_text.setPlainText(tmp_text)
                        else:
                            movement_text.setPlainText("NO MOVEMENT")
                    if APPEND_G50 == 0:
                        movement_text.setPos((cX - 0.075) * SCALE, (cY - 0.09) * SCALE)
                    else:
                        movement_text.setPos((cX - 0.075 - y[9]) * SCALE, (cY - 0.09 - y[8] / -2) * SCALE)
                    tool_path_text.append(movement_text)

                    movement = QtGui.QPainterPath()
                    movement_text = QtWidgets.QGraphicsTextItem()
                    current_pos.append(y[7])
                    eX = cX
                    eY = cY
            elif nc_g == "2" or nc_g == "3":
                cntX, cntY, d1, d2 = R_CENTER_DEGREE(eX, eY, cX, cY, nc_r, nc_g)
                cntX = RND(cntX)
                cntY = RND(cntY)
                d1 = RND(d1)
                d2 = RND(d2)
                movement.moveTo(eX * SCALE, eY * SCALE)
                movement.arcTo((cntX - nc_r) * SCALE, (cntY + nc_r) * SCALE, nc_r * 2 * SCALE, nc_r * -2 * SCALE, d1, d2 - d1)
                eX = cX
                eY = cY
                tool_path.append(movement)

                movement_text.setFont(QtGui.QFont('Times', FONT_SIZE))
                movement_text.setDefaultTextColor(QtGui.QColor(0, 100, 0, 255))
                if APPEND_G50 == 0:
                    PX = str(RND((cY -go_y) * -2))
                    PZ = str(RND(cX - go_x))
                else:
                    PX = str(RND((cY - go_y) * -2  - y[8]))
                    PZ = str(RND(cX - go_x - y[9]))
                if FLAG_PROG == 1:
                    movement_text.setPlainText("G" + y[2] + " X" + PX + " Z" + PZ + " R" + str(y[5]) + " F" + str(y[6]) + "\n[U" + str(y[10]) +" W" + str(y[11]) + "]")
                else:
                    movement_text.setPlainText("X" + PX + " Z" + PZ)
                if APPEND_G50 == 0:
                    movement_text.setPos((cX - 0.075) * SCALE, (cY - 0.09) * SCALE)
                else:
                    movement_text.setPos((cX - 0.075 - y[9]) * SCALE, (cY - 0.09 - y[8] / -2) * SCALE)
                tool_path_text.append(movement_text)

                movement_pos = QtWidgets.QGraphicsEllipseItem(RND(cX - 0.1) * SCALE, RND(cY - 0.1) * SCALE, 0.2 * SCALE, 0.2 * SCALE)
                pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 0), 1, QtCore.Qt.SolidLine) #線分のスタイル設定
                pen.setCosmetic(True) #線分のスタイル設定を適用
                movement_pos.setPen(pen)
                tool_path_pos.append(movement_pos)

                movement = QtGui.QPainterPath()
                movement_text = QtWidgets.QGraphicsTextItem()
                movement_pos = QtWidgets.QGraphicsEllipseItem()
                current_pos.append(y[7])
        TOOLS.append(tool_path[:])
        TOOLS_TEXT.append(tool_path_text[:])
        TOOLS_POS.append(tool_path_pos[:])
        PROGRAM_LINE_POS.append(current_pos[:])
    return TOOLS, PROGRAM_LINE_POS, TOOLS_TEXT, TOOLS_POS #TOOLS（工具毎に各工具軌跡を保持）　PROGRAM_LINE_POS（各軌跡がNCプログラムの何行目を示すかを、TOOLSと同じデータ構造で保持）





#-----NC_MOVEMENTで配列化されたデータから、リアルタイム移動パス作成する為の関数
def NC_REALTIME_MOVEMENT(MOVEMENT_DATA):
    REALTIME_MOVEMENT_DATA = []
    tool_path = []
    tool_line = []
    REALTIME_MOVEMENT_DATA_G50 = []
    tool_path_G50 = []
    tool_line_G50 = []
    for each_tool in MOVEMENT_DATA: #工具毎のデータを取得
        tool_path.clear()
        tool_path_G50.clear()
        fst_data = 1
        for pos in each_tool: #各移動行を取得
            tool_line.clear()
            tool_line_G50.clear()
            G50_U = pos[8] / -2
            G50_W = pos[9]
            nc_g = pos[2]
            nc_r = pos[5]
            nc_f = pos[6]
            g98_99 = pos[0]
            if g98_99 == "98":
                nc_s = pos[1]
                nc_f = CONVERT_G98_TO_G99(nc_s, nc_f)
            if fst_data == 1: #起点の場合の処理
                ex_x = pos[4]
                ex_y = pos[3] / -2
                tool_line.append([ex_x, ex_y])
                tool_line_G50.append([G50_W, G50_U])
                fst_data = 0
            else: #座標データの処理
                if nc_g == "0" or nc_g == "1":
                    current_x = pos[4]
                    current_y = pos[3] / -2
                    move_pos = NC_REALTIME_MOVEMENT_G0_1(ex_x, ex_y, current_x, current_y, nc_g, nc_f, 1)
                    for x in move_pos:
                        tool_line.append([x[0], x[1]])
                        tool_line_G50.append([G50_W, G50_U])
                    ex_x = pos[4]
                    ex_y = pos[3] / -2
                if nc_g == "2" or nc_g == "3":
                    current_x = pos[4]
                    current_y = pos[3] / -2
                    move_pos = NC_REALTIME_MOVEMENT_G2_3(ex_x, ex_y, current_x, current_y, nc_g, nc_f, 1, nc_r)
                    for x in move_pos:
                        tool_line.append([x[0], x[1]])
                        tool_line_G50.append([G50_W, G50_U])
                    ex_x = pos[4]
                    ex_y = pos[3]  / -2
            tool_path.append(tool_line[:])
            tool_path_G50.append(tool_line_G50[:])
        REALTIME_MOVEMENT_DATA.append(tool_path[:])
        REALTIME_MOVEMENT_DATA_G50.append(tool_path_G50[:])
    return REALTIME_MOVEMENT_DATA, REALTIME_MOVEMENT_DATA_G50 #REALTIME_MOVEMENT_DATA[ 各工具[各行の移動データ[], ...], ...]





#-----直線の２点間の座標を算出してリストに格納する関数
def NC_REALTIME_MOVEMENT_G0_1(EX_X, EX_Y, CURRENT_X, CURRENT_Y, NC_G, NC_F, MUTIPLYER): #Xは水平方向 Yは垂直方向
    moving_x = EX_X
    moving_y = EX_Y
    if NC_G == "0":
        NC_F = 2.0 #G0の場合の送り
    NC_F *= MUTIPLYER
    r_counter = 0
    MOVE_POS = []
    if EX_X == CURRENT_X and EX_Y != CURRENT_Y: #Y方向のみの動きの場合
        y_length = abs(EX_Y - CURRENT_Y)
        spin = int(y_length / NC_F) #spinは、2点間を現在の送りで、何回転で移動するかを示す
        if spin <= 0:
             spin = 1
        fy = y_length / spin
        if CURRENT_Y < EX_Y:
            fy *= -1
        while(True):
            moving_y += fy
            if r_counter + 1 == spin:
                moving_y = CURRENT_Y
            MOVE_POS.append([RND(CURRENT_X), RND(moving_y)])
            r_counter += 1
            if r_counter >= spin:
                break
    elif EX_X != CURRENT_X and EX_Y == CURRENT_Y: #X方向のみの動きの場合
        x_length = abs(EX_X - CURRENT_X)
        spin = int(x_length / NC_F) #spinは、2点間を現在の送りで、何回転で移動するかを示す
        if spin <= 0:
            spin = 1
        fx = x_length / spin
        if CURRENT_X < EX_X:
            fx *= -1
        while(True):
            moving_x += fx
            if r_counter + 1 == spin:
                moving_x = CURRENT_X
            MOVE_POS.append([RND(moving_x), RND(CURRENT_Y)])
            r_counter += 1
            if r_counter >= spin:
                break
    elif EX_X != CURRENT_X and EX_Y != CURRENT_Y: #XY両方向の動きの場合
        x_length = abs(EX_X - CURRENT_X)
        y_length = abs(EX_Y - CURRENT_Y)
        if y_length >= x_length:
            spin = int(y_length / NC_F)
        elif y_length < x_length:
            spin = int(x_length / NC_F)
        if spin <= 0:
            spin = 1
        fx = x_length / spin
        fy = y_length / spin
        if CURRENT_Y < EX_Y:
            fy *= -1
        if CURRENT_X < EX_X:
            fx *= -1
        while(True):
            moving_x += fx
            moving_y += fy
            if r_counter + 1 == spin:
                moving_x = CURRENT_X
                moving_y = CURRENT_Y
            MOVE_POS.append([RND(moving_x), RND(moving_y)])
            r_counter += 1
            if r_counter >= spin:
                break
    return MOVE_POS





#-----円弧の２点間の座標を算出してリストに格納する関数
def NC_REALTIME_MOVEMENT_G2_3(EX_X, EX_Y, CURRENT_X, CURRENT_Y, NC_G, NC_F, MUTIPLYER, NC_R): #Xは水平方向 Yは垂直方向
    moving_x = EX_X
    moving_y = EX_Y
    if NC_G == "0":
        NC_F = 0.5
    NC_F *= MUTIPLYER
    r_counter = 0
    MOVE_POS = []
    x_length = abs(EX_X - CURRENT_X)
    y_length = abs(EX_Y - CURRENT_Y)
    if y_length >= x_length:
        spin = int(y_length / NC_F)
    elif y_length < x_length:
        spin = int(x_length / NC_F)
    if spin <= 0:
        spin = 1
    center_x, center_y, degree1, degree2 = R_CENTER_DEGREE(EX_X, EX_Y, CURRENT_X, CURRENT_Y, NC_R, NC_G)
    degree_length = abs(degree1 - degree2)
    move_degree = degree_length / spin
    ex_xx = EX_X
    ex_yy = EX_Y
    RCounter = 0
    while(True):
        if NC_G == "3":
            degree1 -= move_degree
        elif NC_G == "2":
            degree1 += move_degree
        mx, my = R_POSITION(center_x, center_y, NC_R, degree1)
        moving_x += mx - ex_xx
        moving_y += my - ex_yy
        if r_counter + 1 == spin:
            moving_x = CURRENT_X
            moving_y = CURRENT_Y
        MOVE_POS.append([RND(moving_x), RND(moving_y)])
        ex_xx = moving_x
        ex_yy = moving_y
        RCounter += 1
        if RCounter >= spin:
            break
    return MOVE_POS





#-----NC_REALTIME_MOVEMENTで配列化されたデータをパスへ変換する関数
def NC_REALTIME_PATH(REALTIME_MOVEMENT_DATA, SCALE=50):
    REALTIME_TOOLS = []
    for x in REALTIME_MOVEMENT_DATA: #工具毎のデータを取得
        fst_data = 1
        tool_path = QtGui.QPainterPath()
        for y in x: #各移動行を取得
            for z in y:
                if fst_data == 1: #起点の場合の処理
                    tool_path.moveTo(z[0] * SCALE, z[1] * SCALE)
                    fst_data = 0
                else: #座標データの処理
                    tool_path.lineTo(z[0] * SCALE, z[1] * SCALE)
        REALTIME_TOOLS.append(tool_path)
    return REALTIME_TOOLS





#-----G98をG99へ変換する関数
def CONVERT_G98_TO_G99(NC_S, NC_F):
    if NC_S == 0:
        NC_S = 5000
    if NC_F == 0:
        NC_F == 0.001
    NC_F = NC_F / NC_S
    if NC_F < 0.001:
        NC_F= 0.001
    RND(NC_F)
    return NC_F





#-----G98をG99へ変換する関数
def CONVERT_G99_TO_G98(NC_S, NC_F):
    if NC_S == 0:
        NC_S = 5000
    if NC_F == 0:
        NC_F == 0.001
    NC_F = NC_F * NC_S
    if NC_F < 0.001:
        NC_F= 0.001
    RND(NC_F)
    return NC_F





#-----閉じたDXFデータをパスへ変換する関数（工具表示用）
def CONVERT_CLOSED_DXF(FILEPATH, SCALE=50, DIRECTION=-1, SHIFT_X="0", SHIFT_Z="0", OFFSET_X="0", OFFSET_Z="0"):
    SHIFT_X = RND(float(SHIFT_X) + float(OFFSET_X) / 2)
    SHIFT_Z = RND(float(SHIFT_Z) + float(OFFSET_Z))
    ret = 0
    CLOSED_PATH = None
    dxf_data = ezdxf.readfile(FILEPATH)
    msp = dxf_data.modelspace()
    line = {}
    line_path = []
    StartPointFlag = 0
    line.clear()
    line_path.clear()

    #####番号のレイヤー名のみ摘出
    Layer_num = []
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
    #####レイヤー内にあるアイテム毎の処理
    for i, x in enumerate(n_one.entities):
        Line_Type = x.dxf.dxftype #線種
        if Line_Type == "LINE": #線種が直線の場合
            if x.dxf.start != x.dxf.end: #始点と終点が同一点ではない場合
                cx0 = RND(x.dxf.start[0]) + SHIFT_Z
                cy0 = RND(x.dxf.start[1]) + SHIFT_X
                cx1 = RND(x.dxf.end[0]) + SHIFT_Z
                cy1 = RND(x.dxf.end[1]) + SHIFT_X
                line[str(i) + "_T"] = Line_Type
                line[str(i) + "_S"] = [cx0, cy0] #始点
                line[str(i) + "_E"] = [cx1, cy1] #終点
                if StartPointFlag == 0:
                    line_start_point = [cx0, cy0]
                    StartPointFlag = 1 #移動線の開始点有りとする
        elif Line_Type == "ARC": #線種が円弧の場合
            cx0 = RND(x.start_point[0])  + SHIFT_Z #反時計回りの始まりのX
            cy0 = RND(x.start_point[1])  + SHIFT_X #反時計回りの始まりのY
            cx1 = RND(x.end_point[0])  + SHIFT_Z #反時計周りの終わりのX
            cy1 = RND(x.end_point[1])  + SHIFT_X #反時計周りの終わりのY
            cx2 = RND(x.dxf.center[0]) + SHIFT_Z
            cy2 = RND(x.dxf.center[1]) + SHIFT_X
            R = RND(x.dxf.radius)
            F = RND(x.dxf.start_angle)
            N = RND(x.dxf.end_angle)
            line[str(i) + "_T"] = Line_Type
            line[str(i) + "_S"] = [cx0, cy0] #始点
            line[str(i) + "_E"] = [cx1, cy1] #終点
            line[str(i) + "_C"] = [cx2, cy2] #円弧の中心位置
            line[str(i) + "_R"] = R
            line[str(i) + "_F"] = F #反時計回りの始まりの角度
            line[str(i) + "_N"] = N #反時計周りの終わりの角度
            if StartPointFlag == 0:
                line_start_point = [cx0, cy0]
                StartPointFlag = 1 #移動線の開始点有りとする
    if len(line) > 0:
        #####開始点の処理
        line_path.append([line_start_point, "L", "", ""]) #移動線の開始点を配列化
        start_point = line_start_point #次の線分の開始座標とする
        loop_num = 0
        while(True):
            #####以後の座標の処理
            keys = [k for k, v in line.items() if v == start_point] #前の座標を有する辞書キーを検索
            if len(keys) == 0: #該当する座標が無い場合は、移動線の終端迄来たとし、処理を終了する
                break
            p_num, p_com = keys[0].split("_") #辞書キーを番号とコマンドに分離する
            if p_com == "S":
                REV = "NON_REV"
                dist_point = line[p_num + "_E"] #検索したキーにSが含まれた場合、Eを有するキーの座標を線分の終点とする
            elif p_com == "E":
                dist_point = line[p_num + "_S"] #検索したキーにEが含まれた場合、Sを有するキーの座標を線分の終点とする
                REV = "REV"
            line[p_num + "_S"] = ["*", "*"] #座標を*で埋め、検索に掛からないようにする（使用済みにする）
            line[p_num + "_E"] = ["*", "*"] #座標を*で埋め、検索に掛からないようにする（使用済みにする）
            if line[p_num + "_T"] == "LINE":
                line_path.append([dist_point, "L", "", ""]) #終点を線分として配列化
            elif line[p_num + "_T"] == "ARC":
                cnt = line[p_num + "_C"]
                ret_val = ROTATION_DIRECTION_DETECTOR(start_point[0], start_point[1], dist_point[0], dist_point[1], cnt[0], cnt[1]) #円弧がG2とG3の何れか判定
                r = line[p_num + "_R"]
                line_path.append([dist_point, "R", ret_val, r]) #終点を円弧として配列化
            start_point = dist_point #次の線分の開始座標とする
            loop_num += 1
        y_direction = DIRECTION #CADデータを縦方向に反転させる（1 or -1）
        ft = 1
        CLOSED_PATH = QtGui.QPainterPath()
        #####レイヤー内にあるアイテム毎の処理
        for i, x in enumerate(line_path):
            Line_Type = x[1] #線種
            if Line_Type == "L": #線種が直線の場合
                cX = x[0][0]
                cY = x[0][1] * y_direction
                if ft ==1:
                    CLOSED_PATH.moveTo(cX * SCALE, cY * SCALE)
                    ft = 0
                else:
                    CLOSED_PATH.lineTo(cX * SCALE, cY * SCALE)
                eX = cX
                eY = cY
            elif Line_Type == "R": #線種が円弧の場合
                cX = x[0][0]
                cY = x[0][1] * y_direction
                g2_g3 = x[2].replace("G", "")
                R = x[3]
                if g2_g3 == "2" and y_direction == 1:
                    g2_g3 = "3"
                elif g2_g3 == "3" and y_direction == 1:
                    g2_g3 = "2"
                cntX , cntY, d1, d2 = R_CENTER_DEGREE2(eX, eY, cX, cY, R, g2_g3)
                cntX = RND(cntX)
                cntY = RND(cntY)
                d1 = RND(d1)
                d2 = RND(d2)
                dd1 = abs(d1)
                dd2 = abs(d2)
                if dd1 > dd2:
                    DL = 360 - (dd1 - dd2)
                else:
                    DL = dd2 - dd1
                if g2_g3 == "3":
                    DL = DL - 360
                DL = RND(DL)
                CLOSED_PATH.arcTo((cntX - R) * SCALE, (cntY + R) * SCALE, R * 2 * SCALE, R * -2 * SCALE, d1, DL) #円を囲むボックスの右上の頂点（cntX - R, cntY + R）、幅（プラス方向）、高さ（マイナス方向）、開始角度、移動角度
                eX = cX
                eY = cY
    else:
        ret = 1
    return CLOSED_PATH, ret





def PROGRAM_TO_DXF(PROGRAM_TEXT, FILE_PATH):
    ret, NC_PROGRAM = NC_SPLITTER(PROGRAM_TEXT)
    APPEND_G50 = 1
    MOVEMENT_DATA, _, _, _ = NC_MOVEMENT(NC_PROGRAM, APPEND_G50)
    dwg = ezdxf.new('R2018')
    dwg.layers.remove('0')
    dwg.layers.remove('Defpoints')
    dwg.header['$INSUNITS'] = 4
    dwg.header['$MEASUREMENT'] = 1
    dwg.header['$LUNITS'] = 2
    dwg.header['$AUNITS'] = 0
    msp = dwg.modelspace()
    layer_num = 1
    for x in MOVEMENT_DATA:
        #if layer_num >= 1:
        dwg.layers.new(str(layer_num), dxfattribs={'color': layer_num})
        first_line = 1
        for y in x:
            g_code = y[2]
            cur_x = y[4]
            cur_y = RND(y[3] /2)
            nc_r = y[5]
            if first_line == 1:
                msp.add_circle(center=[cur_x, cur_y], radius=0.1, dxfattribs={'layer': str(layer_num)})
                ex_x = cur_x
                ex_y = cur_y
                first_line = 0
            else:
                if g_code == "0" or g_code == "1":
                    msp.add_line((ex_x, ex_y), (cur_x, cur_y), dxfattribs={'layer': str(layer_num)})
                elif g_code == "2" or g_code == "3":
                    if g_code == "2":
                        g_code = "3"
                    else:
                        g_code = "2"
                    cntX, cntY, d1, d2 = R_CENTER_DEGREE(ex_x, ex_y, cur_x, cur_y, nc_r, g_code)
                    #cntX = RND(cntX)
                    #cntY = RND(cntY)
                    d1 = d1
                    d2 = d2
                    if g_code == "2":
                        arc_angle = d2 - d1
                        arc = ConstructionArc.from_2p_angle(start_point=(ex_x, ex_y), end_point=(cur_x, cur_y), angle=arc_angle, ccw = True)
                        #msp.add_arc(center=[cntX, cntY], radius = nc_r, start_angle = d1, end_angle = d2, dxfattribs = {'layer': str(layer_num)})
                    else:
                        arc_angle = d1 - d2
                        arc = ConstructionArc.from_2p_angle(start_point=(ex_x, ex_y), end_point=(cur_x, cur_y), angle=arc_angle, ccw = False)
                        #msp.add_arc(center=[cntX, cntY], radius = nc_r, start_angle = d2, end_angle = d1, dxfattribs = {'layer': str(layer_num)})
                    msp.add_arc(center=arc.center, radius=arc.radius, start_angle=arc.start_angle, end_angle=arc.end_angle, dxfattribs = {'layer': str(layer_num)})
                ex_x = cur_x
                ex_y = cur_y
        layer_num += 1
    if len(MOVEMENT_DATA) == 0:
        msgbox = QtWidgets.QMessageBox()
        msgbox.setWindowTitle("Massage")
        msgbox.setText("変換するデータが有りません。")
        ret = msgbox.exec_()
    else:
        dwg.set_modelspace_vport(0, (0,0))
        dwg.saveas(FILE_PATH)
        msgbox = QtWidgets.QMessageBox()
        msgbox.setWindowTitle("Massage")
        msgbox.setText("プログラムをDXFへ変換しました。")
        ret = msgbox.exec_()
