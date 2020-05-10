from start_stop_handler import *
from timer_handler import *
from PIL import ImageTk, Image


#########################################

time.sleep(2)
camera = cv2.VideoCapture(0)
camera.set(10, 200)

root = Tk()
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2) - 60
positionDown = int(root.winfo_screenheight()/4 - windowHeight/4) - 50

root.geometry("300x600""+{}+{}".format(positionRight, positionDown))
root.config(bg="#F0F0F0")
title = Label(root, text="6.UAssist")
timer = Label(root, text="00:00:00", font=("Courier", 35))

image=Image.open("abstract-image.jpg")
image = image.resize((120, 120), Image.ANTIALIAS)
image = ImageTk.PhotoImage(image)
background_label = Label(root, image=image, height=120, width=120)

title.config(font=("Courier", 35))
switch = Button(root, text='Start', height=2, width= 20, bg="#BBFAC7",font=("Courier", 10))
settings = Button(root, text='Settings', height=2, width=30, bg="#AEAEAE",font=("Courier", 10))
settings.config(command= lambda: settings_click(root, camera, switch, settings, positionRight, positionDown))
switch.config(command=lambda: start_command(root, camera, switch, settings))
def on_closing():
    root.destroy()
    UI_open[0] = False
    exit()

root.protocol("WM_DELETE_WINDOW", on_closing)

background_label.pack()
title.pack(side=TOP, pady = 100)
timer.pack(side=TOP, pady= 10)
settings.pack(side=BOTTOM, pady=5)
switch.pack(side=BOTTOM, pady=5)
update_timer(root, switch, timer)
threading.Thread(target=gesture_start_thread, args=(root, camera, switch, settings)).start()
mainloop()

