$fn=32;

tubeSmushSqueeze = 2.75;
tubeSmushDepth = 2;
heatSinkHeight = 8.25;
heatSinkBaseWidth = 9.40;
heatSinkWidth = 9.05;
heatSinkDepth = 6.09;
heatSinkFinThickness = 0.98;
heatSinkFinSeparation = 1.25;
bracketThickness = 1.25;

xBase = (heatSinkDepth*2)+tubeSmushSqueeze+heatSinkFinSeparation;
yBase = heatSinkHeight;
zBase = bracketThickness;
module base() {    
    cube([xBase,yBase,zBase]);
}

xSmush = tubeSmushSqueeze;
ySmush = heatSinkHeight;
zSmush = tubeSmushDepth;
module smusher() {
    cube([xSmush,ySmush,zSmush]);
}

module clip() {
    cube([heatSinkFinSeparation,yBase,heatSinkFinThickness+zBase]);
    translate([0,0,heatSinkFinThickness+zBase])
    cube([heatSinkFinSeparation+heatSinkFinThickness,yBase,heatSinkFinSeparation]);
}

module sides() {
    cube([xBase+(heatSinkFinSeparation*2),bracketThickness,zBase+hea]);
}

module halfAssem() {
    // Assemble all of the components of the part.
    base();

    translate([(xBase/2)-(xSmush/2),0,bracketThickness])
    smusher();

    translate([-heatSinkFinSeparation,0,0])
    clip();
    translate([heatSinkFinSeparation+xBase,0,0])
    mirror([1,0,0])
    clip();
}

halfAssem();
