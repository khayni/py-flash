from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import * 


def practiceFlags(name, state, functions):
	if name == "reverse":
		if state == 0:
			functions.reverseTrue = False
		elif state == 2:
			functions.reverseTrue = True
	elif name == "timed":
		if state == 0:
			functions.timed = False
		elif state == 2:
			functions.timed = True
	
def practiceInProgress(ui, functions, error, uncheckAll, deckHandler, obj): # starts off a deck cycle, passes on to both handlePractice and handleInput
	functions.practice(ui, handleTimeout) 
	if len(functions.questions) == 0:
		error("This is an empty deck!")
	else:
		try:
			try:
				ui.newImageCont.deleteLater()
				ui.discardPile.widget(1).deleteLater()
				ui.discardPile.removeWidget(ui.discardPile.widget(1))
			except:
				pass
			ui.tabWidget.setTabEnabled(1, True)
			ui.tabWidget.setTabVisible(1, True)
			ui.tabWidget.setCurrentIndex(1)
			ui.tabWidget.setTabEnabled(0, False)
			ui.tabWidget.setTabVisible(0, False)
			ui.tabWidget.setTabEnabled(2, False)
			ui.tabWidget.setTabVisible(2, False)
			ui.numRight.setText("Right: ")
			ui.numWrong.setText("Wrong: ")
			ui.timerDisplay.display("--:--")
			uncheckAll()
			functions.inPractice = True
			handlePractice(functions.i, functions, ui)
			ui.revPractice.setChecked(False)
			ui.timedPractice.setChecked(False)
		except IndexError:	
			error("There is an issue with this deck. Try editing it in the \"Create\" tab.")
			obj.functions = deckHandler()
		except UnicodeDecodeError:
			error("There is an issue with this deck. Try editing it in the \"Create\" tab.")
			obj.functions = deckHandler()

def handlePractice(i, functions, ui): # fetches the answer from the functional module, prints to the textBrowser
	try:
		if functions.inPractice:
			functions.currentQuestion = functions.questions[i]
			functions.currentAnswer = functions.answers[i]
			
			createPage("""QPushButton {border-image: url("assets/card_front.png")} QTextEdit {color: white; border: 0; background-color: rgba(0, 0, 0, 0)}""", functions.currentQuestion, 1, ui)
			createPage("""QPushButton {border-image: url("assets/card_right.png")} QTextEdit {color: white; border: 0; background-color: rgba(0, 0, 0, 0)}""", functions.currentAnswer, 2, ui)
			createPage("""QPushButton {border-image: url("assets/card_wrong.png")} QTextEdit {color: white; border: 0; background-color: rgba(0, 0, 0, 0)}""", functions.currentAnswer, 3, ui)
			ui.stackedWidget.setCurrentIndex(1)
	except IndexError:
		functions.inPractice = False
		percentageRight = round(functions.numright/len(functions.questions) * 100, 2)
		if percentageRight < 70:
			message = "You should practice these cards more."
		elif percentageRight < 80:
			message = "Fair job."
		elif percentageRight < 90:
			message = "Kudos!"
		elif percentageRight < 100:
			message = "Terrific Job!"
		else:
			message = "Perfect!"
		finished = f"You finished with {str(functions.numright)} ({percentageRight}%) cards correct. {message} Hit enter to quit."
		createPage("border: 0", finished, 1, ui)
		ui.stackedWidget.setCurrentIndex(1)
		functions.timer.stop()
		
