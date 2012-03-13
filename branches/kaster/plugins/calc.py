# -*- coding: utf-8 -*-
from __future__ import division
import xmpp
from math import *
from re import sub
def init(bot):
	return {'status':0,'usage':'expression','descr':bot.phrases['DESCR_CALC'],'gc':2}

alias = [("^","**"),
	 ("coth","1/tanh"),
	 ("cot","1/tan"),
	 ("csec","1/sin"),
	 ("sech","1/cosh"),
	 ("sec","1/cos"),
	 ("csh","1/sinh"),
	 ("fact","factorial"),
	 ("gamm","gamma"),
	 ("degr","degrees"),
	 ("rad","radians"),
	 (unichr(8722),"-"),
	 ("arctg","atan"),
	 ("ctg","1/tan"),
	 ("tg","tan"),
	 ("ctan","1/tan"),
	 ("arccos","acos"),
	 ("arcsin","asin"),
	 ("arccos","acos"),
	 ("lg10","log10"),
	 ("lg","log"),
	 ("mod","fmod"),
	 ("true","True"),
	 ("false","False")]

genuine = ["atanh",
	   "atan",
	   "tanh",
	   "tan",
	   "asinh",
	   "asin",
	   "sinh",
	   "sin",
	   "acosh",
	   "acos",
	   "cosh",
	   "cos",
	   "pow",
	   "factorial",
	   "gamma",
	   "radians",
	   "log",
	   "log10",
	   "fabs",
	   "abs",
	   "fmod",
	   "int",
	   "round",
	   "sqrt",
	   "exp",
	   "max",
	   "min",
	   "erf",
	   "e", "pi"]

pats = {"digitpat":"[0-9a-fA-F]",
	"bracespat":"[()\[\]]",
	"arithpat":"[*/%\-+.]",
	"spacespat":"[\s\t]"}

