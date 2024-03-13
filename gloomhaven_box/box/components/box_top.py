import enum

import pysvg
from pysvg import Element, path, svg

from ...util import *
from ..args import GloomhavenBoxArgs


class Variant(enum.Enum):
  TOP = enum.auto()
  MIDDLE = enum.auto()
  BOTTOM = enum.auto()


@register_svgs(Variant)
class write_svg(RegisterSVGCallable[GloomhavenBoxArgs]):
  def __init__(self, variant: Variant):
    self.variant = variant

  def __call__(self, args: GloomhavenBoxArgs):
    length = args.dimension.length
    width = args.dimension.width + (args.thickness * 2)

    horizontal = h_tabs(
        out=False,
        height=args.thickness,
        width=args.thickness,
        gap=(length / 3) - args.thickness,
        max_width=length,
        padding=0,
        kerf=0.07,
    )
    vertical = path.d.v(width)
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
    if self.variant is Variant.MIDDLE:
      children.append(
          path(attrs=path.attrs(
              transform=transforms.translate((length - args.board.length) / 2, (width - args.board.width) / 2),
              d=path.d([
                  path.d.h(args.board.length),
                  path.d.v(args.board.width),
                  -path.d.h(args.board.length),
                  -path.d.v(args.board.width),
              ]),
          ) | args.cut | path.attrs(fill='red')),
      )

    s = svg(
        attrs=svg.attrs(
            width=pysvg.length(d.width, 'mm'),
            height=pysvg.length(d.height, 'mm'),
            viewBox=(0, 0, d.width, d.height),
        ),
        children=children,
    )

    return args.output / filename(__file__, self.variant), s
