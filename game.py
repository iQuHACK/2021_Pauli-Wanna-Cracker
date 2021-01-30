from qiskit import Aer, QuantumCircuit, execute
from qiskit.providers.jobstatus import JobStatus
from qiskit_ionq_provider import IonQProvider
from qiskit.quantum_info import Operator
import time
import numpy as np
import scipy

API_KEY = open("api.env", "r").read().strip()
provider = IonQProvider(token=API_KEY)


GAMMA = 0


def u_hat(theta, phi):
    return np.matrix([[np.exp(1j * phi) * np.cos(theta / 2), np.sin(theta / 2)],
                      [-np.sin(theta / 2), np.exp(-1j * phi) * np.cos(theta / 2)]])

d_hat = u_hat(np.pi, 0)
j_hat = np.matrix(scipy.linalg.expm(np.kron(-1j * GAMMA * d_hat, d_hat / 2)))

q_hat = u_hat(0, np.pi / 2)

qc = QuantumCircuit(2)
qc.unitary(Operator(j_hat), [0, 1], label="j_hat")
#qc.y(0)
#qc.x(0)
#qc.y(1)
#qc.x(1)
qc.x(0)
qc.z(0)
qc.unitary(Operator(j_hat.H), [0, 1], label="j_hat*")
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
