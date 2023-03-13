#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import sys
import RPi.GPIO as GPIO
import random

reversiTable = [[0 for i in range(8)] for i in range(8)]
W, A, S, D, Z, X, LED = 27, 23, 18, 17, 24, 22, 25
direction = [[-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1]]

GPIO.setmode(GPIO.BCM)
GPIO.setup(W, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(A, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(S, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(D, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(Z, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(X, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(LED, GPIO.OUT)


def choose_table(UP, LEFT, DOWN, RIGHT):
	sys.stdout.write("\033[{}A\033[{}D\033[{}B\033[{}C".format(UP, LEFT, DOWN, RIGHT))
	sys.stdout.flush()

def set_stone(color):
	if color == 1:
		sys.stdout.write("○")
		sys.stdout.flush()
		choose_table(0, 3, 0, 0)
	else:
		sys.stdout.write("●")
		sys.stdout.flush()
		choose_table(0, 3, 0, 0)


def get_list(table, vector, y, x, color):
	returnNumber = 0
	color = -1 * color
	for i in range(1, 8):
		yy = y + i * vector[0]
		xx = x + i * vector[1]
		if yy > 7 or yy < 0 or xx > 7 or xx < 0:
			return 0
		number = table[yy][xx]
		if number == color:
			returnNumber += 1
			if i == 7:
				return 0
		elif number == 0:
			return 0
		elif number == -1 * color:
			return returnNumber


def chack_table(table, direct, y, x, color):
	if table[y][x] != 0:
		return True
	for i in direct:
		if get_list(table, i, y, x, color) == 0:
			continue
		else:
			return False
	return True

def judge_stone(table, direct, color):
	color = -1 * color
	for i in range(8):
		for j in range(8):
			if not chack_table(table, direct, i, j, color):
				return color
	return -1 * color

def change_turn(y, x, color):
	for i in range(y + 1):
		choose_table(3, 0, 0, 0)
	if x < 3:
		for i in range(3 - x):
			choose_table(0, 0, 0, 6)
	if x > 3:
		for i in range(x - 3):
			choose_table(0, 6, 0, 0)
	set_stone(color)
	for i in range(y + 1):
		choose_table(0, 0, 3, 0)
	if x < 3:
		for i in range(3 - x):
			choose_table(0, 6, 0, 0)
	if x > 3:
		for i in range(x - 3):
			choose_table(0, 0, 0, 6)


def change_sum(select, y, x, sumB, sumW):
	if select:
		for i in range(8 - y):
			choose_table(0, 0, 3, 0)
		if x < 2:
			for i in range(2 - x):
				choose_table(0, 0, 0, 6)
		elif x > 2:
			for i in range(x - 2):
				choose_table(0, 6, 0, 0)
		if sumB < 10:
			sys.stdout.write(" " + str(sumB))
		else:
			sys.stdout.write(str(sumB))
		sys.stdout.flush()
		choose_table(0, 3, 0, 0)
		for i in range(3):
			choose_table(0, 0, 0, 6)
		if sumW < 10:
			sys.stdout.write(" " + str(sumW))
		else:
			sys.stdout.write(str(sumW))
		sys.stdout.flush()
		choose_table(0, 3, 0, 0)
		for i in range(8 - y):
			choose_table(3, 0, 0, 0)
		if x < 5:
			for i in range(5 - x):
				choose_table(0, 6, 0, 0)
		elif x > 5:
			for i in range(x - 5):
				choose_table(0, 0, 0, 6)

def change_table(table, direct, y, x, color):
	yy = y
	xx = x
	counter = 0
	for i in direct:
		times = 0
		for j in range(get_list(table, i, y, x, color)):
			if i[0] == 1:
				choose_table(0, 0, 3, 0)
				yy += 1
			elif i[0] == -1:
				choose_table(3, 0, 0, 0)
				yy -= 1
			if i[1] == 1:
				choose_table(0, 0, 0, 6)
				xx += 1
			elif i[1] == -1:
				choose_table(0, 6, 0, 0)
				xx -= 1
			set_stone(color)
			table[yy][xx] = color
			counter += 1
			times += 1
		for j in range(times):
			if i[0] == 1:
				choose_table(3, 0, 0, 0)
				yy -= 1
			elif i[0] == -1:
				choose_table(0, 0, 3, 0)
				yy += 1
			if i[1] == 1:
				choose_table(0, 6, 0, 0)
				xx -= 1
			elif i[1] == -1:
				choose_table(0, 0, 0, 6)
				xx += 1
	if color == 1:
		return [table, counter + 1, -1 * counter]
	else:
		return [table, -1 * counter, counter + 1]


def com_get_list(stoneSum, table, direct, color):
	countList = []
	returnList = []
	for i in range(8):
		for j in range(8):
			counter = 0
			if chack_table(table, direct, i, j, color):
				continue
			for h in direct:
				counter += get_list(table, h, i, j, color)
			if counter != 0:
				countList += [[i, j, counter]]
	countList = get_divide_list(countList)
	for i in range(len(countList)):
		if len(countList[i]) == 0:
			continue
		judge = True
		if stoneSum >= 15:
			judge = False
		countList[i] = sorted(countList[i], reverse = judge, key = lambda x: x[2])
		number = countList[i][0][2]
		for j in countList[i]:
			if j[2] == number:
				returnList += [[j[0], j[1]]]
				continue
		return returnList


def get_divide_list(placeList):
	divideList = [[], [], [], []]
	for place in placeList:
		if ((place[0] == 0) or (place[0] == 7)) and ((place[1] == 0) or (place[1] == 7)):
			divideList[0].append(place)
		if ((place[0] >= 2) and (place[0] <= 5)) and ((place[1] >= 2) and (place[1] <= 5)):
			divideList[1].append(place)
		if ((place[0] >= 2) and (place[0] <= 5)) or ((place[1] >= 2) and (place[1] <= 5)):
			divideList[2].append(place)
		else:
			divideList[3].append(place)
	return divideList


def chack_LED(table, direct, y, x, color, LED):
	if chack_table(table, direct, y, x, color):
		GPIO.output(LED, GPIO.LOW)
	else:
		GPIO.output(LED, GPIO.HIGH)


def first_table(W, A, S, D, Z):
	print("スイッチ配置")
	print("                    ○          ")
	print("                    上          ")
	print("               ○            ○ ")
	print("               左            右 ")
	print("  ○    ○               ○     ")
	print(" 決定  終了              下     ")
	print("\n")

	print("これからリバーシゲームをはじめます。")
	print("ゲーム中は上下左右で置く場所を決め、決定を押して石を置きます。")
	print("終了を押すと強制的にゲームを終わらせることができます。")
	print("また、石が置ける場所ではLEDが光ります。")
	print("\n")
	time.sleep(3)

	print("対戦形式を決めます。上下左右で対人戦か対COM戦かを選んで")
	print("決定を押してください。\n\n")
	print("\033[33m  対人戦   \033[37m：ラズパイ一台を使って二人で対戦するモード\n")
	print("  対COM戦  ：コンピュータと戦える一人用モード")
	print("  先攻 後攻：対COM戦のみ左右を使用して先攻後攻を決めてください")
	nowSelect = 1
	while True:
		if GPIO.input(W) == GPIO.LOW:
			if nowSelect != 1:
				choose_table(5, 0, 0, 0)
				print("\033[33m 対人戦   \033[37m：ラズパイ一台を使って二人で対戦するモード\n")
				print("  対COM戦  ：コンピュータと戦える一人用モード")
				print("  先攻 後攻：対COM戦のみ左右を使用して先攻後攻を決めてください")
				nowSelect = 1
		if GPIO.input(A) == GPIO.LOW:
			if nowSelect == 3:
				choose_table(5, 0, 0, 0)
				print(" 対人戦   ：ラズパイ一台を使って二人で対戦するモード\n")
				print("\033[33m  対COM戦  \033[37m：コンピュータと戦える一人用モード")
				print("\033[33m  先攻 \033[37m後攻：対COM戦のみ左右を使用して先攻後攻を決めてください")
				nowSelect = 2
		if GPIO.input(S) == GPIO.LOW:
			if nowSelect == 1:
				choose_table(5, 0, 0, 0)
				print(" 対人戦   ：ラズパイ一台を使って二人で対戦するモード\n")
				print("\033[33m  対COM戦  \033[37m：コンピュータと戦える一人用モード")
				print("\033[33m  先攻 \033[37m後攻：対COM戦のみ左右を使用して先攻後攻を決めてください")
				nowSelect = 2
		if GPIO.input(D) == GPIO.LOW:
			if nowSelect == 2:
				choose_table(5, 0, 0, 0)
				print(" 対人戦   ：ラズパイ一台を使って二人で対戦するモード\n")
				print("\033[33m  対COM戦  \033[37m：コンピュータと戦える一人用モード")
				print("  先攻 \033[33m後攻\033[37m：対COM戦のみ左右を使用して先攻後攻を決めてください")
				nowSelect = 3
		if GPIO.input(Z) == GPIO.LOW:
			print("\nしばらくお待ちください。")
			if nowSelect == 1:
				return [False, 1]
			elif nowSelect == 2:
				return [True, 1]
			else:
				return [True, -1]



def change_sum_switch(A, D, Z):
	time.sleep(3)
	nowSelect = 0
	print("\n\n\nプレイ中に盤上の石の総数を表示しますか？\n")
	print("   \033[33mはい   \033[37mいいえ")
	while True:
		if GPIO.input(A) == GPIO.LOW:
			if nowSelect == 1:
				choose_table(2, 0, 0, 0)
				print("  \033[33mはい   \033[37mいいえ")
				nowSelect = 0
		if GPIO.input(D) == GPIO.LOW:
			if nowSelect == 0:
				choose_table(2, 0, 0, 0)
				print("  \033[37mはい   \033[33mいいえ")
				nowSelect = 1
		if GPIO.input(Z) == GPIO.LOW:
			print("\033[37m")
			if nowSelect == 0:
				return True
			else:
				return False

def reversi_table():
	print("\n\n\nリバーシゲーム")
	print(" " * 7 + "   現在のターン：○")
	for i in range(8):
		print(" " * 7 + "+----+----+----+----+----+----+----+----+")
		print(" " * 7 + "|    |    |    |    |    |    |    |    |")
	print(" " * 7 + "+----+----+----+----+----+----+----+----+")
	print(" " * 7 + "先攻：黒○          |          ●白：後攻")

	choose_table(12, 0, 0, 24)
	set_stone(1)
	choose_table(0, 0, 3, 0)
	set_stone(-1)
	choose_table(0, 0, 0, 6)
	set_stone(1)
	choose_table(3, 0, 0, 0)
	set_stone(-1)
	choose_table(7, 21, 0, 0)


#ここから実行
matchType = first_table(W, A, S, D, Z)
sumOn = change_sum_switch(A, D, Z)
reversi_table()
change_sum(sumOn, 0, 0, 2, 2)
comSystem = False
if matchType[0]:
	comSystem = True
reversiTable[3][3] = 1
reversiTable[3][4] = -1
reversiTable[4][3] = -1
reversiTable[4][4] = 1
y, x = 0, 0
stoneColor = 1
stoneBrack, stoneWhite = 2, 2
stones = 60
judge = 0
isFirst = True
dubleTurn = False

while True:
	if isFirst:
		if matchType[0] and matchType[1] == 1:
			matchType[0] = False
		isFirst = False
	if dubleTurn:
		if -1 * stoneColor == judge_stone(reversiTable, direction, -1 * stoneColor):
			stones = 0
		dubleTurn = False
	if stones == 0:
		if stoneBrack > stoneWhite:
			judge = 1
		elif stoneBrack < stoneWhite:
			judge = -1
		else:
			judge = 2
	if judge != 0:
		for i in range(9 - y):
			choose_table(0, 0, 3, 0)
		print("\n{}対{}で".format(stoneBrack, stoneWhite))
		if judge == 1:
			if comSystem:
				if matchType[1] == 1:
					print("\nあなたの勝ち！")
					break
				else:
					print("\nCOMの勝ち！")
					break
			print("\n黒の勝ち！")
			break
		elif judge == -1:
			if comSystem:
				if matchType[1] == -1:
					print("\nあなたの勝ち！")
					break
				else:
					print("\nCOMの勝ち！")
					break
			print("\n白の勝ち！")
			break
		else:
			print("\nドロー！")
			break
	if comSystem and matchType[0]:
		time.sleep(2)
		comList = com_get_list(stones, reversiTable, direction, stoneColor)
		comAxis = comList[random.randint(0, len(comList) - 1)]
		comAxis[0] -= y
		comAxis[1] -= x
		if comAxis[0] > 0:
			for i in range(comAxis[0]):
				y += 1
				choose_table(0, 0, 3, 0)
		if comAxis[0] < 0:
			for i in range(-1 * comAxis[0]):
				y -= 1
				choose_table(3, 0, 0, 0)
		if comAxis[1] > 0:
			for i in range(comAxis[1]):
				x += 1
				choose_table(0, 0, 0, 6)
		if comAxis[1] < 0:
			for i in range(-1 * comAxis[1]):
				x -= 1
				choose_table(0, 6, 0, 0)
		set_stone(stoneColor)
		returnList = change_table(reversiTable, direction, y, x, stoneColor)
		reversiTable = returnList[0]
		stoneBrack += returnList[1]
		stoneWhite += returnList[2]
		change_sum(sumOn, y, x, stoneBrack, stoneWhite)
		stones -= 1
		reversiTable[y][x] = stoneColor
		stoneColor = judge_stone(reversiTable, direction, stoneColor)
		if reversiTable[y][x] == stoneColor:
			dubleTurn = True
		change_turn(y, x, stoneColor)
		if stoneColor == matchType[1]:
			matchType[0] = False
	if GPIO.input(W) == GPIO.LOW:
		if y != 0:
			y -= 1
			choose_table(3, 0, 0, 0)
			chack_LED(reversiTable, direction, y, x, stoneColor, LED)
			time.sleep(0.25)
	if GPIO.input(A) == GPIO.LOW:
		if x != 0:
			x -= 1
			choose_table(0, 6, 0, 0)
			chack_LED(reversiTable, direction, y, x, stoneColor, LED)
			time.sleep(0.25)
	if GPIO.input(S) == GPIO.LOW:
		if y != 7:
			y += 1
			choose_table(0, 0, 3, 0)
			chack_LED(reversiTable, direction, y, x, stoneColor, LED)
			time.sleep(0.25)
	if GPIO.input(D) == GPIO.LOW:
		if x != 7:
			x += 1
			choose_table(0, 0, 0, 6)
			chack_LED(reversiTable, direction, y, x, stoneColor, LED)
			time.sleep(0.25)
	if GPIO.input(Z) == GPIO.LOW:
		GPIO.output(LED, GPIO.LOW)
		if chack_table(reversiTable, direction, y, x, stoneColor):
			continue
		set_stone(stoneColor)
		returnList = change_table(reversiTable, direction, y, x, stoneColor)
		reversiTable = returnList[0]
		stoneBrack += returnList[1]
		stoneWhite += returnList[2]
		change_sum(sumOn, y, x, stoneBrack, stoneWhite)
		stones -= 1
		reversiTable[y][x] = stoneColor
		stoneColor = judge_stone(reversiTable, direction, stoneColor)
		if reversiTable[y][x] == stoneColor:
			dubleTurn = True
		change_turn(y, x, stoneColor)
		if stoneColor != matchType[1]:
			matchType[0] = True
		time.sleep(0.25)
	if GPIO.input(X) == GPIO.LOW:
		for i in range(9 - y):
			choose_table(0, 0, 3, 0)
		print("\n強制終了されました。")
		break

GPIO.cleanup()
