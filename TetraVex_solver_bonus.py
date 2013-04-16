# Author: Andrew Grammenos
#
# Description:
#     A Simple, kind of heuristic DFS based version of TetraVex game for
#     NxN matrices.
#
# Date: 2/6/2012
# License: BSD License (if you don't know it, get me a beer)
# Contact: andreas.grammenos@gmail.com
#

# Libraries used, nothing special here...
import os
import sys
import time
import math
import string
import search

# Tile data type
# Holds {up,left,right,down} values 
# Used state T/F?

class Tile:    
    def __init__(self,  id):
        # tile_id
        self.id = id
        # tile edge values
        self.values = {'up':-1, 'left':-1,  'right':-1,  'down':-1} # asdf
        self.using = False

# This prints the tiles in the game board.
def pt(tboard):

    # Info, print the range
    print("\nTable Range is: " + str(range(n)) + "\n")
    
    # traverse the rows...!
    for i in range(n):
            # print them!
            for j in range(0,n):
                print " --" + tboard[i*n+j].values["up"] + "-- " ,
            
            print("\n")
            for j in range(0,n):
                print " " + tboard[i*n+j].values["left"] + "---" + tboard[i*n+j].values["right"] + " ", 
            
            print("\n")
            for j in range(0,n):
                print " --" + tboard[i*n+j].values["down"] + "-- ", 
            print("\n\n")
            

# This function, prints the result to a given file using the same
# algorithm we used to print the tileboard
def writeToFile(filename):
    for i in range(n*n):
        if board[i] == 'EMPTY':
            print ('Invalid Board... please try again! bye!')
            return -1
            
    with open(filename, "w") as f:
        # write stats
        f.write("Tetravex solver v1\n")
        f.write("Andrew Grammenos (andreas.grammenos@gmail.com\n")
        f.write("Tetravex solver made " + str(graphNodes) + " node expansions and lasted approximately: {0:.4f} ".format(et)+" seconds\n")
		f.write("Solution was: \n\n")
        # write board
        for i in range(n):
            for j in range(n):
                f.write("--"+(board[i*n+j].values["up"])+"-- ") ,
            f.write('\n')
            for j in range(n):
                f.write(board[i*n+j].values["left"]+"---"+board[i*n+j].values["right"]+" "), 
            f.write('\n')
            for j in range(n):
                f.write("--"+board[i*n+j].values["down"]+"-- " ), 
            f.write('\n\n')
    return 1
        
# Check if our board placement is valid, based on the TetraVex game rules,
# that is all the adjacent sides of each tile must be of the same attirbutes
# with the tiles near it; except if they are at the edges!
#
# The function takes as input two arguments the position in the board as well 
# as the tile in question!
def checkValid(index,  tile):
    if board[index] != 'EMPTY':
        return False
    if index < n:                                    #FIRST row
        if index == 0:                              #first element so put it either way
            return True
        elif index == n-1:                        #up right corner
            if( (board[index-1]=='EMPTY' or tile.values['left'] == board[index-1].values['right']) and 
            (board[index+n] == 'EMPTY' or tile.values['down'] == board[index+n].values['up'])):
                return True
        else:                                            #random tile in 1st row
            if( (board[index-1]=='EMPTY' or tile.values['left'] == board[index-1].values['right'])and 
            (board[index+n]=='EMPTY' or tile.values['down'] == board[index+n].values['up']) and 
            (board[index+1]=='EMPTY' or tile.values['right'] == board[index+1].values['left'])):
                return True
    elif index >= (n-1)*n:                      #LAST row
        if index == (n-1)*n :                    #left down corner
            if( (board[index-n]=='EMPTY' or tile.values['up'] == board[index-n].values['down']) and 
            (board[index+1]=='EMPTY' or tile.values['right'] == board[index+1].values['left'])):
                return True
        elif index == (n*n - 1):                #down-right corner (last element to put?)
            if tile.values['left'] == board[index-1].values['right'] and tile.values['up'] == board[index-n].values['down']:
                return True
        else:                                            #last row random position, can't be the right down corner because it would and there by DFS
            if( (board[index-n]=='EMPTY' or tile.values['up'] == board[index-n].values['down']) and 
            (board[index+1]== 'EMPTY' or tile.values['right'] == board[index+1].values['left']) and 
            (board[index-1]=='EMPTY' or tile.values['left'] == board[index-1].values['right']) ):
                return True
    elif index % n == 0:                        #FIRST column! (and not corners - check above ifs)
        if( (board[index-n]=='EMPTY' or tile.values['up'] == board[index-n].values['down'] ) and 
        (board[index+1]=='EMPTY' or tile.values['right'] == board[index+1].values['left'] ) and 
        (board[index+n]=='EMPTY' or tile.values['down'] == board[index+n].values['up'] )):
            return True
    elif index % n == n-1:                     #LAST column! (and not corners - check above ifs)
        if( (board[index-n]=='EMPTY' or tile.values['up'] == board[index-n].values['down'] ) and 
        (board[index-1]=='EMPTY' or tile.values['left'] == board[index-1].values['right']) and
        (board[index+n]=='EMPTY' or tile.values['down'] == board[index+n].values['up'] )):
            return True
    else:                                                  #Custom tile in the middle not boundary!
        if( (board[index-n]=='EMPTY' or tile.values['up'] == board[index-n].values['down'] ) and 
        (board[index-1]=='EMPTY' or tile.values['left'] == board[index-1].values['right']) and
        (board[index+n]=='EMPTY' or tile.values['down'] == board[index+n].values['up'] )   and
        (board[index+1]=='EMPTY' or tile.values['right'] == board[index+1].values['left']) ):
           return True 
    return False
    
