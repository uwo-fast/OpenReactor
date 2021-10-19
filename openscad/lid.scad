$fn=32;

include <libs/BOSL/constants.scad>
include <libs/threads-scad/threads.scad>
use <libs/BOSL/shapes.scad>
use <libs/BOSL/transforms.scad>
use <libs/threads-scad/threads.scad>
include <nipple.scad>

T=22.090;
Pitch=3.414;
Height=1.845;
Dia=19.960;

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



// All units in mm
releaseCylinderHeight=3;
releaseCylinderID=1.75;
releaseCylinderOD=3;
releaseCylinderConeHeight=8;
releaseBulbID=8;
releaseBulbOD=releaseBulbID+2;
releaseSmidge=0.5;



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



module release() {
  module bulb() {
    translate([0, 0, releaseCylinderHeight+releaseBulbID/2-releaseSmidge]) difference() {
      sphere(d=releaseBulbOD);
      sphere(d=releaseBulbID);
      translate([0, 0, releaseBulbOD/4]) cube([releaseBulbOD, releaseBulbOD, releaseBulbOD/2], center=true);
    }
  }
  translate([0,0,releaseCylinderHeight+releaseBulbID/2]){nipple();}
  translate([0,0,releaseCylinderHeight+releaseBulbID/2]){
    rotate(180,[0,1,0]){
      difference() {  
        union() {
          //cylinder(h=holderCylinderConeHeight, d2=holderCylinderOD, d1=holderCylinderOD+2, center=false);
          bulb();
          cylinder(h=releaseCylinderHeight, d=releaseCylinderOD, center=false);
        }
        cylinder(h=releaseCylinderHeight, d=releaseCylinderID, center=false);  
      }}}
        translate([0,-10,(releaseCylinderID)/2-8]){
                sphere(d=releaseBulbID-0.2);
                down((releaseBulbID)/2) cube([5,5,0.5],center=true);
        }
        //translate([0,0,-2]){cube([1/10*releaseBulbOD,releaseBulbID,.5],center=true);}
        //translate([0,0,-2]){cube([releaseBulbID,1/10*releaseBulbOD,.5],center=true);}
        //down(3-0.75)tube(h=3.25,od=releaseBulbOD,id=releaseBulbID);
        /*difference(){
        down(3-0.75)ScrewThread(releaseBulbOD, 3.25, pitch=0, tooth_angle=60, tolerance=0.1, tip_height=0, tooth_height=0, tip_min_fract=0);
        down(3-0.75)cyl(h=10,d=releaseBulbID);
        }*/
        difference(){
        down(11.5)tube(h=12,od=releaseBulbOD,id=releaseBulbID);
        down(1.5)rotate(90,[0,1,0]){cyl(h=releaseBulbOD,d=1);}
        down(1.5)rotate(90,[1,0,0]){cyl(h=releaseBulbOD,d=1);}
            
        }
        /*
 rotate(180,[0,1,0]){       
        translate([0,15,.75]){
            difference(){
                
                cyl(h=3.35,d=releaseBulbOD+1);
                mirror([0,1,0]){down(3-1.25)ScrewThread(releaseBulbOD+0.1, 3.25, pitch=0, tooth_angle=60, tolerance=0.1, tip_height=0, tooth_height=0, tip_min_fract=0);}
                cyl(h=4,d=releaseBulbID);
        }
        up(3.175/2)cube([1/10*releaseBulbOD,releaseBulbID,.175],center=true);
        up(3.175/2)cube([releaseBulbID,1/10*releaseBulbOD,.175],center=true);
        }
        }*/
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

    threadOD=22.090;
    lidOD=25;
    lidID=19.960;
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
        //cyl(h=nippleTotalH, d=4, align=V_UP);
        tube(h=nippleTotalH, od=lidOD*0.78, id=lidOD*0.68);
        nipple();
        linear_extrude(lidTopThickness/2) union() {
        move(x=(diaIO/4), y=(diaIO*0.95)) text(size=3, halign="center", valign="center", "+");
        move(x=-(diaIO/4), y=(diaIO*0.95)) text(size=3, halign="center", valign="center", "-");
        move(x=(diaIO*1.125)) text(size=3, halign="center", valign="center", "I");
        move(x=-(diaIO*1.125)) text(size=3, halign="center", valign="center", "O");
        move(x=(diaIO/4), y=-(diaIO)) text(size=2.5, halign="center", valign="center", "P");
        move(x=-(diaIO/4), y=-(diaIO)) text(size=2.5, halign="center", valign="center", "B");
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
            // zrot(-30) fwd(diaIO/2) cyl(h=bubblerHoleH, d1=4.5, d2=4.5);
            zrot(-30) fwd(diaIO/2) cyl(h=bubblerHoleH, d1=4.5, d2=6);
            cyl(h=lidTopThickness,d=nippleInDia);
    }

    // Below lid

    down(lidTopThickness/2) union() {
        nippleIn();
        tube(h=ringH, od=ringOD, id=ringID, align=V_DOWN);
        arc_of(d=diaIO, n=3, ea=120) nippleIn();
        left(diaIO/2) nippleOut();
        difference(){
        tube(h=lidH-lidTopThickness, od=lidOD, id=lidID, align=V_DOWN);
        down(lidH){
            AugerThread(threadOD,lidID,lidH-lidTopThickness,Pitch,tooth_angle=55,tolerance=0.2);
    }}
    }

}

//nippleOut();
//nippleIn();
//lid();
//holderCylinder();
release();
