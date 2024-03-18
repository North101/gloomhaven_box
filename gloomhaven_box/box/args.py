from functools import cached_property

import typed_argparse as tap
from pysvg_util import args, types


class GloomhavenBoxArgs(args.SVGArgs):
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
  magnet: types.Dimension = tap.arg()
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
  dia_top: types.Dimension = tap.arg(
      default=types.Dimension(
          length=types.PositiveFloat(136.0),
          width=types.PositiveFloat(70.0),
          height=types.PositiveFloat(4.05),
      ),
  )
  dial_bottom: types.Dimension = tap.arg(
      default=types.Dimension(
          length=types.PositiveFloat(136.0),
          width=types.PositiveFloat(70.0),
          height=types.PositiveFloat(2.05),
      ),
  )
  card: types.Dimension = tap.arg(
      default=types.Dimension(
          length=types.PositiveFloat(68.0),
          width=types.PositiveFloat(93.0),
          height=types.PositiveFloat(19),
      ),
  )
  mini_card: types.Dimension = tap.arg(
      default=types.Dimension(
          length=types.PositiveFloat(70.0),
          width=types.PositiveFloat(47.0),
          height=types.PositiveFloat(19),
      ),
  )

  @cached_property
  def length(self):
    board = self.board.length
    pad = self.pad.length
    card = (self.card.length * 2) + self.thickness
    mini_card = (self.card.length * 2) + self.thickness
    return max(board, pad, card, mini_card)

  @cached_property
  def width(self):
    board = self.board.width
    pad = self.pad.width
    card = self.card.width + self.thickness
    mini_card = (self.mini_card.width * 2) + (self.thickness * 2)
    return max(board, pad, card, mini_card)

  @cached_property
  def height(self):
    return max(self.card.height, self.mini_card.height)

  @cached_property
  def horizontal_dividier_width(self):
    return (self.length - self.thickness) / 6

  @cached_property
  def horizontal_middle_dividier_width(self):
    return (self.horizontal_dividier_width * 2) + self.thickness

  @cached_property
  def horizontal_divider_height(self):
    return self.height

  @cached_property
  def vertical_divider_width(self):
    card = self.card.width
    mini_card = (self.mini_card.width * 2) + self.thickness
    return max(card, mini_card)

  @cached_property
  def vertical_divider_height(self):
    return self.horizontal_divider_height + self.dial_bottom.height + self.dia_top.height

  @cached_property
  def face_height(self):
    return self.vertical_divider_height + self.pad.height + self.board.height
