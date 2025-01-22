
"""
State:          Unai.larrarte subnet1
State type:     unai.larrarte_subnet1
Description:    Unai.larrarte subnet1
Author:         unai.larrarte
Computer Name:  C2P1000LABEDU.escac.es
Date Created:   December 14, 2020

"""

import hou
import viewerstate.utils as su

class State(object): 
    
    def __init__(self, state_name, scene_viewer):
        self.state_name = state_name
        self.scene_viewer = scene_viewer
        self.node = None
        self.contador = 0
        self.collisiongeo = None  # Geometry for collision checks
        self.primNormal = None  # Normal of the intersected primitive      
        
        self.placedobject = False
        self.oldcolor = (0.0, 0.0, 0.0)
        self.entries = 0
        self.placedpos = hou.Vector3()
        self.hitnormal = hou.Vector3()
        
        self.json_list = None  # Placeholder for a JSON list
        self.json_parm = None  # Placeholder for a JSON parameter

        self.ui_event = None  # Placeholder for UI events
        self.moduleIndex = 3  # Index to track module IDs

    def onEnter(self, kwargs):
        """Executed when the state is activated."""
        self.node = kwargs["node"]
        self.placedobject = False

        if not self.node:
            raise RuntimeError("Node is not defined.")

        # Set the collision geometry for ray intersection
        self.collisiongeo = self.node.node("COMPLEXCOLLISION").geometry()

        # Retrieve the multiparm parameter
        self.multiparm = self.node.parm("iPlacements")
        
        # Get the number of existing entries and increment it for the new placement
        entries = self.GetMultiparmEntries(kwargs)
        self.entries = entries
        self.multiparm.set(entries + 1)

        # Activate a parameter to signal the placement process
        self.node.node("/obj/GRID_OBJ_PLACER/subnet1/attribwrangle5").parm("aux").set(1)

      
    def GetMultiparmEntries(self, kwargs):
        return self.multiparm.evalAsInt()

    def onInterrupt(self,kwargs):        
        pass

    def onResume(self, kwargs):
        self.scene_viewer.setPromptMessage( "Continue" )
        
    def onExit(self, kwargs):
        self.placedobject = False  # Reset the placement state
        numentries = self.GetMultiparmEntries(kwargs)  # Retrieve the current number of entries
        self.multiparm.removeMultiParmInstance(numentries - 1)  # Remove the last multiparm entry
        self.lastIteration()  # Execute final cleanup actions

    def lastIteration(self):
        self.node.node("/obj/GRID_OBJ_PLACER/subnet1/attribwrangle5").parm("aux").set(0)
       
    def onMouseWheelEvent(self, kwargs):
        ui_event = kwargs["ui_event"]
        device = ui_event.device()
        scroll = device.mouseWheel()
        
        numentries = self.GetMultiparmEntries(kwargs)                         # Get current multiparm entries
        currentValue = self.node.parm("iId_%s" % numentries).evalAsInt()      # Retrieve current value
        # Update the parameter with the new value, ensuring it doesn't go below 0
        self.node.parm(("iId_%s" % numentries)).set(max(currentValue + scroll, 0))
       
    
    def onMenuAction(self, kwargs):
        menu_item = kwargs["menu_item"]    
        if menu_item == "sometoggle":   
            value = self.node.node("/obj/GRID_OBJ_PLACER/subnet1/attribwrangle5").parm("aux").eval()     # Retrieve the aux atributte
            # Comparing and setting the attribute.
            if value == 0:
                self.node.node("/obj/GRID_OBJ_PLACER/subnet1/attribwrangle5").parm("aux").set(1)         
            if value == 1
                self.node.node("/obj/GRID_OBJ_PLACER/subnet1/attribwrangle5").parm("aux").set(0)
        
        if menu_item == "sometoggle2":
            model_node = hou.node('/obj/GRID_OBJ_PLACER/Nodo')
            merge_node = hou.node('/obj/GRID_OBJ_PLACER/merge3')
            if model_node:
                return model_node

            # Creating a object merge SOP, in case you want to bring a specific SOP
            model_node = hou.node('/obj/GRID_OBJ_PLACER').createNode('object_merge', "Vecinitos")
            # Create a match size SOP, to lay the object on the center
            ms_node = hou.node('/obj/GRID_OBJ_PLACER').createNode('matchsize', "Vecinitos_MS")
            # Adjusting position
            ms_node.parm("justify_y").set(1)

            # Cerate a wrangle to modify ID  
            pw_node = hou.node('/obj/GRID_OBJ_PLACER').createNode('attribwrangle', "Vecinitos_PW")
            numero = 1
            pw_text = "i@id = {0}".format(self.moduleIndex) +  ";"          #  Set the current id with the number of inputs
            self.moduleIndex += 1
            pw_node.parm("snippet").set(pw_text)                            # Setting the code in the wrangle   

            #  Setting input for the new nodes
            ms_node.setInput(0, model_node)
            pw_node.setInput(0, ms_node)

            # Layout the nodes properly
            model_node.moveToGoodPosition()
            ms_node.moveToGoodPosition() 
            pw_node.moveToGoodPosition()

            #  Layout the children nodes
            list = hou.node('/obj/GRID_OBJ_PLACER').layoutChildren()

            # Connecting the wrangle to the merge node
            merge_node.setNextInput(pw_node)
          
        if menu_item == "sometoggle3":
            # Same procedure than before, but in this case instead of creating a Object Merge SOP, we create a File SOP
            model_node = hou.node('/obj/GRID_OBJ_PLACER/Nodo')
            merge_node = hou.node('/obj/GRID_OBJ_PLACER/merge3')
            if model_node:
                return model_node
            model_node = hou.node('/obj/GRID_OBJ_PLACER').createNode('file', "Vecinitos")
            ms_node = hou.node('/obj/GRID_OBJ_PLACER').createNode('matchsize', "Vecinitos_MS")
            ms_node.parm("justify_y").set(1)
            
            pw_node = hou.node('/obj/GRID_OBJ_PLACER').createNode('attribwrangle', "Vecinitos_PW")
            numero = 1
            pw_text = "i@id = {0}".format(self.moduleIndex) +  ";"
            self.moduleIndex += 1
            pw_node.parm("snippet").set(pw_text)             
            
            
            ms_node.setInput(0, model_node)
            pw_node.setInput(0, ms_node)
            
            model_node.moveToGoodPosition()
            ms_node.moveToGoodPosition() 
            pw_node.moveToGoodPosition() 
            
            merge_node.setNextInput(pw_node)
            
            list = hou.node('/obj/GRID_OBJ_PLACER').layoutChildren()
            
        if menu_item == "sometoggle4": 
            self.placedobject = False
            numentries = self.GetMultiparmEntries(kwargs)
            parameter = self.node.node("/obj/GRID_OBJ_PLACER/subnet1/attribwrangle5").parm("aux")
            self.multiparm.removeMultiParmInstance(numentries - 1)
            self.lastIteration()          
                    
        
    
    def onMouseEvent(self, kwargs):
        ui_event = kwargs["ui_event"]
        device = ui_event.device()
        # Ray cast
        origin, direction = ui_event.ray()
        # Stores the action that the user is doing with the mouse.
        reason = ui_event.reason()
        self.entries = self.GetMultiparmEntries(kwargs)

        activeBool = 0
        # Calling the GeometryUntersector, this will check if we hit something with the mouse
        gi = su.GeometryIntersector(self.collisiongeo, scene_viewer = self.scene_viewer)
        # Using the intersect function to check if we hitted something
        gi.intersect(origin, direction)
        
        if gi.prim_num >= 0:        # Check if the ray hits a primitive
        
            hitPos = gi.position                                                # Update the hitPos
            numentries = self.GetMultiparmEntries(kwargs)                                
            micolor = self.collisiongeo.prim(gi.prim_num).attribValue("Cd")     # Update the color of the current object besed on the collided primitive
            
                 
            if self.placedobject == False:
                # Place object at intersection point
                self.node.parmTuple("vPosition_%s" % numentries).set(hitPos)
                if micolor == (1.0, 1.0, 1.0):
                    micolor = self.node.parmTuple("vColor_%s" % (numentries - 1)).eval()
                    
                self.node.parmTuple("vColor_%s" % numentries).set(micolor)
                if (activeBool == 0): 
                        self.node.parmTuple("vNormal_%s" % numentries).set(gi.normal)
                
            
            if reason == hou.uiEventReason.Picked:
                # If we do a click, we create an object. Increment the number of entries
                self.node.parmTuple("vNormal_%s" % numentries).set(gi.normal)
                self.multiparm.set(numentries + 1)
                self.placedobject = False               
                
            if reason == hou.uiEventReason.Start:
              
                self.node.parmTuple("vNormal_%s" % numentries).set(gi.normal)
                self.node.parmTuple("vColor_%s" % numentries).set(micolor)
                self.placedpos = hitPos                
                self.placedobject = True 
                self.hitnormal = gi.normal

            if reason == hou.uiEventReason.Active:
                # If we enter here, we are holding one of the mouse buttons
                activeBool = 1;                
                if self.placedobject == True:                      
                    normalActive = gi.normal                   
                    pos = hou.hmath.intersectPlane(self.placedpos, gi.normal, origin, direction)  
                    scale = pos.distanceTo(self.placedpos)
                    self.node.parm("fScale_%s" % numentries).set(scale)                
               
            if reason == hou.uiEventReason.Changed:              
                self.multiparm.set(numentries + 1)
                self.placedobject = False    
                
            return False


def createViewerStateTemplate():
    state_typename = kwargs["type"].definition().sections()["DefaultState"].contents()
    state_label = "Pruebaass"
    state_cat = hou.sopNodeTypeCategory()

    template = hou.ViewerStateTemplate(state_typename, state_label, state_cat)
    template.bindFactory(State)
    template.bindIcon(kwargs["type"].icon())
    
    menu = hou.ViewerStateMenu('some_menu', 'menu_name')   

    # Create three toggles for the MLB  
    menu.addToggleItem("sometoggle", "Wireframe Holder", False)
    menu.addToggleItem("sometoggle2", "Custom Model OM", False)
    menu.addToggleItem("sometoggle3", "Custom Model FILE", False)

    template.bindMenu(menu)
  
    return template
