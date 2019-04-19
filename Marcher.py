#################################################################
#                                                               #
#    Define any helper functions you need in this file only.    #
#    All classes/hepler functions should be subclass of         #
#    Marcher, do not include any code outside that scope.       #
#                                                               #
#    You cannot include any additional libraries                #
#    If you need something that Python doesn't                  #
#    have natively - implement it.                              #
#                                                               #
#    Make sure you take a look at Map.py to get familiar        #
#    with how the image is loaded in and stored, you will       #
#    need this to implement your solution properly.             #
#                                                               #
#    A few test cases are provided in Test.py. You can test     #
#    your code by running                                       #
#               python3 Test.py                                 #
#    in the directory where the files are located.              #
#                                                               #
#################################################################


class Marcher:
    
    @staticmethod
    class Min_heap:
        def __init__(self):
            # a dummy head
            self.pq = [None]
        
        def insert(self, edge):
            """ 
            edge is a 3 tuple (prev, curv, cost)
            prev is a tuple (px, py)
            curv is a tuple (nx, ny)
            cost is a float
            it will be insert to the pq based on the weight
            """
            i = len(self.pq)
            self.pq.append(edge)
            # percolate
            while (i != 1) and (edge[2] < self.pq[i//2][2]) :
                self.pq[i], self.pq[i//2] = self.pq[i//2], self.pq[i]
                i = i//2

        def extract_min(self):
            """
            extract the edge with minimum weight
            """
            edge = self.pq[1]
            self.pq[1] = self.pq[-1]
            self.pq.pop()
            size = len(self.pq)
            # heapify
            p = 1
            while p < size :
                l = p * 2
                r = l + 1
                pcost = self.pq[p][2]
                lcost = None
                rcost = None
                if l < size :
                    lcost = self.pq[l][2]
                else:
                    break
                if r < size :
                    rcost = self.pq[r][2]
                if (rcost is None) or (lcost <= rcost):
                    if pcost > lcost :
                        self.pq[p], self.pq[l] = self.pq[l], self.pq[p]
                        p = l
                    else:
                        break
                else:
                    if pcost > rcost :
                        self.pq[p], self.pq[r] = self.pq[r], self.pq[p]
                        p = r
                    else:
                        break                    
            return edge
    
        def change_priority(self, prev, cur, newp):
            # delete the old edge
            i = 1
            while i < len(self.pq):
                if self.pq[i][1] == cur :
                    break
                i += 1
            if i < len(self.pq) :
                self.pq.pop(i)
            # insert new edge
            edge = (prev, cur, newp)
            self.insert(edge)              
        
        def is_empty(self):
            return len(self.pq) == 1;
    
    @staticmethod
    def findPath(mp, weight):
        """
        Input: 
            mp - This is a Map object representing the image you are working on. Look at the Map
                class to see details on how we are representing the data.

            weight - This is the weight **function**. You are supposed to use this to find the energy
                required for each step by the Pixel Marcher. This function should be called like this:

                      weight(mp, (x,y), (a, b))

                to find the energy needed to step from pixel (x,y) to pixel (a,b). Note that
                this function may return a value for *any* pair of pixels, and it is your job
                to only be consider valid steps (More on this below). In general this returns a float.

                The return value of this function will always be non-negative, and it is not necessarily
                the case that weight(mp, a, b) = weight(mp, b, a).

        Requirements: 
            Your objective is to find the least-energy edge from pixel (0,0) to pixel(sx-1, sy-1), along
            with the amount of energy required to traverse this edge. Here, sx and sy are the x and y 
            dimensions of the image. (These are stored in 'mp')

            From each pixel, it is possible to step to at most 4 other pixels, namely the ones on it's top, 
            right, bottom and left. All of these steps may require different amounts of energy, and you have 
            to use the given weight function to compute these.

            Note: When going through your neighbours, always go through them in the following order for the sake
                of this assignment: TOP, RIGHT, BOTTOM, LEFT (Start at the top and go clockwise).


                                                        (x, y-1)
                                                            ^
                                                            |
                                        (x-1, y) <------ (x, y) ------> (x+1, y)
                                                            |
                                                            v
                                                        (x, y+1)


            Always doing it in this order will ensure consistency if there are multiple least-energy edges.

            Once you find this edge, you need to store all the nodes along it in mp.edge[], ensuring that 
            the (0,0) is the first element in the array, (sx-1, sy-1) is the last, and all the remaining
            elements are in order.

            Your function additionally needs to return the total energy required for the least-energy edge 
            you have found. You will be graded on this since the cost a least-energy edge is unique and must 
            match the expected answer.

        You are NOT allowed to import any additional libraries. All code must be your own.      

        """
        pq = Marcher.Min_heap()
        pq.insert(((0,0), (0,0), float(0)))
        sx_1 = mp.sx - 1
        sy_1 = mp.sy - 1 
        # creat a path table
        inf = float('inf')
        path_table = []
        for i in range(sx_1 + 1):
            path_table.append([])
            for j in range(sx_1 + 1):
                path_table[i].append([inf])
        path_table[0][0][0] = float(0)
        while not pq.is_empty():
            (prev, curv, total_cost) = pq.extract_min()
            (px,py) = prev
            (x, y) = curv
            # print(path_table[x][y][0])
            # update the pathtable so that we can keep track the
            # best previous node that get to it
            if len(path_table[x][y]) == 1:
                path_table[x][y].append(prev)
            else:
                path_table[x][y][1] = prev
            path_table[x][y][0] = total_cost
            # break out to the loop or insert new edges to heap
            if x == sx_1 and y == sy_1 :
                break                    
            if y != 0 and y != py+1:
                cost = weight(mp, curv, (x, y-1)) + path_table[x][y][0]
                if path_table[x][y-1][0] == inf :
                    edge = (curv, (x, y-1), cost)
                    pq.insert(edge)
                    path_table[x][y-1][0] = cost
                elif cost < path_table[x][y-1][0] :
                    pq.change_priority(curv, (x, y-1), cost)
                    path_table[x][y-1][0] = cost
            if x != 0 and x != px+1 :
                cost = weight(mp, curv, (x-1, y)) + path_table[x][y][0]
                if path_table[x-1][y][0] == inf :
                    edge = (curv, (x-1, y), cost)
                    pq.insert(edge)
                    path_table[x-1][y][0] = cost
                elif cost < path_table[x-1][y][0] :
                    pq.change_priority(curv, (x-1, y), cost)
                    path_table[x-1][y][0] = cost
            if y != sy_1 and y != py-1 :
                cost = weight(mp, curv, (x, y+1)) + path_table[x][y][0]
                if path_table[x][y+1][0] == inf :
                    edge = (curv, (x, y+1), cost)
                    pq.insert(edge)
                    path_table[x][y+1][0] = cost
                elif cost < path_table[x][y+1][0] :
                    pq.change_priority(curv, (x, y+1), cost)
                    path_table[x][y+1][0] = cost
            if x != sx_1 and x != px-1 :
                cost = weight(mp, curv, (x+1, y)) + path_table[x][y][0]
                if path_table[x+1][y][0] == inf :
                    edge = (curv, (x+1, y), cost)
                    pq.insert(edge)
                    path_table[x+1][y][0] = cost
                elif cost < path_table[x+1][y][0] :
                    pq.change_priority(curv, (x+1, y), cost)
                    path_table[x+1][y][0] = cost
        # insert edges into mp.path
        mp.path.insert(0, (sx_1, sy_1))
        (a, b) = path_table[sx_1][sy_1][1]
        while (a, b) != (0,0) :
            mp.path.insert(0, (a, b))
            (a, b) = path_table[a][b][1]
        # return the total cost
        return  path_table[sx_1][sy_1][0]

    @staticmethod
    def all_colour_weight(mp, a, b):
        """
        Input:
            mp : a Map object that represents the image
            a, b : There are both 2-tuples, containing the (x,y) coordinates for the two pixels between
                    which you want to find the energy for a step.


        Requirements:

            Define your own weight function here so that when "25colours.ppm" is run with this function, 
            the least-energy edge in the image satisfies the following constraints:

                (1) The least energy edge must visit every one of the 25 colours in the graph. The order 
                    in which the edge visits these colours does *not* matter, as long as it visits them all. 
                    Be careful - missing even one colour will result in 0 for this function.

                (2) The edge can stay on one colour for as many steps as necessary, however once the edge 
                    leaves a colour, it can NEVER go through another pixel of the same colour again.
                    (Said in another way, it can only enter/exit each coloured box once)

                (3) For any two given pixels, the energy required to step between them *must* be non-negative.
                    If you have negative energies, this function may not work as intended.

            There is no restriction on edge length, it can be as long or as short as needed - as long as it 
            satisfies the conditions above. Also, the amount of energy to step from 'a' to 'b' does not have to be
            the same as the energy to step from 'b' to 'a'. This is up to you.

        Important Note: This weight function will NOT be tested with your solution to the first part of the
                        question. This will be passed into my code and should still produce the results as above,
                        so do not try to change your findedge() method to help with this.

                        This function will be tested ONLY on the specified image, so you do not have to worry
                        about generalizing it. Just make sure that it does not depend on anything else in your
                        code other than the arguments passed in.


        How to test:    Use the 'outputGradient' and 'outputedge' methods in Map to help you debug. Displaying
                        the edge will be useful to start, as it will give you a general idea of what the least-
                        energy edge looks like, but you will also want to display the gradient to make sure that 
                        there are no colours repeated! (This should be obvious visually if it is the case)

        """
        sx = mp.sx
        sy = mp.sy
        x_region = a[0]//(sx/5)
        y_region = a[1]//(sy/5)
        # move 0, 1, 2, 3 represent up, right, down, left 
        move = None
        if b[1] == a[1]-1 :
            move = 'up'
        elif b[0] == a[0]+1 :
            move = 'right'
        elif b[1] == a[1]+1 :
            move = 'down'
        else: # b[0] = a[0]-1
            # move = 3
            return 5
        if x_region in {0, 2, 4} and y_region in {0,1,2,3} :
            if move == 'down':
                return 1
            else:
                return 5
        if x_region in {2,3} and y_region in {1,2,3,4} :
            if move == 'up':
                return 1
            else:
                return 5
        if (x_region, y_region) in {(0,4), (0,1), (2,4), (3,0)} :
            if move == 'right':
                return 1
            else:
                return 5
        else:
            return 1            

if __name__ == "__main__" :
    from Map import Map
    
    def similar_colour(mp, a, b):
        pa = mp.pixels[a]
        pb = mp.pixels[b]
        dst = (pa[0]-pb[0])**2 + (pa[1]-pb[1])**2 + (pa[2]-pb[2])**2
        return (dst ** 0.5 + 0.01)
    
    def how_white(mp, a, b):
        pb = mp.pixels[b]
        dst = (255-pb[0])**2 + (255-pb[1])**2 + (255-pb[2])**2
        return ((dst/100.0) ** 0.5) + 0.01
    
    inp = Map("images/grad.ppm")
    cost = Marcher.findPath(inp, similar_colour)
    inp.outputPath()
    #self.assertAlmostEqual(cost, 278.7514937, 5)
    print(cost)

# 2 18 poped from the heap
# then 1 18 come up and visit the table[2][18]
# which is not inf since table[2][18] was modified before
# and we try to change the priority, but 2 18 not in the heap eigther
# because it been poped.....
