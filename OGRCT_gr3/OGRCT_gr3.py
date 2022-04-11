#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from scipy.optimize import minimize
from math import trunc
from fractions import Fraction
from OGRCT_gr3_ui import Ui_MainWindow

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

# 목표함수 : 정구동 효율을 최대화
def objective(x):
    n_forw = forward_eff(x)
    return 1/ n_forw

# 제한조건 1 : 역구동 효율을 목표값 이상으로 , inequality condition
def constraint1(x):
    n_backw = backward_eff(x)
    return n_backw - n_target

# 제한조건 2 : 기어비 지정 , equality condition
def constraint2(x):
    Gr = gear_ratio(x)
    return Gr - Gr_target

# 제한조건 3 : 1 단 유성기어열 치수제한조건 , equality condition
def constraint3(x):
    S1, P1, R1 = x[0] , x[1] , x[2]
    # 1 단 유성기어
    return R1 - S1 - 2* P1

# 제한조건 4 : 2 단 유성기어열 치수제한조건 , equality condition
def constraint4(x):
    S2, P2, R2 = x[3] , x[4] , x[5]
    # 2 단 유성기어
    return R2 - S2 - 2* P2

# 제한조건 5 : 복합 Planetary 기어의 중심거리 일치조건 , equality condition
def constraint5(x):
    S1, P1, R1 = x[0] , x[1] , x[2]
    S2, P2, R2 = x[3] , x[4] , x[5]
    # 중심거리
    return (S1+P1) - (S2+P2)

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
        self.cc_3.clicked.connect(self.check_read_only_3)
        self.cc_4.clicked.connect(self.check_read_only_4)
        self.cc_5.clicked.connect(self.check_read_only_5)
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

            self.init_s1.setText(str(settings.value('x0_0_save', type = float)))
            self.init_p1.setText(str(settings.value('x0_1_save', type = float)))
            self.init_r1.setText(str(settings.value('x0_2_save', type = float)))
            self.init_s2.setText(str(settings.value('x0_3_save', type = float)))
            self.init_p2.setText(str(settings.value('x0_4_save', type = float)))
            self.init_r2.setText(str(settings.value('x0_5_save', type = float)))
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
            settings.setValue('x0_0_save', float(self.init_s1.text()))
            settings.setValue('x0_1_save', float(self.init_p1.text()))
            settings.setValue('x0_2_save', float(self.init_r1.text()))
            settings.setValue('x0_3_save', float(self.init_s2.text()))
            settings.setValue('x0_4_save', float(self.init_p2.text()))
            settings.setValue('x0_5_save', float(self.init_r2.text()))
            settings.setValue('remember_state', 1)
        else:
            settings.setValue('remember_state', 0)
        self.close()

    def check_read_only_3(self, state) :
        if state == 0:
            self.cc_3.setCheckState(2)
        if state == 1:
            self.cc_3.setCheckState(0)
    def check_read_only_4(self, state) :
        if state == 0:
            self.cc_4.setCheckState(2)
        if state == 1:
            self.cc_4.setCheckState(0)
    def check_read_only_5(self, state) :
        if state == 0:
            self.cc_5.setCheckState(2)
        if state == 1:
            self.cc_5.setCheckState(0)

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
        # 제한조건 (Constraint)
        con1 = { 'type':'ineq', 'fun':constraint1}
        con2 = { 'type':'eq', 'fun':constraint2}
        con3 = { 'type':'eq', 'fun':constraint3}
        con4 = { 'type':'eq', 'fun':constraint4}
        con5 = { 'type':'eq', 'fun':constraint5}
        cons = [ con1,con2,con3,con4,con5]

        try:
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
            bnds = (S_b,P_b,R_b,S_b,P_b,R_b)
            print("S_b =", S_b, "P_b = ", P_b, "R_b =", R_b)

            # 기어 반지름 초기값 지정 [ mm]
            x0 = [float(self.init_s1.text()), float(self.init_p1.text()), float(self.init_r1.text()), float(self.init_s2.text()), float(self.init_p2.text()), float(self.init_r2.text())]
                #[ 24.5, 13.5, 51.5,
                #  25, 13, 51]
            print("x0 =", x0)

            # 목표 기어비
            global Gr_target
            Gr_target = float(self.goal_gr.text()) #100
            print("Gr_target =", Gr_target)

            # 목표 역구동 효율
            global n_target
            n_target = float(self.goal_bde.text())/100 #0.80
            print("n_target =", n_target)

            S1, P1, R1 = x0[0] , x0[1] , x0[2]
            S2, P2, R2 = x0[3] , x0[4] , x0[5]
            I1 = R1/ S1
            I2 = R1/ R2* P2/ P1
            n_backw = (1+I1)* na* (nb* nc- I2)/ (nc* (na* nb+I1)* (1- I2))
            print("S1 =", x0[0])
            print("P1 =", x0[1])
            print("R1 =", x0[2])
            print("S2 =", x0[3])
            print("P2 =", x0[4])
            print("R2 =", x0[5])
            print("I1 =", I1)
            print("I2 =", I2)
            print("n_backw =", n_backw)

            # - - - - - - - - - - - - - - - - - - - - - - INITIAL STATE- - - - - - - - - - - - - - - - - - - - - -
            self.init_gr.setText(str(round(gear_ratio(x0), 9)))
            self.init_fde.setText(str(round(forward_eff(x0)*100, 9)))
            self.init_bde.setText(str(round(backward_eff(x0)*100, 9)))
            print("gear_ratio(x0) =", gear_ratio(x0))
            print("forward_eff(x0) =", forward_eff(x0)*100)
            print("backward_eff(x0)*100 =", backward_eff(x0)*100)

            # 최적화문제 수행
            sol = minimize(objective, x0, method='SLSQP', bounds=bnds, constraints=cons, options={'maxiter':iteration})
            self.optimization.setText(str(sol.message))
            print(sol)
            print("iteration = ",iteration)

            # 결과 출력
            # - - - - - - - - - - - - - - - - - - - - - - OPTIMAL RESULT- - - - - - - - - - - - - - - - - - - - - -
            self.optimal_gr.setText(str(round(gear_ratio(sol.x),9)))
            self.optimal_fde.setText(str(round(forward_eff(sol.x)* 100, 9)))
            self.optimal_bde.setText(str(round(backward_eff(sol.x)* 100, 9)))
            self.optimal_s1.setText(str(round(sol.x[0], 9)))
            self.optimal_p1.setText(str(round(sol.x[1], 9)))
            self.optimal_r1.setText(str(round(sol.x[2], 9)))
            self.optimal_s2.setText(str(round(sol.x[3], 9)))
            self.optimal_p2.setText(str(round(sol.x[4], 9)))
            self.optimal_r2.setText(str(round(sol.x[5], 9)))

            gr = gear_ratio(sol.x)
            gr_int = trunc(gr)
            gr_decimal = gr - gr_int
            gr_fraction = Fraction(gr_decimal)

            # 제한조건 검증
            # - - - - - - - - - - - - - - - - - - - - - - CONSTRAINT CONFIRMATION- - - - - - - - - - - - - - - - - - - - - -
            self.cc_gr.setText(str(round(gear_ratio(sol.x),9)))
            self.cc_gr_f.setText(str(gr_int)+str("+")+str(gr_fraction))
            if round(constraint3(sol.x), 1) == 0:
                self.cc_3.setCheckState(2)
                self.cc_3_L.setText("OK!")
            else:
                self.cc_3.setCheckState(0)
                self.cc_3_L.setText("Fail!")

            if round(constraint4(sol.x), 9) == 0:
                self.cc_4.setCheckState(2)
                self.cc_4_L.setText("OK!")
            else:
                self.cc_4.setCheckState(0)
                self.cc_4_L.setText("Fail!")

            if round(constraint5(sol.x), 9) == 0:
                self.cc_5.setCheckState(2)
                self.cc_5_L.setText("OK!")
            else:
                self.cc_5.setCheckState(0)
                self.cc_5_L.setText("Fail!")

        except:
            self.optimization.setText("Please try again!!!")

