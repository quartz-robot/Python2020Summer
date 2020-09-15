import math, sys, random, os
from direct.showbase.ShowBase import ShowBase

from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
# from pandac.PandaModules import TextNode

from panda3d.core import *
from direct.gui.DirectGui import *

PI = 4.0*math.atan(1.0)
DEGREEStoRADIANS = PI / 180.0
RADIANStoDEGREES = 180.0 / PI

# Set timeout for connection attempts
timeout = 1000

# Setting window properties
# props = WindowProperties()
# props.setCursorHidden(True)

# Function to put instructions on the screen.
def addInstructions(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1,1,1,1),
			pos=(-1.3, pos), align=TextNode.ALeft, scale = .05)

# Function to put title on the screen.
def addTitle(text):
    return OnscreenText(text=text, style=1, fg=(1,1,1,1),
	                pos=(0.0,-0.95), align=TextNode.ACenter, scale = .07)

class Flatland(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Post the instructions
        self.title = addTitle("SIMPLE GAME TESTING NETWORKS")
        self.inst1 = addInstructions(0.95, "[ESC]: Quit")
        self.inst2 = addInstructions(0.90, "[arrow_up]: Move Positive Y")
        self.inst3 = addInstructions(0.85, "[arrow_down]: Move Negative Y")
        self.inst4 = addInstructions(0.80, "[arrow_right]: Move Positive X")
        self.inst5 = addInstructions(0.75, "[arrow_left]: Move Negative X")

        base.setBackgroundColor(0,0,0)

        # Loading Model as 0 Point for Vector calculation (invisible at world base 0,0,0)

        self.fighter = loader.loadModel('./Assets/sphere')
        self.fighter.reparentTo(render)
        self.fighter.setPos(0,0,0)
        self.fighter.setHpr(0,0,0)
        self.fighter.setScale(1.0)
        self.fighter.setColorScale(1.0,0.0,0.0,1.0)



##########################################################################
###                                                                    ###
###                     STAGE 1                                        ###
###                                                                    ###
###   creating the environment through instancing and positioning      ###
###   the same model randomly on the circumference of a circle         ###
###   to create a 'home base'.                                         ###
###                                                                    ###
###                                                                    ###
##########################################################################

        self.parent = loader.loadModel('./Assets/cube')
        self.parent.setPos(0, 0, 0)

        x = 0
        for i in range(100):
            theta = x
            self.placeholder = render.attachNewNode('Placeholder')
            self.placeholder.setPos(50.0*math.cos(theta), \
                    50.0*math.sin(theta), 0.0)
            red = 0.6 + (random.random() * 0.4)
            grn = 0.6 + (random.random() * 0.4)
            blu = 0.6 + (random.random() * 0.4)

            self.placeholder.setColorScale(red, grn, blu, 1.0)
            self.parent.instanceTo(self.placeholder)
            x += 0.06



        #Disable Mouse control over camera
        base.disableMouse()
        base.camera.setPos(0.0, 0.0, 250.0)
        base.camera.setHpr(0.0, -90.0, 0.0)

        # start setting key bindings

        self.accept('arrow_left', self.negX, [1])
        self.accept ('arrow_left-up', self.negX, [0])

        self.accept('arrow_right', self.plusX, [1])
        self.accept('arrow_right-up', self.plusX, [0])

        self.accept('arrow_down', self.negY, [1])
        self.accept('arrow_down-up', self.negY, [0])

        self.accept('arrow_up', self.plusY, [1])
        self.accept('arrow_up-up', self.plusY, [0])

        self.accept('escape', self.quit)
###############################################################################
###                            Stage 3                                      ###
###############################################################################

        self.fightercnode = self.fighter.attachNewNode(CollisionNode('fnode'))
        self.parentcnode = self.parent.attachNewNode(CollisionNode('cnode'))

        self.fightercnode.node().addSolid(CollisionSphere(0, 0, 0, 1.0))
        self.parentcnode.node().addSolid(CollisionSphere(0, 0, 0, 2.0))

        self.pusher = CollisionHandlerPusher()
        self.pusher.addCollider(self.fightercnode, self.fighter)

        self.traverser = CollisionTraverser()
        base.cTrav = self.traverser
        self.traverser.traverse(render)
        self.traverser.addCollider(self.fightercnode, self.pusher)

        base.cTrav.showCollisions(render)


    def negX(self, keyDown):
        if keyDown:
            taskMgr.add(self.mvNegX,'moveNegX')
        else:
            taskMgr.remove('moveNegX')
            self.acceptOnce('left-arrow', self.negX, [1])
            self.acceptOnce('left-arrow-up', self.negX, [0])

    def mvNegX(self, task):
        self.fighter.setX(self.fighter, -1)
        return task.cont
###############################################################################
    def plusX(self, keyDown):
        if keyDown:
            taskMgr.add(self.mvPlusX,'movePlusX')
        else:
            taskMgr.remove('movePlusX')
            self.acceptOnce('right-arrow', self.plusX, [1])
            self.acceptOnce('right-arrow-up', self.plusX, [0])

    def mvPlusX(self, task):
        self.fighter.setX(self.fighter, 1)
        return task.cont
###############################################################################
    def negY(self, keyDown):
        if keyDown:
            taskMgr.add(self.mvNegY,'moveNegY')
        else:
            taskMgr.remove('moveNegY')
            self.acceptOnce('down-arrow', self.negY, [1])
            self.acceptOnce('down-arrow-up', self.negY, [0])

    def mvNegY(self, task):
        self.fighter.setY(self.fighter, -1)
        return task.cont
###############################################################################
    def plusY(self, keyDown):
        if keyDown:
            taskMgr.add(self.mvPlusY,'movePlusY')
        else:
            taskMgr.remove('movePlusY')
            self.acceptOnce('up-arrow', self.plusY, [1])
            self.acceptOnce('up-arrow-up', self.plusY, [0])

    def mvPlusY(self, task):
        self.fighter.setY(self.fighter, 1)
        return task.cont
###############################################################################

    # Prepare message if server wants to quit
    def quit(self):
        ## Network contacts will go here

        sys.exit()

loadPrcFileData('', 'win-size 1720, 900')

play = Flatland()
play.run()
