time_count = [0, 0, 0]
pattern = '{0:02d}:{1:02d}:{2:02d}'

def update_timer(root, button, timer):
    if button['text'] == "Stop":
        time_count[2] += 1
        if time_count[2] >= 100:
            time_count[2] = 0
            time_count[1] += 1
        if time_count[1] >= 60:
            time_count[0] += 1
            time_count[1] = 0
        timer.config(text=pattern.format(time_count[0],time_count[1],time_count[2]))
    elif time_count != [0,0,0]:
        time_count[0],time_count[1],time_count[2] = 0,0,0
        timer.configure(text='00:00:00')
    root.after(10, update_timer, root, button, timer)