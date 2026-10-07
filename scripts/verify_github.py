"""Verify visibility, clean tree, and local/remote main alignment without credentials."""
import argparse, json, subprocess
from pathlib import Path
from common import ROOT

def command(*args):
    return subprocess.check_output(args, cwd=ROOT, text=True).strip()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    local = command('git', 'rev-parse', 'HEAD')
    remote = command('git', 'ls-remote', 'origin', 'refs/heads/main').split()[0]
    repo = json.loads(command('gh', 'repo', 'view', '--json', 'url,visibility,defaultBranchRef'))
    status = command('git', 'status', '--porcelain')
    result = dict(repository=repo['url'], visibility=repo['visibility'],
                  local_sha=local, remote_main_sha=remote, working_tree_clean=not status,
                  passed=local == remote and repo['visibility'] == 'PUBLIC' and not status)
    data = json.dumps(result, indent=2)+'\n'
    print(data, end='')
    if args.output:
        args.output.write_text(data)
    raise SystemExit(0 if result['passed'] else 1)
