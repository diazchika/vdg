import argparse
import sys

from vdg.core import *

def parse_args():
    parser = argparse.ArgumentParser(description="发布稿生成/發佈腳本.")
    parser.add_argument('--version', action='version', version=vdg.__version__)
    subparsers = parser.add_subparsers(dest='command', required=True)

    parser_new = subparsers.add_parser('new', help='在當前目錄下生成新的配置文檔 config.yml, 存放截圖鏈接的文件 url.html 和 url.md, 以及用於存放 MediaInfo 的 mediainfo.txt.')

    parser_gen = subparsers.add_parser('gen', help='根据在当前目录下的配置文檔生成发布稿.')
    parser_gen.add_argument('--path', type=str, help='YAML 配置文件路径.', default='./config.yml')

    parser_pub = subparsers.add_parser('publish', help='開啓半自動化發佈流程.')
    parser_pub.add_argument('--site', type=str, choices=['bangumi', 'nyaa'], help='选择需要发布的站点 (bangumi or nyaa).', required=True)
    parser_pub.add_argument('--username', type=str, help='Username for the site.', required=True)
    parser_pub.add_argument('--password', type=str, help='Password for the site.', required=True)

    # If no arguments are provided, print help and exit
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    if args.command == 'new':
        create_form()
    elif args.command == 'gen':
        generate_drafts(args.path)
    elif args.command == 'publish':
        # Add your publish logic here, using args.site, args.username, and args.password
        pass