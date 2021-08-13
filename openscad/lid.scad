$fn=64;

include <libs/BOSL/constants.scad>
use <libs/BOSL/shapes.scad>
use <libs/BOSL/transforms.scad>
use <libs/threads-scad/threads.scad>
use <libs/smooth-prim/smooth_prim.scad>

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

// Threads have 2mm thickness
// Thread spacing 1.2mm
// Single intersection point

module vial() {
        SmoothCylinder(10,20,3);

}

nippleConeH = 3.4;
nippleConeDia1 = 3.6;
nippleConeDia2 = 2.6;
nippleBodyH = 1.75;
nippleBodyOutDia = 2.9;
nippleInDia = 1.5;

module nipple() {
    up(nippleBodyH)
    difference() {
        union() {
            cyl(h=nippleConeH, d1=nippleConeDia1, d2=nippleConeDia2, align=V_UP);
            downcyl(h=nippleBodyH, d=nippleBodyOutDia);
        }
        down(nippleBodyH)cyl(h=nippleBodyH+nippleConeH, d=nippleInDia, align=V_UP);
    }
}

bigTubeNippleConeH = 3.4;
bigTubeNippleConeDia1 = 3.6;
bigTubeNippleConeDia2 = 2.6;
bigTubeNippleBodyH = 1.75;
bigTubeNippleBodyOutDia = 2.9;
bigTubeNippleInDia = 1.5;

module bigTubeNipple() {
    difference() {
        union() {
          cylinder(bigTubeNippleConeH, d1=bigTubeNippleConeDia1, d2=bigTubeNippleConeDia2, center=true);
          translate([0,0,-(bigTubeNippleConeH/2+bigTubeNippleBodyH/2)])cylinder(bigTubeNippleBodyH, d=bigTubeNippleBodyOutDia, center=true);
        }
        translate([0,0,-(bigTubeNippleBodyH/2)])cylinder((bigTubeNippleConeH+bigTubeNippleBodyH)*2, d=bigTubeNippleInDia, center=true);
    }
}

lilTubeNippleConeH = 3.4;
lilTubeNippleConeDia1 = 3.6;
lilTubeNippleConeDia2 = 2.6;
lilTubeNippleBodyH = 1.75;
lilTubeNippleBodyOutDia = 2.9;
lilTubeNippleInDia = 1.5;

module lilTubeNipple() {
    difference() {
        union() {
          cylinder(lilTubeNippleConeH, d1=lilTubeNippleConeDia1, d2=lilTubeNippleConeDia2, center=true);
          translate([0,0,-(lilTubeNippleConeH/2+lilTubeNippleBodyH/2)])cylinder(lilTubeNippleBodyH, d=lilTubeNippleBodyOutDia, center=true);
        }
        translate([0,0,-(lilTubeNippleBodyH/2)])cylinder(lilTubeNippleConeH+lilTubeNippleBodyH, d=lilTubeNippleInDia, center=true);
    }
}

lidDia = 32;
lidH = 12;
lidTopThickness = 2;
lidSideThickness = 1.5;
o2ProbeDia = 12;
phProbeDia = 12;

module lid() {
  union(){
    %SmoothCylinder(lidDia/2, lidH, 1);
    %translate([0,0,16])bigTubeNipple();}
    //HollowCylinder(lidDia/2, lidDia/2*0.9, lidH);
}

/*
- Rotation does not work currently... Not sure exactly why, need to dig into the smooth-prim library a bit more...
- Top=false also does not work...
*/
module HoleWithFillet(diameter, hole_depth, smooth_rad, top=true, position=[0,0,0], rotation=[0,0,0]) {
    if (top==true) {
        union() {
            difference() {
                SmoothHole(diameter/2, hole_depth, smooth_rad, position=position, rotation=rotation);
                translate(position+[0,0,-smooth_rad])rotate(rotation)cylinder(r=diameter/2+smooth_rad*2, hole_depth/2+smooth_rad, center=false);
            }
            translate(position)rotate(rotation)cylinder(r=diameter/2, hole_depth/2, center=false);
        }
    } else {
        // union() {
        //     difference() {
        //         SmoothHole(diameter/2, hole_depth, smooth_rad, position=position, rotation=rotation);
        //         translate(position+[0,0,-smooth_rad])rotate(rotation)cylinder(r=diameter/2+smooth_rad*2, hole_depth/2+smooth_rad, center=false);
        //     }
        //     translate(position+[0,0,hole_depth/2])rotate(rotation)cylinder(r=diameter/2, hole_depth/2, center=false);
        // }
    }
}

