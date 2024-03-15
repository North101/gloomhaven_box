import pysvg
import pysvg_util as util
from pysvg import Element, path, svg

from ..args import GloomhavenBoxArgs


@util.register_svg()
class write_svg(util.SVGFile[GloomhavenBoxArgs]):
  def __call__(self, args: GloomhavenBoxArgs):
    helper = util.Tab(args.tab, args.thickness, args.kerf)

    length = args.dimension.length
    width = args.dimension.width

    horizontal = helper.h_tabs(False, length, True)
    vertical = helper.v_tabs(False, width, True)
    top_path = horizontal
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
        ) | args.cut | path.attrs(fill='red')),
        path(attrs=path.attrs(
            d=path.d([
                path.d.m((d.width - args.thickness) / 2, 0),
                util.v_slots(
                    thickness=args.thickness,
                    slot=args.tab,
                    gap=args.tab,
                    max_height=d.height,
                    kerf=args.kerf,
                ),
            ]),
        ) | args.cut),
        path(attrs=path.attrs(
            d=path.d([
                path.d.m((d.width + args.thickness) / 2, (d.height - args.thickness) / 2),
                util.h_slots(
                    thickness=args.thickness,
                    slot=args.tab,
                    gap=args.tab,
                    max_width=args.horizontal_dividier_width,
                    kerf=args.kerf,
                ),
            ]),
        ) | args.cut),
        path(attrs=path.attrs(
            d=path.d([
                path.d.m(d.width - args.horizontal_dividier_width - args.thickness, (d.height - args.thickness) / 2),
                util.h_slots(
                    thickness=args.thickness,
                    slot=args.tab,
                    gap=args.tab,
                    max_width=args.horizontal_dividier_width,
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
