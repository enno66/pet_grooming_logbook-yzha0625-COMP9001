from datetime import date

def calculate_age(birthdate):
    """
    Automatically calculate current age based on 'birthday'
    """
    if birthdate is None:
        return " "
        
    today = date.today()
    
    # Compute the current age from a given birthdate.
    # The formula subtracts the birth year from the current year and adjusts the result
    # by checking whether the birthday has already occurred this year.
    # If today's month/day is earlier than the birth month/day, the age is reduced by 1.
    age = today.year - birthdate.year - (
        (today.month, today.day) < (birthdate.month, birthdate.day)
    )
    
    return age

def get_zodiac(birthdate):
    """
    Automatically calculate zodiac sign based on 'birthday'
    """
    if birthdate is None:
        return " "
        
    year = birthdate.year
    zodiacs = [
        "Rat 🐭", "Ox 🐮","Tiger 🐯", "Rabbit 🐰", "Dragon 🐲", "Snake 🐍", 
        "Horse 🐎", "Goat 🐑", "Monkey 🐒", "Rooster 🐔", "Dog 🐶", "Pig 🐷"
    ]
    
    # Use 2020 as the base year (Year of the Rat).
    # In our list, "Rat" is at index 0.
    # The zodiac cycle repeats every 12 years, so we take (year - 2020) % 12
    # to find the correct zodiac index.
    base_year_index = 0
    offset = (year - 2020)
    
    index = (offset + base_year_index) % 12 
    
    return zodiacs[index]


UPLOAD_FILE = "photos" 

def save_uploaded_file(uploaded_file, appointment_id):
    """
    Save the photos that uploaded by staff
    
    """
    if uploaded_file is None:
        return None
        
    try:
        # 1. Get extension from filename
        original_filename = uploaded_file.name
        parts = original_filename.split(".")
        
        if len(parts) > 1:
            # Get the last element (e.g., 'jpg' or 'png')
            file_extension = parts.pop()
        else:
            file_extension = "jpg" # default jpg
            
        # 2. Create a new file name
        new_filename = f"appt_{appointment_id}_groom.{file_extension}"
        
        save_path = f"{UPLOAD_FILE}/{new_filename}"
        
        # 4. Write in the file
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        # 5. save path
        return save_path
        
    except FileNotFoundError:
        print("🔴 Error: upload folder not found! ")
        return None
    except Exception as e:
        print(f"File save failed: {e}")
        return None
