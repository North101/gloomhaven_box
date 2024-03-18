import pysvg
import pysvg_util as util
from pysvg import Element, path, svg

from ..args import GloomhavenBoxArgs


@util.register_svg()
class write_svg(util.SVGFile[GloomhavenBoxArgs]):
  def __call__(self, args: GloomhavenBoxArgs):
    helper = util.Tab(args.tab, args.thickness, args.kerf)

    length = args.length
    width = args.width

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

    print((args.vertical_divider_width + (args.thickness * 2) - args.thickness) / 2)
    print()
    children: list[Element | str] = [
        path(attrs=path.attrs(
            d=d,
        ) | args.cut | path.attrs(fill='red')),
        # box_v_divider
        path(attrs=path.attrs(
            d=util.m_align(
                align=util.Align.BOTTOM | util.Align.CENTER_H,
                parent=d,
                item=util.v_slots(
                    thickness=args.thickness,
                    slot=args.tab,
                    gap=args.tab,
                    max_height=args.vertical_divider_width,
                    kerf=0,
                    padding=args.thickness,
                ),
            ),
        ) | args.cut),
        # box_h_divider:middle
        path(attrs=path.attrs(
            d=path.d([
                path.d.m(
                    x=(d.width + args.thickness) / 2,
                    y=(
                        ((args.vertical_divider_width + (args.thickness * 2) - args.thickness) / 2) +
                        (d.height - (args.vertical_divider_width + (args.thickness * 2)))
                    ),
                ),
                util.h_slots(
                    thickness=args.thickness,
                    slot=args.tab,
                    gap=args.tab,
                    max_width=args.horizontal_dividier_width,
                    kerf=args.kerf,
                ),
            ]),
        ) | args.cut),
        # box_h_divider:right
        path(attrs=path.attrs(
            d=path.d([
                path.d.m(
                    x=d.width - args.horizontal_dividier_width - args.thickness,
                    y=(
                        ((args.vertical_divider_width + (args.thickness * 2) - args.thickness) / 2) +
                        (d.height - (args.vertical_divider_width + (args.thickness * 2)))
                    ),
                ),
                util.h_slots(
                    thickness=args.thickness,
                    slot=args.tab,
                    gap=args.tab,
                    max_width=args.horizontal_dividier_width,
                    kerf=args.kerf,
                ),
            ]),
        ) | args.cut),
        # box_h_back_middle_divider
        path(attrs=path.attrs(
            d=path.d([
                path.d.m(
                    x=(d.width - args.horizontal_middle_dividier_width) / 2,
                    y=d.height - (args.vertical_divider_width + (args.thickness * 2)),
                ),
                util.h_slots(
                    thickness=args.thickness,
                    slot=args.tab,
                    gap=args.tab,
                    max_width=args.horizontal_middle_dividier_width,
                    kerf=args.kerf,
                ),
            ]),
        ) | args.cut),
        # box_h_back_side_divider:left
        path(attrs=path.attrs(
            d=path.d([
                path.d.m(
                    x=args.thickness,
                    y=d.height - (args.vertical_divider_width + (args.thickness * 2)),
                ),
                util.h_slots(
                    thickness=args.thickness,
                    slot=args.tab,
                    gap=args.tab,
                    max_width=args.horizontal_dividier_width,
                    kerf=args.kerf,
                ),
            ]),
        ) | args.cut),
        # box_h_back_side_divider:right
        path(attrs=path.attrs(
            d=path.d([
                path.d.m(
                    x=d.width - (args.horizontal_dividier_width + args.thickness),
                    y=d.height - (args.vertical_divider_width + (args.thickness * 2)),
                ),
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
