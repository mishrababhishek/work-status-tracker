import os
from utils.logger import log
from tracker import get_changes        
from email_generator import generate_work_status_email

def main():
    log("[main] Starting the application...")

    try:
        log("[main] Clearing console...")
        os.system('cls' if os.name == 'nt' else 'clear')
    except Exception as e:
        log(f"[main] Error clearing console: {e}")

    log("[main] Fetching changes from repositories...")
    changes = get_changes()

    log("[main] Generating work status email...")
    email = generate_work_status_email(changes)

    if email:
        output_dir = os.path.join(os.path.dirname(__file__), "..", "output")
        output_path = os.path.join(output_dir, "email.txt")

        try:
            os.makedirs(output_dir, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(email)
            log(f"[main] Email successfully written to: {output_path}")
        except Exception as e:
            log(f"[main] Failed to write email to file: {e}")
    else:
        log("[main] Email generation failed. No output written.")

    log("[main] Application finished.")

if __name__ == "__main__":
    main()
