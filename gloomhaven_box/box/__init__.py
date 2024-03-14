import pysvg_util as util

from .args import GloomhavenBoxArgs
from .components import *


def runner(args: GloomhavenBoxArgs):
  return util.write_svgs(util.generate_svgs(args))
