from GUI import main
import os
import sys
import gtk
from database import Database


db = Database()

if __name__ == "__main__":


    if not db.hasInbox():
        main.FirstStartRootApp().run()

    main.MainApp().run()