def createPage(styleSheet, text, index, ui):
	try:
		ui.stackedWidget.removeWidget(ui.stackedWidget.widget(index))
		ui.stackedWidget.widget(index).deleteLater()
	except:
		pass
	btn = QPushButton()
	
	btn.text = QTextEdit(btn)
	btn.text.setMouseTracking(False)
	
	fontMet = QFontMetrics(ui.tabWidget.font())
	height = fontMet.height()
	numLines = (fontMet.horizontalAdvance(text)//150) + 1
	
	btn.text.setMaximumHeight(height * numLines + height)
	btn.text.viewport().setAutoFillBackground(False)
	btn.text.setText(text)
	btn.text.setAlignment(Qt.AlignCenter)
	btn.text.setTextInteractionFlags(Qt.NoTextInteraction)
	
	btn.setLayout(QVBoxLayout(btn))
	btn.layout().setAlignment(Qt.AlignCenter)
	btn.layout().addStretch()
	btn.layout().addWidget(btn.text)
	btn.layout().addStretch()
	
	btn.setStyleSheet(styleSheet)
	ui.stackedWidget.insertWidget(index, btn)
	
def handleInput(inputO, ui, functions, mainW, deckHandler, obj): # checks input, responds accordingly
	if functions.inAnimation:
		pass
	elif functions.inPractice: 
		functions.inAnimation = True
		createImages(QPixmap(QWidget.grab(ui.stackedWidget.widget(1))), 1, ui, obj)
		createImages(QPixmap(QWidget.grab(ui.stackedWidget.widget(2))), 2, ui, obj)
		createImages(QPixmap(QWidget.grab(ui.stackedWidget.widget(3))), 3, ui, obj)	
		ui.stackedWidget.setCurrentIndex(1)
		
		if inputO.lower() == functions.currentAnswer.lower():
			functions.numright += 1
			ui.numRight.setText(f"Right: {functions.numright}")
			mainW.setMinimumSize(mainW.size())
			mainW.setMaximumSize(mainW.size())
			createImages(ui.stackedWidget.widget(2).pixmap(), 0, ui, obj, True)
			flippingAnimation(2, ui, functions, mainW, obj)
			
		elif inputO.lower() != functions.currentAnswer.lower():
			ui.numWrong.setText(f"Wrong: {functions.i - functions.numright + 1}")
			mainW.setMinimumSize(mainW.size())
			mainW.setMaximumSize(mainW.size())
			createImages(ui.stackedWidget.widget(3).pixmap(), 0, ui, obj, True)
			flippingAnimation(3, ui, functions, mainW, obj)
			
		ui.lineEdit.clear()
		functions.i += 1			
	else:
		ui.tabWidget.setTabEnabled(0, True)
		ui.tabWidget.setTabVisible(0, True)	
		ui.tabWidget.setTabEnabled(2, True)
		ui.tabWidget.setTabVisible(2, True)		
		ui.tabWidget.setCurrentIndex(0)
		ui.lineEdit.clear()
		ui.tabWidget.setTabEnabled(1, False)
		ui.tabWidget.setTabVisible(1, False)
		functions = deckHandler()
		
def handleTimeout(functions, ui):
	if not functions.inAnimation:
		functions.inPractice = False
		message = f"You timed out with {functions.i}/{len(functions.questions)} answered, and {functions.numright} correct. Hit enter to quit."
		createPage("border: 0", message, 1, ui)
		ui.stackedWidget.setCurrentIndex(1)
	
def createImages(pixmap, index, ui, obj, proceed=False): # creates a pixmap image for both the front and back of the cards
	obj.face = pixmap
	
	obj.rounded = QPixmap(obj.face.size())
	obj.rounded.fill(QColor("transparent"))
	obj.painter = QPainter(obj.rounded)
	obj.painter.setRenderHint(QPainter.Antialiasing)
	obj.painter.setBrush(QBrush(obj.face))
	obj.painter.setPen(Qt.NoPen)
	obj.painter.drawRoundedRect(obj.face.rect(), 35, 35)
	obj.painter.end()
	
	if proceed == False:
		ui.stackedWidget.widget(index).deleteLater()
		ui.stackedWidget.removeWidget(ui.stackedWidget.widget(index))
		ui.stackedWidget.insertWidget(index, QLabel())
		ui.stackedWidget.widget(index).setPixmap(obj.rounded)
		ui.stackedWidget.widget(index).setStyleSheet("QLabel {border-radius: 35px}")
		ui.stackedWidget.widget(index).setScaledContents(True)
	else:
		ui.newImageCont = QLabel(ui.tab_2)
		ui.newImageCont.setPixmap(obj.rounded)
		ui.newImageCont.setStyleSheet("QLabel {border-radius: 35px}")
		ui.newImageCont.setScaledContents(True)
		ui.newImageCont.setMinimumHeight(267)
		ui.newImageCont.setMinimumWidth(200)
		
def flippingAnimation(index, ui, functions, mainW, obj):
	obj.shrink = QPropertyAnimation(ui.stackedWidget, b"size")
	obj.shrink.setEndValue(QSize(0, 267))
	obj.shrink.setEasingCurve(QEasingCurve.InCubic)
	obj.shrink.setDuration(400)
	
	obj.moveMid = QPropertyAnimation(ui.stackedWidget, b"pos")
	obj.moveMid.setEndValue(QPoint(ui.stackedWidget.geometry().x()+100, ui.stackedWidget.geometry().y()))
	obj.moveMid.setEasingCurve(QEasingCurve.InCubic)
	obj.moveMid.setDuration(400)
	obj.moveMid.finished.connect(lambda: ui.stackedWidget.setCurrentIndex(index))
	
	obj.flipBack = QParallelAnimationGroup()
	obj.flipBack.addAnimation(obj.shrink)
	obj.flipBack.addAnimation(obj.moveMid)

	obj.expand = QPropertyAnimation(ui.stackedWidget, b"size")
	obj.expand.setEasingCurve(QEasingCurve.OutCubic)
	obj.expand.setStartValue(QSize(0, 267))
	obj.expand.setEndValue(QSize(200, 267))
	obj.expand.setDuration(400)
	
	obj.moveBack = QPropertyAnimation(ui.stackedWidget, b"pos")
	obj.moveBack.setEasingCurve(QEasingCurve.OutCubic)
	obj.moveBack.setStartValue(QPoint(ui.stackedWidget.geometry().x()+100, ui.stackedWidget.geometry().y()))
	obj.moveBack.setEndValue(QPoint(ui.stackedWidget.geometry().x(), ui.stackedWidget.geometry().y()))
	obj.moveBack.setDuration(400)
	
	obj.flipForward = QParallelAnimationGroup()
	obj.flipForward.addAnimation(obj.expand)
	obj.flipForward.addAnimation(obj.moveBack)
	obj.flipForward.finished.connect(ui.newImageCont.show)
	obj.flipForward.finished.connect(lambda: newCard(ui, functions))
	
	obj.slide = QPropertyAnimation(ui.newImageCont, b"pos")
	obj.slide.setStartValue(QPoint(ui.stackedWidget.geometry().x(), ui.stackedWidget.geometry().y()))
	obj.slide.setEndValue(QPoint(ui.discardPile.geometry().x(), ui.discardPile.geometry().y()))
	obj.slide.setEasingCurve(QEasingCurve.InOutCubic)
	obj.slide.setDuration(5000)
	obj.slide.finished.connect(lambda: resetSlide(ui))
	

	obj.fullFlip = QSequentialAnimationGroup()
	obj.fullFlip.addAnimation(obj.flipBack)
	obj.fullFlip.addAnimation(obj.flipForward)
	obj.fullFlip.addAnimation(obj.slide)
	obj.fullFlip.finished.connect(lambda: turnOffAnimation(functions, mainW))
	
	obj.fullFlip.start()

def turnOffAnimation(functions, mainW):
	functions.inAnimation = False
	mainW.setMaximumSize(16777215, 16777215)
	mainW.setMinimumSize(600, 500)

def resetSlide(ui):
	try:
		ui.discardPile.widget(1).deleteLater()
		ui.discardPile.removeWidget(ui.discard.widget(1))
	except:
		pass
	ui.discardPile.insertWidget(1, ui.newImageCont)
	ui.discardPile.setCurrentIndex(1)
	
def newCard(ui, functions):
	ui.stackedWidget.setCurrentIndex(0)
	ui.lineEdit.clear()
	handlePractice(functions.i, functions, ui)
	
