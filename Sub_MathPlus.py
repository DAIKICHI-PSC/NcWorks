import math


#####Round value to plus and minus direction(0.001). 
def RND(VALUE):
    if VALUE > 0:
        addValue = 0.0005
    elif VALUE < 0:
        addValue = -0.0005
    else:
        addValue = 0
    VALUE = int((VALUE + addValue) * 1000) / 1000
    return VALUE


#####Round value to plus and minus direction(0.0001). 
def RND_2(VALUE):
    if VALUE > 0:
        addValue = 0.00005
    elif VALUE < 0:
        addValue = -0.00005
    else:
        addValue = 0
    VALUE = int((VALUE + addValue) * 10000) / 10000
    return VALUE


#####Get start and end position of arc from center position and degree.
def GET_POS_ON_ARC(CENTER_X, CENTER_Y, START_ANGLE, END_ANGLE, R):
    start_x = RND(R * math.cos(math.radians(START_ANGLE)) + CENTER_X)
    start_y = RND(R * math.sin(math.radians(START_ANGLE)) + CENTER_Y)
    end_x = RND(R * math.cos(math.radians(END_ANGLE)) + CENTER_X)
    end_y = RND(R * math.sin(math.radians(END_ANGLE)) + CENTER_Y)
    return start_x, start_y,end_x, end_y


#####Get rotation direction from start position on circle, end position on circle and center position of circle.
def ROTATION_DIRECTION_DETECTOR(START_X_ON_CIRCLE, START_Y_ON_CIRCLE, END_X_ON_CIRCLE, END_Y_ON_CIRCLE, CIRCLE_CENTER_X, CIRCLE_CENTER_Y):
    #(EndX - CenterX) * (StartY - CenterY) - (StartX - CenterX) * (EndY - CenterY)
    ret = (CIRCLE_CENTER_X - END_X_ON_CIRCLE) * (START_Y_ON_CIRCLE - END_Y_ON_CIRCLE) - (START_X_ON_CIRCLE - END_X_ON_CIRCLE) * (CIRCLE_CENTER_Y - END_Y_ON_CIRCLE)
    #ret = (END_X_ON_CIRCLE - CIRCLE_CENTER_X) * (START_Y_ON_CIRCLE - CIRCLE_CENTER_Y ) - (START_X_ON_CIRCLE - CIRCLE_CENTER_X) * (END_Y_ON_CIRCLE - CIRCLE_CENTER_Y)
    if ret < 0:
        ret = "G2" #Anti Clockwise
    elif ret > 0:
        ret = "G3" #Clockwise
    else:
        ret = "0" #3 points on a same line
    return ret


#####Detect intersection of two lines.
def INTERSECTION_DETECTOR(POS0, POS1, POS2, POS3):
    x0 = POS1[0] - POS0[0]
    x1 = POS2[0] - POS3[0]
    x2 = POS1[1] - POS0[1]
    x3 = POS2[1] - POS3[1]
    POS3 = float(x0 * x3 - x1 * x2)
    if POS3 == 0:
        return False
    c0 = POS2[0] - POS0[0]
    c1 = POS2[1] - POS0[1]
    s = (c0 * x3 - c1 * x1) / POS3
    t = (c1 * x0 - c0 * x2) / POS3
    if 0 <= s <= 1 and 0 <= t <= 1:
        return True
    return False


#####Get coordinate of intersection of two lines.
def GET_CROSS_POINT(LINE1_COORDS1, LINE1_COORDS2, LINE2_COORDS1, LINE2_COORDS2):
    cross_point = (0,0)
    denominator = (LINE1_COORDS2[0] - LINE1_COORDS1[0]) * (LINE2_COORDS2[1] - LINE2_COORDS1[1]) - (LINE1_COORDS2[1] - LINE1_COORDS1[1]) * (LINE2_COORDS2[0] - LINE2_COORDS1[0])

    #If lines are pararell
    if (denominator == 0):
        return False, cross_point

    vector11_21 = ((LINE2_COORDS1[0] - LINE1_COORDS1[0]), (LINE2_COORDS1[1] - LINE1_COORDS1[1]))
    r = ((LINE2_COORDS2[1] - LINE2_COORDS1[1]) * vector11_21[0] - (LINE2_COORDS2[0] - LINE2_COORDS1[0]) * vector11_21[1]) / denominator
    s = ((LINE1_COORDS2[1] - LINE1_COORDS1[1]) * vector11_21[0] - (LINE1_COORDS2[0] - LINE1_COORDS1[0]) * vector11_21[1]) / denominator

    #Case of using r
    distance = ((LINE1_COORDS2[0] - LINE1_COORDS1[0]) * r, (LINE1_COORDS2[1] - LINE1_COORDS1[1]) * r)
    cross_point = (RND(LINE1_COORDS1[0] + distance[0]), RND(LINE1_COORDS1[1] + distance[1]))
    return True, cross_point


