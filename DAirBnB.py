
#   dAirBB
#
#   _ a smart contract prototype for a decentralised 
#   accomodation rental market.
#   Guest and Host agreed a rental protocol that has 
#   been encoded in this Tezos smart contract.
#
#   (c) 2020 Andrea Bracciali and Siham Lamssaoui 

import smartpy as sp

class dAirBB(sp.Contract):
    host = sp.sender
    def __init__(self):
        self.init(
            guest = sp.test_account("VOID").address, 
            host = sp.test_account("VOID").address,
            nuki = sp.test_account("VOID").address,
            rent = sp.tez(0), 
            g_deposit = sp.tez(0), 
            h_deposit = sp.tez(0),
            active = False,         # G engaged/sent deposit
            in_house = False,       # G in house
            grace_ended = False,    # No more complaints
            complaint = False,      # G complained
            refund = False,         # G accepted refund
            # contract_id = 0,
            cp = 0) 

    @sp.entry_point
    def Contract_Call(self, params):
        
        sp.if (params.my_method == "Contract_Initialisation"):
            self.Contract_Initialisation(
                rent = params.rent, 
                g_deposit = params.g_deposit, 
                h_deposit = params.h_deposit, 
                host = params.host, 
                guest = params.guest,
                nuki = params.nuki,
                # contract_id = params.id,
                cp = params.cp)
        
        sp.if (params.my_method == "Cancellation_Host"):
            self.Cancellation_Host()
            
        sp.if (params.my_method == "Send_Deposit_Guest"):
            self.Send_Deposit_Guest(g_deposit = params.g_deposit, rent = params.rent, guest = params.guest)
  
        sp.if (params.my_method == "Cancellation_Guest"):
            self.Cancellation_Guest()
  
        sp.if (params.my_method == "Door_Opened"):
            self.Door_Opened(nuki = params.nuki) 
            
        sp.if (params.my_method == "Grace_Period_Ended"):
            self.Grace_Period_Ended()
            
        sp.if (params.my_method == "Guest_Complains"):
            self.Guest_Complains()
            
        sp.if (params.my_method == "Guest_Accepts_Refund"):
            self.Guest_Accepts_Refund()

        sp.if (params.my_method == "Guest_Leaves_Contract"):
            self.Guest_Leaves_Contract()

        sp.if (params.my_method == "End_Of_Rent"):
            self.End_Of_Rent()




    # __Whoever__ runs this and pays the h_deposit is the host
    # The Guest will be identified when paying the g_deposit
    #
    def Contract_Initialisation(self, rent, g_deposit, h_deposit, host, guest, nuki, cp): 
        self.data.rent = rent
        self.data.g_deposit = g_deposit
        self.data.h_deposit = h_deposit
        self.data.host = host
        self.data.guest = guest
        self.data.nuki = nuki
        self.data.cp = cp
        #                The follwoing for resetting purposes
        #                when testing the contract.
        #  >>>>>>        TOBEDONE: reset the balance to 0
        #
        self.active = False,         # G engaged/sent deposit
        self.in_house = False,       # G in house
        self.grace_ended = False,    # No more complaints
        self.complaint = False,      # G complained
        self.refund = False,         # G accepted refund
        # self.data.contract_id = id
        sp.verify(h_deposit == sp.amount)
        sp.verify(self.data.host == sp.sender)
        
        
    # IF the host exists and is the sender, h_deposit has been paid and can be refunded
    # IF the guest exists, the guest gets h_deposit as cancellation fee + g_deposit + rent
    # ONLY IF the rental did not start
    #
    def Cancellation_Host(self):
        sp.verify(self.data.host == sp.sender)
        sp.verify(self.data.in_house == False)
        sp.if (self.data.guest == sp.test_account("VOID").address): 
            sp.send(self.data.host, self.data.h_deposit)
        sp.if (~ (self.data.guest == sp.test_account("VOID").address)):
            sp.send(self.data.guest, (self.data.h_deposit + self.data.g_deposit))


    # G, the one declared in the call and nobody else, pays the agreed deposit and rent,
    # and therefore is registered as guest
    # NOTE here  the request of declaring who G is that has 
    # to be coherent with the sender of the tx.
    #
    def Send_Deposit_Guest(self, g_deposit, rent, guest):
        sp.verify(sp.sender == guest)
        sp.verify(sp.amount == (self.data.g_deposit + self.data.rent))
        self.data.active = True
        self.data.guest = sp.sender
        
        
    # IF G exists, recorded in the system and hence did pay deposit, and is the sender, 
    # can cancel and get refunded according to the agreed policy. To start with, 
    # the policy is 100% of the deposit. H gets H's deposit + deposit of G.
    # This is the basic policy chosen, more elaborate policies, e.g. tracking average
    # income for the flat or protecting G from double renting (see paper), can be 
    # defined at negotiation time. When the contract is built.
    #
    def Cancellation_Guest(self):
        sp.verify(self.data.guest == sp.sender)
        sp.verify(self.data.active == True)
        sp.verify(self.data.in_house == False)
        sp.if (self.data.host == sp.test_account("VOID").address): 
            sp.send(self.data.guest, self.data.g_deposit)
            sp.send(self.data.guest, self.data.rent)
        sp.if (~ (self.data.host == sp.test_account("VOID").address)):
            sp.send(self.data.host, self.data.h_deposit)
            sp.send(self.data.host, self.data.g_deposit)
            sp.send(self.data.guest, self.data.rent)


    # Nuki is a recorded participant, it does two things: 
    # - it notifies that the flat has been accessed, and 
    # - prompt for the end of the grace period.
    # Nuki plays the part of a trusted oracle (although 
    # some checks are possible, like only_once.
    # TOBEDONE: add contract ID and check it - one single 
    # nuki could tamper with different rentals, uncorrectly
    #
    def Door_Opened(self, nuki):
        sp.verify( ~(self.data.in_house) )
        sp.verify(sp.sender == nuki)
        self.data.in_house = True

    # G complains about the flat. Must happen before the end 
    # of the grace period. And G has to be in house.
    #
    def Guest_Complains(self):
        sp.verify(sp.sender == self.data.guest)
        sp.verify( ~(self.data.grace_ended) )
        sp.verify(self.data.in_house)
        self.data.complaint = True


    # G accepts refund after complaints. H offered somehow.
    # This will be taken in consideration by the final payment.
    # Can be done only after a complaint, and if G is still in
    # house - e.g. has not left the rental.
    # TOBEDONE (naive: G can always complaint - currently 
    # H implicitly always offers refund!)
    #
    def Guest_Accepts_Refund(self):
        sp.verify(sp.sender == self.data.guest)
        sp.verify(self.data.in_house)
        sp.verify(self.data.complaint)
        self.data.refund = True

    # G does not accept the refund after complaints. 
    # Or may be G leaves anyway at any time.
    # G looses all  --  in_house = False
    #
    def Guest_Leaves_Contract(self):
        sp.verify(sp.sender == self.data.guest)
        sp.verify(self.data.active == True)
        sp.verify(self.data.in_house == True)
        self.data.guest = sp.test_account("VOID").address
        self.data.in_house = False
        self.data.active = False


    # Same kind of synch event from N as Door_Opened
    # CAREFULL: if G left, and reasonably the contract has 
    # been liquidated, there might not be any money in 
    # the balance of the contract.
    # 
    
    #
    def Grace_Period_Ended(self):
        sp.verify(sp.sender == self.data.nuki)
        self.data.grace_ended = True
        sp.send(self.data.host, sp.split_tokens(self.data.rent, 1, 2))

    
    # End of play: Nuki notifies that the flat has been left.
    # C pays what due at the successful completion of the agreement. 
    # If G has left, or has not entered the flat, H gets all
    # 
    def End_Of_Rent(self): 
        sp.verify(sp.sender == self.data.nuki)
        sp.if ( (~ (self.data.active)) | (~ (self.data.in_house)) ):
            sp.send(self.data.host, sp.balance)
        sp.if (self.data.refund & self.data.in_house):
            # H gets 1/4 rent + deposit
            sp.send(self.data.host, sp.split_tokens(self.data.rent, 1, 4))
            sp.send(self.data.host, self.data.h_deposit)
            # G gets 1/4 rent (refund) + deposit
            sp.send(self.data.guest, sp.split_tokens(self.data.rent, 1, 4))
            sp.send(self.data.guest, self.data.g_deposit)
        sp.if ( ~(self.data.refund) & self.data.in_house):
            # H gets the remaining 1/2 rent + deposit
            sp.send(self.data.host, sp.split_tokens(self.data.rent, 1, 2))
            sp.send(self.data.host, self.data.h_deposit)
            # G gets deposit
            sp.send(self.data.guest, self.data.g_deposit)
        self.data.in_house = False
        # ABORT CONTRACT
    
    
    
    
    
