#load_save.py
import g,om

loaded=[] # list of strings

def load(f):
    global loaded
    try:
        for line in f.readlines():
            loaded.append(line)
    except:
        pass

def save(f):
    f.write(str(g.level)+'\n')
    for n in range(5):
        f.write(str(len(om.found[n]))+'\n')
        for grid in om.found[n]:
            for row in grid:
                f.write(hash1(row)+'\n')

def retrieve():
    global loaded
    if len(loaded)>0:
        try:
            g.level=int(loaded[0])
            ind=0
            for n in range(5):
                ind+=1
                ln=int(loaded[ind])
                om.found[n]=[]
                for i in range(ln):
                    grid=[]
                    for j in range(n+3):
                        ind+=1
                        s=loaded[ind].rstrip()
                        row=dehash(s)
                        grid.append(row)
                    om.found[n].append(grid)
        except:
            pass

def hash1(grid):
    s=''
    for tf in grid:
        v='0'
        if tf: v='1'
        s+=v
    return s
    
def dehash(s):
    grid=[]
    for v in s:
        tf=False
        if v=='1': tf=True
        grid.append(tf)
    return grid

