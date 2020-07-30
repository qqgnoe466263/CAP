#!$SHELL

if [ `uname` != "Linux" ]; then
    echo "Not in Linux, exit."
    exit 0;
fi

sudo apt install build-essential git-core valgrind
sudo apt install cppcheck clang-format aspell colordiff
#sudo apt install linux-headers-`uname -r`
#sudo apt install util-linux strace gnuplot-nox

if [ `echo $SHELL | grep zsh` ]; then
    shellrc="$HOME/.zshrc"
elif [ `echo $SHELL | grep bash` ]; then
    shellrc="$HOME/.bashrc"
fi

# build cppcheck to 1.90
CPPCHECK_VER=$(cppcheck --version | sed -Ee 's/Cppcheck 1.([0-9]+)/\1/;q')
if [ $CPPCHECK_VER -lt 90 ]; then
    sudo snap install cppcheck
    echo "export PATH=/snap/bin:\$PATH" >> ${shellrc}
fi