#####２点を通る円の中心値と２点の角度を算出
def R_CENTER_DEGREE(START_X = 0, START_Y = 0, END_X = 10, END_Y = 10, NC_R = 10, NC_G = "2"):
    #線分の距離
    distanse = math.sqrt((END_X - START_X) ** 2 + (END_Y - START_Y) ** 2)
    #線分から円の中心までの距離
    length = math.sqrt(NC_R ** 2 - distanse  ** 2 / 4)
    #G3はlengthにマイナスをかける。
    if NC_G == "2":
        length *= -1
    #円の中心
    rCenterX = (START_X + END_X) / 2 + (END_Y - START_Y) * length / distanse
    rCenterY = (START_Y + END_Y) / 2 - (END_X - START_X) * length / distanse
    #座標START_X,START_Yの角度
    degree1 = math.acos(RND_2((START_X - rCenterX) / NC_R)) * 180 / math.pi
    #座標END_X,END_Yの角度
    degree2 = math.acos(RND_2((END_X - rCenterX) / NC_R)) * 180 / math.pi
    #円の上下共に同じ角度になる為、下側をマイナスにする
    if START_X > END_X and START_Y < END_Y and NC_G == "3":
        degree1 *= -1
        degree2 *= -1
    if START_X > END_X and START_Y > END_Y and NC_G == "3":
        degree1 *= -1
        degree2 *= -1
    if START_X < END_X and START_Y > END_Y and NC_G == "2":
        degree1 *= -1
        degree2 *= -1
    if START_X < END_X and START_Y < END_Y and NC_G == "2":
        degree1 *= -1
        degree2 *= -1
    #START_X,END_X,START_Y,END_Yは実寸
    #G2は反時計周りに描画。G3は時計周りに描画。
    return rCenterX, rCenterY, degree1, degree2


#####２点を通る円の中心値と２点の角度を算出（QPainterPath用）
def R_CENTER_DEGREE2(START_X = 0, START_Y = 0, END_X = 10, END_Y = 10, NC_R = 10, NC_G = "2"):
    #線分の距離
    distanse = math.sqrt((END_X - START_X) ** 2 + (END_Y - START_Y) ** 2)
    #線分から円の中心までの距離
    length = math.sqrt(NC_R ** 2 - distanse  ** 2 / 4)
    #G3はlengthにマイナスをかける。
    if NC_G == "2":
        length *= -1
    #円の中心
    rCenterX = (START_X + END_X) / 2 + (END_Y - START_Y) * length / distanse
    rCenterY = (START_Y + END_Y) / 2 - (END_X - START_X) * length / distanse
    #座標START_X,START_Yの角度
    degree1 = math.acos(RND_2((START_X - rCenterX) / NC_R)) * 180 / math.pi
    #座標END_X,END_Yの角度
    degree2 = math.acos(RND_2((END_X - rCenterX) / NC_R)) * 180 / math.pi
    #角度をQPainterPath規格と同じにする（円弧の上弦はマイナスとなる）（DXFは下弦がマイナスとなる）
    if START_Y < rCenterY:
        degree1 *= -1
    if END_Y < rCenterY:
        degree2 *= -1
    #通常の角度に変換
    if degree1 < 0:
        degree1 += 360
    if degree2 < 0:
        degree2 += 360
    '''
    #角度をDXF規格と同じにする（円弧の下弦はマイナスとなる）
    if START_Y < rCenterY:
        degree1 *= -1
    if END_Y < rCenterY:
        degree2 *= -1
    #通常の角度に変換
    if degree1 < 0:
        degree1 += 360
    if degree2 < 0:
        degree2 += 360
    '''
    '''
    #円の上下共に同じ角度になる為、下側をマイナスにする
    if START_X > END_X and START_Y < END_Y and NC_G == "3":
        degree1 *= -1
        degree2 *= -1
    if START_X > END_X and START_Y > END_Y and NC_G == "3":
        degree1 *= -1
        degree2 *= -1
    if START_X < END_X and START_Y > END_Y and NC_G == "2":
        degree1 *= -1
        degree2 *= -1
    if START_X < END_X and START_Y < END_Y and NC_G == "2":
        degree1 *= -1
        degree2 *= -1
    #START_X,END_X,START_Y,END_Yは実寸
    #G2は反時計周りに描画。G3は時計周りに描画。
    '''
    return rCenterX, rCenterY, degree1, degree2


#####円の中心座標、半径、角度から、円上の座標を算出
def R_POSITION(rCenterX, rCenterY, NC_R, DEGREE):
    angle = RND(math.pi * DEGREE / 180)
    x_on_r = math.cos(angle) * NC_R + rCenterX
    y_on_r = math.sin(angle) * NC_R + rCenterY
    return x_on_r, y_on_r


#-----2線の角度を計算する関数
def CALCULATE_DEGREE(X_LENGTH = 0.98, Z_LENGTH = 0.986):
    if X_LENGTH >= Z_LENGTH:
        tanA = RND(Z_LENGTH / X_LENGTH)
        MOVE_DEGREE = 90 - RND(math.atan(tanA) * 180 / math.pi)
    elif X_LENGTH < Z_LENGTH:
        tanA = RND(X_LENGTH / Z_LENGTH)
        MOVE_DEGREE = RND(math.atan(tanA) * 180 / math.pi)
    return MOVE_DEGREE


#-----線と角度からもう一辺の長さを求める関数
def CALCULATE_Aa_c(a = 1, DEGREE = 30):
    if DEGREE >= 45:
        DEGREE = 90 - DEGREE
    c = RND(a / math.tan(math.radians(DEGREE)))
    return c


#-----線と角度からもう一辺の長さを求める関数
def CALCULATE_Ac_a(c = 1, DEGREE = 30):
    if DEGREE >= 45:
        DEGREE = 90 - DEGREE
    a = RND(c * math.tan(math.radians(DEGREE)))
    return a


if __name__ == '__main__':
    print(GET_CROSS_POINT((0,0), (10,10), (0,10), (10,0)))
