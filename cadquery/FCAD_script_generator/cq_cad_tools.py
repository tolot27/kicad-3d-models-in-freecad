# -*- coding: utf8 -*-                                                      *
#* This are a FreeCAD & cadquery tools                                      *
#* to export generated models in STEP & VRML format.                        *
#*                                                                          *
#* cad tools functions                                                      *
#*   Copyright (c) 2015                                                     *
#* Maurice https://launchpad.net/~easyw                                     *
#*                                                                          *
#*   This program is free software; you can redistribute it and/or modify   *
#*   it under the terms of the GNU Lesser General Public License (LGPL)     *
#*   as published by the Free Software Foundation; either version 2 of      *
#*   the License, or (at your option) any later version.                    *
#*   for detail see the LICENCE text file.                                  *
#*                                                                          *
#*   This program is distributed in the hope that it will be useful,        *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of         *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          *
#*   GNU Library General Public License for more details.                   *
#*                                                                          *
#*   You should have received a copy of the GNU Library General Public      *
#*   License along with this program; if not, write to the Free Software    *
#*   Foundation, Inc.,                                                      *
#*   51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA           *
#*                                                                          *
#****************************************************************************



import FreeCAD, Draft, FreeCADGui
import ImportGui
from Gui.Command import *

###################################################################
# close_CQ_Example()  maui
#	Function to close CQ Example and restore "
#   "Report view" "Python console" "Combo View"
###################################################################
def close_CQ_Example(App, Gui):

    #close the example
    App.setActiveDocument("Ex000_Introduction")
    App.ActiveDocument=App.getDocument("Ex000_Introduction")
    Gui.ActiveDocument=Gui.getDocument("Ex000_Introduction")
    App.closeDocument("Ex000_Introduction")

    #Getting the main window will allow us to start setting things up the way we want
    mw = FreeCADGui.getMainWindow()

    #Adjust the docks as usual
    dockWidgets = mw.findChildren(QtGui.QDockWidget)
    for widget in dockWidgets:
        if (widget.objectName() == "Report view") or (widget.objectName() == "Python console") or (widget.objectName() == "Combo View"):
            widget.setVisible(True)
        if (widget.objectName()=="cqCodeView"):
            widget.setVisible(False)

    return 0


###################################################################
# FuseObjs_wColors()  maui
#	Function to fuse two objects together.
###################################################################
def FuseObjs_wColors(App, Gui,
                           docName, part1, part2):

    # Fuse two objects
    App.ActiveDocument=None
    Gui.ActiveDocument=None
    App.setActiveDocument(docName)
    App.ActiveDocument=App.getDocument(docName)
    Gui.ActiveDocument=Gui.getDocument(docName)
    App.activeDocument().addObject("Part::MultiFuse","Fusion")
    App.activeDocument().Fusion.Shapes = [App.ActiveDocument.getObject(part1), App.ActiveDocument.getObject(part2)]
    Gui.ActiveDocument.Fusion.ShapeColor=Gui.ActiveDocument.getObject(part1).ShapeColor
    Gui.ActiveDocument.Fusion.DisplayMode=Gui.ActiveDocument.getObject(part1).DisplayMode
    App.ActiveDocument.recompute()

    App.ActiveDocument.addObject('Part::Feature','Fusion').Shape=App.ActiveDocument.Fusion.Shape
    App.ActiveDocument.ActiveObject.Label=docName

    Gui.ActiveDocument.ActiveObject.ShapeColor=Gui.ActiveDocument.Fusion.ShapeColor
    Gui.ActiveDocument.ActiveObject.LineColor=Gui.ActiveDocument.Fusion.LineColor
    Gui.ActiveDocument.ActiveObject.PointColor=Gui.ActiveDocument.Fusion.PointColor
    Gui.ActiveDocument.ActiveObject.DiffuseColor=Gui.ActiveDocument.Fusion.DiffuseColor
    App.ActiveDocument.recompute()

    # Remove the part1 part2 objects
    App.getDocument(docName).removeObject(part1)
    App.getDocument(docName).removeObject(part2)

    # Remove the fusion itself
    App.getDocument(docName).removeObject("Fusion")

    return 0

###################################################################
# GetListOfObjects()  maui
#	Function to fuse two objects together.
###################################################################
def GetListOfObjects(App, docName):

    # Create list of objects, starting with object names
    objs=[]
    for obj in docName.Objects:
        # do what you want to automate
        objs.append(App.ActiveDocument.getObject(obj.Name))
        FreeCAD.Console.PrintMessage(obj.Name)
        FreeCAD.Console.PrintMessage(' objName\r\n')

    return objs

###################################################################
# Color_Objects()  maui
#	Function to color objects.
###################################################################
def Color_Objects(Gui,obj,color):

    FreeCAD.Console.PrintMessage(obj.Name+'\r\n')
    Gui.ActiveDocument.getObject(obj.Name).ShapeColor = color
    Gui.ActiveDocument.getObject(obj.Name).LineColor = color
    Gui.ActiveDocument.getObject(obj.Name).PointColor = color
    Gui.ActiveDocument.getObject(obj.Name).DiffuseColor = color
    #obj.Label=ModelName

    return 0


