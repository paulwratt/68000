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
Sheet 1 8
Title "TS2 68000 Single Board Computer"
Date "2016-09-03"
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
P 2400 4750
F 0 "#PWR01" H 2400 4600 50  0001 C CNN
F 1 "VCC" H 2400 4900 50  0000 C CNN
F 2 "" H 2400 4750 50  0000 C CNN
F 3 "" H 2400 4750 50  0000 C CNN
	1    2400 4750
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR02
U 1 1 57CB98A5
P 2400 5400
F 0 "#PWR02" H 2400 5150 50  0001 C CNN
F 1 "GND" H 2400 5250 50  0000 C CNN
F 2 "" H 2400 5400 50  0000 C CNN
F 3 "" H 2400 5400 50  0000 C CNN
	1    2400 5400
	1    0    0    -1  
$EndComp
$Comp
L PWR_FLAG #FLG03
U 1 1 57CBBC87
P 2400 4750
F 0 "#FLG03" H 2400 4845 50  0001 C CNN
F 1 "PWR_FLAG" H 2400 4930 50  0000 C CNN
F 2 "" H 2400 4750 50  0000 C CNN
F 3 "" H 2400 4750 50  0000 C CNN
	1    2400 4750
	-1   0    0    1   
$EndComp
$Comp
L PWR_FLAG #FLG04
U 1 1 57CBBFC3
P 2400 5400
F 0 "#FLG04" H 2400 5495 50  0001 C CNN
F 1 "PWR_FLAG" H 2400 5580 50  0000 C CNN
F 2 "" H 2400 5400 50  0000 C CNN
F 3 "" H 2400 5400 50  0000 C CNN
	1    2400 5400
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
Text Notes 3450 4400 0    60   ~ 0
One per IC
$EndSCHEMATC