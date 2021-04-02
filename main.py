#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys

sys.path.insert(1, "./lib")
import logging
import oled1in3
import time
from PIL import Image, ImageDraw, ImageFont
from RPi import GPIO  # https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
from textwrap import TextWrapper
import random

# setupLogging
logging.basicConfig(level=logging.WARNING)

# pin setup OLED HAT
RST_PIN = 25
CS_PIN = 8
DC_PIN = 24
KEY_UP_PIN = 6
KEY_DOWN_PIN = 19
KEY_LEFT_PIN = 5
KEY_RIGHT_PIN = 26
KEY_PRESS_PIN = 13
KEY1_PIN = 21
KEY2_PIN = 20
KEY3_PIN = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(KEY_UP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY_DOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY_LEFT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY_RIGHT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY_PRESS_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY3_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# graphics setup OLED HAT (reference: width 128, height 64)
display = oled1in3.SH1106()
fontSizeSmall = 12
fontSizeMedium = 16
fontSizeLarge = 22
currentFontSize = fontSizeSmall
fontSmall = ImageFont.truetype('Font.ttf', fontSizeSmall)
fontMedium = ImageFont.truetype('Font.ttf', fontSizeMedium)
fontLarge = ImageFont.truetype('Font.ttf', fontSizeLarge)
currentFont = fontSmall
maxLineLengthSmallFont = 20
maxLineLengthMediumFont = 15
maxLineLengthLargeFont = 10

# sourceFiles
initialFileNumberSet1 = 0
maxLinesPerFileSet1 = [2, 3]
initialFileNumberSet2 = 10
maxLinesPerFileSet2 = [3, 2]
initialFileNumberSet3 = 20
maxLinesPerFileSet3 = [3]
currentSetFile = 0
currentRowNumber = 0
filenameSuffix = '.txt'


def _display_main_screen():
    display.Init()
    display.clear()
    image = Image.new('1', (display.width, display.height), "WHITE")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 128, 64), outline=255, fill=0)
    draw.text((2, 0), _get_menu_text(), font=fontLarge, fill=1)
    _display_question_screen(draw, 30, 1)
    display.ShowImage(display.getbuffer(image))
    global currentRowNumber
    if currentRowNumber == 0:  _set_random_question_number()


def _display_question_screen(draw, verticalOffset, textFill):
    wrapped_text = _format_text_for_display(_get_question_text())
    for index in range(len(wrapped_text)):
        draw.text((0, verticalOffset + 0 + (currentFontSize * index)), wrapped_text[index], font=currentFont,
                  fill=textFill)


def _get_menu_text():
    headerString = '(^_^) (^o^)'
    return headerString


def _get_question_text():
    filename = str(currentSetFile) + filenameSuffix
    logging.debug('filename: ' + filename)
    with open(filename) as f:
        question_list = f.read().splitlines()
    global currentRowNumber
    logging.debug('questionNumber: ' + str(currentRowNumber))
    text = str(question_list[currentRowNumber])
    logging.debug('text: ' + text)
    return text


def _format_text_for_display(unformatedText):
    wrapperSmallFont = TextWrapper(width=maxLineLengthSmallFont)
    wrappedTextSmall = wrapperSmallFont.wrap(text=unformatedText)
    wrapperMediumFont = TextWrapper(width=maxLineLengthMediumFont)
    wrappedTextMedium = wrapperMediumFont.wrap(text=unformatedText)
    wrapperLargeFont = TextWrapper(width=maxLineLengthLargeFont)
    wrappedTextLarge = wrapperLargeFont.wrap(text=unformatedText)

    linesWrappedTextLarge = len(wrappedTextLarge)
    linesWrappedTextMedium = len(wrappedTextMedium)
    linesWrappedTextSmall = len(wrappedTextSmall)

    logging.debug('linesWrappedTextLarge: ' + str(linesWrappedTextLarge) + ' linesWrappedTextMedium: ' + str(
        linesWrappedTextMedium) + ' linesWrappedTextSmall: ' + str(linesWrappedTextSmall))

    global currentFont
    global currentFontSize
    if linesWrappedTextLarge == 1:
        currentFont = fontLarge
        currentFontSize = fontSizeLarge
        return wrappedTextLarge
    elif linesWrappedTextMedium == 2:
        currentFont = fontMedium
        currentFontSize = fontSizeMedium
        return wrappedTextMedium
    else:
        currentFont = fontSmall
        currentFontSize = fontSizeSmall
        return wrappedTextSmall


def _set_random_question_number():
    global currentSetFile
    global currentRowNumber

    logging.debug(
        'Random question start: file ' + str(currentSetFile) + ' line: ' + str(
            currentRowNumber))

    if initialFileNumberSet1 <= currentSetFile <= initialFileNumberSet2 - 1:
        maxLinesSourceFile = maxLinesPerFileSet1[currentSetFile]
    elif initialFileNumberSet2 <= currentSetFile <= initialFileNumberSet3 - 1:
        maxLinesSourceFile = maxLinesPerFileSet2[currentSetFile - initialFileNumberSet2]
    else:
        maxLinesSourceFile = maxLinesPerFileSet3[currentSetFile - initialFileNumberSet3]

    logging.debug(
        'Random question start: file ' + str(currentSetFile) + ' line: ' + str(
            currentRowNumber) + ' max line: ' + str(maxLinesSourceFile))

    currentRowNumber = random.randrange(1, maxLinesSourceFile)
    logging.debug(
        'Random question start selected: file ' + str(currentSetFile) + ' line: ' + str(
            currentRowNumber))


def _update_file_given_set(startFileNumber, endFileNumber):
    global currentSetFile
    currentSetFile = random.randrange(startFileNumber, endFileNumber)
    global currentRowNumber
    currentRowNumber = 0
    logging.debug('Redefined sourceFile: ' + str(currentSetFile) + filenameSuffix)
    logging.debug('Redefined questionNumber: ' + str(currentRowNumber))


def update_set_1(channel):
    _update_file_given_set(initialFileNumberSet1, initialFileNumberSet1 + len(maxLinesPerFileSet1))
    _display_main_screen()


def update_set_2(channel):
    _update_file_given_set(initialFileNumberSet2, initialFileNumberSet2 + len(maxLinesPerFileSet2))
    _display_main_screen()


def update_set_3(channel):
    _update_file_given_set(initialFileNumberSet3, initialFileNumberSet3 + len(maxLinesPerFileSet3))
    _display_main_screen()


def update_random_question(channel):
    display.clear()
    image = Image.new('1', (display.width, display.height), "WHITE")
    draw = ImageDraw.Draw(image)
    _display_question_screen(draw, 0, 0)
    display.ShowImage(display.getbuffer(image))
    _set_random_question_number()
    time.sleep(0.5)


_display_main_screen()
GPIO.add_event_detect(KEY_PRESS_PIN, GPIO.FALLING, callback=update_random_question, bouncetime=200)
GPIO.add_event_detect(KEY1_PIN, GPIO.FALLING, callback=update_set_1, bouncetime=200)
GPIO.add_event_detect(KEY2_PIN, GPIO.FALLING, callback=update_set_2, bouncetime=200)
GPIO.add_event_detect(KEY3_PIN, GPIO.FALLING, callback=update_set_3, bouncetime=200)

try:
    while True:
        time.sleep(0.3)
except KeyboardInterrupt:
    GPIO.cleanup()
