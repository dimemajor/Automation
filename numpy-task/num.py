import numpy as np


W = 700 # Overall width
H = 1200 # Overall height

L_TCK = 80 # LiningThickness
L_OFF = 10 # LiningOffset
L_DPT = 50 # LiningDepth
L_POFF_Y = 20 # LiningToPanelOffsetY
L_POFF_X = 50 # LiningToPanelOffsetX

F_DPT = 30 # FrameDepth
F_TCK = 50 # FrameThickness

window = {}
output = ['frame', 'panel', 'lining']

def create_rect(w, h, point):
    def new_point(arr, point): # generate a new points from previous point gotten 
        point = np.array(arr) * dim + point
        coord.append(point)
        return point
    coord = [] # list to store the coordinates of the rectangle
    coord.append(point)
    dim = np.array([[w,h]])
    point = new_point([[1,0]], point)
    point = new_point([[0,1]], point)
    point = new_point([[-1,0]], point)
    point = new_point([[0,-1]], point)
    return coord

def get_midpoint(arr): # function to get midpoint of rectangle
    return (((arr[0]+arr[1])/2) * np.array([1,0])) + (((arr[1]+arr[2])/2)[0][1] * np.array([0,1]))

def translate(trfm, arr, direction): # function to translate rectangle to origin with midpoint at origin
    M = np.array([[1, 0, trfm[0][0]],
                [0, 1, trfm[0][1]],
                [0, 0, 1]
                ])
    matrices = []
    for matrix in arr:
        if direction == 'negative':
            new_matrix = np.array([[-matrix[0][0], -matrix[0][1], 1]])
        elif direction == 'positive':
            new_matrix = np.array([[matrix[0][0], matrix[0][1], 1]])
        matrices.append(np.dot(M, new_matrix.transpose()))
    print(matrices)
    return matrices

def scale(scale, arr):
    scale_fac = np.array([[scale, 0, 0],[0, scale, 0], [0, 0, scale]])
    scaled_matrix = [np.dot(scale_fac, point) for point in arr]
    scaled_matrix = [point.transpose() for point in scaled_matrix]
    return scaled_matrix

def translate_point(factor, rect): # move point by a specified thickness or factor
    def get_rotation(): # is the order of rect clockwise or anticlockwise?
        if rect[0][0][0] < rect[1][0][0]:
            rotation = 'anticlockwise'
        elif rect[0][0][1] < rect[1][0][1]:
            rotation = 'clockwise'
        return rotation

    rotation = get_rotation()
    new_rect = []
    if rotation == 'anticlockwise':
        new_rect.append(rect[0][0] + np.array([-factor, -factor]))
        new_rect.append(rect[1][0] + np.array([factor, -factor]))
        new_rect.append(rect[2][0] + np.array([factor, factor]))
        new_rect.append(rect[3][0] + np.array([-factor, factor]))
        new_rect.append(rect[4][0] + np.array([-factor, -factor]))
    elif rotation == 'clockwise':
        new_rect.append(rect[0][0] + np.array([-factor, -factor]))
        new_rect.append(rect[1][0] + np.array([-factor, factor]))
        new_rect.append(rect[2][0] + np.array([factor, factor]))
        new_rect.append(rect[3][0] + np.array([factor, -factor]))
        new_rect.append(rect[4][0] + np.array([-factor, -factor]))

    return new_rect

def transform(thickness, rect):
    mid_point = get_midpoint(rect)
    # translating
    translated_matrix = translate(mid_point, rect, direction='negative')
    # scaling
    scaled_matrix = scale(thickness, translated_matrix)
    # translating
    rev_trans_matrix = translate(mid_point, scaled_matrix, direction='positive')
    rev_trans_matrix = [point.transpose() for point in rev_trans_matrix]
    
    return rev_trans_matrix 

starting_point = np.array([[0, 2]])
window['frame'] = create_rect(W, H, starting_point)
window['panels'] = translate_point(-F_TCK, window['frame'])
window['linings'] = translate_point(L_POFF_X, window['frame'])

print(window)
