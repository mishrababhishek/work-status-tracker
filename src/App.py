import os
from utils.logger import log
from tracker import get_changes        

def main():
    os.system('cls')
    log("Starting the application...")
    changes = get_changes()
    print(changes)

if __name__ == "__main__":
    main()
    log("Application finished.")
