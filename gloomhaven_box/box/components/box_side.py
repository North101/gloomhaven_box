import enum

import pysvg
import pysvg_util as util
from pysvg import Element, path, svg

from ..args import GloomhavenBoxArgs


class Variant(enum.Enum):
  LEFT = enum.auto()
  RIGHT = enum.auto()


@util.register_svg_variants(Variant)
class write_svg(util.VariantSVGFile[GloomhavenBoxArgs, Variant]):
  def __call__(self, args: GloomhavenBoxArgs):
    helper = util.Tab(args.tab, args.thickness, args.kerf)

    height = args.face_height
    width = args.dimension.width

    horizontal = helper.h_tabs(False, height, False)
    vertical = util.v_pad(
        path.placeholder(lambda w, h: helper.v_tabs(True, width - h, True)),
        args.thickness,
    )
    top_path = path.d([
        path.d.h(args.slot_padding),
        path.d.h(args.thickness),
        horizontal,
    ])
    right_path = vertical
    bottom_path = -path.d([
        horizontal,
        path.d.h(args.thickness),
        path.d.h(args.slot_padding),
    ])
    left_path = -path.d.v(vertical.fill_placeholders.height)

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
                path.d.m(args.slot_padding + (args.kerf * 2), 0.001),
                util.v_slot(
                    thickness=args.thickness - (args.kerf * 2),
                    slot=d.height - 0.002,
                    kerf=0,
                )
            ]),
        ) | args.engrave | path.attrs(fill='red')),
    ]
    if self.variant is Variant.RIGHT:
      children.append(path(attrs=path.attrs(
          d=path.d([
              path.d.m(d.width - args.thickness - args.dimension.height, (d.height - args.thickness) / 2),
              util.h_slots(
                  thickness=args.thickness,
                  slot=args.tab / 2,
                  gap=args.tab,
                  max_width=args.dimension.height,
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
