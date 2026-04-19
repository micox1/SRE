'''
We're adding user authentication to the platform. You're building the User class that everything 
else will depend on, so get it right.

A User is constructed from a username and a plaintext password. The plaintext never gets stored — 
hash it immediately using SHA-256 and keep that hashing logic as a static method on the class itself. 
Accounts start unlocked with no failed attempts. There's a lockout threshold that applies globally 
across all users, and it needs to be adjustable at runtime without touching individual instances. 
Failed logins increment a counter — hit the threshold and the account locks. Locked accounts can be 
manually reset.

Expose the lock status through a property rather than the raw attribute. Think carefully about why 
that distinction matters and what it buys you down the line. Same goes for the static method — think 
about why it belongs on the class rather than floating at the module level.

Before you call it done, test what happens when you change the lockout threshold on a single 
instance instead of the class. Make sure you understand what you're seeing.

Deliver clean, working code. Be prepared to walk through every decision you made.
'''

from hashlib import sha256

