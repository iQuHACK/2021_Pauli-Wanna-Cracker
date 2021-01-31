import time
import numpy as np
import scipy
import random
import sys 

# ===============================================
#  Backend
# ===============================================

wallet = []
net_worth = 0
ledger = {}

ZERO_VECT = np.array([[1],[0]])
ONE_VECT = np.array([[0],[1]])
PLUS_VECT = (1/np.sqrt(2)) * np.array([[1],[1]])
MINUS_VECT = (1/np.sqrt(2)) * np.array([[1],[-1]])
VECTS = [ZERO_VECT, ONE_VECT, PLUS_VECT, MINUS_VECT]
VECT_NAMES = ['0', '1', '+', '-']
BASIC_KET_STRINGS = ["|0>","|1>","|+>","|->"]
    
I_GATE = np.array([[1, 0],[0, 1]])
H_GATE = (1/np.sqrt(2)) * np.array([[1, 1],[1, -1]])
X_GATE = np.array([[0, 1],[1, 0]])
Y_GATE = np.array([[0, -1j],[1j, 0]])
Z_GATE = np.array([[1, 0],[0, -1]])

def R_GATE(theta):
    return np.array([[np.cos(theta), 0],[0, np.sin(theta)]])

class Qubit:
    def __init__(self, vect):
        self.vect = vect
    
    def __rmul__(self, other):
        return np.matmul(other,self.vect)
    
    def measure(self, prerotation=I_GATE):
        if random.random() < np.absolute(np.matmul(prerotation,self.vect)[0,0])**2:
            self.vect = np.matmul(prerotation,ZERO_VECT)
            return 0
        else:
            self.vect = np.matmul(prerotation,ONE_VECT)
            return 1

    def seems_to_match(self, state):
        if state in ('0', '1'):
            return state == ('0','1')[self.measure()]
        else:
            return state == ('+','-')[self.measure(H_GATE)]

def mint_qubit():
    return Qubit(random.choice([ZERO_VECT, ONE_VECT, PLUS_VECT, MINUS_VECT]))
        
class Bill:
    def __init__(self, serial_number, state, value, decoy=False):
        self.serial_number = serial_number
        self.state = state
        self.value = value
        self.decoy = decoy

    def __str__(self):
        return f"Bill #{self.serial_number}: ${self.value}" + self.decoy*" (decoy)"

def mint_bill(num_qubits, value):
    serial_number = random.randrange(10**9,10**10)
    secret = ""

    state = []
    for _ in range(num_qubits):
        choice = random.randrange(len(VECTS))
        state.append(Qubit(VECTS[choice]))
        secret += VECT_NAMES[choice]

    ledger[serial_number] = secret
    
    return Bill(serial_number, state, value)

def verify_with_bank(bill, do_on_fail=lambda:None):
    global net_worth
    secret = ledger[bill.serial_number]
    for i in range(len(bill.state)):
        if not bill.state[i].seems_to_match(secret[i]):
            do_on_fail()
            return False
    wallet.remove(bill)
    net_worth += bill.value
    return True

# ===============================================
#  UI/UX
# ===============================================

def pretty_print(s):
    for c in s:
        print(c,end='')
        time.sleep(0.01)
    print()

def print_lines(s, n=80):
    while len(s) > n:
        next_newline = s[:n].find('\n')
        last_space_in_line = s[:n].rfind(' ') if next_newline == -1 else next_newline
        print(s[:last_space_in_line])
        s = s[last_space_in_line+1:]
    print(s)

def alert(prompt, end='[Press ENTER to continue] '):
    print_lines(prompt)
    print_lines(end)
    result = input()
    if result.strip() == 'q':
        sys.exit()
    return result

def selection(prompt, options=[], is_qubit_selection=0):
    print_lines(prompt)

    if is_qubit_selection:
        print_lines(f"[Enter a number between 1 and {is_qubit_selection}]")
    else:
        for i, o in enumerate(options):
            print_lines("[{}] {}".format(i + 1, o))

    while True:
        result = input(">>> ")
        
        if result.strip() == 'q':
            sys.exit()

        try:
            i = int(result) - 1
            if i < 0 or i >= len(options):
                print_lines("Please enter a valid option number.")
                continue
            return i
        except:
            print_lines("Please enter a valid option number.")
            continue

