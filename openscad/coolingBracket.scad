$fn=32;
tubeRad=2.2;
Width=9.4;
Length=8.8;
Height=6.0;
tubeRadOut=3.0;
module bracket(){
    difference(){
        cube([Width+1.5,Length+1,Height+1.5],center=true);
        translate([0,0,0]){
            cube([Width,Length+1,Height+.2],center=true);
            cube([Width,Length,Height+1.6],center=true);
            }
}}
module side(){
    translate([0,0,0]){
        rotate(90,[1,0,0]){
            bracket();
            translate([0,Length,0]){bracket();}
}}}
translate([0,(Width-1.9)/2.1+tubeRad,0]){side();}
translate([0,-((Width-1.9)/2.1+tubeRad),0]){side();}
module tube(){
    translate([0,0,4.4]){
    difference(){
        cube([Width+1.5,1.9*tubeRad,18.6],center=true);
        //cylinder(h=Height,r=tubeRadOut,center=true);
        cylinder(h=20,r=tubeRad,center=true);

    }}}
tube();