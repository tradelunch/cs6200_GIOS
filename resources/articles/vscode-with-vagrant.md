# VS Code with Vagrant Remote Connection

> This post was provided by a former student of ours (Timothy Huynh). I don't use VSCode, so I can't vouch the effectiveness of this approach, but I know it was some use to some of your fellow colleagues last term. I've left the content mostly as-is, with some minor editing.
>
> ~ Patrick

## Introduction

This post is meant to serve as a guide for those who are using VSCode + Vagrant as their development environment. My desire is for people to contribute to this post as well because I only have the bandwidth to really talk about my specific circumstance (Windows 10, VSCode, and Vagrant via the easy setup portion of found in the environment document](environment.md). These were the steps I followed:

## Program Installation

- Download and install VSCode and Vagrant according to "Easy Mode Install" found at https://github.gatech.edu/gios-fall19/environment
- I also downloaded/installed python/python libraries listed in "Submitting Code Outside the VM (I haven't actually tried to submit code as of now and will update this post if necessary)
- Download and install the "Remote - SSH" extension for VSCode
- I actually downloaded the "Remote Development" extension but I think all that does is install the 3 different remote development extensions (i.e. Remote-SSH)

## Connecting VSCode to the Vagrant VM

- Start the VM by invoking "vagrant up". This will take a while if it is the first time you have run this command.
- Get the ssh config needed for VSCode to connect to the VM by running "vagrant ssh-config"
    - You could also direct the output to a file and use that file in the next step
- In VSCode, hit "F1" to bring up the command bar and look for "Remote-SSH: Connect to Host" and select "Configure SSH Hosts..."
- Select a config file to use (I used the first one listed) and paste the output from step 2 into the file
    - Alternatively, I believe you can choose "Settings" and point to the configuration file generated if you re-directed the output from step 2 into a file
- At this point, your setup should show up as a "connection" in the "Remote-SSH" tab at the bottom of the left-hand navigation bar. Right click the connection and select "Open on SSH Host in Current/New Window". VSCode should open a new window (seemingly irregardless of which option you selected previously).

## Development

- To develop remotely, you will need to install the C/C++ extension for VSCode onto the remote VM. In the window opened from step 5 of the previous section, click the "extensions" icon (looks like tetris blocks on the left-hand nav bar) and search for C/C++. This should bring up extensions that match that query (you want the one by "Microsoft").
- Install the extension on the remote VM.
    - You may have to install this locally first? I already had the extension locally and an option popped up that said "Install in SSH: default" which is what you want
- At this point, you should be able to develop as if you were on the remote VM

## Debugging

- Click on the "bug" icon on the left-hand nav bar to bring up the debug context
- At the top, click on the gear icon to create a new launch.json with "C++" as the environment (should select GDB as the debugger)
- Change "program" to point to the binary output from make
    - Only tested this on echoserver so far
    - There may be some issues using gdb with files in the shared folder so you may need to move the binaries to a different folder e.g. ~/debug_binaries or something
- Save the configuration
- To test debugging, set a breakpoint in the file corresponding to the binary from step 2
- In the debug context, select the configuration created from step 3 and hit the green arrow to launch the program
- You should hit the breakpoint set from step 5

## Notes

- I found it helpful to create a "preLaunchTask" that cleans and builds the binary:
    - Create a shell script that cleans, builds, and moves the output files to the folder from the previous section, step 3 substep 2
    - Hit "F1" and look for "Tasks: Configure Task"
    - Set the label to something like "buildProject" and have the command be "./{file-from-step-1}.sh"
    - Add "options" and add "cwd" in options and set it to be in the folder holding the script file from step 1. I wasn't able to use symbols like "~" to reference the user's home directory but if the script is in the current workspace (it probably should be), then you can use the variable "${workspaceFolder}" that VSCode provides
    - In the launch.json from the previous section, add "preLaunchTask" and populate it with "buildProject" or whatever you labeled the task from step 3

Hopefully this is helpful and as I mentioned earlier, feel free to contribute to this post as you find caveats or need to clarify the steps I added (also if you're working in a different environment e.g. macOS).

