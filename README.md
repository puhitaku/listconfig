### listconfig

Convert .config into a menuconfig-like full list with help


### Example

Note: scroll rightward to see the entire line!

```
$ listconfig --help-lines=1 /path/to/linux/Kconfig /path/to/linux/.config
=== General setup ===
  [ ] Compile also drivers which will not load (COMPILE_TEST)                                                     Some drivers can be compiled on a different platform than they are ...
  ()  Local version - append to kernel release (LOCALVERSION)                                                     Append an extra string to the end of your kernel version. ...
  [*] Automatically append version information to the version string (LOCALVERSION_AUTO)                          This will try to automatically determine if the current tree is a ...
  ()  Build ID Salt (BUILD_SALT)                                                                                  The build ID is used to link binaries and their debug info. Setting ...
  -*- Kernel compression mode                                                                                     The linux kernel is a kind of self-extracting executable. ...
     -> Gzip (KERNEL_GZIP)                                                                                        The old and tried gzip compression. It provides a good balance ...
        LZMA (KERNEL_LZMA)                                                                                        This compression algorithm's ratio is best.  Decompression speed ...
        XZ (KERNEL_XZ)                                                                                            XZ uses the LZMA2 algorithm and instruction set specific ...
        LZO (KERNEL_LZO)                                                                                          Its compression ratio is the poorest among the choices. The kernel ...
        LZ4 (KERNEL_LZ4)                                                                                          LZ4 is an LZ77-type compressor with a fixed, byte-oriented encoding. ...
  ((none)) Default hostname (DEFAULT_HOSTNAME)                                                                    This option determines the default system hostname before userspace ...
  [*] Support for paging of anonymous memory (swap) (SWAP)                                                        This option allows you to choose whether you want to have support ...
  [*] System V IPC (SYSVIPC)                                                                                      Inter Process Communication is a suite of library functions and ...
  [ ] POSIX Message Queues (POSIX_MQUEUE)                                                                         POSIX variant of message queues is a part of IPC. In POSIX message ...
  [*] Enable process_vm_readv/writev syscalls (CROSS_MEMORY_ATTACH)                                               Enabling this option adds the system calls process_vm_readv and ...
  [ ] uselib syscall (USELIB)                                                                                     This option enables the uselib syscall, a system call used in the ...
  [ ] Auditing support (AUDIT)                                                                                    Enable auditing infrastructure that can be used with another ...
.
.
.
```

[See the full listconfig](./examples/listconfig_linux_arm_imx28)


### Install

Easier way:

```
$ pip install listconfig
```

To use the bleeding edge version:

```
$ git clone https://github.com/puhitaku/listconfig.git
$ cd listconfig
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
$ listconfig --arch=arm /path/to/Kconfig /path/to/.config > out
```

The description is generated from the "help" section of Kconfig items.
Specify `--help-lines` or `-l` to change how many lines to pick.

```
$ listconfig --help-lines=1 /path/to/Kconfig /path/to/.config
=== General setup ===
  [ ] Compile also drivers which will not load (COMPILE_TEST)                                                     Some drivers can be compiled on a different platform than they are ...
.
.
.
```

```
$ listconfig --help-lines=2 /path/to/Kconfig /path/to/.config
=== General setup ===
  [ ] Compile also drivers which will not load (COMPILE_TEST)                                                     Some drivers can be compiled on a different platform than they are intended to be run on. Despite they cannot be loaded there (or even ...
.
.
.
```

