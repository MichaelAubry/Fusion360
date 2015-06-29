#Author-Michael Aubry
#Description-This script outputs a spiraling fibinacci sequence onto a Fusion 360 sketch

import adsk.core, adsk.fusion

app= adsk.core.Application.get()
design = app.activeProduct
ui = app.userInterface

#**Default User Inputs**
steps = "5 cm"     #How many steps of Fibonacci would you like to plot?
                    #(Note, while the steps variable should be unitless, right now our API can't handle unitless number. 
                    #cm are the absolute units we use on the API side.)
length = "3 cm"     #How long is the first segment? (cm)

input = steps
createInput = ui.inputBox('Enter Steps', 'Steps', input)
if createInput[0]:
                (input, isCancelled) = createInput
                unitsMgr = design.unitsManager
                realSteps = unitsMgr.evaluateExpression(input, unitsMgr.defaultLengthUnits)
                
input = length
createInput = ui.inputBox('Enter Length', 'Length', input)
if createInput[0]:
                (input, isCancelled) = createInput
                realLength = unitsMgr.evaluateExpression(input, unitsMgr.defaultLengthUnits)

#Get root component
rootComp = design.rootComponent
#Create a new sketch on XY plane
sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)

# Create an object collection for the points.
points = adsk.core.ObjectCollection.create()

# R = total steps to be run thru the For loop
R = int(realSteps - 2)

#starting x and y coordiantes
x = 0
y = 0

#Create 1st coordinate
points.add(adsk.core.Point3D.create(x,y,0))

#Starting Loft Profile Diameter
loftProfile1 = realLength/8

#starting values for sequence
fib = 1
fib1 = 1

#Create 2nd coordinate
x = 1 * realLength
points.add(adsk.core.Point3D.create(x,y,0))
ui.messageBox('x: ' + str(x))

#bins for shifting x and y coordinates
Bin1 = range(0,R,4)
Bin2 = range(1,R,4)
Bin3 = range(2,R,4)
Bin4 = range(3,R,4)
BinLoft = range(0,R)

for i in range(R):
    fib2 = fib + fib1
    fib = fib1
    fib1 = fib2
    fibLength = fib*realLength #adds the scalar component to coordinates
    #ui.messageBox('fiblength: ' + str(fibLength))

    if i in Bin1:
        x = x
        y = y + fibLength
        points.add(adsk.core.Point3D.create(x,y,0))
    if i in Bin2:
        x = x - fibLength
        y = y
        points.add(adsk.core.Point3D.create(x,y,0))
    if i in Bin3:
        x = x
        y = y - fibLength
        points.add(adsk.core.Point3D.create(x,y,0))
    if i in Bin4:
        x = x + fibLength
        y = y
        points.add(adsk.core.Point3D.create(x,y,0))
    if i in BinLoft: 
        loftProfile2 = fibLength/8 #Ending Loft Profile Diameter

# Create the spline.
sketch.sketchCurves.sketchFittedSplines.add(points)

# Create the Starting Loft Profile

spline1 = sketch.sketchCurves.sketchFittedSplines.item(0)

planeInput = rootComp.constructionPlanes.createInput() # you could also specify the occurrence in the parameter list
planeInput.setByDistanceOnPath(spline1, adsk.core.ValueInput.createByReal(0))
plane1 = rootComp.constructionPlanes.add(planeInput)

sketch1 = rootComp.sketches.add(plane1)
circles = sketch1.sketchCurves.sketchCircles
circle1 = circles.addByCenterRadius(adsk.core.Point3D.create(0, 0, 0), loftProfile1)

# Create the End Loft Sketch Profile
planeInput.setByDistanceOnPath(spline1, adsk.core.ValueInput.createByReal(1))
plane2 = rootComp.constructionPlanes.add(planeInput)
sketch2 = rootComp.sketches.add(plane2)

circles = sketch2.sketchCurves.sketchCircles
skPosition = sketch2.modelToSketchSpace(spline1.endSketchPoint.geometry)
circle2 = circles.addByCenterRadius(skPosition, loftProfile2) 
