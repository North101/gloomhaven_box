import pysvg
import pysvg_util as util
from pysvg import Element, path, svg

from ..args import GloomhavenBoxArgs


@util.register_svg()
class write_svg(util.RegisterSVGCallable[GloomhavenBoxArgs]):
  def __call__(self, args: GloomhavenBoxArgs):
    helper = util.Tab(args.tab, args.thickness, args.kerf)

    length = args.dimension.length
    height = args.face_height

    horizontal = helper.h_tabs(True, length, True)
    vertical = helper.v_tabs(False, height, False)
    top_path = util.h_tabs(
        out=False,
        height=args.thickness,
        width=args.thickness,
        gap=(length / 3) - args.thickness,
        max_width=length,
        padding=args.thickness,
        kerf=0.07,
    )
    right_path = vertical
    bottom_path = -horizontal
    left_path = -vertical

    d = path.d([
        path.d.m(0, 0),
        top_path,
        right_path,
        bottom_path,
        left_path,
    ])

    children: list[Element | str] = [
        path(attrs=path.attrs(
            d=d,
        ) | args.cut),
        path(attrs=path.attrs(
            d=path.d([
                path.d.m((d.width - args.thickness) / 2, d.height - args.thickness - args.vertical_divider_height),
                util.v_slots(
                    width=args.thickness,
                    height=args.tab,
                    gap=args.tab,
                    max_height=args.vertical_divider_height,
                    padding=0,
                    kerf=args.kerf,
                ),
            ]),
        ) | args.cut),
    ]

    s = svg(
        attrs=svg.attrs(
            width=pysvg.length(d.width, 'mm'),
            height=pysvg.length(d.height, 'mm'),
            viewBox=(0, 0, d.width, d.height),
        ),
        children=children,
    )

    return args.output / util.filename(__file__), s
