from invoke import task

@task
def start(ctx):
    ctx.run("python3 src/game.py", pty=True)

@task
def reset(ctx):
    ctx.run("python3 src/game.py reset", pty=True)

@task
def configure(ctx, setlang=''):
    if setlang:
        ctx.run(f"python3 src/game.py --setlang={setlang}", pty=True)
    else:
        ctx.run("python3 src/game.py --?", pty=True)

@task
def test(ctx):
    ctx.run("pytest src", pty=True)

@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest src", pty=True)

@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html", pty=True)

@task
def lint(ctx):
    ctx.run("pylint src", pty=True)