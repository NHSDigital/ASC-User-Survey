import shutil, pathlib

commit_msg_hook_path = (pathlib.Path(__file__).parent / "commit-msg").absolute()
git_hooks_path = (pathlib.Path(__file__).parent / "../.git/hooks").absolute()
shutil.copy(commit_msg_hook_path, git_hooks_path)