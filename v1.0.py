
import sys
import os
import webbrowser
import threading
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QTabWidget, QTextEdit, QGroupBox, QComboBox, 
                             QMessageBox, QProgressBar, QFrame)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QUrl
from PyQt5.QtGui import QIcon, QFont, QPixmap, QDesktopServices

# 尝试导入 requests，如果失败则提示安装
try:
    import requests
except ImportError:
    print("Please install requests: pip install requests")
    sys.exit(1)

class StyleHelper:
    """UI 样式管理"""
    MAIN_BG = "#1e1e2e"
    CARD_BG = "#282942"
    PRIMARY_COLOR = "#7aa2f7"
    SECONDARY_COLOR = "#bb9af7"
    TEXT_COLOR = "#c0caf5"
    SUCCESS_COLOR = "#9ece6a"
    ERROR_COLOR = "#f7768e"
    
    @staticmethod
    def get_main_style():
        return f"""
            QMainWindow {{
                background-color: {StyleHelper.MAIN_BG};
            }}
            QWidget {{
                color: {StyleHelper.TEXT_COLOR};
                font-family: "Segoe UI", "Microsoft YaHei", sans-serif;
            }}
            QGroupBox {{
                border: 1px solid #414868;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: {StyleHelper.CARD_BG};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: {StyleHelper.PRIMARY_COLOR};
            }}
            QLineEdit {{
                background-color: #1a1b26;
                border: 1px solid #414868;
                border-radius: 6px;
                padding: 8px;
                color: {StyleHelper.TEXT_COLOR};
                selection-background-color: {StyleHelper.PRIMARY_COLOR};
            }}
            QLineEdit:focus {{
                border: 1px solid {StyleHelper.PRIMARY_COLOR};
            }}
            QPushButton {{
                background-color: {StyleHelper.PRIMARY_COLOR};
                color: #1a1b26;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #89b4fa;
            }}
            QPushButton:pressed {{
                background-color: #7aa2f7;
            }}
            QPushButton.secondary {{
                background-color: {StyleHelper.SECONDARY_COLOR};
            }}
            QTextEdit {{
                background-color: #1a1b26;
                border: 1px solid #414868;
                border-radius: 6px;
                padding: 5px;
                color: {StyleHelper.TEXT_COLOR};
            }}
            QComboBox {{
                background-color: #1a1b26;
                border: 1px solid #414868;
                border-radius: 6px;
                padding: 5px;
                color: {StyleHelper.TEXT_COLOR};
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QProgressBar {{
                border: 1px solid #414868;
                border-radius: 6px;
                text-align: center;
            }}
            QProgressBar::chunk {{
                background-color: {StyleHelper.SUCCESS_COLOR};
            }}
        """

