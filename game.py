from qiskit import Aer, QuantumCircuit, execute
from qiskit.providers.jobstatus import JobStatus
from qiskit_ionq_provider import IonQProvider
from qiskit.quantum_info import Operator
import time
import numpy as np
import scipy

API_KEY = open("api.env", "r").read().strip()
provider = IonQProvider(token=API_KEY)

bank_account = []
ledger = {}


def measure(qubit, basis):
    coin_flip = random(0.5)
    if basis == "0/1" and qubit in ('+', '-'):
        return '0' if coin_flip else '1'
    elif basis == "+/-" and qubit in ('0', '1'):
        return '+' if coin_flip else '-'
    return qubit


class State:
    def __init__(self, bitstring):
        self.bitstring = bitstring
class Bill:
    def __init__(self, serial_number, state):
        self.serial_number = serial_number
        self.state = state

def verify_with_bank(serial_number, state_qc):
    pass

def measure_bit(serial_number, q_i):
    pass

qc = QuantumCircuit(1)

print(qc)

#backend = provider.get_backend("ionq_simulator")
#job = backend.run(qc, shots=1000)

#job_id_bell = job.job_id()
#while job.status() is not JobStatus.DONE:
#    print("Job status is ", job.status())
#    time.sleep(1)

#print("Job status is DONE")

backend = Aer.get_backend('statevector_simulator')
job = execute(qc, backend)
result = job.result()
print(result.get_counts())
