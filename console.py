#!/usr/bin/python3
"""
    Entry point to AirBnB project console
"""

import cmd
import sys


class Console(cmd.Cmd):
    """
        Simple command line interpreter
    """
    prompt = '(hbnb) '
    file = None

    def do_EOF(self, line):
        return True

    def do_quit(self, arg):
        self.close()
        quit()
        return True

    def close(self):
        if self.file:
            self.file.close()
            self.file = None


if __name__ == '__main__':
    Console().cmdloop()
