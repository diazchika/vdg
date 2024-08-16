import argparse

from vdg.core import *

def parse_args():
    parser = argparse.ArgumentParser(description="发布稿生成器。")
    parser.add_argument('--version', action='version', version=vdg.__version__)
    subparsers = parser.add_subparsers(dest='command', required=True)
    parser_new = subparsers.add_parser('new', help='生成新的发布稿模版 YAML。')
    parser_gen = subparsers.add_parser('gen', help='根据YAML在当前目录下生成发布稿。')
    parser_gen.add_argument('--path', type=str, help='YAML 配置文件路径。', default='./config.yml')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    if args.command == 'new':
        create_form()
    elif args.command == 'gen':
        generate_drafts(args.path)


if __name__ == "__main__":
    main()
