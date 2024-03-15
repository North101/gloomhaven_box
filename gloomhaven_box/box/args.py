import typed_argparse as tap
from pysvg_util import args, types


class GloomhavenBoxArgs(args.SVGArgs):
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
  slot_depth: float = tap.arg(
      type=types.PositiveFloat,
      default=1.25,
      help='slot depth (mm)',
  )
  slot_padding: float = tap.arg(
      type=types.PositiveFloat,
      default=1.0,
      help='slot padding (mm)',
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
    return self.dimension.height + self.dial.height

  @property
  def face_height(self):
    return self.vertical_divider_height + self.pad.height + self.board.height
