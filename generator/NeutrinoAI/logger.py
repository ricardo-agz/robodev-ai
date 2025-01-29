import os
import threading


class FileLogger:
    def __init__(self, filename="logs.txt"):
        self.filename = f"logs/{filename}"
        self.lock = threading.Lock()

        if not os.path.exists("logs"):
            os.makedirs("logs")

    def log(self, message, filename=None):
        outfile = self.filename if not filename else f"logs/{filename}"
        with self.lock:
            with open(outfile, 'a') as f:
                f.write(f"{message}\n")

    def clear_logs(self):
        with self.lock:
            folder = "logs"
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    os.unlink(file_path)
                except Exception as e:
                    print("Failed to delete %s. Reason: %s" % (file_path, e))


logger = FileLogger()
logger2 = FileLogger()


def main_func():
    logger.clear_logs()

    logger.log("error here: ....")

    logger2.log("another error here: ....", "mylog.txt")


if __name__ == "__main__":
    main_func()
