# import psycopg2
# from unidecode import unidecode
# import os
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# try:
#     # Get database credentials from environment variables
#     DB_HOST = os.getenv("DB_HOST")
#     DB_PORT = os.getenv("DB_PORT")
#     DB_NAME = os.getenv("DB_NAME")
#     DB_USER = os.getenv("DB_USER")
#     DB_PASSWORD = os.getenv("DB_PASSWORD")

#     # Connect to your database using context manager
#     with psycopg2.connect(
#         host=DB_HOST,
#         port=DB_PORT,
#         database=DB_NAME,
#         user=DB_USER,
#         password=DB_PASSWORD
#     ) as conn:
#         # Create a cursor object within the context manager
#         with conn.cursor() as cur:
#             # Fetch all customer names from the customers table
#             cur.execute("SELECT id, name FROM customers")
#             # Iterate through the rows and transliterate non-Latin names to Latin names
#             for row in cur.fetchall():
#                 customer_id, original_name = row
#                 latin_name = unidecode(original_name)  # Transliterate the name to Latin characters
#                 # Update the customers table with the Latin name
#                 cur.execute("UPDATE customers SET name = %s WHERE id = %s", (latin_name, customer_id))

#             # Commit the changes to the database
#             conn.commit()

#     print("Conversion completed. Non-Latin names have been transliterated to Latin characters.")

# except psycopg2.Error as e:
#     print(f"Error: {e}")
# except Exception as e:
#     print(f"An unexpected error occurred: {e}")




def translate_geez_to_latin(geez_text, dictionary):
    latin_text = ""
    for char in geez_text:
        if char in dictionary:
            latin_text += dictionary[char]
        else:
            latin_text += char
    return latin_text

# Example dictionary mapping Geez characters to Latin equivalents
geez_to_latin_dict = {
    "ሙ": "w",
    "ሉ": "xu",
    "ዳ": "d",
    "ኘ": "n",
    "ው": "w",
    "ተ": "t",
    "ፈ": "f",
    "ራ": "r",
    # Add more mappings as needed
}

# Example Geez text
geez_text = "ሙሉ ዳኘው ተፈራ"

# Translate Geez text to Latin using the custom dictionary
latin_text = translate_geez_to_latin(geez_text, geez_to_latin_dict)

print(latin_text)





