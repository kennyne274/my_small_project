# 현재 아무 기능 없음
# 틀만 만들어놓은 상태

import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("뉴스 기사 수집 프로그램")
root.geometry("620x680")
root.resizable(False, False)

# =========================
# 1. 결과 폴더 열기 영역
# =========================
top_frame = ttk.LabelFrame(root, text="결과 폴더 열기")
top_frame.pack(fill="x", padx=10, pady=5)

btn_open = ttk.Button(top_frame, text="결과 폴더 열기", width=25, padding=(10,5))
btn_open.pack(side="left", padx=10, pady=10)

btn_login = ttk.Button(top_frame, text="로그인", width=25, padding=(10,5))
btn_login.pack(side="right", padx=10, pady=10)

# =========================
# 2. 키워드 입력 영역
# =========================
keyword_frame = ttk.LabelFrame(root, text="키워드 입력")
keyword_frame.pack(fill="x", padx=10, pady=5)

ttk.Label(keyword_frame, text="키워드:").pack(side="left", padx=10, pady=10)

keyword_entry = ttk.Combobox(keyword_frame, width=70)
keyword_entry.pack(side="left", padx=5)

# =========================
# 3. 다운로드 개수 영역
# =========================
count_frame = ttk.LabelFrame(root, text="다운로드 개수")
count_frame.pack(fill="x", padx=10, pady=5)

ttk.Label(count_frame, text="개수:").pack(side="left", padx=20, pady=10)

count_spinbox = tk.Spinbox(count_frame, from_=1, to=100, width=40)
count_spinbox.pack(side="left")

# =========================
# 4. 로그 영역
# =========================
log_frame = ttk.LabelFrame(root, text="로그")
log_frame.pack(fill="both", expand=True, padx=10, pady=5)

log_text = tk.Text(log_frame, height=15)
log_text.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(log_frame, command=log_text.yview)
scrollbar.pack(side="right", fill="y")

log_text.config(yscrollcommand=scrollbar.set)

# =========================
# 5. 실행 제어 영역
# =========================
control_frame = ttk.LabelFrame(root, text="실행 제어")
control_frame.pack(fill="x", padx=10, pady=5)

btn_run = ttk.Button(control_frame, text="실행", width=25, padding=(10,5))
btn_run.pack(side="left", padx=10, pady=10)

btn_exit = ttk.Button(control_frame, text="종료", width=25, padding=(10,5), command=root.quit)
btn_exit.pack(side="right", padx=10, pady=10) 

root.mainloop()
