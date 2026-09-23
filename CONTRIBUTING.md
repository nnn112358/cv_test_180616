# Contributing

Thanks for your interest in improving this project! Pull requests from anyone are welcome.

## Reporting bugs and requesting features

Please open an [issue](../../issues/new/choose) first for anything non-trivial, so the
change can be discussed before you spend time on it. Use the provided templates for
bug reports and feature requests.

## Submitting a pull request

1. Fork the repository and create a topic branch from `master`
   (e.g. `fix/csv-parsing` or `feature/ransac-option`).
2. Make your changes. Keep each pull request focused on a single topic.
3. Build and run the program locally (see below) and confirm it still works.
4. Commit with a clear message describing *what* changed and *why*.
5. Push your branch to your fork and open a pull request against `master`.
   Fill in the pull request template.
6. CI will build the code automatically. Please make sure the check passes.
7. A maintainer will review your pull request. Address any feedback by pushing
   additional commits to the same branch.

## Building locally

Requirements: a C++ compiler (g++) and OpenCV 4 development files.

On Ubuntu/Debian:

```sh
sudo apt-get install g++ pkg-config libopencv-dev
```

Build and run:

```sh
g++ homograpy.cpp -o homography $(pkg-config --cflags --libs opencv4)
./homography
```

The program reads `data.csv` (source and destination corner points) and
`input.csv` (points to transform) from the current directory.

## Code style

- Match the style of the surrounding code.
- Avoid unrelated reformatting in the same pull request.

## License

By contributing, you agree that your contributions will be licensed under the
same terms as this project.