# print("- - - - - - - - - - - - - - - - - - - - - - INITIAL STATE- - - - - - - - - - - - - - - - - - - - - - ")
# print("Initial Gear Ratio =", gear_ratio(x0))
# print("Initial Forward Drive Efficiency =", forward_eff(x0)* 100, "%")
# print("Initial Backward Drive Efficiency =", backward_eff(x0)* 100, "%")

# 결과 출력
# print("- - - - - - - - - - - - - - - - - - - - - - OPTIMAL RESULT- - - - - - - - - - - - - - - - - - - - - - ")
# print("Optimal Forward Drive Efficiency =", forward_eff(sol.x)* 100,"%")
# print("Optimal Backward Drive Efficiency =", backward_eff(sol.x)* 100,"%")
# print("S1, P1, R1, S2, P2, R2 =", sol.x[ 0] , sol.x[ 1] , sol.x[ 2] , sol.x[ 3] , sol.x[ 4] ,sol.x[ 5] )

# 제한조건 검증
# print("- - - - - - - - - - - - - - - - - - - - - - CONSTRAINT CONFIRMATION- - - - - - - - - - - - - - - - - - - - - - ")
# print("Gear Ratio =", gear_ratio(sol.x))
# print("R1 - S1 - 2* P1:", constraint3(sol.x))
# print("R2 - S2 - 2* P2:", constraint4(sol.x))
# print("(S1+P1)- (S2+P2):", constraint5(sol.x))

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()