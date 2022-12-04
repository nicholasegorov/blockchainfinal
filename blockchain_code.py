# -*- coding: utf-8 -*-

#Nicholas Egorov ,Curtis Bishop, and Vithushan Vigneswaran
#December 6th 2022
#Final Project Voting System Application

#Imports
import hashlib
import json
from time import time
from hashlib import pbkdf2_hmac
import os


#Blockchain object class
class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.new_block(previous_hash=" ",
                       proof=1)

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.pending_transactions = []
        self.chain.append(block)
        return block

    @property
    def last_block(self):
        return self.chain[-1]

    def new_transaction(self, voter, candidate, count):
        transaction = {
            'voter': voter,
            'candidate': candidate,
            'count': count
        }
        self.pending_transactions.append(transaction)
        return self.last_block['index'] + 1

    def hash(self, block):
      #dumps the data block into a string
        string_object = json.dumps(block, sort_keys=True)
        #we then encode the string
        block_string = string_object.encode()
        #creating a psudeorandom string being the salt with a size of 16
        randomsalt = os.urandom(16)
        #we then use key direvation and encode the string with sha256 with the random salt 
        # and we do 1000 iterations of this
        nestedHex = pbkdf2_hmac('sha256',block_string,randomsalt,1000)
        #convert the final output to a hex
        newNestedHex = nestedHex.hex()
        #we then hash that into a sha512
        hex_hash = hashlib.sha512(newNestedHex.encode())
        #convert it to a hexidecimal and return it
        newHex = hex_hash.hexdigest()
        return newHex


# Added a database to store the voters information and candidate options
database = []
# Place holders for the names of the candidates
C1 = "JULIA"
C2 = "CLEMENT"
C3 = "PATRICK"
C4 = "SANTOS"
# Created a list so that we can check if the person people are voting for is in
# the database
lst = [C1,C2,C3,C4]


# Created a function to add the block
def blockadder():
    # Input for the identification of the voter
    Source = input("Input your ID:")
    # To check if the identification matches with another vote
    if Source in database:
      print("You have already voted!")
    else:
      # Print the choices for the candidates      
      print("1)", C1)
      print("2)", C2)
      print("3)", C3)
      print("4)", C4)        
      # Input for the vote
      Destination = input("Who are you voting for:")
      # Input validation checking if input is a number
      if Destination.isdigit():
        print("Enter Candidate name!")
      # Since we created a list for database and it has names checks if name 
      # in database
      elif Destination.upper() not in lst:
        print("Pick Valid Candidate!")
      # If name there switch to uppercase
      else:
        cand = Destination.upper()
        # Try and catch if we are getting a number as input for # of votes
        try:
          Count = int(input("How many votes:"))
        except: 
          print("Enter a valid number!")
          return
        # If it satisifes the code above add the block with the ID, Name & Count
        else:
          new_Block = blockchain.new_transaction(Source, cand, Count)
          # Appending the ID to the database so no double votes are counted
          database.append(Source)
          blockchain.new_block("1")
          return new_Block



