import pysvg
import pysvg_util as util
from pysvg import Element, path, svg

from ..args import GloomhavenBoxArgs


@util.register_svg()
class write_svg(util.SVGFile[GloomhavenBoxArgs]):
  def __call__(self, args: GloomhavenBoxArgs):
    length = args.length
    width = args.width

    horizontal = path.d([
        path.placeholder(lambda w, h: path.d.h((length - w) / 3)),
        util.h_tab(
            out=False,
            thickness=args.magnet.height,
            tab=args.magnet.length,
            kerf=args.kerf,
        ),
        path.placeholder(lambda w, h: path.d.h((length - w) / 3)),
        util.h_tab(
            out=False,
            thickness=args.thickness,
            tab=args.thickness,
            kerf=args.kerf,
        ),
        path.placeholder(lambda w, h: path.d.h((length - w) / 3)),
    ])
    vertical = util.v_pad(path.d.v(width), args.thickness)
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
