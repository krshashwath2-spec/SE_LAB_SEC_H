"""Track dairy farmers' milk collections using an in-memory SQLite database."""

import hashlib
import sqlite3


def create_connection() -> sqlite3.Connection:
    """Create an in-memory database and its milk collection table."""
    connection = sqlite3.connect(":memory:")
    connection.execute(
        """
        CREATE TABLE milk (
            id INTEGER PRIMARY KEY,
            farmer TEXT NOT NULL,
            litres REAL NOT NULL,
            fat REAL,
            day TEXT NOT NULL
        )
        """
    )
    return connection


def record_milk(
    connection: sqlite3.Connection,
    farmer: str,
    litres: float,
    fat: float,
    day: str,
) -> None:
    """Record one farmer's milk collection using a parameterized query."""
    connection.execute(
        """
        INSERT INTO milk (farmer, litres, fat, day)
        VALUES (?, ?, ?, ?)
        """,
        (farmer, litres, fat, day),
    )
    connection.commit()


def farmer_token(farmer: str) -> str:
    """Return a SHA-256 hexadecimal digest for a farmer's name."""
    return hashlib.sha256(farmer.encode("utf-8")).hexdigest()


def daily_total(connection: sqlite3.Connection, day: str) -> str:
    """Return the total litres of milk collected on a given day."""
    row = connection.execute(
        "SELECT COALESCE(SUM(litres), 0) FROM milk WHERE day = ?",
        (day,),
    ).fetchone()
    total_litres = row[0]
    return f"Total: {total_litres:.1f} litres"


def top_farmer(connection: sqlite3.Connection) -> str | None:
    """Return the farmer with the highest total milk volume, if available."""
    row = connection.execute(
        """
        SELECT farmer, SUM(litres) AS total_litres
        FROM milk
        GROUP BY farmer
        ORDER BY total_litres DESC, farmer ASC
        LIMIT 1
        """
    ).fetchone()
    return row[0] if row else None


def print_slip(farmer: str) -> None:
    """Print a collection-slip message without invoking a shell."""
    print(f"Printing slip for {farmer}")


def low_fat(connection: sqlite3.Connection) -> list[str]:
    """Return unique farmers with missing fat values or fat below 3.5."""
    rows = connection.execute(
        """
        SELECT DISTINCT farmer
        FROM milk
        WHERE fat IS NULL OR fat < ?
        ORDER BY farmer
        """,
        (3.5,),
    ).fetchall()
    return [row[0] for row in rows]


def main() -> None:
    """Run a demonstration of the dairy milk collection tracker."""
    connection = create_connection()
    try:
        record_milk(connection, "Gopal", 12.5, 4.1, "Mon")
        record_milk(connection, "Lata", 20.0, 3.2, "Mon")

        print(daily_total(connection, "Mon"))
        print("Top farmer:", top_farmer(connection))
        print("Low-fat farmers:", low_fat(connection))
        print_slip("Gopal")
        print("Farmer token:", farmer_token("Lata"))
    finally:
        connection.close()


if __name__ == "__main__":
    main()
