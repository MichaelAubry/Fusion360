#Author-Michael Aubry
#Description-This script outputs a spiraling fibinacci sequence onto a Fusion 360 sketch

import adsk.core, adsk.fusion

app= adsk.core.Application.get()
design = app.activeProduct
ui = app.userInterface;

#**User Inputs**
Steps = 15  #How many steps of Fibonacci would you like to plot?
Length = 2  #How long is the first segment? (cm)

#Get root component
rootComp = design.rootComponent
#Create a new sketch on XY plane
sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)

# Create an object collection for the points.
points = adsk.core.ObjectCollection.create()

# R = total steps to be run thru the For loop
R = Steps - 2

#starting x and y coordiantes
x = 0
y = 0

#Create 1st coordinate
points.add(adsk.core.Point3D.create(x,y,0))

#starting values for sequence
fib = 1
fib1 = 1

#1st fib number
#print str(fib)

#Create 2nd coordinate
x = 1 * Length
points.add(adsk.core.Point3D.create(x,y,0))

#bins for shifting x and y coordinates
Bin1 = range(0,R,4)
Bin2 = range(1,R,4)
Bin3 = range(2,R,4)
Bin4 = range(3,R,4)

for i in range(R):
    fib2 = fib + fib1
    fib = fib1
    fib1 = fib2
    fibLength = fib*Length #adds the scalar component to  coordinates

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

# Create the spline.
sketch.sketchCurves.sketchFittedSplines.add(points)
