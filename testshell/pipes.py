from subprocess import *
if __name__ == '__main__':
    p1 = Popen(["python", "printToScreen.py"], stdout=PIPE, shell=None)
    p2 = Popen(["python", "countLines.py"], stdin=p1.stdout, shell=None)
    p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
    print("Before Communicate")
    try:
        outs, errs = p2.communicate()
        print("After Communicate")
        if outs:
            print(outs)

    except TimeoutExpired:
        p2.kill()
        outs, errs = p2.communicate()


