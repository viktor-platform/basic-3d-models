import viktor as vkt


class Parametrization(vkt.ViktorParametrization):
    intro_text = vkt.Text(
        "# 3D Parametric Building App 🏢\n"
        "In this app, the user can change the dimensions of the building, choose the amount of floors and a color for "
        "the facade. The app will generate a 3D building for the user as output."
    )
    width = vkt.NumberField('Width', min=0, default=30)
    length = vkt.NumberField('Length', min=0, default=30)
    number_floors = vkt.NumberField("how many floors", variant='slider', min=10, max=40, default=25)
    building_color = vkt.ColorField("Building Color", default=vkt.Color(221, 221, 221))


class Controller(vkt.ViktorController):
    label = "Parametric Building"
    parametrization = Parametrization

    @vkt.GeometryView("3D building", duration_guess=1, x_axis_to_right=True)
    def get_geometry(self, params, **kwargs):
        # Materials:
        glass = vkt.Material("Glass", color=vkt.Color(150, 150, 255))
        facade = vkt.Material("Concrete", color=params.building_color)

        floor_glass = vkt.SquareBeam(
            length_x=params.width,
            length_y=params.length,
            length_z=2,
            material=glass
        )
        floor_facade = vkt.SquareBeam(
            length_x=params.width + 1,
            length_y=params.length + 2,
            length_z=1,
            material=facade
        )
        floor_facade.translate((0, 0, 1.5))

        floor = vkt.Group([floor_glass, floor_facade])

        building = vkt.LinearPattern(floor, direction=[0, 0, 1], number_of_elements=params.number_floors, spacing=3)

        return vkt.GeometryResult(building)