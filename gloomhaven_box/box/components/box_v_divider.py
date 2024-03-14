import pysvg
import pysvg_util as util
from pysvg import Element, path, svg

from ..args import GloomhavenBoxArgs


@util.register_svg()
class write_svg(util.RegisterSVGCallable[GloomhavenBoxArgs]):
  def __call__(self, args: GloomhavenBoxArgs):
    height = args.vertical_divider_height
    width = args.dimension.width

    top_path = util.h_tabs(
        out=True,
        height=args.thickness,
        width=args.tab,
        gap=args.tab,
        max_width=height,
        padding=0,
        kerf=args.kerf,
    )
    right_path = util.v_tabs(
        out=True,
        height=args.tab,
        width=args.thickness,
        gap=args.tab,
        max_height=width,
        padding=0,
        kerf=args.kerf,
    )
    bottom_path = -top_path
    left_path = -util.v_center(
        segment=lambda _: path.d([
            -path.d.h(args.dial.height),
            path.d.v(args.dial.width),
            path.d.h(args.dial.height),
        ]),
        height=width,
    )

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
                path.d.m(d.width - args.thickness - args.dimension.height, (d.height - args.thickness) / 2),
                util.h_slots(
                    width=args.tab,
                    height=args.thickness,
                    gap=args.tab,
                    max_width=args.dimension.height,
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
