# Pure Python 3.x demo, 256 colors
# Works with bash under Linux and MacOS
# 7 console color print templates
#printColor1(text): #yellow
#printColor2(text):"gray"
#printColor3(text):"light-magenta"
# printColor4(text): "soft-yellow"
#printColor5(text):"light-blue"
#printColor6(text):  "dark-blue"
#printColor7(text): "dark-green"
import os
os.system("")
fg = lambda text, color: "\33[38;5;" + str(color) + "m" + text + "\33[0m"
bg = lambda text, color: "\33[48;5;" + str(color) + "m" + text + "\33[0m"
bgfg = lambda text, colorb,colorf: "\33[48;5;" + str(colorb) + "m" +"\33[38;5;" + str(colorf) + "m"+ text + "\33[0m"
frm_up=lambda text, colorb,colorf,x,y: "\33[48;5;" + str(colorb) + "m" +"\33[38;5;" + str(colorf) + "m"+ "\33[" +str(x)+"A"+ text + "\33[0m"
def print_six(row, format, end="\n"):
    for col in range(6):
        color = row*6 + col - 2
        if color>=0:
            text = "{:3d}".format(color)
            print (format(text,color), end=" ")
            print
        else:
            print(end="    ")   # four spaces
    print(end=end)

# for row in range(0, 43):
#     print_six(row, fg, " ")
#     print_six(row, bg)

def printColor1(text):
    #yellow
    print(bgfg(text+"       ",11,0))
    ##############################
def printColor2(text):
    "gray"
    print(bgfg(text+"       ",15,0))
    ##############################
def printColor3(text):
    "light-magenta"
    print(bgfg(text+"       ",225,0))
####################################
def printColor4(text):
    "soft-yellow"
    print(bgfg(text+"       ",229,0))
##########################################
def printColor5(text):
    "light-blue"
    print(bgfg(text+"         ",159,0))
    #################################
def printColor6(text):
    "dark-blue"
    print(bgfg(text+"        ",20,230))
    ####################################
def printColor7(text):
    "dark=green"
    print(bgfg(text + "        ",22,230))
    ###########################
def printColorErr(text):
    "dark=green"
    print(bgfg(text + "        ",1,230))
############################################
  #  print(frm_up(text,22,230,-1,0))
# Simple usage: print(fg("text", 160))
#print(bgfg("text", 219, 0),)
#print(frm_up("123456",219,0,8,7))
#printColor1("gdgdg hdhdh9 jhdhbd83883 n2222     ")