from viktor.parametrization import ViktorParametrization, NumberField, ColorField, Text
from viktor import ViktorController
from viktor.geometry import SquareBeam, Material, Color, Group, LinearPattern
from viktor.views import GeometryView, GeometryResult


class Parametrization(ViktorParametrization):
    intro_text = Text(
        "# 3D Parametric Building App 🏢\n"
        "In this app, the user can change the dimensions of the building, choose the amount of floors and a color for "
        "the facade. The app will generate a 3D building for the user as output."
    )
    width = NumberField('Width', min=0, default=30)
    length = NumberField('Length', min=0, default=30)
    number_floors = NumberField("how many floors", variant='slider', min=10, max=40, default=25)
    building_color = ColorField("Building Color", default=Color(221, 221, 221))


class Controller(ViktorController):
    label = "Parametric Building"
    parametrization = Parametrization

    @GeometryView("3D building", duration_guess=1, x_axis_to_right=True)
    def get_geometry(self, params, **kwargs):
        # Materials:
        glass = Material("Glass", color=Color(150, 150, 255))
        facade = Material("Concrete", color=params.building_color)

        floor_glass = SquareBeam(
            length_x=params.width,
            length_y=params.length,
            length_z=2,
            material=glass
        )
        floor_facade = SquareBeam(
            length_x=params.width + 1,
            length_y=params.length + 2,
            length_z=1,
            material=facade
        )
        floor_facade.translate((0, 0, 1.5))

        floor = Group([floor_glass, floor_facade])

        building = LinearPattern(floor, direction=[0, 0, 1], number_of_elements=params.number_floors, spacing=3)

        return GeometryResult(building)