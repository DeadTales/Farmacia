import ttkbootstrap as tb
from Core.Router import Router

def main():
    root = tb.Window(themename="minty")
    root.title("Farmacia Si")
    root.geometry("1100x700")

    router = Router(root)

    router.show_login()

    root.mainloop()

if __name__ == "__main__":
    main()