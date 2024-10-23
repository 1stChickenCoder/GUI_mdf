import tkinter as tk
from tkinter import Checkbutton, IntVar, filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from PIL import Image, ImageTk

global cursor_enabled
global vertical_line
vertical_line = None
cursor_enabled = False

# Hàm để vẽ các tín hiệu được chọn
def plot_signals():
    global t
    global ax
    ax.clear()  # Xóa biểu đồ cũ
    ax.set_xlim(0, 1 / zoom_scale)  # Cập nhật giới hạn trục x
    ax.set_ylim(-1.5, 1.5)
    t = np.linspace(0, 1, 100)  # Thời gian từ 0 đến 1 giây
    # ax.set_xlim(1, 2 / 1.5)
    # Kiểm tra từng checkbox và vẽ tín hiệu tương ứng
    if signal_vars[0].get() == 1:  # Sine
        y = np.sin(2 * np.pi * 5 * t)
        ax.plot(t, y, label='Sine')
    
    if signal_vars[1].get() == 1:  # Cosine
        y = np.cos(2 * np.pi * 5 * t)
        ax.plot(t, y, label='Cosine')
    
    if signal_vars[2].get() == 1:  # Square
        y = np.sign(np.sin(2 * np.pi * 5 * t))
        ax.plot(t, y, label='Square')

    ax.set_title("Selected Signals")
    ax.legend()  # Hiển thị chú thích
    canvas.draw()

# Hàm xử lý sự kiện khi người dùng nhấn vào menu
def on_new():
    print("New file created.")

