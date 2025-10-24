
'''
TODO:
. Change buttons to be grid not vbox
. Add proper wait for icons to load before loading buttons
. Make buttons that are selected highlight just like normal toolbar
. Make button hotkeys work like normal toolbar

'''

buttons_we_want = [
	"Freehand Brush Tool",
	"Line Tool",
	"Move Layer or Mask Up",
	"Move Layer or Mask Down",
	"Crop Tool",
	"Freehand Selection Tool",
	"Contiguous Selection Tool",
	"Text Tool",
	"Multibrush Tool",
]

from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QToolButton
from krita import DockWidget, DockWidgetFactory, DockWidgetFactoryBase
import logging
from functools import partial

# Set up logging to debug issues
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("Ass")

class Ass(DockWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Ass Docker")

		# Wait to load the UI until the icons are loaded
		# FIXME: Having this as a time out is retarded. There must be an event we can use.
		QTimer.singleShot(2000, self.setup_ui)

	def canvasChanged(self, canvas):
		pass

	def setup_ui(self):
		# Create a central widget and layout
		mainWidget = QWidget()
		layout = QVBoxLayout()
		mainWidget.setLayout(layout)

		# Print all actions
		#for a in Krita.instance().actions():
		#	print([a.objectName(), a.text()])

		# Find the names of all the actions we want to add buttons for
		things = []
		for action in Krita.instance().actions():
			#print([action.objectName(), action.text()])
			if action.text() in buttons_we_want:
				things.append({
					"action_name" : action.objectName(),
					"action_text" : action.text(),
				})

		# Add a button for each action we want
		for entry in things:
			action_name = entry["action_name"]
			action_text = entry["action_text"]
			action = Krita.instance().action(action_name)
			button = QPushButton()
			button.setToolTip(action_text)
			button.setIcon(action.icon())
			button.repaint()
			button.clicked.connect(partial(self.on_click_button, action_name))
			layout.addWidget(button)

		# Set the main widget to the Docker
		self.setWidget(mainWidget)

	def on_click_button(self, action_name):
		print(["called on_click_button", action_name])
		Krita.instance().action(action_name).trigger()


# Register the Docker with Krita
Krita.instance().addDockWidgetFactory(
	DockWidgetFactory("ass", DockWidgetFactoryBase.DockRight, Ass)
)

