#!/usr/bin/python
# Ominoes.py
"""
    Copyright (C) 2011  Peter Hewitt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

"""
import g,pygame,utils,gtk,sys,buttons,slider,load_save
import om

class Ominoes:

    def __init__(self):
        self.journal=True # set to False if we come in via main()
        self.canvas=None # set to the pygame canvas if we come in via activity.py

    def display(self):
        g.screen.fill((0,0,0))
        buttons.draw()
        self.slider.draw()
        self.omm.draw()
        utils.display_number(self.omm.n,g.number_c,g.font2,self.omm.colr_n)
        s=str(len(om.found[g.level-1]))+' / '+str(self.omm.total)
        utils.text_blit(g.screen,s,g.font1,g.progress_c,utils.CREAM)
        if self.omm.complete():
            utils.centre_blit(g.screen,g.smiley,g.smiley_c)
            

    def do_click(self):
        return self.omm.square_click()
        
    def do_button(self,bu):
        if bu=='try': self.omm.ok()

    def do_key(self,key):
        if key in (pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4):
            self.set_level(key); return
        if key==257 or key==13: self.change_level(); return # tick
        if key==265 or key==pygame.K_o: self.do_button('try'); return
        if key==262 or key==275: self.omm.right(); return
        if key==260 or key==276: self.omm.left(); return
        if key==264 or key==273: self.omm.up(); return
        if key==258 or key==274: self.omm.down(); return
        if key==pygame.K_x or key==259: self.omm.yes(); return

    def change_level(self):
        g.level+=1
        if g.level>5: g.level=1
        self.omm=self.oms[g.level-1]
        r,c=self.omm.green; self.omm.set_mouse(r,c)

    def set_level(self,key):
        g.level=key-48
        self.omm=self.oms[g.level-1]
        r,c=self.omm.green; self.omm.set_mouse(r,c)
        
    def buttons_setup(self):
        buttons.Button('try',(g.sx(7.2),g.sy(16)))

    def flush_queue(self):
        while gtk.events_pending(): gtk.main_iteration()
        for event in pygame.event.get(): pass

    def run(self):
        g.init()
        if not self.journal: utils.load()
        self.oms=[]
        for n in range(3,8):
            omm=om.Om(n); omm.setup(); self.oms.append(omm)
        load_save.retrieve()
        self.omm=self.oms[g.level-1]
        self.buttons_setup()
        self.slider=slider.Slider(g.sx(10.5),g.sy(20),5,utils.YELLOW)
        going=True
        while going:
            # Pump GTK messages.
            while gtk.events_pending():
                gtk.main_iteration()

            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type==pygame.QUIT: # only in standalone version
                    if not self.journal: utils.save()
                    going=False
                elif event.type == pygame.MOUSEMOTION:
                    g.pos=event.pos
                    self.omm.mouse_move()
                    g.redraw=True
                    if self.canvas<>None: self.canvas.grab_focus()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    g.redraw=True
                    if event.button==2: # centre button
                        if not self.journal:
                            g.version_display=not g.version_display
                    if event.button==1:
                        if self.do_click():
                            pass
                        elif self.slider.mouse(): # level changed
                            self.omm=self.oms[g.level-1]
                        else:
                            bu=buttons.check()
                            if bu!='': self.do_button(bu)
                    if event.button==3: # right button
                        self.do_button('try')
                elif event.type == pygame.KEYDOWN:
                    self.do_key(event.key); g.redraw=True
            if not going: break
            if g.redraw:
                self.display()
                if not self.journal: # not on XO
                    if g.version_display: utils.version_display()
                g.screen.blit(g.pointer,g.pos)
                pygame.display.flip()
                g.redraw=False
            g.clock.tick(40)

if __name__=="__main__":
    pygame.init()
    pygame.display.set_mode((800,600))
    game=Ominoes()
    game.journal=False
    game.run()
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)
