import random
import heapq

class board:
    def __init__(self , pos = None) -> None:
        if pos:
            self.pos =[ [i == j for i in range(8) ]for j in pos]
        else:
            self.pos = [[False for i in range(8)] for j in range(8) ]
            self.generate_rand()

        self.count = 0
        
    def __gt__(self, other):
        if(self.count>other.count):
            return True
        else:
            return False

    def generate_rand(self):
        for i in range(8):
            randi = random.randint(0,7)
            self.pos[i][randi] = True

    def check_valid_queens(self): 
        self.count = 0
        for i in range(8):
            for j in range(8):
                if self.pos[i][j]:
                    self.check_if_queen_is_valid(i,j)
        
        if self.count == 0:
            print("\nFOUND")
            print("\n ###############################################################")
            self.print()
            print("\n ###############################################################")
            exit(0)

    def check_if_queen_is_valid(self,i,j) :
        for x in range(8):
            if self.pos[i][x]:
                self.count+=1
        for y in range(8):
            if self.pos[y][j]:
                self.count+=1

        self.check_quadrent(i,j,lambda x : x+1 , lambda x : x+1)
        self.check_quadrent(i,j,lambda x : x+1 , lambda x : x-1)
        self.check_quadrent(i,j,lambda x : x-1 , lambda x : x+1)
        self.check_quadrent(i,j,lambda x : x-1 , lambda x : x-1)

        self.count -= 6


    def check_quadrent(self,i,j,f1,f2):
        while(i < 8 and j < 8 and i >=0 and j >= 0):
            if self.pos[i][j]:
                self.count+=1
            i = f1(i) 
            j = f2(j)
    
    def print(self):
        for i in range(8):
            print(self.pos[i])

    def get_string(self):
        temp=[]
        for i in range(8):
            for j in range(8):
                if self.pos[i][j]:
                    temp.append(j)
                    break
        return temp


def kid(parent1 : board,parent2:board) -> board:
    pos1 = parent1.get_string()
    pos2 = parent2.get_string()
    pos = []
    rnd = random.randint(0,7)
    rndlist = []

    for i in range(8):
        rndlist.append(random.getrandbits(1))

    for i in range(8):
        pos.append( (lambda : (pos1[i],pos2[i]) [rndlist[i]])() )
        if i == rnd:
            pos[-1] = random.randint(0,7)
    return board(pos)


def mix(parent1 : board,parent2:board):
    temp = []
    for i in range(4):
        temp.append(kid(parent1,parent2))
    return temp

inital_set_len = 10
search_space = []

for i in range(inital_set_len):
    temp = board()
    temp.check_valid_queens()
    search_space.append( temp )  
heapq.heapify(search_space)

while len(search_space) > 2:

    # [parent1,parent2] = search_space[:2]
    parent1 = heapq.heappop(search_space)
    parent2 = heapq.heappop(search_space)
    offsprings = mix(parent1,parent2)
    
    for offspring in offsprings:
        offspring.check_valid_queens()
        heapq.heappush( search_space , offspring )
        