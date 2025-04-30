## Neosync transformer function in Python

- To call neosync functions from Python, we export those functions into C, using Golang's `C` library, and call them using Python's `ctypes` library.

- The project `neosync_exporter` consists of a single `main.go` file (`go.mod` and `go.sum` are dependency files, similar to `requirements.txt` in Python projects). This file exports the neosync transformation functionality. If any change to this file is needed, we have to rebuild / recompile the `main.so` and `main.h` files after the modification using the following command.

```shell
make neosync-exporter-build
```

- Given the compiled files `main.so` and `main.h`, we can import the Golang function in Python using the C language as the bridge, by importing the `ctypes`.

- An example usage of the function exists under `example.py`.

