import pysvg
import pysvg_util as util
from pysvg import Element, path, svg

from ..args import GloomhavenBoxArgs


@util.register_svg()
class write_svg(util.RegisterSVGCallable[GloomhavenBoxArgs]):
  def __call__(self, args: GloomhavenBoxArgs):
    width = args.horizontal_dividier_width
    height = args.dimension.height

    top_path = path.d.h(width)
    right_path = path.d.v(height)
    bottom_path = -util.h_tabs(
        out=True,
        height=args.thickness,
        width=args.tab,
        gap=args.tab,
        max_width=width,
        padding=0,
        kerf=args.kerf,
    )
    left_path = -util.v_tabs(
        out=True,
        height=args.tab,
        width=args.thickness,
        gap=args.tab,
        max_height=height,
        padding=0,
        kerf=args.kerf,
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
