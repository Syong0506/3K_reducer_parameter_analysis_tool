#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from scipy.optimize import minimize
from numpy import trunc
from numpy import round
from numpy import arange
from OGRCT_m5_ui import Ui_MainWindow

def forward_eff(x):
    S1, P1, R1 = x[0] , x[1] , x[2]
    S2, P2, R2 = x[3] , x[4] , x[5]

    I1 = R1/ S1
    I2 = R1/ R2* P2/ P1
    n_forw = (1+na* nb* I1)* (1- I2)/ ((1+I1)* (1- nb* nc* I2))
    return n_forw

def backward_eff(x):
    S1, P1, R1 = x[0] , x[1] , x[2]
    S2, P2, R2 = x[3] , x[4] , x[5]
    I1 = R1/ S1
    I2 = R1/ R2* P2/ P1
    n_backw = (1+I1)* na* (nb* nc- I2)/ (nc* (na* nb+I1)* (1- I2))
    return n_backw

def gear_ratio(x):
    S1, P1, R1 = x[0] , x[1] , x[2]
    S2, P2, R2 = x[3] , x[4] , x[5]
    I1 = R1/ S1
    I2 = R1/ R2* P2/ P1
    # 기어비
    Gr = (1+I1)/ (1- I2)
    return Gr

# x_list = [S1, P1, R1, S2, P2, R2, 정구동효율, 역구동효율, 기어비, 기어비오차]

def module_min_max(m_min, m_max_step, step):
    m_list = []
    for i in arange(m_min, m_max_step, step):
        m_list.append(i)
     
    return m_list

# 모듈 계산
def module_range(minimum, maximum, module):
    if minimum%module == 0:
        start = minimum/module
    else:
        start = trunc(minimum/module) + 1
    if maximum%module == 0:
        end = maximum/module
    else:
        end = trunc(maximum/module) + 1
    list_range = []
    for i in arange(start, end):
        value = round(i*module,9)
        list_range.append(value)
    return list_range

def module1_gear_list(m_list, bnds):
    S1_module_list = []
    P1_module_list = []
    R1_module_list = []

    for i in range(len(m_list)):
        S1_list = module_range(bnds[0], bnds[1], m_list[i])
        P1_list = module_range(bnds[2], bnds[3], m_list[i])
        R1_list = module_range(bnds[4], bnds[5], m_list[i])

        S1_module_list.append(S1_list)
        P1_module_list.append(P1_list)
        R1_module_list.append(R1_list)

    return S1_module_list, P1_module_list, R1_module_list

def module2_gear_list(m_list, bnds):
    S2_module_list = []
    P2_module_list = []
    R2_module_list = []

    for i in range(len(m_list)):     
        S2_list = module_range(bnds[0], bnds[1], m_list[i])
        P2_list = module_range(bnds[2], bnds[3], m_list[i])
        R2_list = module_range(bnds[4], bnds[5], m_list[i])

        S2_module_list.append(S2_list)
        P2_module_list.append(P2_list)
        R2_module_list.append(R2_list)
    return S2_module_list, P2_module_list, R2_module_list

# 제한조건 : 유성기어열 치수제한조건 , equality condition
def dimension_constraint(m_list, S_list, P_list, R_list):
    dimenstion_list = []
    dimenstion_module_list = []
    for n in range(len(m_list)):
      S = S_list[n]
      P = P_list[n]
      R = R_list[n]
      for i in range(len(S)):
        for j in range(len(P)):
          for k in range(len(R)):
            if R[k] - S[i] - 2* P[j] == 0:
              dimenstion_list.append(S[i])
              dimenstion_list.append(P[j])
              dimenstion_list.append(R[k])
      dimenstion_module_list.append(dimenstion_list)
    return dimenstion_module_list

