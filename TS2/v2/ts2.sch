EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:ts2-cache
EELAYER 25 0
EELAYER END
$Descr A 11000 8500
encoding utf-8
Sheet 1 9
Title "TS2 68000 Single Board Computer"
Date "2017-01-14"
Rev "2.0"
Comp "Jeff Tranter"
Comment1 "Top Level Schematic"
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Sheet
S 2100 2200 900  600 
U 57B645BE
F0 "page1" 50
F1 "page1.sch" 50
$EndSheet
$Sheet
S 3400 2200 900  600 
U 57B64777
F0 "page2" 50
F1 "page2.sch" 50
$EndSheet
$Sheet
S 4700 2200 950  600 
U 57C2F822
F0 "page3" 60
F1 "page3.sch" 60
$EndSheet
$Sheet
S 6050 2200 900  600 
U 57C3779E
F0 "page4" 60
F1 "page4.sch" 60
$EndSheet
$Sheet
S 2100 3250 900  600 
U 57C4CE2D
F0 "page5" 60
F1 "page5.sch" 60
$EndSheet
$Sheet
S 3400 3250 900  600 
U 57C4D163
F0 "page6" 60
F1 "page6.sch" 50
$EndSheet
Text Notes 3250 1450 0    100  ~ 20
             68000 Single Board Computer\n                     from\n"Microprocessor Systems Design" by Alan Clements\n              Modified by Jeff Tranter
Text Notes 5050 3700 0    250  ~ 0
7
Text Notes 3700 3700 0    250  ~ 0
6
Text Notes 2400 3700 0    250  ~ 0
5
Text Notes 6350 2650 0    250  ~ 0
4
Text Notes 5050 2650 0    250  ~ 0
3
Text Notes 3700 2650 0    250  ~ 0
2
Text Notes 2450 2650 0    250  ~ 0
1
$Sheet
S 4700 3250 950  600 
U 57C65407
F0 "page7" 50
F1 "page7.sch" 50
$EndSheet
$Comp
L VCC #PWR01
U 1 1 57CB9891
P 2400 4650
F 0 "#PWR01" H 2400 4500 50  0001 C CNN
F 1 "VCC" H 2400 4800 50  0000 C CNN
F 2 "" H 2400 4650 50  0000 C CNN
F 3 "" H 2400 4650 50  0000 C CNN
	1    2400 4650
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR02
U 1 1 57CB98A5
P 2400 5450
F 0 "#PWR02" H 2400 5200 50  0001 C CNN
F 1 "GND" H 2400 5300 50  0000 C CNN
F 2 "" H 2400 5450 50  0000 C CNN
F 3 "" H 2400 5450 50  0000 C CNN
	1    2400 5450
	1    0    0    -1  
$EndComp
$Comp
L PWR_FLAG #FLG03
U 1 1 57CBBC87
P 2400 4650
F 0 "#FLG03" H 2400 4745 50  0001 C CNN
F 1 "PWR_FLAG" H 2400 4830 50  0000 C CNN
F 2 "" H 2400 4650 50  0000 C CNN
F 3 "" H 2400 4650 50  0000 C CNN
	1    2400 4650
	-1   0    0    1   
$EndComp
$Comp
L PWR_FLAG #FLG04
U 1 1 57CBBFC3
P 2400 5450
F 0 "#FLG04" H 2400 5545 50  0001 C CNN
F 1 "PWR_FLAG" H 2400 5630 50  0000 C CNN
F 2 "" H 2400 5450 50  0000 C CNN
F 3 "" H 2400 5450 50  0000 C CNN
	1    2400 5450
	1    0    0    -1  
$EndComp
$Comp
L CP1 C4
U 1 1 57D36826
P 3050 4800
F 0 "C4" H 3075 4900 50  0000 L CNN
F 1 "100uF" H 3075 4700 50  0000 L CNN
F 2 "" H 3050 4800 50  0000 C CNN
F 3 "" H 3050 4800 50  0000 C CNN
	1    3050 4800
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR05
U 1 1 57D36855
P 3050 4950
F 0 "#PWR05" H 3050 4700 50  0001 C CNN
F 1 "GND" H 3050 4800 50  0000 C CNN
F 2 "" H 3050 4950 50  0000 C CNN
F 3 "" H 3050 4950 50  0000 C CNN
	1    3050 4950
	1    0    0    -1  
