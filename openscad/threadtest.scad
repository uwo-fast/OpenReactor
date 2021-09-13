use <libs/threads-scad/threads.scad>
T=22.090;
Pitch=3.414;
Height=1.845;
Dia=19.960;


module lid(){
    
        difference(){
            linear_extrude(12){
                circle(d=25);}
            AugerThread(T,Dia,8,Pitch,tooth_angle=55,tolerance=0.2);
}}
lid();


//AugerThread(T,Dia,6,Pitch,tooth_angle=55,tolerance=0.2);