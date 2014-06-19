from GUI import main
import os
import sys

firstStart_bool = False

if __name__ == "__main__":
    if firstStart_bool:
        main.FirstStartApp().run()
    else:
        main.MainApp().run()