import argparse
import sys

import yaml

from vdg import __version__
from vdg.draftgen import DraftGenerator
from vdg.autopub import BangumiUploader, NyaaUploader
from vdg.utils import read_from_file, write_to_file

def parse_args():
    parser = argparse.ArgumentParser(description="发布稿生成/發佈腳本.")
    parser.add_argument('--version', action='version', version=__version__)
    subparsers = parser.add_subparsers(dest='command', required=True)

    subparsers.add_parser('new', help='在當前目錄下生成新的配置文檔 config.yml, 存放截圖鏈接的文件 url.html 和 url.md, 以及用於存放 MediaInfo 的 mediainfo.txt.')

    parser_gen = subparsers.add_parser('gen', help='根据在当前目录下的配置文檔生成发布稿.')
    parser_gen.add_argument('--site', type=str, choices=['bangumi', 'nyaa', 'vcb-s', 'all'], help='选择需要生成稿件的站点 (bangumi,nyaa,vcb-s,all).', default='all')

    parser_pub = subparsers.add_parser('publish', help='開啓半自動化發佈流程.')
    parser_pub.add_argument('--site', type=str, choices=['bangumi', 'nyaa'], help='选择需要发布的站点 (bangumi or nyaa).', required=True)
    parser_pub.add_argument('--username', type=str, help='Username for the site.', required=True)
    parser_pub.add_argument('--password', type=str, help='Password for the site.', required=True)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    if args.command == 'new':
        DraftGenerator.generate_configs()
    elif args.command == 'gen':
        site = args.site
        release_info = yaml.safe_load(read_from_file("./config.yml"))
        gen = DraftGenerator(release_info)
        sites = ['bangumi', 'nyaa', 'vcb-s'] if site == 'all' else [site]

        for site in sites:
            ext = "md" if site == 'nyaa' else "html"
            write_to_file(
                f"{release_info["filename"]}_{site}.{ext}",
                gen.generate(site, "title") + "\n" + gen.generate(site, "draft")
            )

    elif args.command == 'publish':
        site = args.site
        if site == 'bangumi':
            uploader = BangumiUploader()
        elif site == 'nyaa':
            uploader = NyaaUploader()
        release_info = yaml.safe_load(read_from_file("./config.yml"))
        gen = DraftGenerator(release_info)
        uploader.run(
            args.username,
            args.password,
            gen.generate(site, "title"),
            release_info["category"][site],
            gen.generate(site, "draft"),
            release_info["种子文件路径"]
        )
