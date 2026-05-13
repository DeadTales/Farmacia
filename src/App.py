import ttkbootstrap as tb
from Core.Router import Router

def main():
    root = tb.Window(themename="litera")
    root.title("Farmacia Si")
    root.geometry("1500x900")
    root.minsize(1280, 720)

    router = Router(root)

    router.show_login()

    root.mainloop()

if __name__ == "__main__":
    main()
