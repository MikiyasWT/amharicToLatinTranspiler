import psycopg2
import os
from dotenv import load_dotenv  # Import load_dotenv here
from tqdm import tqdm


#dictionary
def translate_geez_to_latin(geez_text):
    # Example dictionary mapping Geez characters to Latin equivalents
    geez_to_latin_dict = {
        "ሀ": "ha", "ሁ": "hu", "ሂ": "hi", "ሃ": "ha", "ሄ": "he", "ህ": "h", "ሆ": "ho",
        "ለ": "le", "ሉ": "lu", "ሊ": "li", "ላ": "la", "ሌ": "le", "ል": "l", "ሎ": "lo", "ሏ": "lua",
        "ሐ": "ha", "ሑ": "hu", "ሒ": "hi", "ሓ": "ha", "ሔ": "he", "ሕ": "h", "ሖ": "ho", "ሗ": "hua",
        "መ": "me", "ሙ": "mu", "ሚ": "mi", "ማ": "ma", "ሜ": "me", "ም": "m", "ሞ": "mo",
        "ሰ": "se", "ሱ": "su", "ሲ": "si", "ሳ": "sa", "ሴ": "se", "ስ": "s", "ሶ": "so", "ሷ": "sua",
        "ሠ": "se", "ሡ": "su", "ሢ": "si", "ሣ": "sa", "ሤ": "se", "ሥ": "s", "ሦ": "so", "ሧ": "sua",
        "ረ": "re", "ሩ": "ru", "ሪ": "ri", "ራ": "ra", "ሬ": "rie", "ር": "r", "ሮ": "ro", "ሯ": "rua",
        "ቀ": "qe", "ቁ": "qu", "ቂ": "qi", "ቃ": "qa", "ቄ": "qie", "ቅ": "q", "ቆ": "qo", "ቋ": "qua", "ቕ": "qee",
        "ሸ": "she", "ሹ": "shu", "ሺ": "shi", "ሻ": "sha", "ሼ": "shie", "ሽ": "sh", "ሾ": "sho", "ሿ": "shua",
        "በ": "be", "ቡ": "bu", "ቢ": "bi", "ባ": "ba", "ቤ": "bie", "ብ": "b", "ቦ": "bo", "ቧ": "bua",
        "ተ": "te", "ቱ": "tu", "ቲ": "ti", "ታ": "ta", "ቴ": "tie", "ት": "t", "ቶ": "to", "ቷ": "tua",
        "ቸ": "che", "ቹ": "chu", "ቺ": "chi", "ቻ": "cha", "ቼ": "chie", "ች": "ch", "ቾ": "cho", "ቿ": "chua",
        "ኀ": "he", "ኁ": "hu", "ኂ": "hi", "ኃ": "ha", "ኄ": "hie", "ኅ": "h", "ኆ": "ho",
        "ነ": "ne", "ኑ": "nu", "ኒ": "ni", "ና": "na", "ኔ": "nie", "ን": "n", "ኖ": "no", "ኗ": "nua",
        "ኘ": "ngne", "ኙ": "ngnu", "ኚ": "ngni", "ኛ": "ngna", "ኜ": "ngnie", "ኝ": "nge", "ኞ": "ng", "ኟ": "ngnua",
        "አ": "a", "ኡ": "ou", "ኢ": "e", "ኣ": "a", "ኤ": "ei", "እ": "e", "ኦ": "o", "ኧ": "hee",
        "ዐ": "a", "ዑ": "ou", "ዒ": "e", "ዓ": "a", "ዔ": "ei", "ዕ": "e", "ዖ": "o",
        "ከ": "ke", "ኩ": "ku", "ኪ": "ki", "ካ": "ka", "ኬ": "kie", "ክ": "k", "ኮ": "ko", "ኳ": "kua",
        "ኸ": "khe", "ኹ": "khu", "ኺ": "khi", "ኻ": "kha", "ኼ": "khie", "ኽ": "kh", "ኾ": "kho", "ዃ": "khua",
        "ወ": "we", "ዉ": "wu", "ዊ": "wi", "ዋ": "wa", "ዌ": "wie", "ው": "w", "ዎ": "wo",
        "ዘ": "ze", "ዙ": "zu", "ዚ": "zi", "ዛ": "za", "ዜ": "zie", "ዝ": "z", "ዞ": "zo", "ዟ": "zua",
        "ዠ": "zhe", "ዡ": "zhu", "ዢ": "zhi", "ዣ": "zha", "ዤ": "zhie", "ዥ": "zh", "ዦ": "zho", "ዧ": "zhua",
        "የ": "ye", "ዩ": "yu", "ዪ": "yi", "ያ": "ya", "ዬ": "yie", "ይ": "y", "ዮ": "yo",
        "ደ": "de", "ዱ": "du", "ዲ": "di", "ዳ": "da", "ዴ": "die", "ድ": "d", "ዶ": "do", "ዷ": "dua",
        "ጀ": "je", "ጁ": "ju", "ጂ": "ji", "ጃ": "ja", "ጄ": "jie", "ጅ": "j", "ጆ": "jo", "ጇ": "jua",
        "ገ": "ge", "ጉ": "gu", "ጊ": "gi", "ጋ": "ga", "ጌ": "gie", "ግ": "g", "ጎ": "go", "ጓ": "gua",
        "ጠ": "te", "ጡ": "tu", "ጢ": "ti", "ጣ": "ta", "ጤ": "tie", "ጥ": "t", "ጦ": "to", "ጧ": "tua",
        "ጨ": "che", "ጩ": "chu", "ጪ": "chi", "ጫ": "cha", "ጬ": "chie", "ጭ": "ch", "ጮ": "cho", "ጯ": "chua",
        "ጰ": "pe", "ጱ": "pu", "ጲ": "pi", "ጳ": "pa", "ጴ": "pe", "ጵ": "p", "ጶ": "po", "ጷ": "pua",
        "ጸ": "tse", "ጹ": "tsu", "ጺ": "tsi", "ጻ": "tsa", "ጼ": "tsie", "ጽ": "ts", "ጾ": "tso", "ጿ": "tsua",
        "ፀ": "tse", "ፁ": "tsu", "ፂ": "tsi", "ፃ": "tsa", "ፄ": "tsie", "ፅ": "ts", "ፆ": "tso",
        "ፈ": "fe", "ፉ": "fu", "ፊ": "fi", "ፋ": "fa", "ፌ": "fie", "ፍ": "f", "ፎ": "fo", "ፏ": "fua",
        "ፐ": "pe", "ፑ": "pu", "ፒ": "pi", "ፓ": "pa", "ፔ": "pie", "ፕ": "p", "ፖ": "po", "ፗ": "pua",
        "ቨ": "ve", "ቩ": "vu", "ቪ": "vi", "ቫ": "va", "ቬ": "vie", "ቭ": "v", "ቮ": "vo", "ቯ": "vua"
     }
    latin_text = ""
    for char in geez_text:
        if char in geez_to_latin_dict:
            latin_text += geez_to_latin_dict[char]
        else:
            latin_text += char
    return latin_text
