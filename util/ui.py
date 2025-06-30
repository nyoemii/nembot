import platform
import subprocess
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt, QTimer, QRectF, QSettings
from PyQt6.QtGui import QRegion, QPainterPath, QCursor
from PyQt6.QtWidgets import QGraphicsOpacityEffect
import os
import sys
import screeninfo
import config


class UI(QMainWindow):
	def __init__(self):
		print("Initializing UI...")
		super().__init__()
		self.is_minimized = False
		self.restoring = False
		self.minimizing = False
		self.dragging = False
		self.pos_drag_start = None
		self.current_alpha = 0.4
		self.settings = QSettings("nembot", "UI")

		# Window setup
		self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
		self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
		self.setFixedSize(340, 120)
		self.setWindowTitle("nembot")

		# Catpuccin mocha
		self.background_color = "#11111b"
		self.foreground_color = "#cdd6f4"
		self.active_background = "#313244"
		self.separator_color = "#6c7086"
		self.button_background_color = "#11111b"
		self.button_hover_color = "#7f849c"
		self.button_pressed_color = "#585b70"

		# Position the window on the right-hand side of the primary screen
		monitors = screeninfo.get_monitors()
		primary_screen = next((s for s in monitors if s.is_primary), monitors[0])
		screen_width, screen_height = primary_screen.width, primary_screen.height
		window_width, window_height = 340, 80
		x_position = screen_width - window_width - 10
		y_position = (screen_height - window_height) // 2

		# Check for saved position
		saved_pos = self.settings.value("window_position", None)
		if saved_pos:
			x_position, y_position = map(int, saved_pos.split(","))
		else:
			# Save the position for future reference
			self.settings.setValue("window_position", f"{x_position},{y_position}")

		self.setGeometry(x_position, y_position, window_width, window_height)

		# Apply rounded corners
		self._create_rounded_rectangle(10)

		# Opacity effect
		self.opacity_effect = QGraphicsOpacityEffect()
		self.opacity_effect.setOpacity(self.current_alpha)
		self.setGraphicsEffect(self.opacity_effect)

		# Central widget and layout
		self.central_widget = QFrame(self)
		self.central_widget.setStyleSheet(f"background-color: {self.background_color};")
		self.setCentralWidget(self.central_widget)

		# Add minimize and close buttons
		self._create_wrench_button()
		self._create_minimize_button()
		self._create_close_button()

		# Separator
		self.separator = QFrame(self.central_widget)
		self.separator.setStyleSheet(f"background-color: {self.separator_color};")
		self.separator.setGeometry(22, 38, 296, 2)

		# Main label
		self.label = QLabel(self.windowTitle(), self.central_widget)
		self.label.setStyleSheet(f"color: {self.foreground_color}; font: 12pt Arial; background-color: transparent;")
		self.label.setGeometry(15, 8, 240, 20)

		# Status label
		self.status_label = QLabel("test", self.central_widget)
		self.status_label.setStyleSheet(f"color: {self.foreground_color}; font: 12pt Arial; background-color: transparent;")
		self.status_label.setGeometry(15, 47, 320, 20)

		# Command queue label
		self.command_queue_label = QLabel("", self.central_widget)
		self.command_queue_label.setStyleSheet(f"color: {self.foreground_color}; font: 12pt Arial; background-color: transparent;")
		self.command_queue_label.setGeometry(15, 76, 320, 20)

	def _create_rounded_rectangle(self, radius):
		"""Create a rounded rectangle shape for the window."""
		path = QPainterPath()
		rect = QRectF(0, 0, self.width(), self.height())  # Use QRectF instead of QRect
		path.addRoundedRect(rect, radius, radius)
		region = QRegion(path.toFillPolygon().toPolygon())
		self.setMask(region)

	def _create_wrench_button(self):
		"""Create a custom wrench button to open the config file."""
		self.wrench_button = QPushButton("🔧", self.central_widget)  # Use a wrench emoji as the icon
		self.wrench_button.setToolTip("Edit Config")
		self.wrench_button.setStyleSheet(
			f"color: {self.foreground_color}; background-color: {self.button_background_color}; "
			f"font: 11pt Consolas; border: none;"
			f"""
			QPushButton {{
				color: {self.foreground_color};
				background-color: {self.button_background_color};
				font: 11pt Consolas;
				border: none;
			}}
			QPushButton:hover {{
				background-color: {self.button_hover_color};  /* Slightly darker */
			}}
			QPushButton:pressed {{
				background-color: {self.button_pressed_color};  /* Even darker */
			}}
			"""
		)
		self.wrench_button.setGeometry(250, 10, 20, 20)  # Position to the left of the minimize button
		self.wrench_button.clicked.connect(self.open_config_file)

	def open_config_file(self):
		"""Open the config.toml file in the platform's default text editor."""
		config_path = config.__file__
		try:
			if platform.system() == "Windows":
				os.startfile(config_path)  # Windows
			elif platform.system() == "Darwin":
				subprocess.call(["open", config_path])  # macOS
			else:
				subprocess.call(["xdg-open", config_path])  # Linux
		except Exception as e:
			raise Exception(f"Error opening config file: {e}")

	def _create_minimize_button(self):
		"""Create a custom minimize button."""
		self.minimize_button = QPushButton("━", self.central_widget)
		self.minimize_button.setToolTip("Minimize")
		self.minimize_button.setStyleSheet(
			f"color: {self.foreground_color}; background-color: {self.button_background_color}; "
			f"font: 11pt Consolas; border: none;"
			f"""
			QPushButton {{
				color: {self.foreground_color};
				background-color: {self.button_background_color};
				font: 11pt Consolas;
				border: none;
			}}
			QPushButton:hover {{
				background-color: {self.button_hover_color};  /* Slightly darker */
			}}
			QPushButton:pressed {{
				background-color: {self.button_pressed_color};  /* Even darker */
			}}
			"""
		)
		self.minimize_button.setGeometry(280, 10, 20, 20)
		self.minimize_button.clicked.connect(self.minimize_window)

	def _create_close_button(self):
		"""Create a custom close button."""
		self.close_button = QPushButton("Ｘ", self.central_widget)
		self.close_button.setToolTip("Close")
		self.close_button.setStyleSheet(
			f"color: {self.foreground_color}; background-color: {self.button_background_color}; "
			f"font: 11pt Consolas; border: none;"
			f"""
			QPushButton {{
				color: {self.foreground_color};
				background-color: {self.button_background_color};
				font: 11pt Consolas;
				border: none;
			}}
			QPushButton:hover {{
				background-color: {self.button_hover_color};  /* Slightly darker */
			}}
			QPushButton:pressed {{
				background-color: {self.button_pressed_color};  /* Even darker */
			}}
			"""
		)
		self.close_button.setGeometry(310, 10, 20, 20)
		self.close_button.clicked.connect(self.close_window)

	def update_command_status(self, text):
		"""Update the command queue label text on the main thread."""
		self.command_queue_label.setText(f"{text}")

	def update_status(self, text):
		"""Update the status label text on the main thread."""
		self.status_label.setText(f"{text}")

	def get_status(self):
		"""Get the status label text."""
		return self.status_label.text()

	def close_window(self):
		"""Close the window and stop the bot."""
		self.close()

	def _hex_to_rgb(self, hex_color):
		"""Convert a hex color to an RGB tuple."""
		hex_color = hex_color.lstrip("#")
		return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

	def _rgb_to_hex(self, rgb_color):
		"""Convert an RGB tuple to a hex color."""
		return "#{:02x}{:02x}{:02x}".format(*rgb_color)

	def fade_to_alpha(self, target_alpha, step=0.05, delay=10):
		"""Smoothly fade the window's alpha to the target value."""
		# Cancel any ongoing fade by updating the target
		if hasattr(self, "_fade_target") and self._fade_target == target_alpha:
			return  # If the current fade is already targeting this alpha, do nothing

		self._fade_target = target_alpha  # Set the new fade target

		def fade_step():
			nonlocal target_alpha, step, delay
			# Stop fading if the target has changed
			if self._fade_target != target_alpha:
				return

			if abs(self.current_alpha - target_alpha) < step:
				self.current_alpha = target_alpha
				self.opacity_effect.setOpacity(target_alpha)
				return

			self.current_alpha += step if self.current_alpha < target_alpha else -step
			self.opacity_effect.setOpacity(self.current_alpha)
			QTimer.singleShot(delay, fade_step)

		fade_step()  # Start the fade process

	def enterEvent(self, event):
		"""Increase opacity when the mouse enters the window."""
		self.fade_to_alpha(1)

	def leaveEvent(self, event):
		"""Decrease opacity when the mouse leaves the window."""
		mouse_pos = QCursor.pos()  # Get the global position of the mouse cursor
		window_rect = self.geometry()
		if not window_rect.contains(self.mapFromGlobal(mouse_pos)):
			self.fade_to_alpha(0.4)

	def _handle_leave_event(self, element):
		"""Handle leave event for buttons."""
		mouse_pos = self.mapFromGlobal(element.mapToGlobal(element.rect().center()))

	def start(self):
		"""Start the UI and associate it with the bot."""
		self.show()

	def minimize_window(self):
		"""Minimize the window as an icon."""
		self.is_minimized = True
		self.minimizing = True
		self.restoring = False
		self.setWindowFlags(Qt.WindowType.Window)
		self.opacity_effect.setOpacity(0.0)
		self.showMinimized()
		QTimer.singleShot(100, self._reset_minimizing_flag)

	def showEvent(self, event):
		"""Handle the window being restored."""
		if self.minimizing or not self.is_minimized or self.restoring:
			return
		self.restoring = True
		self.is_minimized = False
		self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
		self._create_rounded_rectangle(10)
		self.opacity_effect.setOpacity(self.current_alpha)
		self.showNormal()
		self.restoring = False

	def _reset_minimizing_flag(self):
		"""Reset the minimizing flag after a short delay."""
		self.minimizing = False

	def mouseMoveEvent(self, event):
		"""Handle mouse movement events."""
		# Check if the window is minimized
		if self.is_minimized:
			return

		# Check if the mouse is over the window
		if self.dragging:
			# If the mouse is inside the window, update the window position
			d_mouse = event.pos() - self.pos_drag_start
			new_window_pos = self.pos() + d_mouse
			self.move(new_window_pos)

		return super().mouseMoveEvent(event)

	def mousePressEvent(self, event):
		"""Handle mouse press events."""
		# Check if the window is minimized
		if self.is_minimized:
			return

		# Check if the mouse is over the window above the separator
		if event.button() == Qt.MouseButton.LeftButton and event.pos().y() < 38 and not self.dragging:
			# Start dragging the window
			self.dragging = True
			self.pos_drag_start = event.pos()
			self.setCursor(QCursor(Qt.CursorShape.SizeAllCursor))

		return super().mousePressEvent(event)

	def mouseReleaseEvent(self, event):
		"""Handle mouse release events."""
		# Check if the window is minimized
		if self.is_minimized:
			return

		if event.button() == Qt.MouseButton.LeftButton and self.dragging:
			# Stop dragging the window
			self.dragging = False
			self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
			self.settings.setValue("window_position", f"{self.x()},{self.y()}")  # Save the new position

		return super().mouseReleaseEvent(event)


if __name__ == "__main__":
	app = QApplication(sys.argv)
	ui_instance = UI()
	ui_instance.show()
	sys.exit(app.exec())
