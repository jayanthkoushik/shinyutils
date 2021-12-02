# shinyutils.sh module

Stateful wrapper to execute shell commands.


### _class_ shinyutils.sh.SH(shell=('sh', '-i'), loop=None)
Wrapper around an interactive shell process.

This class can be used to execute multiple shell commands within a single shell
session; shell output (stdout and stderr) is captured and returned as a string.
The class must be used as a context manager; both synchronous and asynchronous
modes are supported.


* **Parameters**


    * **shell** – The shell command to execute, as a sequence of strings. This must start
    an interactive shell, and defaults to `sh -i`.


    * **loop** – Optional event loop to use. If not provided, the default event loop is
    used instead.


Usage:

```python
# synchronous mode
with SH() as sh:
    sh("x=1")
    print(sh("echo $x"))

# asynchronous mode
async with SH() as sh:
    await sh("x=1")
    print(await sh("echo $x"))
```

**NOTE**: The class uses a custom prompt string to identify the end of a command. So,
do not run any commands that change the prompt. Similarly, background jobs are
not supported, if they produce any output. The behavior in these cases is
undefined.
