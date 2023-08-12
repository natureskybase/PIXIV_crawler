import subprocess
import time

def run_program():
    while True:
        try:
            # 启动爬虫 程序
            subprocess.run(["python", "pixiv_bugger.py"])
        except subprocess.CalledProcessError:
            print("Program exited with an error, restarting... ")
            time.sleep(5)  # 等待一段时间后重新启动
            



if __name__ == "__main__":
    run_program()
