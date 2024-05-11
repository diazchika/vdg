import argparse

from vdg.core import *


def parse_args():
    parser = argparse.ArgumentParser(description="发布稿生成器。")
    subparsers = parser.add_subparsers(dest='command', required=True)

    parser_new = subparsers.add_parser('new', help='生成新的发布稿模版 YAML。vdg new -h')
    parser_new.add_argument('-p', '--path', type=str, help='YAML文件路径', default='./config.yaml')

    parser_gen = subparsers.add_parser('gen', help='根据YAML在当前目录下生成发布稿。vdg gen -h')
    parser_gen.add_argument('-p', '--path', type=str, help='YAML文件路径', default='./config.yaml')
    parser_gen.add_argument('-l', '--links', action='store_true', help='输出方便在主站粘贴的BT站点链接。')

    args = parser.parse_args()

    return args


def main():
    args = parse_args()

    if args.command == 'new':
        create_yaml_config(args.path)
    elif args.command == 'gen' and not args.links:
        generate_drafts(args.path)
    elif args.command == 'gen' and args.links:
        generate_links(args.path)


if __name__ == "__main__":
    main()
