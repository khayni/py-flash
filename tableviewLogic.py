from PyQt5.QtWidgets import *
import os, shutil, csv, json

# new, modularized version of what had previously been in gui_flashcards.py

def importing(tab, ui, deleteSelection, selectionDisplay): # handles importing a csv file to the app's decks file
	try:
		filedir = QFileDialog(tab)
		filedir.setOption(filedir.DontUseNativeDialog, True)
		filedir.setFileMode(QFileDialog.ExistingFile)
		filedir.setNameFilter("CSV files (*.csv)")
		filedir.setDirectory("C:")
		impFile = ""
		if filedir.exec_():
			impFile = filedir.selectedFiles()
		fromDir = impFile[0] 
		name = os.path.split(fromDir)[1]			
		toDir = os.path.abspath("Decks/")
		if name in os.listdir(toDir):
			self.error("This file already exists!")
		else:
			shutil.copy(fromDir, toDir)			
			deleteSelection()
			selectionDisplay()
			ui.tabWidget.setCurrentIndex(0)
			ui.comboBox.setCurrentIndex(0)
	except IndexError: # thrown when the window is prematurely closed
		pass 

def creation(tableData, model, ui, error, deleteSelection, selectionDisplay): # handles the click of createButton
	inputName = ui.inputName.text().strip()
	deckname = "Decks/" + inputName + ".csv"
	if not checkForEmpty(tableData, error):
		pass
	else:		
		if ui.createButton.text() == "Save":
			fileWrite(deckname, tableData)
			ui.createButton.setText("Create")
			tableData.clear()
			ui.inputName.clear()
			model.verticalHeader = False
			tableData.append(["", ""])
			ui.tableView.setShowGrid(False)
			model.layoutChanged.emit()
		else:
			if inputName == "":
				error("You need to name your deck!")
			elif inputName + ".csv" in os.listdir("Decks"):
				error("This deck already exists!")
			else:
				fileWrite(deckname, tableData)
				tableData.clear()
				model.verticaHeader = False
				tableData.append(["",""])
				ui.tableView.setShowGrid(False)
				ui.inputName.clear()
				model.layoutChanged.emit()
				deleteSelection()
				selectionDisplay()
				ui.tabWidget.setCurrentIndex(0)
				ui.comboBox.setCurrentIndex(0)
		ui.inputName.setReadOnly(False)
		ui.deckDelBtn.hide()
			
def fileWrite(deckname, tabledata): # actually writes the files edited/produced in the interface
	try:
		with open(deckname, "w+", newline="", encoding="utf-8") as f:
			f.truncate()
			filewriter = csv.writer(f)
			
			for i in tabledata:
				testForEmpty = []
				for j in i:
					if j.strip() != "":
						testForEmpty.append(j)
				if testForEmpty != []:
					filewriter.writerow(i)
		f.close()		
	except PermissionError:
		os.chmod(deckname, stat.S_IWRITE)
		self.fileWrite(deckname, tabledata)
		
def checkForEmpty(tableData, error):
	rows = []
	for count,i in enumerate(tableData):
		if i[0].strip() == "" and i[1].strip() == "":
			pass
		elif i[0].strip() == "" or i[1].strip() == "":
			rows.append(count)
	if rows == []:
		return True
	else:
		if len(rows) == 1:
			row = ["Row", "has an empty value."]
		else:
			row = ["Rows", "have empty values."]
		nums = ''.join((str(i+1) + ", ") if rows.index(i) != (len(rows)-1) else str(i+1) for i in [i for i in rows])
		error(f"{row[0]} {nums} {row[1]}")
		return False
		
