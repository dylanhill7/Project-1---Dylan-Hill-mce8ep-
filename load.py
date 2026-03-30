import duckdb
import logging
import os
from pathlib import Path

# -------------------------------
# Logging setup
# -------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="load.log"
)
logger = logging.getLogger(__name__)


# -------------------------------
# Configuration
# -------------------------------
DB_NAME = "mlb_analysis.duckdb"

# Update these paths to match your folders (think about this in terms of github, not local machine)
AGE_20_25_FOLDER = "Data/20-25" 
AGE_30_35_FOLDER = "Data/30-35"

# Excluding 2020, 2000-2025 (lower bound included, upper bound excluded)
YEARS = [y for y in range(2000, 2026) if y != 2020]

AGE_20_25_PATTERN = "20-25({year}).csv"
AGE_30_35_PATTERN = "30-35({year}).csv"


# -------------------------------
# Helper functions
# -------------------------------

# function to check if a table already exists in duckDB
def table_exists(con, table_name):
    """
    Check whether a table already exists in DuckDB.
    """
    query = """
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = ?
    """
    result = con.execute(query, [table_name]).fetchone()[0]
    return result > 0

# function to check if a file exists, and raise an error if it doesn't
def validate_file_exists(file_path):
    """
    Raise an error if a required file does not exist.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Required file not found: {file_path}")

# function that loads in all CSVs (all years) for a given age group and appends 
# season column for each file with value in that column reflecting the year
def load_age_group_table(con, table_name, folder_path, file_pattern, years):
    """
    Load all CSVs for one age group into DuckDB and append a Season column
    based on the file's year.
    """
    if table_exists(con, table_name):
        logger.info("Table '%s' already exists. Skipping load.", table_name)
        print(f"'{table_name}' already exists, nothing to load.")
        return

    first_file_loaded = False

    for year in years:
        file_name = file_pattern.format(year=year)
        file_path = os.path.join(folder_path, file_name)

        try:
            validate_file_exists(file_path)

            if not first_file_loaded:
                # Create table from first file and append Season column
                con.execute(f"""
                    CREATE TABLE {table_name} AS
                    SELECT
                        *,
                        ? AS Season
                    FROM read_csv_auto(?, HEADER=TRUE)
                """, [year, file_path])

                logger.info(
                    "Created table '%s' from file %s with Season=%s",
                    table_name, file_path, year
                )
                print(f"Created '{table_name}' with {file_name} (Season={year})")
                first_file_loaded = True

            else:
                # Insert remaining files with appended Season column
                con.execute(f"""
                    INSERT INTO {table_name}
                    SELECT
                        *,
                        ? AS Season
                    FROM read_csv_auto(?, HEADER=TRUE)
                """, [year, file_path])

                logger.info(
                    "Inserted file %s into '%s' with Season=%s",
                    file_path, table_name, year
                )
                print(f"Loaded {file_name} into '{table_name}' (Season={year})")

        except FileNotFoundError as fnf_error:
            logger.error("Missing file for table '%s': %s", table_name, fnf_error)
            print(f"Missing file: {fnf_error}")
            raise

        except Exception as e:
            logger.error("Failed while loading %s into %s: %s", file_path, table_name, e)
            print(f"An error occurred while loading {file_name}: {e}")
            raise

# prints and logs basic summary info for a table
def print_table_summary(con, table_name):
    try:
        row_count = con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        logger.info("Total rows in '%s': %s", table_name, row_count)
        print(f"Total rows in '{table_name}': {row_count}")

        summary = con.execute(f"""
            SELECT
                MIN(Season) AS min_season,
                MAX(Season) AS max_season,
                COUNT(DISTINCT Name) AS unique_players
            FROM {table_name}
        """).fetchone()

        min_season, max_season, unique_players = summary

        summary_str = (
            f"Summary for '{table_name}':\n"
            f"  Seasons covered: {min_season} to {max_season}\n"
            f"  Unique players: {unique_players}\n"
        )

        logger.info(summary_str)
        print(summary_str)

    except Exception as e:
        logger.error("Could not summarize table '%s': %s", table_name, e)
        print(f"Could not summarize '{table_name}': {e}")


# -------------------------------
# Main loader, where database connection is established and all loading functions are called
# -------------------------------
def load_mlb_data():
    con = None

    try:
        con = duckdb.connect(database=DB_NAME, read_only=False)
        logger.info("Connected to DuckDB database: %s", DB_NAME)
        print(f"Connected to DuckDB database: {DB_NAME}")

        age_20_25_folder = str(Path(AGE_20_25_FOLDER))
        age_30_35_folder = str(Path(AGE_30_35_FOLDER))

        load_age_group_table(
            con=con,
            table_name="hitters_20_25",
            folder_path=age_20_25_folder,
            file_pattern=AGE_20_25_PATTERN,
            years=YEARS
        )

        load_age_group_table(
            con=con,
            table_name="hitters_30_35",
            folder_path=age_30_35_folder,
            file_pattern=AGE_30_35_PATTERN,
            years=YEARS
        )

        print_table_summary(con, "hitters_20_25")
        print_table_summary(con, "hitters_30_35")

        logger.info("Finished loading all MLB Fangraphs data.")
        print("Finished loading all MLB Fangraphs data.")

    except Exception as e:
        logger.error("An error occurred in load_mlb_data: %s", e)
        print(f"An error occurred: {e}")

    finally:
        if con:
            con.close()
            logger.info("DuckDB connection closed.")
            print("DuckDB connection closed.")

if __name__ == "__main__":
    load_mlb_data()