def open_file():
    global dir_temp  # Sử dụng biến toàn cục để lưu đường dẫn file

    # Hiển thị hộp thoại mở file
    file_path = filedialog.askopenfilename(
        title="Open a file", 
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    
    if file_path:  # Nếu người dùng chọn file
        dir_temp = file_path  # Lưu đường dẫn file vào biến dir_temp
        print(f"Đường dẫn file đã chọn: {dir_temp}")


def on_save():
    # Hiển thị hộp thoại để chọn đường dẫn lưu file
    file_path = filedialog.asksaveasfilename(
        title="Save Image",
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
    )
    
    if file_path:  # Nếu người dùng chọn đường dẫn
        fig.savefig(file_path)  # Lưu biểu đồ vào đường dẫn chỉ định
        print(f"Biểu đồ đã được lưu tại: {file_path}")

def resize_image(image_path, size):
    image = Image.open(image_path)
    image = image.resize(size)  # Thay đổi kích thước
    return ImageTk.PhotoImage(image)

# Hàm xóa tín hiệu
def delete_signal(signal_index):
    # Đặt trạng thái của checkbox thành không được chọn
    signal_vars[signal_index].set(0)

    # Xóa label và checkbox tương ứng
    checkbox = checkboxes[signal_index]
    checkbox.pack_forget()  # Ẩn checkbox

    # Nếu bạn cũng cần xóa label (nếu có), làm như sau:
    if labels[signal_index]:
        labels[signal_index].pack_forget()  # Ẩn label

    # Xóa khỏi danh sách
    checkboxes.pop(signal_index)
    signal_vars.pop(signal_index)
    labels.pop(signal_index)

    # Cập nhật biểu đồ
    plot_signals()

# Hàm hiển thị menu ngữ cảnh
def show_context_menu(event, signal_index):
    context_menu = tk.Menu(root, tearoff=0)
    context_menu.add_command(label="Delete Signal", command=lambda: delete_signal(signal_index))
    context_menu.post(event.x_root, event.y_root)  # Hiển thị menu tại vị trí chuột

# Biến toàn cục để quản lý tỷ lệ zoom
zoom_scale = 1.0  # Tỷ lệ zoom ban đầu

# Hàm để thực hiện chức năng "Zoom In"
def zoom_in():
    global zoom_scale
    zoom_scale *= 1.2
    plot_signals()   # Tăng tỷ lệ zoom

# Hàm để thực hiện chức năng "Zoom Out"
def zoom_out():
    global zoom_scale
    zoom_scale /= 1.2
    plot_signals()   # Giảm tỷ lệ zoom

# Hàm để bật tắt chức năng cursor
def set_cursor():
    global cursor_enabled
    cursor_enabled = not cursor_enabled  # Chuyển đổi trạng thái cursor

    if cursor_enabled:
        # Thay đổi hình dạng con trỏ
        root.config(cursor="crosshair")
        # Đăng ký sự kiện chuột cho canvas
        canvas.mpl_connect('motion_notify_event', on_mouse_move)
    else:
        # Đặt lại con trỏ
        root.config(cursor="")
        # Ngắt kết nối sự kiện chuột
        canvas.mpl_disconnect('motion_notify_event')

# Hàm xử lý sự kiện di chuyển chuột
def on_mouse_move(event):
    global vertical_line  # Sử dụng biến toàn cục
    if cursor_enabled and event.inaxes:  # Nếu cursor đang bật và chuột nằm trong trục
        x = event.xdata
        y = event.ydata

        # Chỉ vẽ đường thẳng đứng nếu nhấn chuột trái
        if event.button == 1:  # 1 là nút chuột trái
            # Xóa đường thẳng trước đó nếu nó đã tồn tại
            if vertical_line is not None:
                vertical_line.remove()

            # Tạo đường thẳng mới
            vertical_line = ax.axvline(x=x, color='red', linestyle='--', label='Cursor Line')
            ax.legend()  # Hiển thị chú thích nếu cần
            canvas.draw()  # Vẽ lại biểu đồ

    elif vertical_line is not None:  # Nếu không còn trong trục, xóa đường thẳng
        vertical_line.remove()
        vertical_line = None
        canvas.draw()  # Vẽ lại biểu đồ

# Khởi tạo cửa sổ chính
root = tk.Tk()
root.title("Signal Plotter")

# Đặt kích thước ban đầu cho cửa sổ
root.geometry("800x400")

# Tạo thanh menu
menubar = tk.Menu(root)

# Tạo menu "File"
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Open", command=open_file)  # Tạo mục "Open"
file_menu.add_command(label="Save image", command=on_save)  # Tạo mục "Save"
file_menu.add_separator()                             # Thêm dấu ngăn cách
file_menu.add_command(label="Exit", command=root.quit)  # Tạo mục "Exit"
menubar.add_cascade(label="File", menu=file_menu)

tool_menu = tk.Menu(menubar, tearoff=0)
tool_menu.add_command(label="Fit", command=open_file)
tool_menu.add_command(label="Zoom In", command=zoom_in)
tool_menu.add_command(label="Zoom Out", command=zoom_out)
tool_menu.add_separator()   
tool_menu.add_command(label="Cursor", command=set_cursor)
menubar.add_cascade(label="Tools", menu=tool_menu)
# Thêm menu "File" vào thanh menu chính


# Tạo menu "Help"
help_menu = tk.Menu(menubar, tearoff=0)
help_menu.add_command(label="About", command=lambda: print("Signal Plotter v1.0"))

# Thêm menu "Help" vào thanh menu chính
menubar.add_cascade(label="Help", menu=help_menu)

# Gán thanh menu vào cửa sổ chính
root.config(menu=menubar)

# Tạo khoảng trống phía trên
top_padding = tk.Frame(root, height=10)
top_padding.pack()


# Tạo ảnh cho các nút
open_image = resize_image("folder_open.png", (20, 20))  # Thay thế bằng tên tệp hình ảnh của bạn
save_image = resize_image("file_save.png", (20, 20)) # Thay thế bằng tên tệp hình ảnh của bạn
exit_image = resize_image("exit.png", (20, 20))

# Tạo các nút chức năng và đặt chúng vào khung top_padding
open_button = tk.Button(top_padding,  image=open_image, command=open_file)
open_button.pack(side=tk.LEFT, pady=(5, 0), anchor='w')  # Thêm nút "Open File"

save_button = tk.Button(top_padding, image=save_image, command=on_new)
save_button.pack(side=tk.LEFT, pady=(5, 0), anchor='w')  # Thêm nút "Save File"

exit_button = tk.Button(top_padding, image=exit_image, command=on_new)
exit_button.pack(side=tk.LEFT, pady=(5, 0), anchor='w')  # Thêm nút "Exit"

# Tạo PanedWindow để chứa các frame
paned_window = tk.PanedWindow(root, orient=tk.HORIZONTAL)
paned_window.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

# Tạo frame bên trái cho danh sách tín hiệu
left_frame = tk.Frame(paned_window, bg='lightgray')
paned_window.add(left_frame)

# Đặt kích thước tối thiểu và tối đa cho frame bên trái
paned_window.paneconfigure(left_frame, minsize=80)

# Tạo biến cho các checkbox
signal_vars = [IntVar(), IntVar(), IntVar()]  # Danh sách lưu trạng thái checkbox
checkboxes = []  # Danh sách chứa checkbox
labels = []  # Danh sách chứa label (nếu có)

# Tạo checkbox cho từng tín hiệu
signals = ["Sine", "Cosine", "Square"]
for i, signal in enumerate(signals):
    cb = Checkbutton(left_frame, text=signal, variable=signal_vars[i], command=plot_signals)
    cb.pack(anchor=tk.W)  # Đặt checkbox lề trái
    checkboxes.append(cb)  # Thêm checkbox vào danh sách

    cb.bind("<Button-3>", lambda event, index=i: show_context_menu(event, index))

# Tạo frame bên phải cho biểu đồ
right_frame = tk.Frame(paned_window, bg='white')
paned_window.add(right_frame)

# Tạo biểu đồ với matplotlib
fig = Figure(figsize=(5, 4))
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=right_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)  # Mở rộng theo chiều cao của frame

# Chạy ứng dụng
root.mainloop()
