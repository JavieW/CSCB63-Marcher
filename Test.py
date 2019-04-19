import unittest
from Marcher import Marcher
from Map import Map

#####################################################################
#                                                                   #
#   There will be other test cases when your code is graded.        #
#   Feel free to add your own test cases here, this file will       #
#   not be submitted. These are just for reference. You should      #
#                                                                   #
#   All timings are on BV473 machines with no one else logged       #
#   in averaged across several runs. (Mathlab tends to be slower)   #
#                                                                   #
#   You can check how many users are logged in using the command    #
#   'uptime' on the machine. (People might SSH'ing in)              #
#                                                                   #
#   Individial tests can be run as follows:                         #
#      python3 Test.py Marcher.test_Maze_One      (etc)             #
#                                                                   #
#####################################################################


# Weight function (1)
#   The weight between two pixels is the euclidean distance between
#   the (R,G,B) values of the 2 pixels. (If we think of them as vectors)
def similar_colour(mp, a, b):
    pa = mp.pixels[a]
    pb = mp.pixels[b]
    dst = (pa[0]-pb[0])**2 + (pa[1]-pb[1])**2 + (pa[2]-pb[2])**2
    return (dst ** 0.5 + 0.01)


# Weight function (2)
#   The weight between two pixels is simply how close pixel (b) is from
#   the colour white (255, 255, 255).
def how_white(mp, a, b):
    pb = mp.pixels[b]
    dst = (255-pb[0])**2 + (255-pb[1])**2 + (255-pb[2])**2
    return ((dst/100.0) ** 0.5) + 0.01


class TestMarcher(unittest.TestCase):

    # Time on my solution ~0.45s
    def test_One(self):
        inp = Map("images/water.ppm")
        cost = Marcher.findPath(inp, similar_colour)
        inp.outputPath()
        self.assertAlmostEqual(cost, 1280.8152597, 5)

    # Time on my solution ~0.45s
    def test_Two(self):
        inp = Map("images/spiral.ppm")
        cost = Marcher.findPath(inp, similar_colour)
        inp.outputPath()
        self.assertAlmostEqual(cost, 991.25540719, 5)

    # If we have black and white mazes, using weight function (2)
    #   makes sure that the Pixel Marcher always tries to walk along
    #   the white paths and solves the maze!

    # Time on my solution ~0.32s
    def test_Maze(self):
        inp = Map("images/maze.ppm")
        cost = Marcher.findPath(inp, how_white)
        inp.outputPath()
        self.assertAlmostEqual(cost, 12.3999999, 5)

    # Time on my solution ~1.25s
    def test_Maze_Big(self):
        inp = Map("images/bigmaze.ppm")
        cost = Marcher.findPath(inp, how_white)
        inp.outputPath()
        self.assertAlmostEqual(cost, 8.6199999, 5)

    # The following two test cases use the same image. You might
    # want to run them separately when debugging because they will
    # will over write the (already existing) output file.

    # Time on my solution ~0.1s
    def test_Gradient_One(self):
        inp = Map("images/grad.ppm")
        cost = Marcher.findPath(inp, similar_colour)
        inp.outputPath()
        self.assertAlmostEqual(cost, 278.7514937, 5)

    # Time on my solution ~0.1s
    def test_Gradient_Two(self):
        inp = Map("images/grad.ppm")
        cost = Marcher.findPath(inp, how_white)
        inp.outputPath()
        self.assertAlmostEqual(cost, 2168.3216577, 5)

    # This is just to help you run the function from Part (ii)
    #   The autotester will actually be checking the path to make
    #   sure that all the conditions given are satisfied, but here
    #   it is going to be your job to do so.

    #def test_25_Colours(self):
        #inp = Map("images/25colours.ppm")

        ## Currently being run with your solution... But this
        ##   will be replaced with a call to mine.
        #Marcher.findPath(inp, Marcher.all_colour_weight)

        ## Outputs both the path and gradient along it.
        ## Uncomment these out if you want to use them

        #inp.outputPath()
        #inp.outputGradient()

if __name__ == "__main__":
    unittest.main()