# 제한조건 : 복합 Planetary 기어의 중심거리 일치조건 , equality condition
def center_constraint(m_list, list_1, list_2):
    x = []
    list_module = []
    for n in range(len(m_list)):
      module_list_1 = list_1[n]
      module_list_2 = list_2[n]
      for i in range(len(module_list_1)//3):
        for j in range(len(module_list_2)//3):
          if (module_list_1[i*3] + module_list_1[i*3+1]) - (module_list_2[j*3] + module_list_2[j*3+1]) == 0:
            if module_list_1[i*3+2]/module_list_2[j*3+2]*module_list_2[j*3+1]/module_list_1[i*3+1] != 1:
              x.append(module_list_1[i*3])
              x.append(module_list_1[i*3+1])
              x.append(module_list_1[i*3+2])
              x.append(module_list_2[j*3])
              x.append(module_list_2[j*3+1])
              x.append(module_list_2[j*3+2])
      list_module.append(x)
    return list_module

# 기어값 수치를 6개로 묶음
def x_list_div(m_list, x_list):
  x_module_list = []
  x_module_list_6 = []
  for n in range(len(m_list)):
    x_module_list = x_list[n]
    x_list_6 = [x_module_list[i:i+6] for i in range(0, len(x_module_list), 6)]
    x_module_list_6.append(x_list_6)
  return x_module_list_6

# 정구동 효율 계산 : 정구동 효율이 음수인 경우 제외
def forward_eff_list(x_list_6):
    x_list_f = []
    for i in range(len(x_list_6)):
        x = x_list_6[i]
        x_forw = round(forward_eff(x),4)
        x_list_6[i].append(x_forw)
        if x_forw > 0:
            x_list_f.append(x_list_6[i])
    #x_list_6.sort(key=lambda x: -x[6])
    return x_list_f

# 역구동 효율 계산 : 역구동 효율이 음수이 경우 제외
def backward_eff_lsit(x_list_f):
    x_list_fb = []
    for i in range(len(x_list_f)):
        x = x_list_f[i]
        x_backw = round(backward_eff(x),4)
        x_list_f[i].append(x_backw)
        if x_backw > 0:
            x_list_fb.append(x_list_f[i])
    return x_list_fb
# 기어비 계산 : 기어비가 음수인 경우 제외
def gear_ratio_list(x_list_fb):
    x_list_fbgr = []
    for i in range(len(x_list_fb)):
        x = x_list_fb[i]
        x_gr = round(gear_ratio(x),2)
        x_list_fb[i].append(x_gr)
        if x_gr > 0:
            x_list_fbgr.append(x_list_fb[i])
    return x_list_fbgr

# 제한조건 : 역구동 효율 목표이상
def backward_constraint(x_list_fbgr,n_target):
    x_list_bc = []
    for i in range(len(x_list_fbgr)):
        if x_list_fbgr[i][7] >= n_target:
            x_list_bc.append(x_list_fbgr[i])
    return x_list_bc

# 제한조건 : 목표 기어비와 오차계산 후 기어비오차, 정구동효율 내림차순으로 정렬
def gear_ratio_constraint(x_list_bc, Gr_target):
    for i in range(len(x_list_bc)):
        x_gr_error = round(abs(x_list_bc[i][8]-Gr_target),4)
        x_list_bc[i].append(x_gr_error)
    x_list_bc.sort(key=lambda x: (x[9], -x[6]))
    return x_list_bc

# 중복값 제거
def Remove_duplicate_values(x_list_grc):
  x_list_final = []
  for i in x_list_grc:
    if i not in x_list_final:
      x_list_final.append(i)
  return x_list_final[:10]

# 모듈1 계산
def calculate_module1(x_list_final, m_list):
  x_list_final_module = []
  x_list = []
  for i in range(len(x_list_final)):
    x_list = x_list_final[i]
    for j in range(len(m_list)):
      x0 = x_list[0]
      x1 = x_list[1]
      x2 = x_list[2]
      m = m_list[j]
      # print("---------------------------------------------------------")
      # print( round(trunc((x0 / m)*10000)/ 10000,3) == round(x0 / m) , round(trunc((x1 / m)*10000)/ 10000,3) == round(x1 / m) , round(trunc((x2 / m)*10000)/ 10000,3) == round(x2 / m))
      # print(x0 / m, x1 / m , x2 / m)
      # print( round(trunc((x0 / m)*10000)/ 10000,3) , round(trunc((x1 / m)*10000)/ 10000,3) , round(trunc((x2 / m)*10000)/ 10000,3))
      if round(trunc((x0 / m)*10000)/ 10000,3)  == round(x0 / m) and round(trunc((x1 / m)*10000)/ 10000,3)  == round(x1 / m) and round(trunc((x2 / m)*10000)/ 10000,3)  == round(x2 / m):
        x_list.append(m)
    x_list_final_module.append(x_list)
  return x_list_final_module

# 모듈2 계산
def calculate_module2(x_list_final, m_list):
  x_list_final_module = []
  x_list = []
  for i in range(len(x_list_final)):
    x_list = x_list_final[i]
    for j in range(len(m_list)):
      x0 = x_list[3]
      x1 = x_list[4]
      x2 = x_list[5]
      m = m_list[j]
      # print("---------------------------------------------------------")
      # print( round(trunc((x0 / m)*10000)/ 10000,3) == round(x0 / m) , round(trunc((x1 / m)*10000)/ 10000,3) == round(x1 / m) , round(trunc((x2 / m)*10000)/ 10000,3) == round(x2 / m))
      # print(x0 / m, x1 / m , x2 / m)
      # print( round(trunc((x0 / m)*10000)/ 10000,3) , round(trunc((x1 / m)*10000)/ 10000,3) , round(trunc((x2 / m)*10000)/ 10000,3))
      if round(trunc((x0 / m)*10000)/ 10000,3)  == round(x0 / m) and round(trunc((x1 / m)*10000)/ 10000,3)  == round(x1 / m) and round(trunc((x2 / m)*10000)/ 10000,3)  == round(x2 / m):
        x_list.append(m)
    x_list_final_module.append(x_list)
  return x_list_final_module

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, Ui_MainWindow) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        
        global settings
        settings = QtCore.QSettings('DPD_org', 'DPD_app')
        global iteration
        iteration = 1000

        self.quit_Button.clicked.connect(self.quit_click)
        self.iteration_1.clicked.connect(self.iteration_1_clicked)
        self.iteration_2.clicked.connect(self.iteration_2_clicked)
        self.iteration_3.clicked.connect(self.iteration_3_clicked)
        self.optimal_Button.clicked.connect(self.optimal_click)

        if settings.value('remember_state',type=float) == 1:
            self.ebg_a.setText(str(settings.value('na_save', type = float)))
            self.ebg_b.setText(str(settings.value('nb_save', type = float)))
            self.ebg_c.setText(str(settings.value('nc_save', type = float)))
            
            self.min_s.setText(str(settings.value('min_S_b_save', type = float)))
            self.max_s.setText(str(settings.value('max_S_b_save', type = float)))
            self.min_p.setText(str(settings.value('min_P_b_save', type = float)))
            self.max_p.setText(str(settings.value('max_P_b_save', type = float)))
            self.min_r.setText(str(settings.value('min_R_b_save', type = float)))
            self.max_r.setText(str(settings.value('max_R_b_save', type = float)))

            self.module_1.setText(str(settings.value('module_1_save', type = float)))
            self.module_2.setText(str(settings.value('module_2_save', type = float)))
            self.module_3.setText(str(settings.value('module_3_save', type = float)))
            self.remember.setCheckState(2)

    #remember checkbox checked
    def quit_click(self):
        if self.remember.checkState() == 2:
            settings.setValue('na_save', float(self.ebg_a.text()))
            settings.setValue('nb_save', float(self.ebg_b.text()))
            settings.setValue('nc_save', float(self.ebg_c.text()))
            settings.setValue('min_S_b_save', float(self.min_s.text()))
            settings.setValue('max_S_b_save', float(self.max_s.text()))
            settings.setValue('min_P_b_save', float(self.min_p.text()))
            settings.setValue('max_P_b_save', float(self.max_p.text()))
            settings.setValue('min_R_b_save', float(self.min_r.text()))
            settings.setValue('max_R_b_save', float(self.max_r.text()))
            settings.setValue('module_1_save', float(self.module_1.text()))
            settings.setValue('module_2_save', float(self.module_2.text()))
            settings.setValue('module_3_save', float(self.module_3.text()))
            settings.setValue('remember_state', 1)
        else:
            settings.setValue('remember_state', 0)
        self.close()

    def iteration_1_clicked(self):
        global iteration
        iteration = 1000
    def iteration_2_clicked(self):
        global iteration
        iteration = 5000
    def iteration_3_clicked(self):
        global iteration
        iteration = 10000

    def optimal_click(self):
        # 모듈
        global module1
        global module2
        global module3
        module1 = float(self.module_1.text())
        module2 = float(self.module_2.text())
        module3 = float(self.module_3.text())
        print("Module_min = ", module1, "Module_max = ", module2, "Module_step = ", module3)

        # 기어간의 효율
        global na
        global nb
        global nc
        na = float(self.ebg_a.text()) #0.977
        nb = float(self.ebg_b.text()) #0.996
        nc = float(self.ebg_c.text()) #0.997
        print("na =", na, "nb =", nb, "nc =", nc)

        # 기어 반지름 경계조건 (Boundary Condition) [ mm]
        S_b = (float(self.min_s.text()), float(self.max_s.text())) #(20,30)
        P_b = (float(self.min_p.text()), float(self.max_p.text())) #(10,20)
        R_b = (float(self.min_r.text()), float(self.max_r.text())) #(40,55)
        bnds = (S_b[0], S_b[1], P_b[0], P_b[1], R_b[0], R_b[1])
        print("S_b =", S_b, "P_b = ", P_b, "R_b =", R_b)
        print("bnds =", bnds)

        # 목표 기어비
        global Gr_target
        Gr_target = float(self.goal_gr.text()) #100
        print("Gr_target =", Gr_target)

        # 목표 역구동 효율
        global n_target
        n_target = float(self.goal_bde.text())/100 #0.80
        print("n_target =", n_target)

        #치수를 모듈의 배수로 제한
        m_list = round(module_min_max(module1, module2+ module3, module3),4)
        S1_list, P1_list, R1_list = module1_gear_list(m_list, bnds)
        S2_list, P2_list, R2_list = module2_gear_list(m_list, bnds)

        #유성기어 치수 제한조건
        list_1 = dimension_constraint(m_list, S1_list, P1_list, R1_list)
        list_2 = dimension_constraint(m_list, S2_list, P2_list, R2_list)

        #중심거리 일치조건
        x_list = center_constraint(m_list, list_1, list_2)

        #[S1, P1, P1, S2, P2, R2] 
        x_list_6  = x_list_div(m_list, x_list)
        x_list_6_sum = sum(x_list_6,[])

        #[S1, P1, P1, S2, P2, R2, forward_eff] 
        x_list_f = forward_eff_list(x_list_6_sum)

        #[S1, P1, P1, S2, P2, R2, forward_eff, backward_eff] 
        x_list_fb = backward_eff_lsit(x_list_f)

        #[S1, P1, P1, S2, P2, R2, forward_eff, backward_eff, gear_ratio] 
        x_list_fbgr = gear_ratio_list(x_list_fb)

        #역구동효율 제한조건
        x_list_bc = backward_constraint(x_list_fbgr,n_target)


        #[S1, P1, P1, S2, P2, R2, forward_eff, backward_eff, gear_ratio, gear_ratio_error] 
        x_list_grc = gear_ratio_constraint(x_list_bc, Gr_target)

        x_list_final = Remove_duplicate_values(x_list_grc)
        x_list_module1 = calculate_module1(x_list_final, m_list)
        x_list_module2 = calculate_module2(x_list_module1, m_list)

        # 결과 출력
        # - - - - - - - - - - - - - - - - - - - - - - OPTIMAL RESULT- - - - - - - - - - - - - - - - - - - - - -
        if len(x_list_module2) == 0:
            self.tableWidget.setRowCount(1)
        else:
            self.tableWidget.setRowCount(len(x_list_module2))

        x_list_error = ["", "", "", "", "", "", "최적화", "결과", "없음", "","",""] 

        if len(x_list_module2) == 0:
            for j in range(0, 12):
                item = QtWidgets.QTableWidgetItem()
                text = str(x_list_error[j]) 
                item.setText(text)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(0,j,item)
        else:
            for i in range(len(x_list_module2)):
                for j in range(0, 12):
                    item = QtWidgets.QTableWidgetItem()
                    text = str(x_list_module2[i][j]) 
                    item.setText(text)
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.tableWidget.setItem(i,j,item)
                 
if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()