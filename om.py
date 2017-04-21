# om.py
import copy,g,pygame,utils

found=[[],[],[],[],[]]

class Om:
    def __init__(self,n): # n= # of squares ... 3,4,5 or 6
        self.n=n
        self.grid=[]
        for r in range(n):
            self.grid.append([])
            for c in range(n):
                self.grid[r].append(False)
        self.x0=g.sx(1); self.y0=g.sy(1)
        if n==3:
            self.total=2; self.w0=g.sy(4); self.dw0=g.sy(.1)
            self.x1, self.y1, self.d, self.w1, self.ncols=\
            g.sx(17), g.sy(1), g.sy(8), g.sy(2.5), 1
            self.colr=(0,0,255)
        if n==4:
            self.total=5; self.w0=g.sy(3); self.dw0=g.sy(.1)
            self.x1, self.y1, self.d, self.w1, self.ncols=\
            g.sx(15), g.sy(1), g.sy(7), g.sy(1.5), 2
            self.colr=(0,255,0)
        if n==5:
            self.total=12; self.w0=g.sy(2.4); self.dw0=g.sy(.1)
            self.x1, self.y1, self.d, self.w1, self.ncols=\
            g.sx(15), g.sy(1), g.sy(5.5), g.sy(.9), 3
            self.colr=(255,0,255)
        if n==6:
            self.total=35; self.w0=g.sy(2); self.dw0=g.sy(.1)
            self.x1, self.y1, self.d, self.w1, self.ncols=\
            g.sx(15), g.sy(1), g.sy(3.5), g.sy(.5), 5
            self.colr=(0,255,255)
        if n==7:
            self.total=108; self.w0=g.sy(1.65); self.dw0=g.sy(.1)
            self.x1, self.y1, self.d, self.w1, self.ncols=\
            g.sx(14.4), g.sy(.2), g.sy(2), g.sy(.26), 9
            self.colr=utils.ORANGE

    def setup(self):
        n=self.n; self.grid_n=0
        for r in range(n):
            for c in range(n):
                self.grid[r][c]=False
        found[n-3]=[]
        self.red=None
        self.colr_n=utils.CREAM
        self.mark_fail=False
        self.green=(0,0) # r,c
        self.set_mouse(0,0)
        
    def draw(self):
        n=self.n
        y=self.y0; d=self.w0+self.dw0
        gy=100
        for r in range(n):
            x=self.x0
            for c in range(n):
                colr=(gy,gy,gy)
                if self.grid[r][c]==1:
                    colr=self.colr
                    if self.mark_fail: colr=utils.RED
                pygame.draw.rect(g.screen,colr,(x,y,self.w0,self.w0))
                if (r,c)==self.green:
                    if not self.complete():
                        pygame.draw.rect(g.screen,utils.YELLOW,\
                                 (x,y,self.w0,self.w0),10-self.n)
                x+=d
            y+=d
        self.draw_found()

    def set_mouse(self,r0,c0):
        n=self.n
        y=self.y0; d=self.w0+self.dw0
        for r in range(n):
            x=self.x0
            for c in range(n):
                if (r,c)==(r0,c0):
                    pygame.mouse.set_pos((x+self.w0/2,y+self.w0/2))
                    return
                x+=d
            y+=d

    def mouse_move(self):
        n=self.n
        y=self.y0; d=self.w0+self.dw0
        for r in range(n):
            x=self.x0
            for c in range(n):
                if utils.mouse_in(x,y,x+self.w0,y+self.w0):
                    self.green=(r,c)
                    return 
                x+=d
            y+=d

    def draw_found(self):
        x=self.x1; y=self.y1; d=self.d; cols=0; ymax=0
        for grid in found[self.n-3]:
            colr=self.colr
            if grid==self.red: colr=(255,0,0)
            y2=self.draw1(grid,x,y,colr)
            if y2>ymax: ymax=y2
            x+=d
            cols+=1
            if cols==self.ncols: x=self.x1; cols=0; y=ymax; ymax=0

    def draw1(self,grid,x0,y0,colr):
        n=self.n
        y=y0; d=self.w1
        for r in range(n):
            x=x0
            more=False
            for c in range(n):
                if grid[r][c]:
                    pygame.draw.rect(g.screen,colr,(x,y,self.w1,self.w1))
                    more=True
                x+=d
            if more: y+=d
        y+=d
        return y
        
    def square_click(self):
        self.mark_fail=False
        self.red=None
        self.colr_n=utils.CREAM
        n=self.n
        y=self.y0; d=self.w0+self.dw0
        for r in range(n):
            x=self.x0
            for c in range(n):
                if utils.mouse_in(x,y,x+self.w0,y+self.w0):
                    self.do_square(r,c)
                    return True 
                x+=d
            y+=d
        return False

    def yes(self):
        self.mark_fail=False
        self.red=None
        self.colr_n=utils.CREAM
        r,c=self.green
        self.do_square(r,c)
        
    def do_square(self,r,c):
        self.grid[r][c]=not self.grid[r][c]
        if self.grid[r][c]:
            self.grid_n+=1
        else:
            self.grid_n-=1

    def transform(self,grid,k):
        grid1=copy.deepcopy(grid); n=self.n; l=n-1
        for r in range(n):
            for c in range(n):
                v=grid[r][c]
                if   k==1: grid1[r][c]=v # identity
                elif k==2: grid1[c][l-r]=v # rotn 90
                elif k==3: grid1[l-r][l-c]=v # rotn 180
                elif k==4: grid1[l-c][r]=v # rotn 270
                elif k==5: grid1[l-r][c]=v # flip
                elif k==6: grid1[r][l-c]=v # mirrror
                elif k==7: grid1[l-c][l-r]=v # diag 1
                elif k==8: grid1[c][r]=v # diag 2
        return grid1

    def move(self,grid): # move to top left corner
        grid1=copy.deepcopy(grid); n=self.n; rmin=10; cmin=10
        for r in range(n):
            for c in range(n):
                grid1[r][c]=False
                if grid[r][c]:
                    if r<rmin: rmin=r
                    if c<cmin: cmin=c
        for r in range(n-rmin):
            for c in range(n-cmin):
                grid1[r][c]=grid[r+rmin][c+cmin]
        return grid1
       
    def clear(self,grid):
        for r in range(self.n):
            for c in range(self.n):
                grid[r][c]=False
                
    def count(self,grid):
        n=0
        for r in range(self.n):
            for c in range(self.n):
                if grid[r][c]: n+=1
        return n
                
    def ok(self):
        if self.grid_n!=self.n:
            self.colr_n=utils.RED; return False # wrong number of squares
        grid1=self.move(self.grid)
        mark_grid=copy.deepcopy(grid1); self.clear(mark_grid)
        found=False
        for r in range(self.n):
            for c in range(self.n):
                if grid1[r][c]: found=True; break
            if found: break
        self.mark(grid1,mark_grid,r,c)
        n=self.count(mark_grid)
        if n!=self.n:
            self.mark_fail=True; return False # squares not all connected
        if not self.check_new(grid1): return False # already found
        return True

    def check_new(self,grid):
        for k in range(1,9):
            grid1=self.transform(grid,k)
            grid1=self.move(grid1)
            if grid1 in found[self.n-3]:
                self.red=grid1
                return False # already found
        grid1=self.move(grid)
        found[self.n-3].append(grid1)
        return True

    def mark(self,grid,mark_grid,r,c):
        if r<0: return
        if c<0: return
        if r==self.n: return
        if c==self.n: return
        if not grid[r][c]: return # empty
        if mark_grid[r][c]: return # already marked
        mark_grid[r][c]=True
        self.mark(grid,mark_grid,r+1,c)
        self.mark(grid,mark_grid,r-1,c)
        self.mark(grid,mark_grid,r,c+1)
        self.mark(grid,mark_grid,r,c-1)
        return

    def right(self):
        r,c=self.green
        c+=1
        if c==self.n: c=0
        self.green=(r,c)
        self.set_mouse(r,c)

    def left(self):
        r,c=self.green
        c-=1
        if c<0: c=self.n-1
        self.green=(r,c)
        self.set_mouse(r,c)

    def down(self):
        r,c=self.green
        r+=1
        if r==self.n: r=0
        self.green=(r,c)
        self.set_mouse(r,c)

    def up(self):
        r,c=self.green
        r-=1
        if r<0: r=self.n-1
        self.green=(r,c)
        self.set_mouse(r,c)

    def complete(self):
        return len(found[g.level-1])==self.total
        

        
                    
            
