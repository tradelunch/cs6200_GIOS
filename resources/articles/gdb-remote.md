## Remote Debugging with GDB

I noticed that a lot of students like to work in their own environment while debugging. Unfortunately, to get the most out of these projects and match with what's on the Bonnie system, you'll need to use Ubuntu 20.04 as mentioned in in our [environment setup file](environment.md). I recommend the Vagrant or Docker environments for best mileage, but you can use any Ubuntu 20.04 setup that you prefer.

However, if you want the best of both worlds, you can [use CLion](https://www.jetbrains.com/clion/) to remotely debug with GDB against your compiled programs on the virtual machine. I've used this in the past via Mac OSX and Windows and it works quite well. You can stay within the CLion IDE, but run your code in the official class environment.

CLion does this by connecting to a [gdbserver instance](https://sourceware.org/gdb/onlinedocs/gdb/Server.html) that runs on the virtual machine. Gdbserver should already be installed on the VM if you're using the Vagrant instance referred to earlier.

> A similar procedure can be used with VS Code as [described in this blog post](https://medium.com/@spe_/debugging-c-c-programs-remotely-using-visual-studio-code-and-gdbserver-559d3434fb78).

> You can also install CLion directly inside the VM if there is a windowing system installed.


This is not a required way to debug, but for those of you who are interested in combining remote debugging with the Vagrant VM and CLion, here are some pointers to help you get started.


> Note that you can get a student copy of CLion using your gatech.edu email address. In general, you may also find that the process I describe here will work with other IDEs as well, such as MS Visual Studio Code.


## Port Forwarding in Vagrant

Add a forwarded port to your Vagrantfile similar to the following. Note that the ports are arbitrary, just make sure they don't conflict with anything else; 2159 is the usual for gdbserver.

```bash
config.vm.network "forwarded_port", guest: 2159, host: 2159
```

You'll most likely need to run vagrant provision and then restart the vm after you set this port configuration.

## CLion

Open or create a project for your local code base (e.g. PR1) in CLion


### Configuration

Set up a Remote GDB Debug configuration in CLion by following the [instructions in this help guide](https://www.jetbrains.com/help/clion/2016.3/remote-debug.html).


> On some environments, such as Mac OSX, you may have to compile your own version of binutils-gdb to select in the GDB section. See the help guide linked to above for details. Make sure you select the compiled symbol file (which is the compiled version of your application). Make sure you set up the remote (vm) and local (host) path mappings (these are the fully qualified paths to your code repository on both the remote and host environments)


## Debugging Session

Fnally, start your debugging session:


First, start the gdbserver on the remote VM as mentioned in [this manual page](https://sourceware.org/gdb/onlinedocs/gdb/Server.html), for example:

```bash
gdbserver :2159 echoclient
```

Then, start the debug session in CLion by following the [information in this guide](https://www.jetbrains.com/help/clion/2016.3/remote-debug.html) (also [see this blog post](https://blog.jetbrains.com/clion/2016/07/clion-2016-2-eap-remote-gdb-debug/)).

One important caveat to all of this, is that you need to compile your programs inside the VM, not on your host OS.

You are on your own if you want to try this, but it might be worth the effort for those willing to try something a little different.

Also take a look at the [Debugging with GDB](gdb-debugging.md) document, for some pointers on using the command-line GDB interface from within the VM.

> Good luck with your projects!
>
> ~ Patrick

