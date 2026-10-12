import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QMenu, QAction
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QIcon

CONFIG_FILE = "widget_config.json"

class ImageWidget(QWidget):
    def __init__(self, image_path):
        super().__init__()
        
        # Настройки окна: без рамок, без задачи, всегда поверх
        self.setWindowFlags(
            Qt.FramelessWindowHint | 
            Qt.WindowStaysOnTopHint | 
            Qt.Tool | 
            Qt.WindowDoesNotAcceptFocus
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Загрузка оригинальной картинки (сохраняем её, чтобы не терять качество при масштабировании)
        self.original_pixmap = QPixmap(image_path)
        if self.original_pixmap.isNull():
            print(f"Не удалось загрузить: {image_path}")
            sys.exit(1)
            
        self.label = QLabel(self)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)
        
        # Загрузка настроек
        self.config = self.load_config()
        self.opacity = self.config.get("opacity", 1.0)
        self.setWindowOpacity(self.opacity)
        
        # Применение сохраненных размеров (или исходных, если их нет в конфиге)
        target_w = self.config.get("width", self.original_pixmap.width())
        target_h = self.config.get("height", self.original_pixmap.height())
        self.apply_size(target_w, target_h)
        
        # Позиция
        pos = self.config.get("position")
        if pos:
            self.move(pos["x"], pos["y"])
            
        self.drag_pos = None

    def apply_size(self, w, h):
        """Масштабирует картинку и применяет размер к виджету"""
        # KeepAspectRatio сохраняет пропорции, SmoothTransformation делает сглаживание
        self.current_pixmap = self.original_pixmap.scaled(
            w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.label.setPixmap(self.current_pixmap)
        self.setFixedSize(self.current_pixmap.size())

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_config(self):
        pos = self.pos()
        self.config["opacity"] = self.opacity
        self.config["position"] = {"x": pos.x(), "y": pos.y()}
        # Сохраняем текущие размеры
        self.config["width"] = self.width()
        self.config["height"] = self.height()
        
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.drag_pos and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.drag_pos = None
        self.save_config()

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        
        # Если зажат Ctrl - меняем размер
        if event.modifiers() & Qt.ControlModifier:
            scale_factor = 1.1 if delta > 0 else 0.9
            new_w = int(self.width() * scale_factor)
            new_h = int(self.height() * scale_factor)
            
            # Ограничение минимального размера, чтобы не схлопнуть виджет
            if new_w < 20 or new_h < 20:
                return
                
            self.apply_size(new_w, new_h)
        else:
            # Если Ctrl не зажат - меняем прозрачность
            step = 0.05
            if delta > 0:
                self.opacity = min(1.0, self.opacity + step)
            else:
                self.opacity = max(0.05, self.opacity - step)
            self.setWindowOpacity(self.opacity)
            
        self.save_config()

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        
        # Можно добавить сброс размера до оригинала
        reset_action = QAction("Сбросить размер", self)
        reset_action.triggered.connect(lambda: self.reset_size())
        menu.addAction(reset_action)
        
        menu.addSeparator()
        
        quit_action = QAction("Выйти", self)
        quit_action.triggered.connect(QApplication.quit)
        menu.addAction(quit_action)
        menu.exec_(event.globalPos())

    def reset_size(self):
        """Возвращает картинке оригинальный размер"""
        self.apply_size(self.original_pixmap.width(), self.original_pixmap.height())
        self.save_config()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    image_path = "Kordebalet67-gitfut.png"
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        
    widget = ImageWidget(image_path)
    widget.show()
    sys.exit(app.exec_())