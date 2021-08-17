include <libs/BOSL/constants.scad>
use <libs/BOSL/shapes.scad>
use <libs/BOSL/transforms.scad>

nippleConeH = 3.0; //3.4
nippleConeDia1 = 4; //3.6
nippleConeDia2 = 2.75; //2.6
nippleBodyH = 1.75;
nippleTotalH = nippleConeH+nippleBodyH;
nippleBodyOutDia = 3.0;
nippleInDia = 1.75; //1.5

module nipple() {
    up(nippleBodyH)
    difference() {
        union() {
            cyl(h=nippleConeH, d1=nippleConeDia1, d2=nippleConeDia2, align=V_UP);
            downcyl(h=nippleBodyH, d=nippleBodyOutDia);
        }
        down(nippleBodyH)cyl(h=nippleTotalH, d=nippleInDia, align=V_UP);
    }
}

//nipple();
