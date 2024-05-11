import argparse

from vdg.core import generate_drafts, create_yaml_config


def parse_args():
    parser = argparse.ArgumentParser(description="发布稿生成器。")
    subparsers = parser.add_subparsers(dest='command', required=True)

    parser_new = subparsers.add_parser('new', help='生成新的发布稿模版 YAML。默认在当前目录生成，传 -p/--path <path> 指定路径')
    parser_new.add_argument('-p', '--path', type=str, help='YAML文件路径', default='./config.yaml')

    parser_gen = subparsers.add_parser('gen', help='根据YAML生成发布稿。默认当前目录下的 config.yaml，传 -p/--path <path> 指定路径')
    parser_gen.add_argument('-p', '--path', type=str, help='YAML文件路径', default='./config.yaml')

    args = parser.parse_args()

    return args


def main():
    args = parse_args()

    if args.command == 'new':
        create_yaml_config(args.path)
    elif args.command == 'gen':
        generate_drafts(args.path)


if __name__ == "__main__":
    main()
