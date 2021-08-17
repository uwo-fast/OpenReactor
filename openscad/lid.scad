$fn=32;

include <libs/BOSL/constants.scad>
use <libs/BOSL/shapes.scad>
use <libs/BOSL/transforms.scad>
use <libs/threads-scad/threads.scad>
include <nipple.scad>

bigTubeInDia = 2.5;
bigTubeOutDia = 4.5;
lilTubeInDia = 1.5875; // 1/16"
lilTubeOutDia = 4.7625; // 3/16"

vialNeckInDia = 22;
vialNeckOutDia = 25;
vialBodyInDia = 30;
vialBodyOutDia = 35;
vialTotalH = 95;
vialNeckH = 10;
vialBodyH = vialTotalH-vialNeckH;
vialBodySmoothRad = 3;

// All units in mm
holderCylinderHeight=50;
holderCylinderID=4;
holderCylinderOD=7;
holderCylinderConeHeight=8;
bulbID=14;
bulbOD=17;
smidge=0.5;



module holderCylinder() {
  module bulb() {
    translate([0, 0, holderCylinderHeight+bulbID/2-smidge]) difference() {
      sphere(d=bulbOD);
      sphere(d=bulbID);
      translate([0, 0, bulbOD/4]) cube([bulbOD, bulbOD, bulbOD/2], center=true);
    }
  }

  difference() {  
    union() {
      //cylinder(h=holderCylinderConeHeight, d2=holderCylinderOD, d1=holderCylinderOD+2, center=false);
      bulb();
      cylinder(h=holderCylinderHeight, d=holderCylinderOD, center=false);
    }
    cylinder(h=holderCylinderHeight, d=holderCylinderID, center=false);  
  }
}


// Threads have 2mm thickness
// Thread spacing 1.2mm
// Single intersection point

module vial() {
        SmoothCylinder(10,20,3);

}



module nippleIn() {
    totalH=5;
    od=5;
    id1=2.75;
    id2=nippleInDia;

    tube(h=totalH, od=od, id1=id1, id2=id2, align=V_DOWN);
}

module nippleOut() {
    totalH=35;
    od=5;
    od1=4.25;
    od2=od;
    id1=2.75;
    id2=nippleInDia;
    coneH=4;
    cylH=totalH-coneH;

    union() {
        tube(h=cylH, od=od, id1=id1, id2=id2, align=V_DOWN);
        down(cylH)tube(h=coneH, od1=od1, od2=od2, id=id1, align=V_DOWN);
    }
}

module lid() {

    lidOD=25;
    lidID=22;
    lidH=12;
    lidTopThickness=2;
    lidSideThickness=(lidOD-lidID)/2;

    lidHandleX=26;
    lidHandleY=10;
    bubblerHoleD1=3.8;
    bubblerHoleD2=4;
    bubblerHoleH=lidTopThickness;
    diaIO=10.5;

    ringOD=15.75;
    ringID=14.5;
    ringH=2.5;

    module handle() {
    difference() {
        cuboid([lidHandleX, lidHandleY, lidTopThickness], align=V_RIGHT, fillet=5, edges=EDGE_FR_RT+EDGE_BK_RT);
        right(22.5) cyl(h=2.5, d=3.25);
    }
}
    
    // Above lid
    up(lidTopThickness/2) union() {
        arc_of(d=diaIO, n=4, ea=180) nipple();
        cyl(h=nippleTotalH, d=4, align=V_UP);
        tube(h=nippleTotalH, od=lidOD*0.78, id=lidOD*0.68);
        linear_extrude(lidTopThickness/2) union() {
        move(x=(diaIO/4), y=(diaIO*0.95)) text(size=3, halign="center", valign="center", "+");
        move(x=-(diaIO/4), y=(diaIO*0.95)) text(size=3, halign="center", valign="center", "-");
        move(x=(diaIO*1.125)) text(size=3, halign="center", valign="center", "I");
        move(x=-(diaIO*1.125)) text(size=3, halign="center", valign="center", "O");
        move(x=(diaIO/4), y=-(diaIO)) text(size=2.5, halign="center", valign="center", "B");
        move(x=-(diaIO/4), y=-(diaIO)) text(size=2.5, halign="center", valign="center", "P");
        }
    }

    // Lid top, holes, sides, and threads
    difference() {
        union() {
            cyl(h=lidTopThickness, d=lidOD);
            //handle();
            //xflip() handle();
        }
            arc_of(d=diaIO, n=6, ea=360) cyl(h=lidTopThickness, d=nippleInDia);
            zrot(30) fwd(diaIO/2) cyl(h=bubblerHoleH, d1=bubblerHoleD1, d2=bubblerHoleD2);
            zrot(-30) fwd(diaIO/2) cyl(h=bubblerHoleH, d1=4.5, d2=6);
    }

    // Below lid
    down(lidTopThickness/2) union() {
        tube(h=ringH, od=ringOD, id=ringID, align=V_DOWN);
        arc_of(d=diaIO, n=3, ea=120) nippleIn();
        left(diaIO/2) nippleOut();
        tube(h=lidH-lidTopThickness, od=lidOD, id=lidID, align=V_DOWN);
    }
}

//nippleOut();
//nippleIn();
lid();
//holderCylinder();
