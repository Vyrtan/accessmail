from GUI import main
from database import Database
from GUI.firstStartRootLayout import FirstStartRootApp


db = Database()

if __name__ == "__main__":
    if not db.hasInbox():
        FirstStartRootApp().run()

    main.MainApp().run()