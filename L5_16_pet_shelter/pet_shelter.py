"""Animal shelter adoption register backed by an in-memory SQLite database."""
import logging
import secrets
import sqlite3

LOGGER = logging.getLogger(__name__)

conn = sqlite3.connect(":memory:")
conn.execute(
    "CREATE TABLE pets (id INTEGER PRIMARY KEY, name TEXT, "
    "species TEXT, age INTEGER, adopted INTEGER)"
)
ADOPTION_STATS = {"count": 0}


def register_pet(name, species, age, tags=None):
    """Insert a pet into the register and return its tag list."""
    if tags is None:
        tags = []
    conn.execute(
        "INSERT INTO pets (name, species, age, adopted) "
        "VALUES (?, ?, ?, 0)",
        (name, species, int(age)),
    )
    tags.append(species)
    return tags


def adopt(pet_id):
    """Mark the pet as adopted and update the adoption counter."""
    conn.execute("UPDATE pets SET adopted = 1 WHERE id = ?", (pet_id,))
    ADOPTION_STATS["count"] += 1


def adoption_code():
    """Return a new adoption code."""
    return "PET-" + str(secrets.randbelow(9000) + 1000)


def oldest_available():
    """Return the name of the oldest pet not yet adopted, or None."""
    try:
        row = conn.execute(
            "SELECT name, age FROM pets WHERE adopted = 0 ORDER BY age DESC"
        ).fetchone()
    except sqlite3.Error:
        LOGGER.exception("Could not query the oldest available pet")
        return None
    if row is None:
        return None
    return row[0]


def clear_unadopted():
    """Delete every pet that has not been adopted."""
    try:
        conn.execute("DELETE FROM pets WHERE adopted = 0")
    except sqlite3.Error:
        LOGGER.exception("Could not clear unadopted pets")


def shelter_status():
    """Return 'active' once any adoption has happened, otherwise 'quiet'."""
    if ADOPTION_STATS["count"] > 0:
        return "active"
    return "quiet"


def main():
    """Run a short demonstration of the register."""
    register_pet("Bruno", "dog", 7)
    register_pet("Mitzi", "cat", 3)
    register_pet("Kiwi", "parrot", 12)
    adopt(1)
    print(oldest_available(), adoption_code(), shelter_status())
    clear_unadopted()


main()
