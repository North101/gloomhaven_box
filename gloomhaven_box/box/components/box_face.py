import enum

import pysvg
import pysvg_util as util
from pysvg import Element, path, svg

from ..args import GloomhavenBoxArgs


class Variants(enum.Enum):
  TOP = enum.auto()
  BOTTOM = enum.auto()


@util.register_svg_variants(Variants)
class write_svg(util.VariantSVGFile[GloomhavenBoxArgs, Variants]):
  def __call__(self, args: GloomhavenBoxArgs):
    helper = util.Tab(args.tab, args.thickness, args.kerf)

    length = args.length
    height = args.face_height

    horizontal = helper.h_tabs(True, length, False)
    vertical = helper.v_tabs(True, height, False)
    top_path = path.d([
        path.d.h(args.thickness),
        util.h_tab(
            out=False,
            thickness=args.magnet.height,
            tab=args.magnet.length,
            kerf=args.kerf,
        ),
        path.placeholder(
            lambda w, h: path.d.h(length - w),
        ),
        util.h_tab(
            out=False,
            thickness=args.thickness,
            tab=args.thickness,
            kerf=args.kerf,
        ),
        path.d.h(args.thickness),
    ])
    right_path = vertical
    bottom_path = -horizontal
    left_path = -vertical

    d = path.d([
        path.d.m(args.thickness, 0),
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
    if self.variant == Variants.BOTTOM:
      children.append(path(attrs=path.attrs(
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
      ) | args.cut))

    s = svg(
        attrs=svg.attrs(
            width=pysvg.length(d.width, 'mm'),
            height=pysvg.length(d.height, 'mm'),
            viewBox=(0, 0, d.width, d.height),
        ),
        children=children,
    )

    return args.output / util.filename(__file__, self.variant), s
