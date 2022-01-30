import numpy as np
# Importing standard Qiskit libraries
from qiskit import QuantumCircuit, execute, transpile, Aer, IBMQ
from qiskit.tools.jupyter import *
from qiskit.visualization import *
from random import getrandbits
import binascii
import time
import os
from IPython.display import display

from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute
from qiskit.tools.visualization import plot_histogram, circuit_drawer

from quantuminspire.credentials import get_authentication
from quantuminspire.qiskit import QI
from getpass import getpass

QI_URL = os.getenv('QI_URL', 'https://api.quantum-inspire.com/')

def get_authentication():
    """Gets the authentication for connecting to the
       Quantum Inspire API.
    """
    email = "bolivares8090@gmail.com"
    password = "RNP25SeOmHlt7sZyrMx1"
    return [email, password] 


if 'authentication' not in vars().keys():
    authentication = get_authentication()
QI.set_authentication_details(*authentication)
qi_backend = QI.get_backend('Spin-2')

def encrypt_message(unencrypted_string, key):
    # Convert ascii string to binary string
    bits = bin(int(binascii.hexlify(unencrypted_string.encode('utf-8', 'surrogatepass')), 16))[2:]
    bitstring = bits.zfill(8 * ((len(bits) + 7) // 8))
    # created the encrypted string using the key
    encrypted_string = ""
    for i in range(len(bitstring)):
        encrypted_string += str( (int(bitstring[i])^ int(key[i])) )
    return encrypted_string
    
def decrypt_message(encrypted_bits, key):
    # created the unencrypted string using the key
    unencrypted_bits = ""
    for i in range(len(encrypted_bits)):
        unencrypted_bits += str( (int(encrypted_bits[i])^ int(key[i])) )
    # Convert bitstring into
    i = int(unencrypted_bits, 2)
    hex_string = '%x' % i
    n = len(hex_string)
    bits = binascii.unhexlify(hex_string.zfill(n + (n & 1)))
    unencrypted_string = bits.decode('utf-8', 'surrogatepass')
    return unencrypted_string


message = input("Please enter a message: ")
print("Original Message:", message)
bits = bin(int(binascii.hexlify(message.encode('utf-8', 'surrogatepass')), 16))[2:]
bitstring = bits.zfill(8 * ((len(bits) + 7) // 8))

alice_bits = [] #This list will store Alice's bits
for i in range(3*len(bitstring)):  
    alice_bits.append(str(getrandbits(1))) 

alice_bases = [] # List to store Alice's bases
for i in range(3*len(bitstring)):
    base = getrandbits(1)
    if base == 0:
        alice_bases.append("Z")
    else:
        alice_bases.append("X")

encoded_qubits = []
for i in range(3*len(bitstring)):
    qc = QuantumCircuit(1,1)
    if alice_bases[i] == "Z":
        if alice_bits[i] == '0':
            pass # We want nothing to happen here - the qubit is already in the state |0>

        elif alice_bits[i] == '1':
            qc.x(0) # Applying an X gate to change the qubit state to |1>
            
    elif alice_bases[i] == "X":
        if alice_bits[i] == '0':
            qc.h(0) # Applying an H gate to change the qubit state to |+>
        elif alice_bits[i] == '1':
            qc.x(0) # Applying an X and H gate to change the qubit state to |->
            qc.h(0)
            
    encoded_qubits.append(qc) # Adding the qubit with the right state to the list of qubits that Alice will send Bob

bob_bases = []
for i in range(3*len(bitstring)):
    bit = getrandbits(1)
    if bit == 0:
        bob_bases.append("Z")
    else:
        bob_bases.append("X")

bob_bits = [] # List of Bob's bits generated from the results of Bob's measurements
    
for i in range(3*len(bitstring)):
    qc = encoded_qubits[i]
        
    if bob_bases[i] == "Z": # Bob's basis is Z
            qc.measure(0,0) #Code to measure in the Z basis
        

    elif bob_bases[i] == "X": #The case that bob_bases[i] is X
            qc.h(0) #WRITE CODE HERE: Bob needs to add a gate here to correctly measure in the X basis. Which gate is this?  
            qc.measure(0,0)  #Measurement in the X basis
            
            
      # Now that the measurements have been added to the circuit, let's run them.
    
    
    job = execute(qc, backend = Aer.get_backend("qasm_simulator", shots = 1) 
    results = job.result()
    counts = results.get_counts()
    measured_bit = max(counts, key=counts.get)

        # Append measured bit to Bob's measured bitstring
    bob_bits.append(measured_bit) 

agreeing_indices = []
    
for i in range(3*len(bitstring)):
    if alice_bases[i]==bob_bases[i]:
        agreeing_indices.append(i)

alice_key = []
for index in agreeing_indices:
    alice_key.append(alice_bits[index])

bob_key = []
for index in agreeing_indices:
    bob_key.append(bob_bits[index])

# Call the function encrypt_message with the right inputs
encrypted_message = encrypt_message(message,alice_key)
print("Encrypted message:", encrypted_message)

# Call the function deencrypt_message with the right inputs
decrypted_message = decrypt_message(encrypted_message, bob_key)
print("Decrypted message:", decrypted_message)