# g.py - globals
import pygame,utils,random

app='Ominoes'; ver='1.0'
ver='1.1'
# tablet version
ver='1.2'
# 1,2,3,4-> level space->try
ver='1.3'
# standard gamepad
ver='1.4'
# Enter=change level, right arrow ok
ver='1.5'
# mouse move rather than yellow square
ver='1.6'
# yellow square again and mouse follows arrows
ver='1.7'
# mouse hide removed
ver='1.8'
# fake cursor
ver='1.9'
# right button same as O

def init(): # called by run()
    random.seed()
    global redraw
    global screen,w,h,font1,font2,clock
    global factor,offset,imgf,message,version_display
    global pos,pointer
    redraw=True
    version_display=False
    screen = pygame.display.get_surface()
    pygame.display.set_caption(app)
    screen.fill((70,0,70))
    pygame.display.flip()
    w,h=screen.get_size()
    if float(w)/float(h)>1.5: #widescreen
        offset=(w-4*h/3)/2 # we assume 4:3 - centre on widescreen
    else:
        h=int(.75*w) # allow for toolbar - works to 4:3
        offset=0
    factor=float(h)/24 # measurement scaling factor (32x24 = design units)
    imgf=float(h)/900 # image scaling factor - all images built for 1200x900
    clock=pygame.time.Clock()
    if pygame.font:
        t=int(50*imgf); font1=pygame.font.Font(None,t)
        t=int(150*imgf); font2=pygame.font.Font(None,t)
    message=''
    pos=pygame.mouse.get_pos()
    pointer=utils.load_image('pointer.png',True)
    pygame.mouse.set_visible(False)
    
    # this activity only
    global level,smiley,smiley_c,progress_c,number_c
    level=1 # 1 to 5 -> no. of squares 3 to 7
    smiley=utils.load_image('smiley.png',True); smiley_c=(sx(25.5),sy(19.8))
    progress_c=(sx(11.2),sy(16))
    number_c=(sx(3.5),sy(16))
    
def sx(f): # scale x function
    return int(f*factor+offset+.5)

def sy(f): # scale y function
    return int(f*factor+.5)