# This function is the 'brain' of the game, essentially it traverses the possible solutions using the
# classic DFS algorithm in order to find the first (not necessarely optimal) solution to the problem.
#
# The DFS algorithm was implemented with a lot of wisdom and inspiration borrowed from the 
# python implementation of the Book's code that are widely available in the net!
def DFS(index):
    # our nodes
    global graphNodes
    # check if we have completed our board filling
    if index >= (n*n):                     
        return graphNodes
    # check if we reached our max!
    if graphNodes >= nMax :               #if we reached the maximum number of expanded graphNodes
        # return, say we need more!
        return 'more'  
    
    # move on, let's have more nodes!
    graphNodes = graphNodes + 1
    
    # debug info
    if(debug == 'y' or debug == 'Y'):
        print("\n\nDFS was Called: " + str(graphNodes) + " times")
    
    
    # sort for best first @ index using a kind of-heuristic way when we have a tile 'right', 
    # sort the tiles based on parameters of the tile and on their used status with the goal 
    # to reduce the search path needed
   
    for tile in tiles:
        # check if the current tile is placed
        tiles.sort(key=lambda tile: tile.using==False)
        if tile.using == False:
            # check if we can put it at current board[index]
            if checkValid(index,  tile):
                    # print if we must!
                    if debug == 'y' or debug == 'Y':
                        print ("--> placing tile " + str(tile.id)+  " in position "+str(index))
                    # we can put it, place it!
                    board[index] = tile
                    # we are using it now, update its status
                    tile.using = True
                        
                    # search, but now advancing the index    
                    # a titbit of explanation here: here we search for every successful placement of a
                    # tile all the possible combination from using left -> right and up -> down logic. 
                    
                    
                    # search in all tiles
                    r = DFS(index+1)
                    # should the recursion reach to an end, which is when we either exhausted our search 
                    # space, found a solution or reached the dfs cutoff limit of expansion
                    if r != 'qq':
                        return r
                        
                    # print debug messages if we must
                    if debug=='y' or debug =='Y':
                        print ("--> extrating tile "+str(tile.id)+" from position "+str(index))
                
                    # release leafs and try again
                    tile.using = False
                    board[index]='EMPTY'
                    
    # if you play SC2 then you know what qq is, if not 
    #it's gg, if you still don't get it then go play a 
    # computer game!
    return 'qq'
    
'''Check the input files given'''
def readFile(filename):
    with open(filename, "r") as f:
        for j in range(n):
            #we read each line and then loop for every line in its words containing
            #one number each one. We need 3 lines for every tile (check input.txt)
            line = f.readline()
            words = line.split(' ')
            i=j*n
            for s in words:
                tiles[i].values['up'] = s[2]
                i = i+1
            #nextline
            line = f.readline()
            words = line.split(' ')
            i=j*n
            for s in words:
                tiles[i].values['left'] = s[0]
                tiles[i].values['right'] = s[4]
                i = i+1
            #nextline
            line = f.readline()
            words = line.split(' ')
            i = j*n
            for s in words:
                tiles[i].values['down'] = s[2]
                i = i+1
            f.readline()                                         #there is a blank line after each whole tile in input files
   
 # main function, gets parameters and calls dfs function in order to attempt to find a solution.
def main():
    # globals
    global n
    global graphNodes
    global board
    global tiles
    global nMax
    global debug
    graphNodes = 0
    global et
    board = []
    tiles = []
    
    n = int(input('Enter board size (NxN): '))
    # create our table
    for i in range(n*n):
        # append  as many object as NxN
        tiles.append ( Tile(i) )
        # but those object should be blank!
        board.append('EMPTY')
    # get our cutoff limit
    nMax = raw_input('DFS Cutoff: ')
    # file name for input
    filename = raw_input('Enter input file name:  ')
    
    # read data from input file
    readFile(filename)
    # print data, for viewing
    print 'Tiles read:' 
    pt(tiles)                                           
    debug = raw_input('Print execution debug info (y or n): ')
    
    # time it
    st = time.time()
    # search
    r = DFS(0)
    et = time.time() - st
    
    # print results!
    print "\nSearch made "+str(graphNodes)+" node expansions and lasted approximately: {0:.4f} ".format(et)+" seconds\n\n" 
    # check our search result, we have 3 cases, one we need more search space 
    #(and consequently graph depth), the other is that we exhausted our search space
    # and found no solution and finally...the last outcome is that we found a solution!
    if r == 'qq':
        print ("\nExausted all possible combinations, nothing found. Change input!")
    # need more!
    elif r == 'more':
        print ("DFS CutOff limit of: " + str(nMax) + " reached; expansion needed to find a solution, if any!" )
    # Solution found!
    elif r != 'qq':
        # write dat nice solution to file!
        print ("Solution found, output file: tetra.out")
        r = writeToFile("tetra.out")
        # ask the user if he wants to view that solution!
        if(r == -1):
            print("Something went wrong, could not print to file! Bye!")
        else:
            y = raw_input("Display Solution? (y or n): ")
            if y == 'y' or y =='Y':
                pt(board)
    

if __name__ == '__main__':
        main()
