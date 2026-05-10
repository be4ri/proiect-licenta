import sys
from PyQt6.QtWidgets import QApplication
from views.main_page_view import  MainPageView
from views.home_page_view import HomePageView

def main():
    # 1. Create the application instance
    app = QApplication(sys.argv)

    # 2. Instantiate the home page view
    # Because MainPageView inherits from QWidget, it acts as our main window here
    window = HomePageView()

    # 3. Show the window
    window.show()

    # 4. Start the application event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()