from GUI import main
import os
import sys

firstStart_bool = True

if __name__ == "__main__":
    if firstStart_bool:
        main.FirstStartRootApp().run()
    else:
        main.MainApp().run()