# Translate Geez text to Latin using the custom dictionary
# Load environment variables from .env file
load_dotenv()

try:
    # Get database credentials from environment variables
    # you should define environmnt varibale like below
    # DB_HOST='your host '
    # DB_PORT=your host port
    # DB_NAME='your postgress database name'
    # DB_USER='database user name'
    # DB_PASSWORD='database user password'
    
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    # Connect to your database using context manager
    with psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    ) as conn:
        # Create a cursor object within the context manager
        with conn.cursor() as cur:
            # Fetch all customer names from the customers table
            cur.execute("SELECT id, name FROM customers")
            
            # Get the total number of rows for tqdm
            total_rows = cur.rowcount
            
            # Create tqdm progress bar
            progress_bar = tqdm(total=total_rows, desc="Translating Names", unit=" row")
            
            # Iterate through the rows and transliterate non-Latin names to Latin names
            for row in cur.fetchall():
                customer_id, geez_text = row
                latin_name = translate_geez_to_latin(geez_text)  # Transliterate the name to Latin characters
                # Update the customers table with the Latin name
                cur.execute("UPDATE customers SET name = %s WHERE id = %s", (latin_name, customer_id))
                
                # Update the progress bar
                progress_bar.update(1)

            # Close the progress bar
            progress_bar.close()

            # Commit the changes to the database
            conn.commit()

    print("Conversion completed. Non-Latin names have been transliterated to Latin characters.")

except psycopg2.Error as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

















