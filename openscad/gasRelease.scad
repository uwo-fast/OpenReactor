include <libs/BOSL/constants.scad>
use <libs/BOSL/shapes.scad>
use <libs/BOSL/transforms.scad>

$fn=64;
nippleConeH = 3.4;
nippleConeDia1 = 4; //3.6
nippleConeDia2 = 2.75; //2.6
nippleBodyH = 1.75;
nippleBodyOutDia = 2.9;
nippleInDia = 1.75; //1.5

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

difference() {
    union () {
        xrot(180) xspread(5, n=2) nipple();

        upcube([12,7,1]);
        difference() {
            downcube([12,7,nippleBodyH+nippleConeH]);
            downcube([10,5,nippleBodyH+nippleConeH]);
        }
    }
    xspread(5, n=2) cyl(h=5, d=nippleInDia);
}

module plug() {
    xrot(90)cube([10,10,20]);  
}

//plug();
/*
translate([0,0,bigTubeNippleBodyH]){
    rotate(180,[0,1,0]){
        bigTubeNipple();
}}
difference(){
translate([0,0,bigTubeNippleBodyH+bigTubeNippleConeH+bigTubeNippleBodyH]){
cylinder(h=5,d1=bigTubeNippleBodyOutDia,d2=bigTubeNippleConeDia1*2,center=true);}
translate([0,0,bigTubeNippleBodyH+bigTubeNippleConeH+bigTubeNippleBodyH]){
cylinder(h=5,d1=bigTubeNippleInDia,d2=bigTubeNippleConeDia1*2-bigTubeNippleInDia,center=true);
}}

translate([10,0,(bigTubeNippleInDia+0.2)/2]){sphere(d=bigTubeNippleInDia+0.2);}*/
