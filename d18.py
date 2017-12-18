from collections import defaultdict
from queue import Queue, Empty
from threading import Thread

test_input = [line.split() for line in """
set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2
""".strip().splitlines()]

test_input2 = [line.split() for line in """
snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d""".strip().splitlines()]

with open('d18_input.txt') as f:
    puzzle_input = [line.strip().split() for line in f.readlines()]


def run_program(instructions, *part2_args):
    registers = defaultdict(int)

    if part2_args:
        instance_id, out_queue, in_queue, results_queue = part2_args
        registers['p'] = instance_id

    pointer = 0
    frequency = 0
    send_count = 0

    def get_value(n):
        return int(n) if not n.isalpha() else registers[n]

    def snd1(x):
        nonlocal frequency
        frequency = (get_value(x))

    def snd2(x):
        nonlocal send_count
        out_queue.put(get_value(x))
        send_count += 1

    def cpy(x, y):
        registers[x] = get_value(y)

    def add(x, y):
        registers[x] += get_value(y)

    def mul(x, y):
        registers[x] *= get_value(y)

    def mod(x, y):
        registers[x] = registers[x] % (get_value(y))

    def rcv1(x):
        nonlocal frequency
        if (x if not x.isalpha() else registers[x]) != 0:
            return frequency

    def rcv2(x):
        registers[x] = in_queue.get(timeout=1)
        in_queue.task_done()

    def jgz(x, y):
        nonlocal pointer
        if (get_value(x)) > 0:
            pointer += get_value(y)
        else:
            pointer += 1

    if not part2_args:
        commands = dict(snd=snd1, set=cpy, add=add, mul=mul, mod=mod, rcv=rcv1, jgz=jgz)
    else:
        commands = dict(snd=snd2, set=cpy, add=add, mul=mul, mod=mod, rcv=rcv2, jgz=jgz)

    while 0 <= pointer < len(instructions):
        try:
            cmd, *par = instructions[pointer]
        except IndexError:
            break

        try:
            result = commands[cmd](*par)
        except Empty:
            results_queue.put((instance_id, send_count))

        if cmd != 'jgz':
            pointer += 1

        if cmd == 'rcv' and result:
            return frequency


def run_concurrent(inp):
    q1 = Queue()  # messages from instance 1 to instance 2
    q2 = Queue()  # messages from instance 2 to instance 1
    q_results = Queue()

    worker0 = Thread(target=run_program, args=(inp, 0, q1, q2, q_results))
    worker1 = Thread(target=run_program, args=(inp, 1, q2, q1, q_results))

    worker0.setDaemon(True)
    worker1.setDaemon(True)

    worker0.start()
    worker1.start()

    q1.join()
    q2.join()

    return dict(q_results.get() for _ in (0, 1))


print(run_program(test_input))
print(run_program(puzzle_input))

print(run_concurrent(test_input2)[1])
print(run_concurrent(puzzle_input)[1])
