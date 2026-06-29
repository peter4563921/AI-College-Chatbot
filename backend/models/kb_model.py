from backend.db import query   # ✅ FIXED IMPORT

RESOURCE_CONFIG = {
    'courses': ('Courses', ['department_id', 'name', 'degree', 'duration', 'eligibility', 'description', 'is_active']),
    'departments': ('Departments', ['name', 'short_name', 'description', 'level', 'is_active']),
    'fees': ('FeeStructure', ['course_id', 'category', 'amount', 'notes']),
    'admission': ('Admissions', ['title', 'process_steps', 'eligibility', 'required_documents', 'important_dates']),
    'placements': ('Placements', ['title', 'details', 'companies', 'training_support']),
    'hostel': ('Hostels', ['title', 'facilities', 'transport_details']),
    'scholarships': ('Scholarships', ['name', 'eligibility', 'details']),
    'contact': ('Contacts', ['college_name', 'address', 'phone', 'email', 'website']),
    'faculty': ('Faculty', ['department_id', 'name', 'designation', 'qualification', 'specialization']),
    'faqs': ('FAQs', ['question', 'answer', 'category', 'is_active']),
}

# -------------------------
# READ (LIST)
# -------------------------
def list_resource(resource):
    if resource not in RESOURCE_CONFIG:
        raise ValueError("Invalid resource")

    table, _ = RESOURCE_CONFIG[resource]
    return query(f"SELECT * FROM {table} ORDER BY id DESC")


# -------------------------
# CREATE
# -------------------------
def create_resource(resource, payload):
    if resource not in RESOURCE_CONFIG:
        raise ValueError("Invalid resource")

    table, columns = RESOURCE_CONFIG[resource]

    data = {key: payload.get(key) for key in columns if payload.get(key) is not None}

    if not data:
        raise ValueError("No valid fields supplied")

    cols = ", ".join(data.keys())
    placeholders = ", ".join(["%s"] * len(data))

    result = query(
        f"INSERT INTO {table} ({cols}) VALUES ({placeholders})",
        tuple(data.values()),
        commit=True
    )

    return {"id": result["lastrowid"], **data}


# -------------------------
# UPDATE
# -------------------------
def update_resource(resource, item_id, payload):
    if resource not in RESOURCE_CONFIG:
        raise ValueError("Invalid resource")

    table, columns = RESOURCE_CONFIG[resource]

    data = {key: payload.get(key) for key in columns if payload.get(key) is not None}

    if not data:
        raise ValueError("No valid fields supplied")

    assignments = ", ".join([f"{key}=%s" for key in data])

    query(
        f"UPDATE {table} SET {assignments} WHERE id=%s",
        tuple(data.values()) + (item_id,),
        commit=True
    )

    return {"id": item_id, **data}


# -------------------------
# DELETE
# -------------------------
def delete_resource(resource, item_id):
    if resource not in RESOURCE_CONFIG:
        raise ValueError("Invalid resource")

    table, _ = RESOURCE_CONFIG[resource]

    query(
        f"DELETE FROM {table} WHERE id=%s",
        (item_id,),
        commit=True
    )

    return {"id": item_id}


# -------------------------
# PUBLIC DATA (FOR CHATBOT)
# -------------------------
def get_public_knowledge():
    return {
        'courses': query('SELECT name, degree, duration, eligibility, description FROM Courses WHERE is_active=1 ORDER BY name'),
        'departments': query('SELECT name, short_name, description, level FROM Departments WHERE is_active=1 ORDER BY name'),
        'fees': query('SELECT category, amount, notes FROM FeeStructure ORDER BY id DESC'),
        'admissions': query('SELECT title, process_steps, eligibility, required_documents, important_dates FROM Admissions ORDER BY id DESC'),
        'placements': query('SELECT title, details, companies, training_support FROM Placements ORDER BY id DESC'),
        'hostels': query('SELECT title, facilities, transport_details FROM Hostels ORDER BY id DESC'),
        'scholarships': query('SELECT name, eligibility, details FROM Scholarships ORDER BY id DESC'),
        'contacts': query('SELECT college_name, address, phone, email, website FROM Contacts ORDER BY id DESC'),
        'faculty': query('SELECT name, designation, qualification, specialization FROM Faculty ORDER BY id DESC'),
        'faqs': query('SELECT question, answer, category FROM FAQs WHERE is_active=1 ORDER BY id DESC'),
    }