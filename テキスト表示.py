import tkinter as tk

# ルートウィンドウの作成
root = tk.Tk()

# Scrollbarの作成
scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Textウィジェットの作成
text_widget = tk.Text(root, wrap=tk.NONE, yscrollcommand=scrollbar.set)
text_widget.pack(side=tk.LEFT, fill=tk.BOTH)

# ScrollbarにTextウィジェットを連動させる
scrollbar.config(command=text_widget.yview)

# 大量の文字列を挿入
for i in range(10000):
    text_widget.insert(tk.END, f"Line {i}\n")

root.mainloop()
