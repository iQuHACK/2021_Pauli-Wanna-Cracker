from qiskit import Aer, QuantumCircuit, execute
from qiskit.quantum_info import Operator
import numpy as np
import scipy
import random
import sys


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


GAMMA = 0


def u_hat(theta, phi):
    return np.matrix([[np.exp(1j * phi) * np.cos(theta / 2), np.sin(theta / 2)],
                      [-np.sin(theta / 2), np.exp(-1j * phi) * np.cos(theta / 2)]])


d_hat = u_hat(np.pi, 0)

q_hat = u_hat(0, np.pi / 2)

alice_hp = 100
bob_hp = 100


def payoff(alice, bob):
    if alice == 0 and bob == 0:
        return (20, 20)
    elif alice == 0 and bob == 1:
        return (0, 40)
    if alice == 1 and bob == 0:
        return (40, 0)
    elif alice == 1 and bob == 1:
        return (5, 5)


PLAYER_NAMES = ['Bulbasaur', 'Charmander', 'Squirtle', 'Pikachu']
random.shuffle(PLAYER_NAMES)
alice_name, bob_name = PLAYER_NAMES[0], PLAYER_NAMES[1]

OPERATIONS = ['Z', 'Y', 'X', 'H']
random.shuffle(OPERATIONS)


def rand_gate():
    gate = ''
    for i in range(random.randint(1, 4)):
        gate += OPERATIONS[i]
    return gate


OPTION_NAMES = ["Growl", "Tackle", "Scratch", "Slash", "Bite", "Charm"]
rand_gates = {g: rand_gate() for g in OPTION_NAMES}


def game_over():
    if alice_hp > bob_hp:
        print("{} wins!".format(alice_name))
    elif bob_hp > alice_hp:
        print("{} wins!".format(bob_name))
    else:
        print("It's a draw!")
    print("Please play again!")


def loop():
    global alice_hp
    global bob_hp
    global GAMMA

    qc = QuantumCircuit(2)
    j_hat = np.matrix(scipy.linalg.expm(
        np.kron(-1j * GAMMA * d_hat, d_hat / 2)))
    qc.unitary(Operator(j_hat), [0, 1], label="")

    def defect(q):
        qc.x(q)
        qc.z(q)

    def quantum(q):
        qc.y(q)
        qc.x(q)

    def exec_gate(q, gate):
        for g in gate:
            if g == 'Z':
                qc.z(q)
            elif g == 'Y':
                qc.y(q)
            elif g == 'X':
                qc.x(q)
            elif g == 'H':
                qc.h(q)
            elif g == 'T':
                qc.t(q)
            elif g == 'S':
                qc.s(q)

    def prompt(q):
        while True:
            print("What will {} do?".format(alice_name if q == 0 else bob_name))

            options = ["Fight", "Defend", "Befriend"] + \
                list(random.sample(OPTION_NAMES, 3))

            for i, o in enumerate(options):
                print("[{}] {}".format(i + 1, o))

            result = input(bcolors.WARNING + ">>> " + bcolors.ENDC)
            try:
                i = int(result) - 1
                if i == 0:
                    defect(q)
                elif i == 1:
                    pass
                elif i == 2:
                    quantum(q)
                else:
                    gate = rand_gates[options[i]]
                    exec_gate(q, gate)
            except:
                print("Please enter an option number.")
                continue
            return

    prompt(0)
    prompt(1)
    qc.unitary(Operator(j_hat.H), [0, 1], label="")
    print(qc)

    backend = Aer.get_backend('statevector_simulator')
    job = execute(qc, backend)
    result = job.result().get_counts()

    alice_exp = 0
    bob_exp = 0

    for outcome, prob in result.items():
        alice, bob = int(outcome[1]), int(outcome[0])
        alice, bob = payoff(alice, bob)
        alice_exp += prob * alice
        bob_exp += prob * bob

    if alice_exp == bob_exp:
        print("It's a draw!")
        bob_hp += bob_exp
        alice_hp += alice_exp
        bob_hp = min(bob_hp, 100)
        alice_hp = min(alice_hp, 100)
    elif alice_exp > bob_exp:
        print("{} hits {} for {:.2f} damage!".format(
            alice_name, bob_name, alice_exp - bob_exp))
        bob_hp -= alice_exp - bob_exp
    else:
        print("{} hits {} for {:.2f} damage!".format(
            bob_name, alice_name, bob_exp - alice_exp))
        alice_hp -= bob_exp - alice_exp

    friendliness = min(abs(alice_hp - bob_hp) / 50, 1)
    GAMMA = friendliness * np.pi / 2
    print("Friendliness now {:.2f}".format(friendliness))

    print(bcolors.WARNING + "{} HP: {:.2f}, {} HP: {:.2f}".format(alice_name,
                                                                  alice_hp, bob_name, bob_hp) + bcolors.ENDC)
    if alice_hp <= 0 or bob_hp <= 0:
        game_over()
        sys.exit(0)


try:
    while True:
        loop()
except (KeyboardInterrupt, EOFError):
    game_over()
