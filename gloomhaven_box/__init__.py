import typed_argparse as tap

from . import box


def main():
  tap.Parser(
      box.GloomhavenBoxArgs,
  ).bind(
      box.runner,
  ).run()
