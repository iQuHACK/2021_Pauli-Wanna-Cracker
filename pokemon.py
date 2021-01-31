from qiskit import Aer, QuantumCircuit, QuantumRegister, execute
from qiskit.quantum_info import Operator
import numpy as np
import scipy
import random
import sys
import time


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
        return (-10, -10)


PLAYER_NAMES = ['Bulbasaur', 'Charmander', 'Squirtle', 'Pikachu']
random.shuffle(PLAYER_NAMES)
alice_name, bob_name = PLAYER_NAMES[0], PLAYER_NAMES[1]

OPERATIONS = ['Z', 'Y', 'X', 'H']


def rand_gate():
    gate = ''
    random.shuffle(OPERATIONS)
    for i in range(random.randint(1, 4)):
        gate += OPERATIONS[i]
    return gate


OPTION_NAMES = ["Growl", "Tackle", "Scratch", "Slash", "Bite", "Charm"]
rand_gates = {g: rand_gate() for g in OPTION_NAMES}


def crawl(s):
    for letter in s:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(.02)
    print("")


def game_over():
    print("")
    if alice_hp > bob_hp:
        print("{} fainted!".format(bob_name))
        print("{} wins!".format(alice_name))
    elif bob_hp > alice_hp:
        print("{} fainted!".format(alice_name))
        print("{} wins!".format(bob_name))
    else:
        print("It's a draw!")
    print("Please play again!")


def print_hp():
    print(bcolors.HEADER + "{0: <10} [".format(alice_name) + int(alice_hp // 5)
          * "=" + (20 - int(alice_hp // 5)) * " " + "] {:.2f}".format(alice_hp))
    print("{0: <10} [".format(bob_name) + int(bob_hp // 5) * "=" + (20 -
                                                                    int(bob_hp // 5)) * " " + "] {:.2f}".format(bob_hp) + bcolors.ENDC)


def loop():
    global alice_hp
    global bob_hp
    global GAMMA

    qc = QuantumCircuit(QuantumRegister(1, alice_name.lower()),
                        QuantumRegister(1, bob_name.lower()))
    j_hat = np.matrix(scipy.linalg.expm(
        np.kron(-1j * GAMMA * d_hat, d_hat / 2)))
    qc.unitary(Operator(j_hat), [0, 1], label="Friendship")

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
            print("\nWhat will {} do?".format(
                alice_name if q == 0 else bob_name))

            options = tuple(random.sample(OPTION_NAMES, 3))

            print("[1] Fight\t[2] Heal\t[3] Befriend")
            print("[4] {}\t[5] {}\t[6] {}".format(*options))

            result = input(bcolors.WARNING + ">>> " + bcolors.ENDC)
            try:
                i = int(result) - 1
                if i == 0:
                    defect(q)
                    return "Fight"
                elif i == 1:
                    return "Heal"
                elif i == 2:
                    quantum(q)
                    return "Befriend"
                else:
                    exec_gate(q, rand_gates[options[i - 3]])
                    return options[i - 3]
            except (ValueError, IndexError):
                print("Please enter an option number.")
                continue

    alice_move = prompt(0)
    bob_move = prompt(1)
    qc.unitary(Operator(j_hat.H), [0, 1], label="Battle")
    print(qc)

    crawl("{} used {}!".format(alice_name, alice_move))
    crawl("{} used {}!".format(bob_name, bob_move))

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

    if alice_move == "Befriend" and bob_move not in ("Befriend", "Heal") and alice_exp > bob_exp or bob_move == "Befriend" and alice_move not in ("Befriend", "Heal") and bob_exp > alice_exp:
        crawl(bcolors.OKCYAN + bcolors.BOLD +
              "It's the power of friendship!" + bcolors.ENDC)

    if alice_exp == bob_exp:
        if alice_exp > 0:
            crawl(bcolors.OKGREEN +
                  "It's a draw! Both sides heal {:.2f} damage!".format(alice_exp) + bcolors.ENDC)
        else:
            crawl(
                bcolors.FAIL + "It's a draw! Both sides take {:.2f} damage!".format(abs(alice_exp)) + bcolors.ENDC)
        bob_hp += bob_exp
        alice_hp += alice_exp
        bob_hp = min(bob_hp, 100)
        alice_hp = min(alice_hp, 100)
    elif alice_exp > bob_exp:
        crawl(bcolors.FAIL + "{} hits {} for {:.2f} damage!".format(
            alice_name, bob_name, alice_exp - bob_exp) + bcolors.ENDC)
        bob_hp -= alice_exp - bob_exp
    else:
        crawl(bcolors.FAIL + "{} hits {} for {:.2f} damage!".format(
            bob_name, alice_name, bob_exp - alice_exp) + bcolors.ENDC)
        alice_hp -= bob_exp - alice_exp

    if alice_hp <= 0 or bob_hp <= 0:
        game_over()
        sys.exit(0)

    print("")
    print_hp()

    friendliness = min(max(abs(alice_hp - bob_hp) / 50,
                           1 - max(alice_hp, bob_hp) / 50), 1)
    GAMMA = friendliness * np.pi / 2
    if friendliness < 0.1:
        crawl("It's like an awkward first encounter...")
    elif friendliness < 0.3:
        crawl("Have these two met before?")
    elif friendliness < 0.5:
        crawl("Feels like an old reunion.")
    elif friendliness < 0.7:
        crawl("Friendship is in the air!")
    else:
        crawl("You can feel friendship all around you!")


try:
    crawl(bcolors.OKGREEN + bcolors.BOLD +
          "A wild quantum state appeared!\n{} VS {}".format(alice_name, bob_name) + bcolors.ENDC)

    print_hp()
    while True:
        loop()
except (KeyboardInterrupt, EOFError):
    game_over()
