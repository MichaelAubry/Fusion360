#Mike Aubry (w/ true credit going to Sebastian Morales and Brian Ekins)
#Description - This Fusion 360 Script allows you to create a construction point where the center of mass is for 
# the top level component. This is especially useful for balancing applications.

import adsk.core, adsk.fusion, adsk.cam, traceback
app = adsk.core.Application.get()
if app:
    ui = app.userInterface

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # Get all components in the active design.
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        title = 'Create Center of Mass Point'
        
        
        if not design:
            ui.messageBox('No active Fusion design', title)
            return
        
        # Get the root component of the active design
        rootComp = design.rootComponent
        
        # Get physical properties from component (high accuracy)
        physicalProperties = rootComp.getPhysicalProperties(adsk.fusion.CalculationAccuracy.HighCalculationAccuracy)
        
        # Get center of mass from physical properties
        cog = physicalProperties.centerOfMass
        
        # Check to see if a base feature named "Center of Gravities" exists.
        baseFeature = rootComp.features.itemByName('Center of Gravities')
        if not baseFeature:
            # Create a new base feature.
            baseFeature = rootComp.features.baseFeatures.add()
            baseFeature.name = 'Center of Gravities'

            # Begin editing the base feature.
            baseFeature.startEdit()                
            
            # Create a construction point at the COG position.
            constructionPoints = rootComp.constructionPoints
            pointInput = constructionPoints.createInput()
            pointInput.setByPoint(cog)
            pointInput.targetBaseOrFormFeature = baseFeature
            constPoint = constructionPoints.add(pointInput)
            constPoint.name = 'Center of Gravity'
            
            # End the base feature edit.
            baseFeature.finishEdit()
        else:
            # Check that the "Center of Gravity construction point exists.
            cogPoint = rootComp.constructionPoints.itemByName('Center of Gravity')
            
            # Because of a problem with updating an existing point, this current deletes
            # the existing point so the code in the "else" is never executed.
            if cogPoint:
                cogPoint.deleteMe()
                cogPoint = None
            
            if not cogPoint:
                # Create the construction point.
                # Begin editing the base feature.
                baseFeature.startEdit()                
                
                # Create a construction point at the COG position.
                constructionPoints = rootComp.constructionPoints
                pointInput = constructionPoints.createInput()
                pointInput.setByPoint(cog)
                pointInput.targetBaseOrFormFeature = baseFeature
                constPoint = constructionPoints.add(pointInput)
                constPoint.name = 'Center of Gravity'
                
                # End the base feature edit.
                baseFeature.finishEdit()
            else:
                # Edit the existing construction point.
                pointDef = adsk.fusion.ConstructionPointPointDefinition.cast(cogPoint.definition)
                baseFeature.startEdit()                
                pointDef.pointEntity = cog
                baseFeature.finishEdit()
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
