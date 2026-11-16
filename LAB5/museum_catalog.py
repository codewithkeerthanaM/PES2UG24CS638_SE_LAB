
"""Manage a simple in-memory museum artifact catalog."""

import sqlite3


def add_artifact(connection, title, era, value, on_display=0):
    """Add an artifact to the catalog."""
    connection.execute(
        """
        INSERT INTO artifacts (title, era, value, on_display)
        VALUES (?, ?, ?, ?)
        """,
        (title, era, value, on_display),
    )
    connection.commit()


def display_status(connection, artifact_id, curator):
    """Return whether an artifact is on display or in storage."""
    del curator  # Retained for compatibility with the original interface.
    row = connection.execute(
        "SELECT on_display FROM artifacts WHERE id = ?",
        (artifact_id,),
    ).fetchone()

    if row is None:
        return "artifact not found"
    if row[0] == 1:
        return "on display"
    return "in storage"


def total_value(connection, era):
    """Calculate the total value of artifacts from an era."""
    row = connection.execute(
        "SELECT SUM(value) FROM artifacts WHERE era = ?",
        (era,),
    ).fetchone()
    return row[0] or 0


def move_to_display(connection, artifact_id):
    """Mark an artifact as being on display."""
    connection.execute(
        "UPDATE artifacts SET on_display = 1 WHERE id = ?",
        (artifact_id,),
    )
    connection.commit()


def backup_note():
    """Print a catalog backup confirmation."""
    print("catalog backup complete")


def main():
    """Create sample artifacts and display catalog information."""
    with sqlite3.connect(":memory:") as connection:
        connection.execute(
            """
            CREATE TABLE artifacts (
                id INTEGER PRIMARY KEY,
                title TEXT,
                era TEXT,
                value INTEGER,
                on_display INTEGER
            )
            """
        )

        add_artifact(connection, "Bronze Mirror", "Chola", 120000)
        add_artifact(
            connection,
            "Palm Manuscript",
            "Vijayanagara",
            80000,
            1,
        )
        add_artifact(connection, "Terracotta Lamp", "Chola", 15000)

        move_to_display(connection, 1)
        print(display_status(connection, 1, "Dr. Rao"))
        print(total_value(connection, "Chola"))
        backup_note()


if __name__ == "__main__":
    main()