$EndComp
$Comp
L VCC #PWR06
U 1 1 57D3686B
P 3050 4650
F 0 "#PWR06" H 3050 4500 50  0001 C CNN
F 1 "VCC" H 3050 4800 50  0000 C CNN
F 2 "" H 3050 4650 50  0000 C CNN
F 3 "" H 3050 4650 50  0000 C CNN
	1    3050 4650
	1    0    0    -1  
$EndComp
$Comp
L C C5
U 1 1 57D36890
P 3650 4800
F 0 "C5" H 3675 4900 50  0000 L CNN
F 1 "0.1uF" H 3675 4700 50  0000 L CNN
F 2 "" H 3688 4650 50  0000 C CNN
F 3 "" H 3650 4800 50  0000 C CNN
	1    3650 4800
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR07
U 1 1 57D368BF
P 3650 4950
F 0 "#PWR07" H 3650 4700 50  0001 C CNN
F 1 "GND" H 3650 4800 50  0000 C CNN
F 2 "" H 3650 4950 50  0000 C CNN
F 3 "" H 3650 4950 50  0000 C CNN
	1    3650 4950
	1    0    0    -1  
$EndComp
$Comp
L VCC #PWR08
U 1 1 57D368D7
P 3650 4650
F 0 "#PWR08" H 3650 4500 50  0001 C CNN
F 1 "VCC" H 3650 4800 50  0000 C CNN
F 2 "" H 3650 4650 50  0000 C CNN
F 3 "" H 3650 4650 50  0000 C CNN
	1    3650 4650
	1    0    0    -1  
$EndComp
Text Notes 3450 4350 0    60   ~ 0
Bypass caps,\none per IC
$Comp
L LED D2
U 1 1 57D89DCF
P 4300 4850
F 0 "D2" V 4300 4950 50  0000 C CNN
F 1 "POWER" V 4300 4650 50  0000 C CNN
F 2 "" H 4300 4850 50  0000 C CNN
F 3 "" H 4300 4850 50  0000 C CNN
	1    4300 4850
	0    -1   -1   0   
$EndComp
$Comp
L R R25
U 1 1 57D89E08
P 4300 5300
F 0 "R25" V 4380 5300 50  0000 C CNN
F 1 "330" V 4300 5300 50  0000 C CNN
F 2 "" V 4230 5300 50  0000 C CNN
F 3 "" H 4300 5300 50  0000 C CNN
	1    4300 5300
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR09
U 1 1 57D89E43
P 4300 5450
F 0 "#PWR09" H 4300 5200 50  0001 C CNN
F 1 "GND" H 4300 5300 50  0000 C CNN
F 2 "" H 4300 5450 50  0000 C CNN
F 3 "" H 4300 5450 50  0000 C CNN
	1    4300 5450
	1    0    0    -1  
$EndComp
$Comp
L VCC #PWR010
U 1 1 57D89E5F
P 4300 4650
F 0 "#PWR010" H 4300 4500 50  0001 C CNN
F 1 "VCC" H 4300 4800 50  0000 C CNN
F 2 "" H 4300 4650 50  0000 C CNN
F 3 "" H 4300 4650 50  0000 C CNN
	1    4300 4650
	1    0    0    -1  
$EndComp
Wire Wire Line
	4300 5050 4300 5150
Text Notes 6500 4200 0    60   ~ 0
Spare Gates
$Comp
L 74LS06 U4
U 6 1 58430894
P 5850 4600
F 0 "U4" H 6045 4715 50  0000 C CNN
F 1 "74LS06" H 6040 4475 50  0000 C CNN
F 2 "" H 5850 4600 50  0000 C CNN
F 3 "" H 5850 4600 50  0000 C CNN
	6    5850 4600
	1    0    0    -1  
$EndComp
$Comp
L 74LS08 U7
U 3 1 58430C38
P 6000 5300
F 0 "U7" H 6000 5350 50  0000 C CNN
F 1 "74LS08" H 6000 5250 50  0000 C CNN
F 2 "" H 6000 5300 50  0000 C CNN
F 3 "" H 6000 5300 50  0000 C CNN
	3    6000 5300
	1    0    0    -1  
$EndComp
$Comp
L 74LS08 U7
U 4 1 58430C82
P 7800 5300
F 0 "U7" H 7800 5350 50  0000 C CNN
F 1 "74LS08" H 7800 5250 50  0000 C CNN
F 2 "" H 7800 5300 50  0000 C CNN
F 3 "" H 7800 5300 50  0000 C CNN
	4    7800 5300
	1    0    0    -1  