/* Same Deal...
- Rotation does not work currently... Not sure exactly why, need to dig into the smooth-prim library a bit more...
- Top=false also does not work...
*/
module HoleWithChamfer(diameter, hole_depth, smooth_rad, top=true, position=[0,0,0], rotation=[0,0,0]) {
    if (top==true) {
        union() {
            difference() {
                ChamferHole(diameter/2, hole_depth, smooth_rad, position=position, rotation=rotation);
                translate(position+[0,0,-smooth_rad])rotate(rotation)cylinder(r=diameter/2+smooth_rad*2, hole_depth/2+smooth_rad, center=false);
            }
            translate(position)rotate(rotation)cylinder(r=diameter/2, hole_depth/2, center=false);
        }
    } else {
        // union() {
        //     difference() {
        //         SmoothHole(diameter/2, hole_depth, smooth_rad, position=position, rotation=rotation);
        //         translate(position+[0,0,-smooth_rad])rotate(rotation)cylinder(r=diameter/2+smooth_rad*2, hole_depth/2+smooth_rad, center=false);
        //     }
        //     translate(position+[0,0,hole_depth/2])rotate(rotation)cylinder(r=diameter/2, hole_depth/2, center=false);
        // }
    }
}

module FilletCylinder(diameter, height, smooth_rad, top=true) {
    if (top==true) {
        translate([0,0,-smooth_rad]) {
            difference() {
                SmoothCylinder(diameter/2, height+smooth_rad, smooth_rad);
                cylinder(r=diameter/2, smooth_rad, center=false);
            }
        }
    } else {
        difference() {
            SmoothCylinder(diameter/2, height+smooth_rad, smooth_rad);
            translate([0,0,height])cylinder(r=diameter/2, smooth_rad, center=false);

        }
    }
}

module lidHoles() {
    union() {
        HoleWithFillet(o2ProbeDia, lidTopThickness, 0.5, top=true, position=[7,-3,0], rotation=[0,0,0]);
        HoleWithFillet(phProbeDia, lidTopThickness, 0.5, position=[-7,-3,0], rotation=[0,0,0]);
        translate([0,10,0])cylinder(lidTopThickness,d=bigTubeInDia);
        translate([-3,7,0])cylinder(lidTopThickness,d=bigTubeInDia);
        translate([3,7,0])cylinder(lidTopThickness,d=bigTubeInDia);
        translate([0,4,0])cylinder(lidTopThickness,d=bigTubeInDia);
        translate([3,-12,0])cylinder(lidTopThickness,d=bigTubeInDia);
        translate([-3,-12,0])cylinder(lidTopThickness,d=bigTubeInDia);
    }
}

// Need at least 6mm of space between every nipples center to center
module lidNipplesOld() {
    union() {
        translate([0,10,0])bigTubeNipple();
        translate([-3,7,0])bigTubeNipple();
        translate([3,7,0])bigTubeNipple();
        translate([0,4,0])bigTubeNipple();
        translate([3,-12,0])bigTubeNipple();
        translate([-3,-12,0])bigTubeNipple();
    }
}

module lidNipples() {
    //place_copies([[0,10,0],[-3.7.0],[3,7,0],[0,4,0],[3,-12,0],[-3,-12,0]]) nipple();
    place_copies([[0,10,0], [-3,7,0], [3,7,0], [0,4,0], [3,-12,0], [-3,-12,0]]) nipple();
}

//lid();
//testHoles();


difference(){
    FilletCylinder(lidDia, lidH, 1, top=true);
    translate([0,0,lidH-lidTopThickness])lidHoles();
    translate([0,0,-lidTopThickness])cylinder(lidH,d=lidDia-(lidSideThickness*2));
}
translate([0,0,lidH+bigTubeNippleBodyH+bigTubeNippleConeH/2])lidNipples();
