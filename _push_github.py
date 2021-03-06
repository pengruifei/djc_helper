# 构建发布压缩包
import subprocess

from version import now_version


def push_github(version):
    # 先尝试移除该tag，并同步到github，避免后面加标签失败
    subprocess.call(['git', 'tag', '-d', version])
    subprocess.call(['git', 'push', 'origin', 'master', ':refs/tags/{version}'.format(version=version)])
    # 然后添加新tab，并同步到github
    subprocess.call(['git', 'tag', '-a', version, '-m', 'release {version}'.format(version=version)])
    subprocess.call(['git', 'push', 'origin', 'master', '--tags'])


def main():
    version = 'v' + now_version
    push_github(version)

    import os
    os.system("PAUSE")


if __name__ == '__main__':
    main()
