# A Refresher on GDB

One of the most important tools in your C arsenal is a good debugger. On most Linux environments, like the one provided in the class virtual machine, you'll find GDB (the GNU Debugger). It's interface can be a bit daunting at first, but with a few tips and pointers in the right direction, I think you'll find it will give you an advantage in finding and fixing bugs for your projects.

While it's possible to use CLion or some other IDE for this class, I found that for most projects, using GDB is all you need and will get you up and running faster. It can be used directly on the VM so that you can stay within the class environment. When I took this class, GDB helped me find some tricky bugs that I wouldn't have found without stepping through my code.

I've also posted a tutorial on [using gdbserver to remotely debug in CLion](gdb-remote.md).

To help you get familiar with GDB, the following short tutorial and tips may be of some assistance. Please note that this tutorial assumes you are running GDB from within the class VM. However, it is possible to use outside of the VM as well.


## Use the Makefiles

First, make sure you're using the Makefiles that we provide. The Makefiles for each project are already set to add debugging information into your compiled executables. GDB will use that debugging information when you run your program with GDB.

##  Using GDB

To start using GDB with your compiled executables, enter "gdb" then the name of your executable on the command line, for example:

```bash
gdb echoserver
```

If you want to add specific command-line arguments that are to be run with your executable, use the `--args` parameter followed by the name of your executable and then followed by any additional arguments that are to be passed to your executable. For example, this will run echoserver in gdb, passing in the port (-p) and maximum connections (-n) for an echoserver executable.

```bash
gdb --args echoserver -p 8080 -n 5
```

Once you've started GDB, you'll find yourself at the (gdb) prompt. The next few tips are to be run within GDB at the (gdb) prompt.

## Finding help

If you want to know more about what commands are available in GDB you can use the "help" command:

```bash
(gdb) help
```

If you need help with a specific command, type "help" followed by the command:

```bash
(gdb) help break
```

Note that commands are separated into the groups and that you can see all of the commands in that group by typing the group name. For example, to see all of the running commands type the following:

```bash
(gdb) help running
```

## Running your program

To run your executable, use the "run" command:

```bash
(gdb) run
```

If there are no issues with your code, the program will run without error.

However, if there is an issue, then GDB will print out some useful information.

```bash
Program received signal SIGSEGV, Segmentation fault.
0x0000000000400524 in sum array region (arr=0x7fffc809a361, r1=2, c1=7,
r2=4, c2=7) at echoserver.c:70
```

See the note on using "backtrace" below for how this can be made more useful.

## Setting a break point

If you do have a bug in your program and you want to investigate, setting a breakpoint will let you pause execution when GDB reaches that breakpoint line.

The easiest way to set a breakpoint is to tell it the file and line number you want to break at. Use the "break" command followed by the filename and line number separated by a colon (:).

For example, let's set a breakpoint on line 217 of echoserver.c:

```bash
(gdb) break echoserver.c:217
```

Then, when you "run" the executable from within GDB, execution will pause all execution at line 217.

## Stepping through code

Once you've reach your breakpoint, you'll want to step through your code to see what's happening.

Using the "continue" command, will just continue on to the next breakpoint or to the end of the program if there are no other breakpoints.

```bash
(gdb) continue
```

To step to the next line of code, use the "step" command.

```bash
(gdb) step
```

The "step" command will simply move to the next line of code in your program. If the next line of code is a subroutine, "step" will "step into" that subroutine and allow you to step through the lines for that subroutine as well.

If the next line is a subroutine and you want to "step over" the subroutine without moving through each line of the subroutine, use the "next" command.

```bash
(gdb) next
```

The "next" command will step to the next line of your current scope, without stepping into any subroutines.

To save you time, you don't have to keep entering "step" or "next" for each line. If you press the "ENTER" key, GDB will repeat the the last command you gave it. So, if the last command was "step", pressing ENTER will send the "step" command again.

If you just want to run to the end of the current function, then use the "finish" command.

```bash
(gdb) finish
```

## Finding Information about a variable

Setting a breakpoint paused the program execution, but you probably want to know what's happening at that point in your program as well. To do that, you can print out the variables in your current scope.

For example, if you had a variable named client_addr at your breakpoint, you could print that out using the following command:

```bash
(gdb) print client_addr
```

If your variable happens to be a pointer, when you print the variable you'll get the memory address of that pointer.

```bash
(gdb) print addrinfo_hints
```

If it's a struct, you may get the contents of the struct.

However, you can use the reference arrow to print the details for that pointer. For example, if you have an addrinfo pointer you can get flags or length for that pointer:

```bash
(gdb) print addrinfo_hints->ai_flags
```

You can also use the dereference and dot operators in lieu of the arrow for true pointers:

```bash
(gdb) print (*some_ptr).my_variable
```

Linked pointers also work:

```bash
(gdb) print addrinfo_hints->ai_next->ai_next
```

## Finding Backtraces

If your program crashes, such as in the example segfault shown above, you may want to find out what was happening prior to the crash.

To examine the stack, you can enter the "backtrace" command, which will provide you with a program's current stack that led to your current position in the program (or that lead to the fault you are examining).

```bash
(gdb) backtrace
```

This can be extremely useful as it will show you each call that was made leading up to the particular issue you are having.

However, please note that you may have to look further back into the stack in order to find the actual source of the problem. Bugs can trickle up but not break the program until some later point in the stack. So, look through the entire stack if you're still stumped as to why something crashed.

## Managing Breakpoints

Once you've set a breakpoint or two, you may want to know where those are. To examine all of the breakpoints you've set, use the "info breakpoints" command to get a list of all breakpoints set during the current GDB session.

```bash
(gdb) info breakpoints
```

If you're done with a breakpoint, you can delete it using the "delete" command followed by the id of the breakpoint that you found using the "info breakpoints" command above.

```bash
(gdb) delete 2
```
The previous command will delete breakpoint id 2.

One last note on breakpoints.

It can be useful to use a conditional when setting a breakpoint. For example, if I only want to break when a variable has a particular value, then you can use a boolean conditional to tell GDB to only break when that occurs.

```bash
(gdb) break echoserver.c:217 if client_addr == NULL
```

You may also want to look into the "watch" command, which will break whenever a watched variable changes. However, be aware that GDB will break on any watched variable regardless of the scope of that variable. You have to be aware of the scope.

## Working with Threads

GDB also has the ability to work with threads inside your project. The following commands might help you debug a multithreaded program:

Use the "info threads" command to list information about all available threads.

```bash
(gdb) info threads
```

Use the "thread threadno" command to switch among threads. After you switch to a particular thread, you can use any of the commands above.

```bash
(gdb) thread 42
```

Use the "thread apply [threadno] [all] args" command to apply a command to a list of threads

```bash
# Show the backtrace for thread 15
(gdb) thread apply 15 bt

# Show the backtrace for all threads
(gdb) thread apply all bt
```

This little tutorial only scratches the surface of what you can do with GDB, but it will provide you with most of the commands you'll need to get started and may be all you need to debug your programs. I encourage you to use the help command to explore commands that I've describe as well as others that are available.

For more information take a look at the GNU Manual for GDB.

> Good luck with your projects!
>
> ~ Patrick

