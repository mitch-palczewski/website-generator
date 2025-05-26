
from app.gui.main_window import MainWindow

if __name__ == "__main__":
    try:
        main_window = MainWindow()
        main_window.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")
        input("Press enter to exit...") 