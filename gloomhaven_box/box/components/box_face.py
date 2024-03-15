import pysvg
import pysvg_util as util
from pysvg import Element, path, svg

from ..args import GloomhavenBoxArgs


@util.register_svg()
class write_svg(util.SVGFile[GloomhavenBoxArgs]):
  def __call__(self, args: GloomhavenBoxArgs):
    helper = util.Tab(args.tab, args.thickness, args.kerf)

    length = args.dimension.length
    height = args.face_height

    horizontal = helper.h_tabs(True, length, False)
    vertical = helper.v_tabs(True, height, False)
    top_path = path.d.h(length)
    right_path = vertical
    bottom_path = -horizontal
    left_path = -vertical

    d = path.d([
        path.d.m(args.thickness, args.thickness),
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
                    thickness=args.thickness,
                    slot=args.tab / 2,
                    gap=args.tab,
                    max_height=args.vertical_divider_height,
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