$EndComp
$Comp
L 74LS32 U10
U 4 1 5843109B
P 7800 4600
F 0 "U10" H 7800 4650 50  0000 C CNN
F 1 "74LS32" H 7800 4550 50  0000 C CNN
F 2 "" H 7800 4600 50  0000 C CNN
F 3 "" H 7800 4600 50  0000 C CNN
	4    7800 4600
	1    0    0    -1  
$EndComp
NoConn ~ 8400 4600
NoConn ~ 8400 5300
NoConn ~ 6600 5300
NoConn ~ 6300 4600
$Comp
L GND #PWR011
U 1 1 58432036
P 5400 4600
F 0 "#PWR011" H 5400 4350 50  0001 C CNN
F 1 "GND" H 5400 4450 50  0000 C CNN
F 2 "" H 5400 4600 50  0000 C CNN
F 3 "" H 5400 4600 50  0000 C CNN
	1    5400 4600
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR012
U 1 1 584320D8
P 5400 5200
F 0 "#PWR012" H 5400 4950 50  0001 C CNN
F 1 "GND" H 5400 5050 50  0000 C CNN
F 2 "" H 5400 5200 50  0000 C CNN
F 3 "" H 5400 5200 50  0000 C CNN
	1    5400 5200
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR013
U 1 1 584320FC
P 5400 5400
F 0 "#PWR013" H 5400 5150 50  0001 C CNN
F 1 "GND" H 5400 5250 50  0000 C CNN
F 2 "" H 5400 5400 50  0000 C CNN
F 3 "" H 5400 5400 50  0000 C CNN
	1    5400 5400
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR014
U 1 1 584321C8
P 7200 4500
F 0 "#PWR014" H 7200 4250 50  0001 C CNN
F 1 "GND" H 7200 4350 50  0000 C CNN
F 2 "" H 7200 4500 50  0000 C CNN
F 3 "" H 7200 4500 50  0000 C CNN
	1    7200 4500
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR015
U 1 1 584321EC
P 7200 4700
F 0 "#PWR015" H 7200 4450 50  0001 C CNN
F 1 "GND" H 7200 4550 50  0000 C CNN
F 2 "" H 7200 4700 50  0000 C CNN
F 3 "" H 7200 4700 50  0000 C CNN
	1    7200 4700
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR016
U 1 1 58432210
P 7200 5200
F 0 "#PWR016" H 7200 4950 50  0001 C CNN
F 1 "GND" H 7200 5050 50  0000 C CNN
F 2 "" H 7200 5200 50  0000 C CNN
F 3 "" H 7200 5200 50  0000 C CNN
	1    7200 5200
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR017
U 1 1 58432234
P 7200 5400
F 0 "#PWR017" H 7200 5150 50  0001 C CNN
F 1 "GND" H 7200 5250 50  0000 C CNN
F 2 "" H 7200 5400 50  0000 C CNN
F 3 "" H 7200 5400 50  0000 C CNN
	1    7200 5400
	1    0    0    -1  
$EndComp
$Sheet
S 6000 3250 950  600 
U 584DB98F
F0 "page8" 60
F1 "page8.sch" 60
$EndSheet
Text Notes 6350 3700 0    250  ~ 0
8
$Comp
L D D3
U 1 1 585E8EAF
P 4800 4800
F 0 "D3" H 4800 4900 50  0000 C CNN
F 1 "1N5404" H 4800 4700 50  0000 C CNN
F 2 "" H 4800 4800 50  0000 C CNN
F 3 "" H 4800 4800 50  0000 C CNN
	1    4800 4800
	0    1    1    0   
$EndComp
$Comp
L VCC #PWR018
U 1 1 585E8EEE
P 4800 4650
F 0 "#PWR018" H 4800 4500 50  0001 C CNN
F 1 "VCC" H 4800 4800 50  0000 C CNN
F 2 "" H 4800 4650 50  0000 C CNN
F 3 "" H 4800 4650 50  0000 C CNN
	1    4800 4650
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR019
U 1 1 585E8F6D
P 4800 4950
F 0 "#PWR019" H 4800 4700 50  0001 C CNN
F 1 "GND" H 4800 4800 50  0000 C CNN
F 2 "" H 4800 4950 50  0000 C CNN
F 3 "" H 4800 4950 50  0000 C CNN
	1    4800 4950
	1    0    0    -1  
$EndComp
$EndSCHEMATC
