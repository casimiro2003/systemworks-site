"""
MongoDB CRUD CLI — Contact Book

A beginner-friendly tool that demonstrates the four core MongoDB operations
(Create, Read, Update, Delete) against a local MongoDB instance.

SETUP
  1. Install MongoDB Community Edition and start it:
       - macOS:  brew install mongodb-community && brew services start mongodb-community
       - Linux:  sudo systemctl start mongod
       - Docker: docker run -d -p 27017:27017 --name mongo mongo:7
  2. Install the Python driver:
       pip install pymongo
  3. Run this script:
       python contacts.py

CONCEPTS YOU'LL LEARN
  - Connecting to MongoDB with a connection string (URI)
  - Database -> Collection -> Document hierarchy (vs SQL's DB -> Table -> Row)
  - Documents are dictionaries (BSON under the hood)
  - ObjectId: MongoDB's default primary key
  - Query filters: {"field": value}, {"field": {"$regex": ...}}
  - Update operators: $set
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson import ObjectId
from bson.errors import InvalidId


MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "contact_book"
COLLECTION_NAME = "contacts"


def connect():
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
    # ping forces the driver to actually talk to the server so we fail fast
    # if MongoDB isn't running, instead of erroring later on the first query.
    client.admin.command("ping")
    return client[DB_NAME][COLLECTION_NAME]


def create_contact(contacts):
    name = input("Name: ").strip()
    email = input("Email: ").strip()
    phone = input("Phone: ").strip()

    document = {"name": name, "email": email, "phone": phone}
    result = contacts.insert_one(document)
    print(f"Added contact with id: {result.inserted_id}")


def list_contacts(contacts):
    docs = list(contacts.find())
    if not docs:
        print("No contacts yet.")
        return
    for doc in docs:
        print(f"  [{doc['_id']}] {doc['name']} | {doc['email']} | {doc['phone']}")


def search_contacts(contacts):
    term = input("Search name (case-insensitive): ").strip()
    # $regex with $options 'i' does case-insensitive partial matching.
    query = {"name": {"$regex": term, "$options": "i"}}
    docs = list(contacts.find(query))
    if not docs:
        print("No matches.")
        return
    for doc in docs:
        print(f"  [{doc['_id']}] {doc['name']} | {doc['email']} | {doc['phone']}")


def update_contact(contacts):
    raw_id = input("Contact id to update: ").strip()
    try:
        oid = ObjectId(raw_id)
    except InvalidId:
        print("Invalid id format.")
        return

    existing = contacts.find_one({"_id": oid})
    if not existing:
        print("No contact with that id.")
        return

    print("Press Enter to keep the current value.")
    name = input(f"Name [{existing['name']}]: ").strip() or existing["name"]
    email = input(f"Email [{existing['email']}]: ").strip() or existing["email"]
    phone = input(f"Phone [{existing['phone']}]: ").strip() or existing["phone"]

    # $set only modifies the listed fields; without it the whole doc gets replaced.
    contacts.update_one(
        {"_id": oid},
        {"$set": {"name": name, "email": email, "phone": phone}},
    )
    print("Updated.")


def delete_contact(contacts):
    raw_id = input("Contact id to delete: ").strip()
    try:
        oid = ObjectId(raw_id)
    except InvalidId:
        print("Invalid id format.")
        return

    result = contacts.delete_one({"_id": oid})
    if result.deleted_count:
        print("Deleted.")
    else:
        print("No contact with that id.")


MENU = """
Contact Book
  1. Add contact
  2. List all
  3. Search by name
  4. Update contact
  5. Delete contact
  6. Quit
Choose: """


def main():
    try:
        contacts = connect()
    except ConnectionFailure:
        print("Could not connect to MongoDB at", MONGO_URI)
        print("Make sure mongod is running (see SETUP at top of file).")
        return

    actions = {
        "1": create_contact,
        "2": list_contacts,
        "3": search_contacts,
        "4": update_contact,
        "5": delete_contact,
    }

    while True:
        choice = input(MENU).strip()
        if choice == "6":
            break
        action = actions.get(choice)
        if action:
            action(contacts)
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
