package com.example.awrad.data

import android.content.Context
import android.util.Log
import com.example.awrad.data.utils.JsonDataLoader
import com.google.firebase.firestore.FirebaseFirestore
import com.google.firebase.firestore.SetOptions
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.tasks.await
import org.json.JSONObject
import javax.inject.Inject
import javax.inject.Singleton

/**
 * Uploads all content to Firestore in the unified `content/` collection.
 * Includes ar, en, and tr translations.
 *
 * Schema per document:
 *   content/{id} -> { type, order, categoryId?, count?,
 *                      ar: { title?, content, fadl? },
 *                      en: { title?, content, fadl? },
 *                      tr: { title?, content, fadl? }, ... }
 */
@Singleton
class DataUploader @Inject constructor(
    private val firestore: FirebaseFirestore,
    private val jsonDataLoader: JsonDataLoader,
    @ApplicationContext private val context: Context
) {
    companion object {
        private const val TAG = "DataUploader"
        private const val COLLECTION = "content"
    }

    // Lazy-loaded Turkish full content from turkish_full_content.json
    private val turkishContent: Map<String, String> by lazy { loadTurkishFullContent() }

    suspend fun uploadAllData() {
        try {
            Log.d(TAG, "Starting full content upload to Firestore (ar+en+tr)...")
            uploadAwrad()
            uploadMunajat()
            uploadHisn()
            uploadStaticContent()
            Log.d(TAG, "All content uploaded successfully!")
        } catch (e: Exception) {
            Log.e(TAG, "Error uploading data", e)
            throw e
        }
    }

    // ═══════════════════════════════════════════
    // Awrad (Dalail al-Khayrat) — 7 daily wirds
    // ═══════════════════════════════════════════

    private suspend fun uploadAwrad() {
        Log.d(TAG, "Uploading Awrad (ar+en+tr)...")
        val arList = jsonDataLoader.loadAwrad("ar")
        val enList = jsonDataLoader.loadAwrad("en")

        val dayNames = listOf("saturday", "sunday", "monday", "tuesday", "wednesday", "thursday", "friday")

        for (i in dayNames.indices) {
            val docId = "awrad_${dayNames[i]}"
            val arItem = arList.getOrNull(i) ?: continue
            val enItem = enList.getOrNull(i)

            val data = hashMapOf<String, Any>(
                "type" to "awrad",
                "order" to i,
                "ar" to hashMapOf(
                    "title" to (arItem.dayTitle ?: ""),
                    "content" to arItem.content
                )
            )

            if (enItem != null) {
                data["en"] = hashMapOf(
                    "title" to (enItem.dayTitle ?: ""),
                    "content" to enItem.content
                )
            }

            // Turkish from turkish_full_content.json
            val trContent = turkishContent[docId]
            if (!trContent.isNullOrEmpty()) {
                val trTitle = when (dayNames[i]) {
                    "saturday" -> "Cumartesi Virdi"
                    "sunday" -> "Pazar Virdi"
                    "monday" -> "Pazartesi Virdi"
                    "tuesday" -> "Salı Virdi"
                    "wednesday" -> "Çarşamba Virdi"
                    "thursday" -> "Perşembe Virdi"
                    "friday" -> "Cuma Virdi"
                    else -> ""
                }
                data["tr"] = hashMapOf(
                    "title" to trTitle,
                    "content" to trContent
                )
            }

            firestore.collection(COLLECTION).document(docId)
                .set(data, SetOptions.merge()).await()
        }
        Log.d(TAG, "Uploaded ${dayNames.size} Awrad documents with tr")
    }

    // ═══════════════════════════════════════════
    // Munajat (15 prayers)
    // ═══════════════════════════════════════════

    private suspend fun uploadMunajat() {
        Log.d(TAG, "Uploading Munajat (ar+en+tr)...")
        val arList = jsonDataLoader.loadMunajat("ar")
        val enList = jsonDataLoader.loadMunajat("en")

        // Mapping from munajat index (1-based) to turkish_full_content.json key
        val trMunajatKeys = listOf(
            "munajat_zahidin",        // munajat_1
            "munajat_raghibin_1",     // munajat_2
            "munajat_dhakirin",       // munajat_3
            "munajat_arifin",         // munajat_4
            "munajat_muftaqirin",     // munajat_5
            "munajat_mutawassilin",   // munajat_6
            "munajat_muhibbin",       // munajat_7
            "munajat_muridin",        // munajat_8
            "munajat_mutiin",         // munajat_9
            "munajat_shakirin",       // munajat_10
            "munajat_rajin",          // munajat_11
            "munajat_raghibin_2",     // munajat_12
            "munajat_khaifin",        // munajat_13
            "munajat_shakin",         // munajat_14
            "munajat_taibin"          // munajat_15
        )

        val trTitles = listOf(
            "Zâhidlerin Münacaatı",
            "Rağbet Edenlerin Münacaatı (1)",
            "Zikredenlerin Münacaatı",
            "Ariflerin Münacaatı",
            "Muhtaçların Münacaatı",
            "Tevessül Edenlerin Münacaatı",
            "Sevenlerin Münacaatı",
            "Müridlerin Münacaatı",
            "İtaat Edenlerin Münacaatı",
            "Şükredenlerin Münacaatı",
            "Umut Edenlerin Münacaatı",
            "Rağbet Edenlerin Münacaatı (2)",
            "Korkanların Münacaatı",
            "Şikâyet Edenlerin Münacaatı",
            "Tövbe Edenlerin Münacaatı"
        )

        for (i in arList.indices) {
            val docId = "munajat_${i + 1}"
            val arItem = arList[i]
            val enItem = enList.getOrNull(i)

            val data = hashMapOf<String, Any>(
                "type" to "munajat",
                "order" to i,
                "ar" to hashMapOf(
                    "title" to (arItem.title ?: ""),
                    "content" to arItem.content
                )
            )

            if (enItem != null) {
                data["en"] = hashMapOf(
                    "title" to (enItem.title ?: ""),
                    "content" to enItem.content
                )
            }

            // Turkish from turkish_full_content.json
            val trKey = trMunajatKeys.getOrNull(i)
            val trContent = if (trKey != null) turkishContent[trKey] else null
            val trTitle = trTitles.getOrNull(i) ?: ""
            if (!trContent.isNullOrEmpty()) {
                data["tr"] = hashMapOf(
                    "title" to trTitle,
                    "content" to trContent
                )
            }

            firestore.collection(COLLECTION).document(docId)
                .set(data, SetOptions.merge()).await()
        }
        Log.d(TAG, "Uploaded ${arList.size} Munajat documents with tr")
    }

    // ═══════════════════════════════════════════
    // Hisn al-Muslim — categories + items
    // ═══════════════════════════════════════════

    private suspend fun uploadHisn() {
        Log.d(TAG, "Uploading Hisn (ar+en+tr)...")
        val arCategories = jsonDataLoader.loadHisn("ar")
        val enCategories = jsonDataLoader.loadHisn("en")
        val trCategories = jsonDataLoader.loadHisn("tr")

        for (i in arCategories.indices) {
            val arCat = arCategories[i]
            val enCat = enCategories.getOrNull(i)
            val trCat = trCategories.find { it.id == arCat.id }
            val catDocId = "hisn_category_${arCat.id}"

            val catData = hashMapOf<String, Any>(
                "type" to "hisn_category",
                "order" to i,
                "icon" to getIconName(arCat.iconResId),
                "ar" to hashMapOf("title" to (arCat.title ?: ""))
            )
            if (enCat != null) {
                catData["en"] = hashMapOf("title" to (enCat.title ?: ""))
            }
            if (trCat != null) {
                catData["tr"] = hashMapOf("title" to (trCat.title ?: ""))
            }

            firestore.collection(COLLECTION).document(catDocId)
                .set(catData, SetOptions.merge()).await()

            // Upload items for this category
            for (j in arCat.items.indices) {
                val arItem = arCat.items[j]
                val enItem = enCat?.items?.getOrNull(j)
                val trItem = trCat?.items?.getOrNull(j)
                val itemDocId = "hisn_${arCat.id}_${j + 1}"

                val itemData = hashMapOf<String, Any>(
                    "type" to "hisn",
                    "categoryId" to arCat.id,
                    "order" to j,
                    "count" to arItem.count,
                    "ar" to hashMapOf(
                        "content" to arItem.content,
                        "fadl" to arItem.fadl
                    )
                )
                if (enItem != null) {
                    itemData["en"] = hashMapOf(
                        "content" to enItem.content,
                        "fadl" to enItem.fadl
                    )
                }
                if (trItem != null) {
                    itemData["tr"] = hashMapOf(
                        "content" to trItem.content,
                        "fadl" to trItem.fadl
                    )
                }

                firestore.collection(COLLECTION).document(itemDocId)
                    .set(itemData, SetOptions.merge()).await()
            }
        }
        Log.d(TAG, "Uploaded ${arCategories.size} Hisn categories with items (ar+en+tr)")
    }

    // ═══════════════════════════════════════════
    // Static content (Istiftah, Ibrahimi)
    // ═══════════════════════════════════════════

    private suspend fun uploadStaticContent() {
        Log.d(TAG, "Uploading Static Content (ar+en+tr)...")
        val staticMap = jsonDataLoader.loadStaticContent()

        // Turkish static translations
        val trStatic = mapOf(
            "istiftah" to "Bismillahirrahmanirrahim.\n\nAllah'ım! Senden istiyorum, ey Allah! Sen Vahid, Ehad, Ferd, Samed'sin; doğurmamış ve doğurulmamışsın ve Sana denk olan hiç kimse yoktur. Günahlarımı bağışlamanı diliyorum, çünkü Sen Gafur ve Rahim'sin.\n\nAllah'ım! Senden istiyorum; hamd Sanadır, Senden başka ilah yoktur, teksin, ortağın yoktur, Mennan'sın, ey gökleri ve yeri yoktan var eden, ey Celal ve İkram Sahibi, ey Hayy, ey Kayyum! Senden cenneti istiyorum ve cehennemden Sana sığınıyorum.\n\nAllah'ım! Hamd Sanadır; Sen göklerin ve yerin ve onlardakilerin nurusun. Hamd Sanadır; Sen göklerin ve yerin ve onlardakilerin kayyumisun. Hamd Sanadır; Sen göklerin ve yerin ve onlardakilerin Rabbisin. Sen Hak'sın, vaadin haktır, sözün haktır, Sana kavuşmak haktır, cennet haktır, cehennem haktır, peygamberler haktır, Muhammed sallallahu aleyhi ve sellem haktır ve kıyamet haktır. Allah'ım! Sana teslim oldum, Sana inandım, Sana tevekkül ettim, Sana yöneldim, Senin uğruna mücadele ettim ve Sana muhakeme oldum. Geçmiş ve gelecek, gizli ve açık günahlarımı bağışla. İlahım Sensin, Senden başka ilah yoktur.\n\nSeni tenzih ederim Allah'ım ve Sana hamd ederim. İsmin mübarektir, şanın yücedir ve Senden başka ilah yoktur.\n\nİşiten ve bilen Allah'a, kovulmuş şeytanın vesvesesinden, üflemesinden ve tükrüğünden sığınırım.\n\nBismillahirrahmanirrahim.\n\nAlemlerin Rabbi olan Allah'a hamd olsun. Rahman ve Rahim olan, hesap gününün sahibi olan Allah'a. Yalnız Sana kulluk eder ve yalnız Senden yardım dileriz. Bizi doğru yola ilet. Kendilerine nimet verdiklerinin yoluna; gazaba uğrayanların ve sapıtanların yoluna değil. Amin.\n\nAllah'ım! Senden fazlından ve rahmetinden istiyorum, çünkü onlara yalnız Sen maliksin, ey Merhametlilerin En Merhametlisi, ey Keremlilerin En Keremlisi.",
            "ibrahimi" to "Allah'ım! Efendimiz İbrahim'e ve Efendimiz İbrahim'in âline salât ettiğin gibi, Efendimiz Muhammed'e ve Efendimiz Muhammed'in âline de salât eyle. Şüphesiz Sen Hamîd'sin, Mecîd'sin.\n\nAllah'ım! Efendimiz İbrahim'e ve Efendimiz İbrahim'in âline bereket verdiğin gibi, Efendimiz Muhammed'e ve Efendimiz Muhammed'in âline de bereket ver. Şüphesiz Sen Hamîd'sin, Mecîd'sin."
        )

        for ((id, item) in staticMap) {
            val docId = "static_$id"
            val data = hashMapOf<String, Any>(
                "type" to "static",
                "order" to 0,
                "ar" to hashMapOf(
                    "content" to item.content
                )
            )
            if (item.translation.isNotEmpty()) {
                data["en"] = hashMapOf(
                    "content" to item.translation
                )
            }
            // Turkish
            val trContent = trStatic[id]
            if (!trContent.isNullOrEmpty()) {
                data["tr"] = hashMapOf(
                    "content" to trContent
                )
            }

            firestore.collection(COLLECTION).document(docId)
                .set(data, SetOptions.merge()).await()
        }
        Log.d(TAG, "Uploaded ${staticMap.size} static content items with tr")
    }

    /**
     * Add a new language translation for a specific content item.
     */
    suspend fun addLanguage(contentId: String, languageCode: String, title: String?, content: String, fadl: String? = null) {
        val langMap = hashMapOf<String, Any>(
            "content" to content
        )
        if (!title.isNullOrEmpty()) langMap["title"] = title
        if (!fadl.isNullOrEmpty()) langMap["fadl"] = fadl

        firestore.collection(COLLECTION).document(contentId)
            .update(languageCode, langMap)
            .await()
        Log.d(TAG, "Added $languageCode translation for $contentId")
    }

    private fun getIconName(iconResId: Int): String {
        return "ic_default"
    }

    /**
     * Load turkish_full_content.json from assets.
     * Returns map of key -> content string.
     */
    private fun loadTurkishFullContent(): Map<String, String> {
        return try {
            val jsonStr = context.assets.open("data/turkish_full_content.json")
                .bufferedReader().use { it.readText() }
            val jsonObj = JSONObject(jsonStr)
            val map = mutableMapOf<String, String>()
            for (key in jsonObj.keys()) {
                map[key] = jsonObj.getString(key)
            }
            Log.d(TAG, "Loaded ${map.size} Turkish content entries")
            map
        } catch (e: Exception) {
            Log.e(TAG, "Error loading turkish_full_content.json", e)
            emptyMap()
        }
    }
}
