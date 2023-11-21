from sys import stderr
from eyeofjupyter import config
from eyeofjupyter.commandline import cli
from eyeofjupyter.errors import NoProject


def config_exception_handling():
    import sys

    def exception_handler(exc_cls, exc_obj, traceback):
        if exc_cls == NoProject:
            print(
                f"No project description file `{config.CONFIG_FILE_NAME}` found",
                file=stderr,
            )
            sys.exit(1)
        else:
            sys.__excepthook__(exc_cls, exc_obj, traceback)

    sys.excepthook = exception_handler


def main():
    config_exception_handling()
    cli()


if __name__ == "__main__":
    main()
