### listconfig
Format .config → config list with description and metadata


### Install

```
$ pip install -e .
```


### Usage

Specify a `.config` file in somewhere like Linux Kernel.
Formatted list is output from stdout. Redirect it at which you like to put.

```
$ listconfig /path/to/Kconfig /path/to/.config > out
```

The `ARCH` is automatically detected from `.config`.
Specify `--arch` option to change it manually.

```
$ listconfig /path/to/Kconfig /path/to/.config --arch=arm > out
```