def welcome_message():
    skip_intro = alert("Welcome to Wiesners Thievers, the only game on the market that teaches you how to be a crook and a quantum theorist at the same time. The game is simple: counterfeit as much money as you can, and don't get caught doing it!", end="[Would you like to skip intro? (y/N)]")
    if skip_intro == "y":
        return
    alert("Here in Wiesnerville, we had a rampant counterfeiting problem. The issue was that classical information is just too easy to copy, too easy to fake.")
    alert("We heard that the No-Cloning Theorem prevents anyone from copying a quantum state, and our scientists got to work.")
    alert("Now, every dollar bill has a monetary value ($1, $10, etc.), a unique serial number, AND a single qubit embedded in the fabric of the bill.")
    alert("Bada bing, bada boom: uncopiable money! Problem solved, right?")
    alert("This qubit will always be in one of 4 possible states: |0>, |1>, |+>, or |->.")
    alert('''As a reminder: 
    |+> = (|0> + |1>) / sqrt(2) 
    |-> = (|0> - |1>) / sqrt(2)
These states are 'the plus state' and 'the minus state,' and you can create them by applying a Hadamard gate to a |0> or |1> respectively.''')
    alert("We don't want any fake bills being used, so every time a Wiesnerville resident tries to buy something, they have to mail their bill to the Wiesner Central Bank to verify that it's the real deal. After whatever we do to check the bill, we'll send the bill back to you.")
    alert("At the bank, we keep a ledger - a list of every bill's serial number, and the secret true identity of the qubit on that bill.")
    alert('''Here's what one row of that top-secret ledger might look like:
    Bill #0198308187: |+>''')
    alert("Now, your job is to get filthy rich. You found a few dollars on the floor and you happen to own a dollar printing factory - find a way to fool the bank into accepting fake bills!")
    
def level0_intro():
    print_lines("="*50 + "\n LEVEL 1\n" + "="*50 + "\n")
    alert("You found 3 dollar bills on the ground. Your objective is to have a net worth of $10.")

def level1_intro():
    alert("No worries. Our system is tougher for larger bills. For $10 bills, instead of a single qubit on each bill, we embed 5 qubits.")
    alert('''Here's what a row of the bank's ledger might look like now:
    Bill #0198308187: |1>|+>|+>|0>|->
Good luck cracking this one!''')

def copy_bill(bill):
    fake_bill = Bill(bill.serial_number, [], bill.value, decoy=True)
    for i in range(len(bill.state)):
        qubit_choice = selection(f"What state would you like qubit #{i+1} to be in?", BASIC_KET_STRINGS)
        fake_bill.state.append(Qubit(VECTS[qubit_choice]))
    wallet.append(fake_bill)
    alert(f"Success! You made a copy of bill #{bill.serial_number}. Note that it won't affect your net worth until you successfully cash it in with the bank.")

def measure_bill(bill):
    qubit_index = 0
    if len(bill.state) > 1:
        qubit_index = selection("Which qubit do you want to measure?", len(bill.state))

    basis = selection("What basis do you want to measure in?",["{|0>,|1>}","{|+>,|->}"])

    print_lines(f"Measuring qubit #{qubit_index+1} in bill #{bill.serial_number}...")
    is_oneish = bill.state[qubit_index].measure(H_GATE if basis else I_GATE)
    alert(f"Result: {BASIC_KET_STRINGS[basis*2 + is_oneish]}")

first_time_success = True
first_time_failure = True
def verify_bill(bill):
    global first_time_success, first_time_failure, bill_options
    print_lines("The bank is checking your bill...")
    time.sleep(1)
    if verify_with_bank(bill):
        alert(f"Success! Your net worth has gone up by ${bill.value}, and the bank has taken that bill away from you."
        + first_time_success*"\n\n(In real life, the bank would return the bill to whatever shop you were trying to spend money at.)")
        first_time_success = False
        bill_options[2] = "Cash it out at the bank"
    else:
        alert("No luck. The bill was rejected but at least it's back in your wallet. "
        + first_time_failure*"\nPerhaps the measurements done by the bank have changed the state?")
        first_time_failure = False

bill_options = [
    "Print a copy with the same serial number",
    "Measure a qubit",
    "Cash it out at the bank (This will increase your net worth, but you will no longer have the bill if it is validated.)"
]
bill_actions = [
    lambda bill: copy_bill(bill),
    lambda bill: measure_bill(bill),
    lambda bill: verify_bill(bill),
]

def inspect_bill(bill):
    choice = selection(f"What would you like to do with Bill #{bill.serial_number}?", bill_options)
    bill_actions[choice](bill)

def run_level(level_threshold):
    global first_time_success
    while net_worth < level_threshold:
        print_lines(f"Your net worth: ${net_worth}." + first_time_success*" (This only goes up when you verify a bill with the bank.)")
        bill_index = selection("Choose a bill to take a closer look:", wallet)
        inspect_bill(wallet[bill_index])
    alert(f"Wow, you cracked the system fast! Congratulations! You made ${net_worth}!")
    
def play():
    welcome_message()
    for _ in range(3):
        wallet.append(mint_bill(1,1))
    level0_intro()
    run_level(10)
    level1_intro()

play()