# ---------------------------------  TEST

@sp.add_test(name = "My_dAirBB")
def test():
   
   
    gaia   = sp.test_account("Gaia")
    herbert = sp.test_account("Herbert")
    nuki = sp.test_account("Nuki")
    void = sp.test_account("VOID")
    
    c1 = dAirBB()
    
    scenario  = sp.test_scenario()
    scenario += c1

    scenario.h1("Payment for real")


    scenario.h2("Accounts")
    scenario.show([herbert, gaia, nuki, void])
    
    scenario.h2("Contract Initialisation")
    scenario += c1.Contract_Call(
            my_method = "Contract_Initialisation", 
            rent = sp.tez(30), 
            #start_date = "00",
            #dep_date = "10",
            g_deposit = sp.tez(10), 
            h_deposit = sp.tez(15),
            host = herbert.address,
            guest = gaia.address,
            nuki = nuki.address,
            cp = 0
            ).run(sender = herbert, amount = sp.tez(15))

    scenario.h2("Cancellation Host")
    scenario += c1.Contract_Call(
            my_method = "Cancellation_Host",
            rent = sp.tez(0), 
            #start_date = "00",
            #dep_date = "00",
            g_deposit = sp.tez(0), 
            h_deposit = sp.tez(0),
            host = herbert.address,
            guest = gaia.address,
            nuki = nuki.address,
            cp = 0).run(sender = herbert)

    scenario.h2("Send Deposit Guest")
    scenario += c1.Contract_Call(
            my_method = "Send_Deposit_Guest",
            rent = sp.tez(30), 
            #start_date = "00",
            #dep_date = "00",
            g_deposit = sp.tez(10), 
            h_deposit = sp.tez(0),
            host = herbert.address,
            guest = gaia.address,
            nuki = nuki.address,
            cp = 0).run(sender = gaia, amount = sp.tez(40))
    
    scenario.h2("Deposit Guest (FAKE guest)")
    scenario += c1.Contract_Call(
            my_method = "Send_Deposit_Guest",
            rent = sp.tez(30), 
            #start_date = "00",
            #dep_date = "00",
            g_deposit = sp.tez(10), 
            h_deposit = sp.tez(0),
            host = herbert.address,
            guest = gaia.address,
            nuki = nuki.address,
            cp = 0).run(sender = void, amount = sp.tez(40), valid = False)
 
    scenario.h2("Deposit Guest (FAKE not enough money)")
    scenario += c1.Contract_Call(
            my_method = "Send_Deposit_Guest",
            rent = sp.tez(30), 
            #start_date = "00",
            #dep_date = "00",
            g_deposit = sp.tez(10), 
            h_deposit = sp.tez(0),
            host = herbert.address,
            guest = gaia.address,
            nuki = nuki.address,
            cp = 0).run(sender = gaia, amount = sp.tez(39), valid = False)
            
    scenario.h2("Cancellation Guest")
    scenario += c1.Contract_Call(
            my_method = "Cancellation_Guest",
            rent = sp.tez(30), 
            #start_date = "00",
            #dep_date = "00",
            g_deposit = sp.tez(10), 
            h_deposit = sp.tez(15),
            host = herbert.address,
            guest = gaia.address,
            nuki = nuki.address,
            cp = 0).run(sender = gaia) 
            
    scenario.h2("Door Opened")
    scenario += c1.Contract_Call(
            my_method = "Door_Opened",
            rent = sp.tez(0), 
            #start_date = "00",
            #dep_date = "00",
            g_deposit = sp.tez(0), 
            h_deposit = sp.tez(0),
            host = herbert.address,
            guest = gaia.address,
            nuki = nuki.address,
            cp = 0).run(sender = nuki)
    
    scenario.h2("Door Opened FAKE - already opened")
    scenario += c1.Contract_Call(
            my_method = "Door_Opened",
            rent = sp.tez(0), 
            #start_date = "00",
            #dep_date = "00",
            g_deposit = sp.tez(0), 
            h_deposit = sp.tez(0),
            host = herbert.address,
            guest = gaia.address,
            nuki = nuki.address,
            cp = 0).run(sender = nuki, valid = False)
            
    scenario.h2("Guest Complains")
    scenario += c1.Contract_Call(
            my_method = "Guest_Complains",
            rent = sp.tez(0), 
            #start_date = "00",
            #dep_date = "00",
            g_deposit = sp.tez(0), 
            h_deposit = sp.tez(0),
            host = herbert.address,
            guest = gaia.address,
            nuki = nuki.address,
            cp = 0).run(sender = gaia)
    
    scenario.h2("Grace Eneded")
    scenario += c1.Contract_Call(
            my_method = "Grace_Period_Ended",
            rent = sp.tez(0), 
            #start_date = "00",
            #dep_date = "00",
            g_deposit = sp.tez(0), 
            h_deposit = sp.tez(0),
            host = herbert.address,
            guest = gaia.address,
            nuki = nuki.address,
            cp = 0).run(sender = nuki)
            
    scenario.h2("Guest Complains FAKE - too late, grace ended")
    scenario += c1.Contract_Call(
            my_method = "Guest_Complains",
            rent = sp.tez(0), 
            #start_date = "00",
            #dep_date = "00",
            g_deposit = sp.tez(0), 
            h_deposit = sp.tez(0),
            host = herbert.address,
            guest = gaia.address,
            nuki = nuki.address,
            cp = 0).run(sender = gaia, valid = False)
            
    scenario.h2("Guest Accepts Refund")
    scenario += c1.Contract_Call(
            my_method = "Guest_Accepts_Refund",
            rent = sp.tez(0), 
            #start_date = "00",
            #dep_date = "00",
            g_deposit = sp.tez(0), 
            h_deposit = sp.tez(0),
            host = herbert.address,
            guest = gaia.address,
            nuki = nuki.address,
            cp = 0).run(sender = gaia)
            
            
            
    #  RUN AS LAST -- UNFINISEHD        
    scenario.h2("Guest Leaves -- TBC <<< does not work add does not change")
    scenario += c1.Contract_Call(
            my_method = "Guest_Leaves_Contract",
            rent = sp.tez(0), 
            #start_date = "00",
            #dep_date = "00",
            g_deposit = sp.tez(0), 
            h_deposit = sp.tez(0),
            host = herbert.address,
            guest = gaia.address,
            nuki = nuki.address,
            cp = 0).run(sender = gaia)
            

  
