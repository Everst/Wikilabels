def listboxmsg(num,leny,line,listbox,index):
        if num == int(leny*0.1):
            line+="10%"
            listbox.delete(index)
            listbox.insert(index, line)
        elif num == int(leny*0.2):
            line+="10%...20%"
            listbox.delete(index)
            listbox.insert(index, line)
        elif num == int(leny*0.3):
            line+="10%...20%...30%"
            listbox.delete(index)
            listbox.insert(index, line)
        elif num == int(leny*0.4):
            line+="10%...20%...30%...40%"
            listbox.delete(index)
            listbox.insert(index, line)
        elif num == int(leny*0.5):
            line+="10%...20%...30%...40%...50%"
            listbox.delete(index)
            listbox.insert(index, line)
        elif num == int(leny*0.6):
            line+="10%...20%...30%...40%...50%...60%"
            listbox.delete(index)
            listbox.insert(index, line)
        elif num == int(leny*0.7):
            line+="10%...20%...30%...40%...50%...60%...70%"
            listbox.delete(index)
            listbox.insert(index, line)
        elif num == int(leny*0.8):
            line+="10%...20%...30%...40%...50%...60%...70%...80%"
            listbox.delete(index)
            listbox.insert(index, line)
        elif num == int(leny*0.9):
            line+="10%...20%...30%...40%...50%...60%...70%...80%...90%"
            listbox.delete(index)
            listbox.insert(index, line)
        elif num == int(leny-1):
            line+="10%...20%...30%...40%...50%...60%...70%...80%...90%...Done!"
            listbox.delete(0)
            listbox.insert(0, line)
        else:
            pass
        
        
def listboxmsg_1half(num,leny,line,listbox,index):
        if num == int(leny*0.2):
            line+="10%"
            listbox.delete(index)
            listbox.insert(index, line)
        elif num == int(leny*0.4):
            line+="10%...20%"
            listbox.delete(index)
            listbox.insert(index, line)
        elif num == int(leny*0.6):
            line+="10%...20%...30%"
            listbox.delete(index)
            listbox.insert(index, line)
        elif num == int(leny*0.8):
            line+="10%...20%...30%...40%"
            listbox.delete(index)
            listbox.insert(index, line)
        elif num == int(leny-1):
            line+="10%...20%...30%...40%...50%"
            listbox.delete(index)
            listbox.insert(index, line)
        else:
            pass
        
def listboxmsg_2half(num,leny,line,listbox,index):
        if num == int(leny*0.2):
            line+="10%...20%...30%...40%...50%...60%"
            listbox.delete(index)
            listbox.insert(index, line)
        elif num == int(leny*0.4):
            line+="10%...20%...30%...40%...50%...60%...70%"
            listbox.delete(index)
            listbox.insert(index, line)
        elif num == int(leny*0.6):
            line+="10%...20%...30%...40%...50%...60%...70%...80%"
            listbox.delete(index)
            listbox.insert(index, line)
        elif num == int(leny*0.8):
            line+="10%...20%...30%...40%...50%...60%...70%...80%...90%"
            listbox.delete(index)
            listbox.insert(index, line)
        elif num == int(leny-1):
            line+="10%...20%...30%...40%...50%...60%...70%...80%...90%...Done!"
            listbox.delete(index)
            listbox.insert(index, line)
        else:
            pass

def listboxmsg_2half_v2(num,leny,line,listbox,index):
        if num == int(leny*0.2):
            line+="...60%"
            listbox.delete(index)
            listbox.insert(index, line)
        elif num == int(leny*0.4):
            line+="...60%...70%"
            listbox.delete(index)
            listbox.insert(index, line)
        elif num == int(leny*0.6):
            line+="...60%...70%...80%"
            listbox.delete(index)
            listbox.insert(index, line)
        elif num == int(leny*0.8):
            line+="...60%...70%...80%...90%"
            listbox.delete(index)
            listbox.insert(index, line)
        elif num == int(leny-1):
            line+="...60%...70%...80%...90%...Done!"
            listbox.delete(index)
            listbox.insert(index, line)
        else:
            pass