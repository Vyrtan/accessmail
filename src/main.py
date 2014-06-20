from GUI import main
import os
import sys
from database import Database


firstStart_bool = True
db = Database()

if __name__ == "__main__":
    if not db.hasInbox():
        main.FirstStartRootApp().run()
    else:
        main.MainApp().run()