def run(bot,mess,mode='chat'):
	command = mess.getBody()[5:]
	if command == 'help':
		ans = u'Наберите\n\
		!calc help arith или !calc help 1 - для справки по арифмитическим операциям\n\
		!calc help base или !calc help 2 - по базовым функциями\n\
		!calc help repr или !calc help 3 - по функциям представления числа\n\
		!calc help spec или !calc help 4 - по спецфункциям\n\
		!calc help const или !calc help 5 - по константам\n\
		!calc help aux или !calc help 6 - по вспомогательным функциям\n\
		!calc help convert или !calc help 7 - по функциями конвертаций чисел в разные системы исчисления'
	elif 'help' in command:
		ans = u'Плагин для выполнения базовых математических операций - Калькулятор (calc).\n'
		ans += u'---------------------------------------------------------------------------\n'
		ans += u'Неполный список функций и констант:\n'
		if (command == 'help arith') or (command == 'help 1'):
			ans += u'\tАрифметические операции\n\
		"+" - Сложение\n\
		"- t- Вычитание\n\
		"/" - Деление\n\
		"^|**" - Возведение в степень (работают оба варианта)\n\
		"//" - Целочисленное деление\n\
		"%" - Остаток от деления\n'
		elif (command == 'help base') or (command == 'help 2'):
			ans += u'\tБазовые функции\n\
		"sin" - Синус угла (угол в радианах)\n\
		"cos" - Косинус угла (угол в радианах)\n\
		"tan" - Тангенс угла (угол в радианах)\n\
		"cot" - Котангенс угла (угол в радианах)\n\
		"sec" - Секанс угла (угол в радианах)\n\
		"csec" - Косеканс угла (угол в радианах)\n\
		"sinh" - Гиперболический синус (Шинус)\n\
		"cosh" - Гиперболический косинус (Кошинус)\n\
		"tanh" - Гиперболический тангенс\n\
		"coth" - Гиперболический котангенс\n\
		"sech" - Гиперболический секанс\n\
		"csh" - Гиперболический косеканс\n\
		"asin" - Арксинус числа\n\
		"acos" - Арккосинус числа\n\
		"atan" - Арктангенс числа\n\
		"asinh" - Гиперболический арксинус\n\
		"acosh" - Гиперболический арккосинус\n\
		"atanh" - Гиперболический арктангенс\n\
		"exp"  - Экспонента\n\
		"log" - Логарифм (Второй аргумент - основание. Без указания - натуральный логарифм)\n\
		"sqrt" - Квадратный корень числа\n\
		"abs" - Абсолютное значение числа\n\
		"fact" - Факториал числа\n\
		"max" - Максимальный элемент (Аргумент должен быть списком вида [a1, a2, ..., an])\n\
		"min" - Минимальный элемент (Аргумент должен быть списком вида [a1, a2, ..., an])'
		elif (command == 'help repr') or (command == 'help 3'):
			ans += u'\tФункции представления\n\
		"floor" - Наименьшее целое число не превышающее данное\n\
		"ceil" - Наибольше целое число не превышающее данное'
		elif (command == 'help spec') or (command == 'help 4'):
			ans += u'\tСпециальные функции\n\
		"erf" - Функция ошибок\n\
		"gam" - Гамма-функция Эйлера'
		elif command == ('help const') or (command == 'help 5'):
			ans += u'\tКонстанты\n\
		"pi" - Число \'пи\'\n\
		"e" - Число эйлера, основание натурального логарифма'
		elif command == ('help aux') or (command == 'help 6'):
			ans += u'\tВспомогательные функции\n\
		"degr" - Перевод угла из радианов в градусы\n\
		"rad" - Перевод угла из градусов в радианы'
		elif command == ('help convert') or (command == 'help 7'):
			ans += u'\tФункции конвертации\n\
		"oct" - Перевод числа в восьмеричную систему исчисления\n\
		"bin" - Перевод числа в двоичную систему исчисления\n\
		"hex" - Перевод числа в шестнадцатеричную систему исчисления\n\
		"bool" - Перевод числа в булево число\n\
		"int" - Перевод строки состоящей из цифр или любого другого числа в целое\n'
			ans += '---------------------------------------------------------------------------\n'
			ans += u'\tЗамечание\n\
			Формат записи восьмеричных чисел - 0nnnn... (ведущий символ - 0/нуль)\n\
			Формат записи двоичных чисел - 0bnnnn... (ведущие символы 0b/нуль+\'b\')\n\
			Формат записи шестнадцатеричных чисел - 0xnnnn... (ведущие символы 0x/нуль+\'x\')\n\
			Булевы числа понимаются в обычном смысле и имеют два состояния и соответствующий формат - \'True/False\'\n\
			Функции oct, hex и bin возвращают строки, поэтому не могут быть вложены друг в друга, т.к. аргумент должен быть целым числом.'
		else:
			ans = u'К сожалению, такой справки у меня нет'
	else:
		for pair in alias:
			command = command.replace(pair[0], pair[1])
		rem = command
		for func in genuine:
			rem = rem.replace(func, "")
		for pat in pats:
			rem = sub(pats[pat], "", rem)
		if not rem:
			try:
				ans = eval(command)
			except ValueError:
				ans = u'Аргументы некоторых функций некорректны'
			except ZeroDivisionError:
				ans = u'Произошло деление на ноль'
			except TypeError:
				ans = u'Типы аргументов некоторых функций некорректны'
			except NameError:
				ans = u'Некоторые функции мне неизвестны. Используйте !calc help для списка функций'
			except SyntaxError:
				ans = u'Неверный синтаксис выражения'
			else:
				try:
					ans = round(ans, 14)
				except TypeError:
					ans = u'Не могу произвести числовые операции. Тип передаваемых аргументов неверен. Попробуйте целые числа для конвертации чисел'
				finally:
					ans = str(ans)
		else:
			ans = u"Введенное вами выражение не может быть посчитано"
	bot.send(xmpp.Message(mess.getFrom(),ans,mode))

def rungc(bot,mess):
	mess.setFrom(unicode(mess.getFrom()).split('/')[0])
	run(bot,mess,'groupchat')
