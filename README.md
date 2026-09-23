# cv_test_180616
Computes a homography from four point correspondences (`data.csv`) with OpenCV
and applies it to the points in `input.csv`.

## Build

```sh
g++ homograpy.cpp -o homography $(pkg-config --cflags --libs opencv4)
./homography
```

## Contributing

Pull requests are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).
