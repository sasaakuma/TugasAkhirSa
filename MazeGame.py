import tkinter as tk #untuk GUI
import time #untuk memberi delay animasi
import random #untuk membuat maze secara acak

# Ukuran maze
ROWS, COLS = 15, 15
CELL_SIZE = 30

class MazeGame:
    def __init__(self, master):
        self.master = master
        master.title("Maze game")

        # GUI

        # Frame atas (Membuat frame atas (tempat tombol & judul))
        top_frame = tk.Frame(master, bg="white")
        top_frame.pack(fill=tk.X)

        # Menampilkan judul besar di atas GUI
        self.title_label = tk.Label(top_frame, text=" 🔍 Welcome to Maze Explorer ",
                                    font=("Helvetica", 20, "bold"), fg="#0a3d62", bg="white")
        self.title_label.pack(pady=10)

        # Tombol “Generate New Maze” untuk membuat labirin baru, Saat ditekan, akan memanggil fungsi generate_new_maze
        self.button = tk.Button(top_frame, text="🧩 Generate New Maze", font=("Arial", 12),
                                command=self.generate_new_maze, bg="#38ada9", fg="white")
        self.button.pack(pady=5)

        # Status pesan, Label status: menunjukkan informasi seperti “solving maze…” atau “solved!”
        self.status_label = tk.Label(top_frame, text="Click the button to start.",
                                     font=("Arial", 11), fg="#333", bg="white")
        self.status_label.pack(pady=5)

        # Canvas utama tempat labirin digambar
        self.canvas = tk.Canvas(master, width=COLS * CELL_SIZE, height=ROWS * CELL_SIZE, bg="white")
        self.canvas.pack()

        self.generate_new_maze() 

        # MEMBUAT MAZE BARU

    def generate_new_maze(self): #Akan membuat maze baru dan mulai mencari solusi
        self.canvas.delete("all")
        self.status_label.config(text="✨ Generating maze...")

        # Membuat maze 2D penuh dinding (1), Matriks visited: melacak posisi yang sudah dikunjungi
        self.maze = [[1 for _ in range(COLS)] for _ in range(ROWS)]
        self.visited = [[False for _ in range(COLS)] for _ in range(ROWS)]
        self.path = []

        # Bangun maze dari titik (1, 1) secara rekursif 
        self.build_maze(1, 1)

        self.start = (1, 1)
        self.end = (ROWS - 2, COLS - 2)
        # Menentukan titik awal dan akhir
        self.maze[self.start[0]][self.start[1]] = 0
        self.maze[self.end[0]][self.end[1]] = 0

        # Gambar labirin ke layar setelah 1000 milidetik, mulai proses backtracking (fungsi solve)
        self.draw_maze()
        self.status_label.config(text="🚶‍♂️ Solving maze...")
        self.master.after(1000, lambda: self.solve(self.start[0], self.start[1]))

        # MENGGAMBAR MAZE DAN SEL
    def draw_maze(self):
        for i in range(ROWS):
            for j in range(COLS):
                color = "#222f3e" if self.maze[i][j] == 1 else "white"
                self.draw_cell((i, j), color)

        self.draw_cell(self.end, "#78e08f")  # tujuan akhir


    # Gambar satu sel dengan warna tertentu, Gunakan update() dan time.sleep() untuk animasi
    def draw_cell(self, pos, color):
        i, j = pos
        x1 = j * CELL_SIZE
        y1 = i * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#c8d6e5")
        self.master.update()
        time.sleep(0.015)

    # Algoritma recursive backtracking maze generation 
    # Membuka jalan ke arah acak 2 Langkah Menyambungkan dua sel dengan memecah dinding di tengah
    def build_maze(self, x, y):
        self.maze[x][y] = 0
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 1 <= nx < ROWS-1 and 1 <= ny < COLS-1 and self.maze[nx][ny] == 1:
                self.maze[x + dx // 2][y + dy // 2] = 0
                self.build_maze(nx, ny)

    # Fungsi utama yang mencari solusi dari start ke end menggunakan backtracking
    def solve(self, x, y):

        #Validasi posisi: keluar dari grid atau dinding atau sudah dikunjungi → tidak valid

        if not (0 <= x < ROWS and 0 <= y < COLS):
            return False
        if self.maze[x][y] == 1 or self.visited[x][y]:
            return False

        # Tandai sel sedang dikunjungi, Warnai oranye (eksplorasi)
        self.visited[x][y] = True
        self.draw_cell((x, y), "#f6b93b")  # warna eksplorasi
        self.status_label.config(text=f"Exploring {x},{y}")

        # Jika posisi sekarang adalah tujuan: maze selesai
        if (x, y) == self.end:
            self.path.append((x, y))
            self.draw_cell((x, y), "#54a0ff")
            self.status_label.config(text="✅ Maze Solved!")
            return True

        # Urutan gerak
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # kiri, bawah, kanan, atas

        # Coba semua arah jika salah satu berhasil, masukkan ke solusi (path)
        for dx, dy in directions:
            if self.solve(x + dx, y + dy):
                self.path.append((x, y))
                self.draw_cell((x, y), "#54a0ff")  # jalur benar
                return True

        # Kalau semua arah gagal → backtrack Warnai pink muda (jalur yang ditinggalkan)
        self.draw_cell((x, y), "#faccff")  # backtrack
        self.status_label.config(text=f"Backtracking from {x},{y}")
        return False

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeGame(root)
    root.mainloop()
