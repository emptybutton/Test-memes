import uvicorn

from media.presentation.api.apps import app


def main() -> None:
    uvicorn.run(app)


if __name__ == "__main__":
    main()