###################################################################
# restore_Main_Tools()  maui
#	Function to restore
#   "Report view" "Python console" "Combo View"
###################################################################
def restore_Main_Tools():

    #Getting the main window will allow us to start setting things up the way we want
    mw = FreeCADGui.getMainWindow()

    #Adjust the docks as usual
    dockWidgets = mw.findChildren(QtGui.QDockWidget)
    for widget in dockWidgets:
        if (widget.objectName() == "Report view") or (widget.objectName() == "Python console") or (widget.objectName() == "Combo View"):
            widget.setVisible(True)
        if (widget.objectName()=="cqCodeView"):
            widget.setVisible(False)

    return 0


###################################################################
# z_RotateObject()  maui
#	Function to z-rotate an object
#
###################################################################
def z_RotateObject(doc, rot):

    # z-Rotate
    FreeCAD.getDocument(doc.Name).getObject("Fusion001").Placement = FreeCAD.Placement(FreeCAD.Vector(0,0,0),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),rot))

    return 0


###################################################################
# exportSTEP()  maui
#	Function to Export to STEP
#
###################################################################
def exportSTEP(doc,modelName, dir):

    ## Export to STEP
    ## Get cwd

    outdir=os.path.dirname(os.path.realpath(__file__))+dir
    FreeCAD.Console.PrintMessage('\r\n'+outdir)
    StepFileName=outdir+'/'+modelName+'.step'
    objs=[]
    # objs=GetListOfObjects(FreeCAD, doc)
    objs.append(FreeCAD.getDocument(doc.Name).getObject("Fusion001"))
    import ImportGui
    FreeCAD.Console.PrintMessage('\r\n'+StepFileName)
    # FreeCAD.Console.PrintMessage(objs)
    FreeCAD.Console.PrintMessage('\r\n'+outdir)
    ImportGui.export(objs,StepFileName)

    return 0

###################################################################
# exportVRML()  maui
#	Function to Export to VRML
#
###################################################################
def exportVRML(doc,modelName,scale,dir):

    ## Export to VRML scaled 1/2.54
    #VrmlFileName='.//'+doc.Label+'.wrl'
    outdir=os.path.dirname(os.path.realpath(__file__))+dir
    FreeCAD.Console.PrintMessage('\r\n'+outdir)
    VrmlFileName=outdir+'/'+modelName+'.wrl'
    StepFileName=outdir+'/'+modelName+'.step'
    objs=[]
    # objs=GetListOfObjects(FreeCAD, doc)
    objs.append(FreeCAD.getDocument(doc.Name).getObject("Fusion001"))
    FreeCAD.ActiveDocument.addObject('Part::Feature','Vrml_model').Shape=objs[0].Shape
    FreeCAD.ActiveDocument.ActiveObject.Label='Vrml_model'
    FreeCADGui.ActiveDocument.ActiveObject.ShapeColor=FreeCADGui.getDocument(doc.Name).getObject(objs[0].Name).ShapeColor
    FreeCADGui.ActiveDocument.ActiveObject.LineColor=FreeCADGui.getDocument(doc.Name).getObject(objs[0].Name).LineColor
    FreeCADGui.ActiveDocument.ActiveObject.PointColor=FreeCADGui.getDocument(doc.Name).getObject(objs[0].Name).PointColor
    FreeCADGui.ActiveDocument.ActiveObject.DiffuseColor=FreeCADGui.getDocument(doc.Name).getObject(objs[0].Name).DiffuseColor
    FreeCAD.ActiveDocument.recompute()
    newObj=FreeCAD.getDocument(doc.Name).getObject('Vrml_model')
    #scale to export vrml  start
    Draft.scale(newObj,delta=FreeCAD.Vector(scale,scale,scale),center=FreeCAD.Vector(0,0,0),legacy=True)

    FreeCAD.activeDocument().recompute()
    #we need to remove object to export only scaled model
    FreeCAD.getDocument(doc.Name).removeObject(objs[0].Name)
    __objs__=[]
    __objs__.append(FreeCAD.getDocument(doc.Name).getObject("Vrml_model"))
    FreeCADGui.export(__objs__,VrmlFileName)
    FreeCAD.activeDocument().recompute()

    #restoring step module
    import ImportGui
    ImportGui.insert(StepFileName,doc.Name)

    FreeCAD.Console.PrintMessage(FreeCAD.ActiveDocument.ActiveObject.Label+" exported and scaled to Vrml\r\n")
    del __objs__

    return 0

###################################################################
# saveFCdoc()  maui
#	Function to save in Native FreeCAD format the doc
#
###################################################################
def saveFCdoc(App, Gui, doc, modelName,dir):

    ## Save to disk in native format
    App.ActiveDocument=None
    Gui.ActiveDocument=None
    App.setActiveDocument(doc.Name)
    App.ActiveDocument=App.getDocument(doc.Name)
    Gui.ActiveDocument=Gui.getDocument(doc.Name)

    outdir=os.path.dirname(os.path.realpath(__file__))+dir
    FreeCAD.Console.PrintMessage('\r\n'+outdir)
    FCName=outdir+'/'+modelName+'.FCStd'
    App.getDocument(doc.Name).saveAs(FCName)
    App.ActiveDocument.recompute()

    App.getDocument(doc.Name).Label = doc.Name
    Gui.SendMsgToActiveView("Save")
    App.getDocument(doc.Name).save()

    return 0