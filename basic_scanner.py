# 간단한 포트 스캐너
# 공부하려고 만든 심플한 포트 스캐너에요.
# 본인 컴퓨터나 허락받은 서버에만 사용하세요. 허락받지 않은 스캔은 불법입니다.

import socket
import threading
from time import time

# 포트 스캔 함수
def scan_port(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)

        result = s.connect_ex((target, port))
        if result == 0:
            print(f"[OPEN] Port {port}")

        s.close()

    except KeyboardInterrupt:
        print ("You pressed Ctrl+C")
        return
    except socket.gaierror:
        print ('Hostname could not be resolved.')
        return
    except socket.error:
        print ("Couldn't connect to server")
        return 

def thread_scan(target, start_port, end_port):
    threads = []
   
    for port in range(start_port, end_port + 1):
        
        t = threading.Thread(target=scan_port, args=(target, port))
        threads.append(t)
        t.start()

    # 모든 스레드 종료 대기
    for t in threads:
        t.join()

def main():

    target = "45.33.32.156" # nmap의 테스트용 서버 ip "sanme.nmap.org (45.33.32.156)"
    start_port = 1
    end_port = 1025

    print(f"\n{target} 스캔 시작...\n")
    t1 = time()

    thread_scan(target, start_port, end_port)

    t2 = time()
    total = t2 - t1
    print("\n스캔 완료")
    print(f"소요시간 : {round(total, 2)}")

if __name__ == "__main__":
    main()
