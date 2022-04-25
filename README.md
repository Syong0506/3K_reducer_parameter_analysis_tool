# 3K reducer parameter analysis tool manual

Contents
1. Introduction
    1. Program Purpose
    2. Program Type  

2. How to use
    1. Gear Dimensions Version
    2. Gear Ratio Version
    3. Module Version  

3. Precautions for Use
    1. Program Stopping  

4. Other inquiries

# 1. Introduction
### A. Program Purpose
It is a parameter analysis program for the optimal design of a 3K type compound planetary gear reducer to reduce the optimal design time due to the repetition of planetary gear reducer design and dynamic analysis.

### B. Program Type
#### 1) Gear Dimensions Version(OGRCT_d Version)  
The gear dimension version is a program designed with the number of decimal places selected by the optimal result value of each radius to facilitate the machining of the gear. It is easy to design the compound planetary friction reducer optimally.

#### 2) Gear Ratio Version(OGRCT_gr Version)
The gear ratio version is the preferred version of the target gear ratio of the gear and is an optimal program designed to be as close as possible to the target gear ratio. It is easy to design the compound planetary friction reducer optimally.

#### 3) Module Version(OGRCT_m Version)
The module version is an optimal design program that reflects the module of the gear, making it easy to optimally design the compoud planetary gear reducer.

# 2. How to use
### A. Gear Dimensions Version  
(1) Enter an arbitrary value within the boundary condition for the initial value.  
(2) Enter the boundary conditions according to the convenience of the motor or the user.  
(3) Enter the efficiency($\eta_a$, $\eta_b$, $\eta_c$) between gears.  If there is no data, enter $\eta_a = 0.977$, $\eta_b = 0.996$, $\eta_c = 0.997$.  
(4) If you want to remember the initial value, boundary condition, and efficiency between gears after optimization, check Remember Initialization Setting.  
(5) A target gear ratio and a target backdrive efficiency are input.  
(6) Select the maximum iteration number of times of optimization. The more times, the more accurate, but the longer the optimization time.  
(7) Select demical point of optimization.  
(8) Press the Optimization button to proceed with optimization.  
(9) Check whether the optimization is successful and whether the optimization results meet the constraints.  
(10) The gear ratio, forword efficiency, and backdrive efficiency of the initial value and the optimum value can be confirmed in Comparison.  
(11) Optimal design radius can be determined in the Optimal Result.  
(12) Exit the program with the Quit button.  
### B. Gear Ratio Version
(1) Enter an arbitrary value within the boundary condition for the initial value.  
(2) Enter the boundary conditions according to the convenience of the motor or the user.  
(3) Enter the efficiency($\eta_a$, $\eta_b$, $\eta_c$) between gears.  If there is no data, enter $\eta_a = 0.977$, $\eta_b = 0.996$, $\eta_c = 0.997$.  
(4) If you want to remember the initial value, boundary condition, and efficiency between gears after optimization, check Remember Initialization Setting.  
(5) A target gear ratio and a target backdrive efficiency are input.  
(6) Select the maximum iteration number of times of optimization. The more times, the more accurate, but the longer the optimization time.  
(7) Press the Optimization button to proceed with optimization.  
(8) Check whether the optimization is successful and whether the optimization results meet the constraints.  
(9)  The gear ratio, forword efficiency, and backdrive efficiency of the initial value and the optimum value can be confirmed in Comparison.  
(10) Optimal design radius can be determined in the Optimal Result.  
(11)  Exit the program with the Quit button.  
### C. Module Version
(1) Enter the range of the module and the spacing of the modules.
(2) Enter the boundary conditions according to the convenience of the motor or the user.  
(3) Enter the efficiency($\eta_a$, $\eta_b$, $\eta_c$) between gears.  If there is no data, enter $\eta_a = 0.977$, $\eta_b = 0.996$, $\eta_c = 0.997$.  
(4) If you want to remember the initial value, boundary condition, and efficiency between gears after optimization, check Remember Initialization Setting.  
(5) A target gear ratio and a target backdrive efficiency are input.  
(6) Select the maximum iteration number of times of optimization. The more times, the more accurate, but the longer the optimization time.  
(7) Press the Optimization button to proceed with optimization.  
(8) Check whether the optimization is successful and whether the optimization results meet the constraints.  
(9)  The gear ratio, forword efficiency, and backdrive efficiency of the initial value and the optimum value can be confirmed in Comparison.  
(10) Optimal design radius can be determined in the Optimal Result.  
(11)  Exit the program with the Quit button.  
# 3. Precautions for Use
### A. Program Stopping  
(1) When input data is not entered  
If the Optimization button is pressed without entering all input data, the program may end or stop.
(2)  Module version  
The module version may seem to stop after pressing the Optimization button because of its long computation time, but the optimization results appear after approximately 20 to 30 seconds.  
# 4. Other inquiries
If you have any questions or improvements regarding the program, please contact syong0506@naver.com.