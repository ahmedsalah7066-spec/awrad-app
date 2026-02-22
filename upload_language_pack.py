
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Hardcoded English Translations mapped to IDs
# Based on the content in HisnContent.kt, Awrad.kt, Munajat.kt
# We use the IDs defined in our plan:
# Awrad: awrad_saturday, awrad_sunday, ...
# Munajat: munajat_0, munajat_1, ...
# Hisn: hisn_morning_0... hisn_category_...

english_pack = {
    # --- AWRAD (DALAIL) ---
    "awrad_saturday": {
        "main": """O Allah, send blessings upon our Master Muhammad, who is the guardian of the Trust and the conveyer of the Message.
O Allah, send blessings upon our Master Muhammad, a blessing by which You open for us the doors of goodness and make easy for us every difficulty.

O Allah, send blessings upon our Master Muhammad, and upon his Family and Companions, a blessing that will be a cause for the forgiveness of slips and the raising of ranks.
O Allah, send blessings upon our Master Muhammad, a blessing by which You save us from all fears and perils, and by which You fulfill for us all needs.

O Allah, send blessings upon our Master Muhammad, a blessing by which You untie the knot of my tongue and relieve my distress.
O Allah, send blessings upon our Master Muhammad, and upon his Family, a blessing that has no end in the universes.
O Allah, send blessings upon our Master Muhammad, and upon the Family of our Master Muhammad, as long as stars shine and vines sprout leaves.
O Allah, send blessings upon our Master Muhammad, and upon the Family of our Master Muhammad, a blessing that cannot be counted nor limited.

O Allah, send blessings upon our Master Muhammad, a blessing that befits his station with You, and by which You make us reach the utmost of our hope in You.
O Allah, send blessings upon our Master Muhammad, a blessing that will be a veil for us from Your punishment, and a cause for attaining Your reward.

O Allah, send blessings upon our Master Muhammad, the number of sand grains and pebbles, and the number of what was and what has passed.
O Allah, send blessings upon our Master Muhammad, a blessing that pleases him and by which You honor his offspring, and by which You grant him his request on the Day of Resurrection.

O Allah, send blessings upon our Master Muhammad, and upon his Family, a blessing whose newness does not wear out, and whose number cannot be counted.
O Allah, send blessings upon our Master Muhammad, the Prophet who turns much to Allah, the Light by whom doors are opened.
O Allah, send blessings upon our Master Muhammad, and upon his Family, a blessing by which You make us among the successful, the triumphant.

O Allah, send blessings upon our Master Muhammad, a blessing by which You weigh down the scales of our good deeds, and by which You forgive our sins and evil deeds.
O Allah, send blessings upon our Master Muhammad, a blessing that brings us near to his presence, and makes us happy by seeing him.

O Allah, send blessings upon our Master Muhammad, and upon his Family, his Wives, and his Descendants, the number of the breaths of his nation.
O Allah, by the blessing of sending prayers upon him, make us, through the prayer upon him, among the triumphant; and at his Basin, among those who arrive and drink; and by his Sunnah and his obedience, among those who act; and do not intervene between us and him on the Day of Resurrection, O Lord of the worlds.

And forgive us, our parents, and all Muslims. And all praise is due to Allah, Lord of the worlds."""
    },
    
    # --- WIRD ---
    "wird_istiftah": {
        "main": """In the Name of Allah, the Most Gracious, the Most Merciful.
O Allah, to You belongs all praise, You represent the light of the heavens and the earth and everyone therein. To You belongs all praise, You represent the sustainer of the heavens and the earth and everyone therein. To You belongs all praise, You are the Truth, Your promise is true, Your words are true, the meeting with You is true, Paradise is true, Hell is true, the Prophets are true, Muhammad (peace be upon him) is true, and the Hour is true.
O Allah, to You I have submitted, in You I have believed, upon You I rely, to You I turn in repentance, by You I argue, and to You I refer for judgment. So forgive me for what I have sent before me and what I have left behind, what I have concealed and what I have declared, and what You know about me more than I do. You are the One Who brings forward and You are the One Who delays, there is no god but You, and there is no power or might except with Allah."""
    },
    "wird_ibrahimi": {
        "main": """O Allah, send blessings upon our Master Muhammad and upon the Family of our Master Muhammad, as You sent blessings upon our Master Abraham and upon the Family of our Master Abraham, indeed You are Praiseworthy, Glorious.
O Allah, bless our Master Muhammad and the Family of our Master Muhammad, as You blessed our Master Abraham and the Family of our Master Abraham, indeed You are Praiseworthy, Glorious."""
    },

    # --- HISN CATEGORIES ---
    "hisn_category_morning": { "main": "Morning Adhkar" },
    "hisn_category_evening": { "main": "Evening Adhkar" },
    "hisn_category_sleep": { "main": "Sleep Adhkar" },
    "hisn_category_prayer": { "main": "Prayer Adhkar" },
    "hisn_category_food": { "main": "Food Adhkar" },
    "hisn_category_travel": { "main": "Travel Adhkar" },
    "hisn_category_mosque": { "main": "Mosque Adhkar" },
    "hisn_category_tasbeehat": { "main": "Tasbeehat" }
}

def upload_language_pack(lang_code, pack):
    print(f"Uploading language pack for: {lang_code}")
    doc_ref = db.collection('locales').document(lang_code)
    doc_ref.set(pack)
    print("Upload complete!")

if __name__ == "__main__":
    upload_language_pack("en", english_pack)
