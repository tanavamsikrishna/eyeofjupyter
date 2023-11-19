import os

import click


def start_browser(path):
    selected_file_index = 0
    while True:
        click.clear()
        click.echo(click.style(path, fg="white", bg="bright_black", bold=True))
        click.echo()
        if os.path.isfile(path):
            print(path)
            click.launch(path)
            return
        files = os.listdir(path)
        for i, f in enumerate(files):
            msg = f
            if i == selected_file_index:
                msg = click.style(msg, fg="blue", bold=True)
            click.echo(msg)
        inp = click.getchar().encode("utf-8")
        match inp:
            case b"\x1b[A":
                selected_file_index = (selected_file_index - 1) % len(files)
            case b"\x1b[B":
                selected_file_index = (selected_file_index + 1) % len(files)
            case b"\x1b[C":
                path = f"{path}/{files[selected_file_index]}"
                selected_file_index = 0
            case b"\x1b[D":
                path = os.path.dirname(path)
            case _:
                print(inp)
                break
