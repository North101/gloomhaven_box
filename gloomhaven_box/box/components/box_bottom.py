import pysvg
from pysvg import Element, path, svg

from ...util import *
from ..args import GloomhavenBoxArgs


@register_svg()
class write_svg(RegisterSVGCallable[GloomhavenBoxArgs]):
  def __call__(self, args: GloomhavenBoxArgs):
    helper = Tab(args.tab, args.thickness, args.kerf)

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
                path.d.m(0, 0),
                m_center(
                    lambda w, h: v_slots(
                        width=args.thickness,
                        height=args.tab,
                        gap=args.tab,
                        max_height=d.height,
                        padding=0,
                        kerf=args.kerf,
                    ),
                    width=d.width,
                    height=d.height,
                ),
            ]),
        ) | args.cut),
        path(attrs=path.attrs(
            d=path.d([
                path.d.m(0, 0),
                m_center(
                    lambda w, h: path.d([
                        path.d.m(args.thickness, 0),
                        h_slots(
                            width=args.tab,
                            height=args.thickness,
                            gap=args.tab,
                            max_width=args.horizontal_dividier_width,
                            padding=0,
                            kerf=args.kerf,
                        ),
                    ]),
                    width=d.width + args.horizontal_dividier_width,
                    height=d.height,
                ),
            ]),
        ) | args.cut),
        path(attrs=path.attrs(
            d=path.d([
                path.d.m(0, 0),
                m_center(
                    lambda w, h: path.d([
                        path.d.m(-args.thickness, 0),
                        h_slots(
                            width=args.tab,
                            height=args.thickness,
                            gap=args.tab,
                            max_width=args.horizontal_dividier_width,
                            padding=0,
                            kerf=args.kerf,
                        ),
                    ]),
                    width=(d.width * 2) - args.horizontal_dividier_width,
                    height=d.height,
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

    return args.output / filename(__file__), s
