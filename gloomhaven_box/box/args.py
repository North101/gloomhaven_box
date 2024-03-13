import typed_argparse as tap

from .. import types, util


class GloomhavenBoxArgs(util.SVGArgs):
  dimension: types.Dimension = tap.arg(
      help='box dimensions [length] [width] [height] (mm)',
  )
  thickness: float = tap.arg(
      type=types.PositiveFloat,
      help='material thickness (mm)',
  )
  kerf: float = tap.arg(
      type=types.PositiveFloat,
      help='kerf (mm)',
  )
  tab: float = tap.arg(
      type=types.PositiveFloat,
      default=4.0,
      help='tab size (mm)',
  )
  board: types.Dimension = tap.arg(
      default=types.Dimension(
          length=types.PositiveFloat(145),
          width=types.PositiveFloat(95),
          height=types.PositiveFloat(2.3),
      ),
  )
  pad: types.Dimension = tap.arg(
      default=types.Dimension(
          length=types.PositiveFloat(140),
          width=types.PositiveFloat(114.3),
          height=types.PositiveFloat(3),
      ),
  )
  dial: types.Dimension = tap.arg(
      default=types.Dimension(
          length=types.PositiveFloat(136.0),
          width=types.PositiveFloat(70.0),
          height=types.PositiveFloat(4.25),
      ),
  )

  @property
  def horizontal_dividier_width(self):
    return (self.dimension.length - self.thickness) / 6

  @property
  def vertical_divider_height(self):
    return self.dimension.height + (self.dial.height * 2)

  @property
  def face_height(self):
    return self.vertical_divider_height + self.pad.height
