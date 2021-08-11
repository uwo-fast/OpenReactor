$fn=32;
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

translate([10,0,0]){sphere(d=bigTubeNippleInDia+0.2);}