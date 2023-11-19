from eyeofjupyter.commandline import cli


def main():
    cli()


if __name__ == "__main__":
    main()
    # char = click.getchar().encode("utf-8")
    # match char:
    #     case b'\x1b[B':
    #         print("down press")
    # print(f"Char is `{char}`")