def loadToEdit(tableData, model, ui, dropdown, error): # creates and returns lists of the data from a selected file
	try:
		filedir = QFileDialog(ui.tab_3)
		filedir.setOption(filedir.DontUseNativeDialog, True)
		filedir.setFileMode(QFileDialog.ExistingFile)
		filedir.setNameFilter("CSV files (*.csv)")
		filedir.setDirectory("Decks/")
		filedir.directoryEntered.connect(lambda: dropdown.dirCheck(self.filedir))
		impFile = ""
		if filedir.exec_():
			impFile = filedir.selectedFiles()
		realName = os.path.split(impFile[0])[1].split(".csv")[0]
		subName = "Decks/" + realName + ".csv"

		ui.createButton.setText("Save")
		model.verticalHeader = True
		ui.tableView.setShowGrid(True)
		tableData.clear()
		reformat = []
		newLine = []
		
		with open(subName, "r", newline="", encoding="utf-8") as f:
			fileReader = csv.reader(f, delimiter=",")
			for line in fileReader:
				reformat.append(line)
		f.close()
		for i in reformat: # copying, filtering, and formatting the read-in data
			for j in i:
				if j != "":
					if "," in j: # splits csv data into an app-readable format
						newLine.append(j.split(","))
					elif "\t" in j: # splits tsv data into an app-readable format
						newLine.append(j.split("\t"))
		if newLine == [] and reformat == []:
			tableData.append(["",""])
			model.verticalHeader = False
			ui.tableView.setShowGrid(False)
		elif len(newLine) != len(reformat):
			for i in reformat:
				tableData.append(i)
		else:
			for i in newLine:
				tableData.append(i)
				
		model.layoutChanged.emit()
		ui.inputName.setText(realName)
		ui.inputName.setReadOnly(True)	
		ui.deckDelBtn.show()			
	except FileNotFoundError: # thrown when the window is prematurely closed
		pass
	except UnicodeDecodeError:
		error("This file is formatted incorrectly.\nTry opening it in Notepad and checking its format.")
	except IndexError:
		pass

def addRow(tableData, model, ui): # adds a row in the Create interface
	ref = ui.tableView.selectionModel().currentIndex().row()+1
	after = []
	if len(tableData) == 0:
		tableData.append(["",""])
		model.verticalHeader = False
		ui.tableView.setShowGrid(False)
	elif len(tableData) == 1 and not model.verticalHeader:
		model.verticalHeader = True
		ui.tableView.setShowGrid(True)
	elif ref == len(tableData):
		tableData.append(["", ""])
	else:
		for i in range(ref, len(tableData)):
			x = tableData.pop()
			after.append(x)
		tableData.append(["",""])
		
		for i in range(len(after)):
			x = after.pop()
			tableData.append(x)
			ui.tableView.selectRow(ref)
	ui.scrollArea_2.ensureWidgetVisible(ui.tableView.selectRow(ref-1))
	model.layoutChanged.emit()
	
def removeRow(tableData, model, ui): # removes a row in the Create interface
	if len(tableData) == 1:
		tableData.pop()
		tableData.append(["",""])
		ui.tableView.setShowGrid(False)
		model.verticalHeader = False
		model.layoutChanged.emit()
	else:
		ref = ui.tableView.selectionModel().currentIndex().row()
		try:
			tableData.pop(ref)
		except:
			pass
		ui.tableView.selectRow(len(tableData)-1)
		ui.scrollArea_2.ensureWidgetVisible(ui.tableView.selectRow(ref-1))
		model.layoutChanged.emit()

def deleteDeck(tableData, model, ui): # deletes
	name = ui.inputName.text().strip()
	os.remove(f"Decks/{name}.csv")
	ui.inputName.clear()
	ui.inputName.setReadOnly(False)
	ui.deckDelBtn.hide()
	ui.createButton.setText("Create")
	tableData.clear()
	model.verticalHeader = False
	tableData.append(["",""])
	ui.tableView.setShowGrid(False)
	model.layoutChanged.emit()
	
	with open("collections.txt", "r+", encoding="utf-8") as collections:
		data = json.load(collections)
		for i in data:
			try:
				if f"{name}.csv" in data[i]:
					data[i].remove(f"{name}.csv")
			except:
				pass
		collections.seek(0)
		collections.truncate()
		json.dump(data, collections)
	collections.close()
	ui.comboBox.setCurrentIndex(-1)
	ui.comboBox.setCurrentIndex(0)
