import aerosandbox as asb
from aerosandbox.geometry import airfoil
import aerosandbox.numpy as np
import matplotlib.pyplot as plt

def inch_to_meter(n: int) -> int:
    return n * 0.0254

def main():
    ClarkZ = asb.Airfoil("ClarkZ", airfoil.get_UIUC_coordinates(name='clarkz'))
    naca0005 = asb.Airfoil("naca0005")

    wing_span = inch_to_meter(44) # in
    wing_chord = inch_to_meter(8) # in

    Htail_span = inch_to_meter(15) # in
    Htail_chord = inch_to_meter(4) # in

    Vtail_span = inch_to_meter(5) # in
    Vtail_chord = inch_to_meter(4) # in

    cg_location = inch_to_meter(3)

    Lht = inch_to_meter(24)
    Lvt = inch_to_meter(24)

    z_tail = inch_to_meter(-0.5)


    wing = asb.Wing(
        xsecs= [
            asb.WingXSec(
                xyz_le=[0, 0, 0],
                chord=wing_chord,
                airfoil=ClarkZ
            ),
            asb.WingXSec(
                xyz_le=[0, wing_span/2, 0],
                chord=wing_chord,
                airfoil = ClarkZ
            )
        ],
        symmetric=True
    )

    Htail = asb.Wing(
        xsecs=[
            asb.WingXSec(
                xyz_le=[Lht, 0, z_tail],
                chord=Htail_chord,
                airfoil=naca0005
            ),
            asb.WingXSec(
                xyz_le=[Lht, Htail_span/2, z_tail],
                chord=Htail_chord,
                airfoil=naca0005
            )
        ],
        symmetric=True
    )

    Vtail = asb.Wing(
        xsecs=[
            asb.WingXSec(
                xyz_le=[Lvt, 0, z_tail],
                chord=Htail_chord,
                airfoil=naca0005
            ),
            asb.WingXSec(
                xyz_le=[Lvt, 0, z_tail + Vtail_span],
                chord=Vtail_chord,
                airfoil=naca0005
            )
        ],
    )

    plane = asb.Airplane(
        name = "Plane 1", 
        xyz_ref=[cg_location,0,0],
        wings=[wing, Htail, Vtail]
    )

    plane.draw_three_view()
   
    analysis = asb.VortexLatticeMethod(
        airplane=plane,
        op_point=asb.OperatingPoint(
            velocity=inch_to_meter(32*12), # m/s
            alpha=0, # deg
        )
        )

    data = analysis.run_with_stability_derivatives()
    analysis.draw()

    for key in data:
        print(f"{key}: {data[key]}")


if __name__ == '__main__':
    main()