class GitHubProxyWorker(QThread):
    """后台处理线程，用于生成链接和测试速度"""
    finished_signal = pyqtSignal(str, str) # url, message
    log_signal = pyqtSignal(str)
    
    def __init__(self, github_url, proxy_type):
        super().__init__()
        self.github_url = github_url.strip()
        self.proxy_type = proxy_type
        
    def run(self):
        if not self.github_url:
            self.finished_signal.emit("", "请输入有效的 GitHub URL")
            return
            
        # 简单的 URL 验证
        if "github.com" not in self.github_url:
            self.finished_signal.emit("", "URL 必须包含 github.com")
            return
            
        generated_url = ""
        try:
            if self.proxy_type == "Cloudflare Workers (ghproxy)":
                # 使用常见的 gh-proxy 模式
                generated_url = f"https://gh.api.99988866.xyz/{self.github_url}"
            elif self.proxy_type == "Fastly Mirror":
                # 使用 fastgit 或类似镜像 (注意：公共镜像可能不稳定，此处为示例逻辑)
                # 实际中可能需要替换为具体的 Fastly CDN 映射 IP 或域名
                clean_url = self.github_url.replace("https://github.com/", "").replace("http://github.com/", "")
                generated_url = f"https://hub.fastgit.org/{clean_url}"
            elif self.proxy_type == "Direct Cloudflare":
                 # 模拟直接 CF 加速逻辑 (通常需要通过 hosts 或特定 DNS，这里仅做 URL 转换示例)
                 generated_url = self.github_url # 实际 CF 加速往往不需要改 URL，而是改 DNS/Hosts
                 
            self.finished_signal.emit(generated_url, "生成成功")
        except Exception as e:
            self.finished_signal.emit("", f"错误: {str(e)}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GitHub Accelerator Pro")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(StyleHelper.get_main_style())
        
        self.init_ui()
        
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_frame = QFrame()
        header_layout = QHBoxLayout(header_frame)
        title_label = QLabel("GitHub Accelerator Pro")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {StyleHelper.PRIMARY_COLOR};")
        
        subtitle_label = QLabel("支持 Cloudflare & Fastly 加速方案")
        subtitle_label.setStyleSheet("color: #6c7086; font-size: 12px;")
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(subtitle_label)
        main_layout.addWidget(header_frame)
        
        # Input Section
        input_group = QGroupBox("资源链接")
        input_layout = QVBoxLayout(input_group)
        
        url_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("粘贴 GitHub 仓库、Release 或 Raw 文件链接...")
        self.url_input.returnPressed.connect(self.generate_link)
        
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Cloudflare Workers (ghproxy)", "Fastly Mirror (hub.fastgit)", "Direct Cloudflare"])
        self.type_combo.setFixedWidth(200)
        
        url_layout.addWidget(self.url_input)
        url_layout.addWidget(self.type_combo)
        input_layout.addLayout(url_layout)
        
        btn_layout = QHBoxLayout()
        self.gen_btn = QPushButton("生成加速链接")
        self.gen_btn.clicked.connect(self.generate_link)
        self.copy_btn = QPushButton("复制链接")
        self.copy_btn.setStyleSheet(f"background-color: {StyleHelper.SECONDARY_COLOR};")
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        self.open_btn = QPushButton("在浏览器打开")
        self.open_btn.setStyleSheet(f"background-color: {StyleHelper.SUCCESS_COLOR}; color: #1a1b26;")
        self.open_btn.clicked.connect(self.open_in_browser)
        
        btn_layout.addWidget(self.gen_btn)
        btn_layout.addWidget(self.copy_btn)
        btn_layout.addWidget(self.open_btn)
        input_layout.addLayout(btn_layout)
        
        main_layout.addWidget(input_group)
        
        # Result Section
        result_group = QGroupBox("加速结果")
        result_layout = QVBoxLayout(result_group)
        
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setPlaceholderText("生成的加速链接将显示在这里...")
        result_layout.addWidget(self.result_display)
        
        main_layout.addWidget(result_group)
        
        # Status Bar / Log
        self.status_label = QLabel("就绪")
        self.status_label.setStyleSheet("color: #6c7086; font-size: 12px;")
        main_layout.addWidget(self.status_label)
        
    def generate_link(self):
        url = self.url_input.text()
        proxy_type = self.type_combo.currentText()
        
        self.status_label.setText("正在处理...")
        self.gen_btn.setEnabled(False)
        
        self.worker = GitHubProxyWorker(url, proxy_type)
        self.worker.finished_signal.connect(self.on_generation_finished)
        self.worker.start()
        
    def on_generation_finished(self, url, message):
        self.gen_btn.setEnabled(True)
        if url:
            self.result_display.setText(url)
            self.status_label.setText(message)
            self.status_label.setStyleSheet(f"color: {StyleHelper.SUCCESS_COLOR};")
        else:
            self.status_label.setText(message)
            self.status_label.setStyleSheet(f"color: {StyleHelper.ERROR_COLOR};")
            
    def copy_to_clipboard(self):
        text = self.result_display.toPlainText()
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            self.status_label.setText("已复制到剪贴板")
            self.status_label.setStyleSheet(f"color: {StyleHelper.SUCCESS_COLOR};")
        else:
            self.status_label.setText("没有可复制的内容")
            
    def open_in_browser(self):
        text = self.result_display.toPlainText()
        if text:
            QDesktopServices.openUrl(QUrl(text))
        else:
            QMessageBox.warning(self, "警告", "请先生成链接")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
