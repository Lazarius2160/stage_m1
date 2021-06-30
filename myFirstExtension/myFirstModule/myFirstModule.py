import os
import unittest
import logging
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin

#
# myFirstModule
#

class myFirstModule(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "myFirstModule"  
    self.parent.categories = ["Test"]  
    self.parent.dependencies = []  
    self.parent.contributors = ["Marine CAMBA - CENIR Paris Brain Institute, Sara FERNANDEZ VIDAL - CENIR Paris Brain Institute"]  
    self.parent.helpText = """
This module allows user to display in QuadBuffer Stereo mode in Slicer 4.11 using VTK 8"""
    # TODO: replace with organization, grant and thanks
    self.parent.acknowledgementText = """
This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc., Andras Lasso, PerkLab,
and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
"""



class myFirstModuleWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):

  def __init__(self, parent=None):
    """
    Called when the user opens the module the first time and the widget is initialized.
    """
    ScriptedLoadableModuleWidget.__init__(self, parent)
    VTKObservationMixin.__init__(self)  # needed for parameter node observation
    self.logic = None
    self._parameterNode = None
    self._updatingGUIFromParameterNode = False

  def setup(self):
    """
    Called when the user opens the module the first time and the widget is initialized.
    """
    ScriptedLoadableModuleWidget.setup(self)

    # Load widget from .ui file (created by Qt Designer).
    # Additional widgets can be instantiated manually and added to self.layout.
    uiWidget = slicer.util.loadUI(self.resourcePath('UI/myFirstModule.ui'))
    self.layout.addWidget(uiWidget)
    self.ui = slicer.util.childWidgetVariables(uiWidget)

    # Set scene in MRML widgets. Make sure that in Qt designer the top-level qMRMLWidget's
    # "mrmlSceneChanged(vtkMRMLScene*)" signal in is connected to each MRML widget's.
    # "setMRMLScene(vtkMRMLScene*)" slot.
    uiWidget.setMRMLScene(slicer.mrmlScene)
    self.setupQuadBufferMode()

  def setupQuadBufferMode(self):
    # layout name is used to create and identify the underlying view node and  should be set to a value that is not used in any of the layouts owned by the layout manager
    layoutName = "QuadBuffered window"
    layoutLabel = "QB"
    layoutColor = [0.5, 0.5, 1.0]
    # ownerNode manages this view instead of the layout manager (it can be any node in the scene)
    self.viewOwnerNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLScriptedModuleNode")

    # Create MRML node
    self.viewLogic = slicer.vtkMRMLViewLogic()
    self.viewLogic.SetMRMLScene(slicer.mrmlScene)
    self.viewNode = self.viewLogic.AddViewNode(layoutName)
    self.viewNode.SetLayoutLabel(layoutLabel)
    self.viewNode.SetLayoutColor(layoutColor)
    self.viewNode.SetAndObserveParentLayoutNodeID(self.viewOwnerNode.GetID())
    #self.viewNode.SetStereoType(5) #active le mode stereo sur l'image + dans le menu déroulant, cad comme si clique moi sur le bouton, 1=redblue, 4=interlaced

    # Create widget
    self.viewWidget = slicer.qMRMLThreeDWidget()
    # self.viewWidget.setQuadBufferStereoSupportEnabled(1)
    self.viewWidget.setMRMLScene(slicer.mrmlScene)
    self.viewWidget.setMRMLViewNode(self.viewNode)
    self.viewWidget.resize(800, 800)
    # self.viewWidget.setFormat(self.setStrereo(True)) #passe au format stereo, voit si bonne forme pour le code
    
    #Modify render window
    #attention a quelle render window on touche, normalement celle de viewWidget donc OK
    # self.renderWindowQuadBuffer = self.viewWidget.threeDView().renderWindow()
    # self.renderWindowQuadBuffer.SetStereoType(2) #1=crystaleyes, 2=red blue
    #self.renderWindowQuadBuffer.SetStereoCapableWindow(1)  #on off if the window is created in stereo capable mode
    #self.renderWindowQuadBuffer.SetStereoRender(1)  #on off for stereo rendering
    # comme on créer la fenetre a partir de view widget surement pas besoin de ces 3 lignes :
    #self.viewWidget.setRenderWindow(self.renderWindowQuadBuffer)
    #self.viewWidget.renderWindowQuadBuffer.StereoUpdate()
    #self.renderWindowQuadBuffer.Render()
    
    self.ui.EnableQuadBufferButton.connect('clicked(bool)', self.showQuadBufferWidget)


  def showQuadBufferWidget(self):
    self.viewWidget.show()
    print(self.viewNode.GetStereoType())