#  ---------------------------------------------
@sp.add_test(name = "Rental with refund")
def test():
   
      
    gaia   = sp.test_account("Gaia")
    herbert = sp.test_account("Herbert")
    nuki = sp.test_account("Nuki")
    void = sp.test_account("VOID")
    
    c1 = dAirBB()
  
    scenario = sp.test_scenario()
    scenario += c1

    scenario.h1("Init/G_deposit/In_house/Complaint/Accept/End")


    scenario.h2("Accounts")
    scenario.show([herbert, gaia, nuki, void])
    
    scenario.h2("Contract Initialisation")
    scenario += c1.Contract_Call(
            my_method = "Contract_Initialisation", 
            rent = sp.tez(30), 
            #start_date = "00",
            #dep_date = "10",
            g_deposit = sp.tez(10), 
            h_deposit = sp.tez(15),
            host = herbert.address,
            guest = gaia.address,
            nuki = nuki.address,
            cp = 0
            ).run(sender = herbert, amount = sp.tez(15))
            
    # G cannot cancel before the contract is active, i.e.
    # G has paid the deposit. Fails - see valid = False
    #
    scenario.h2("Cancellation Guest")
    scenario += c1.Contract_Call(
            my_method = "Cancellation_Guest",
            rent = sp.tez(30), 
            #start_date = "00",
            #dep_date = "00",
            g_deposit = sp.tez(10), 
            h_deposit = sp.tez(15),
            host = herbert.address,
            guest = gaia.address,
            nuki = nuki.address,
            cp = 0).run(sender = gaia, valid = False) 

    scenario.h2("Deposit Guest")
    scenario += c1.Contract_Call(
            my_method = "Send_Deposit_Guest",
            rent = sp.tez(30), 
            #start_date = "00",
            #dep_date = "00",
            g_deposit = sp.tez(10), 
            h_deposit = sp.tez(0),
            host = herbert.address,
            guest = gaia.address,
            nuki = nuki.address,
            cp = 0).run(sender = gaia, amount = sp.tez(40))
            
    scenario.h2("Door Opened")
    scenario += c1.Contract_Call(
            my_method = "Door_Opened",
            rent = sp.tez(0), 
            #start_date = "00",
            #dep_date = "00",
            g_deposit = sp.tez(0), 
            h_deposit = sp.tez(0),
            host = herbert.address,
            guest = gaia.address,
            nuki = nuki.address,
            cp = 0).run(sender = nuki)
            
    scenario.h2("Guest Complains")
    scenario += c1.Contract_Call(
            my_method = "Guest_Complains",
            rent = sp.tez(0), 
            #start_date = "00",
            #dep_date = "00",
            g_deposit = sp.tez(0), 
            h_deposit = sp.tez(0),
            host = herbert.address,
            guest = gaia.address,
            nuki = nuki.address,
            cp = 0).run(sender = gaia)
    
    scenario.h2("Grace Eneded")
    scenario += c1.Contract_Call(
            my_method = "Grace_Period_Ended",
            rent = sp.tez(0), 
            #start_date = "00",
            #dep_date = "00",
            g_deposit = sp.tez(0), 
            h_deposit = sp.tez(0),
            host = herbert.address,
            guest = gaia.address,
            nuki = nuki.address,
            cp = 0).run(sender = nuki)
            
    scenario.h2("Guest Accepts Refund")
    scenario += c1.Contract_Call(
            my_method = "Guest_Accepts_Refund",
            rent = sp.tez(0), 
            #start_date = "00",
            #dep_date = "00",
            g_deposit = sp.tez(0), 
            h_deposit = sp.tez(0),
            host = herbert.address,
            guest = gaia.address,
            nuki = nuki.address,
            cp = 0).run(sender = gaia)
            
    #
    #   Run as disaster scenario ...
    #
    # scenario.h2("Guest Leaves Contract")
    # scenario += c1.Contract_Call(
    #         my_method = "Guest_Leaves_Contract",
    #         rent = sp.tez(0), 
    #         #start_date = "00",
    #         #dep_date = "00",
    #         g_deposit = sp.tez(0), 
    #         h_deposit = sp.tez(0),
    #         host = herbert.address,
    #         guest = gaia.address,
    #         nuki = nuki.address,
    #         cp = 0).run(sender = gaia)
            
    scenario.h2("End Of Rent")
    scenario += c1.Contract_Call(
            my_method = "End_Of_Rent",
            rent = sp.tez(0), 
            #start_date = "00",
            #dep_date = "00",
            g_deposit = sp.tez(0), 
            h_deposit = sp.tez(0),
            host = herbert.address,
            guest = gaia.address,
            nuki = nuki.address,
            cp = 0).run(sender = nuki)
            
# ----------------------------------------------END TEXT



            
