package com.example.awrad.data.repository

import android.util.Log
import com.example.awrad.Awrad
import com.example.awrad.Munajat
import com.example.awrad.DhikrItem
import com.example.awrad.HisnCategory
import com.example.awrad.domain.repository.WirdRepository
import com.example.awrad.data.room.TranslationDao
import com.example.awrad.data.room.TranslationEntity
import com.example.awrad.data.utils.JsonDataLoader
import javax.inject.Inject
import javax.inject.Singleton

/**
 * Repository with Room-first strategy:
 * 1. Try Room (populated from Firebase or seeded from JSON)
 * 2. Fall back to embedded JSON for ar/en only
 */
@Singleton
class SimpleContentRepository @Inject constructor(
    private val translationDao: TranslationDao,
    private val jsonDataLoader: JsonDataLoader
) : WirdRepository {

    companion object {
        private const val TAG = "ContentRepo"
        private val EMBEDDED_LANGUAGES = setOf("ar", "en", "ur", "tr", "ml", "uz", "id", "ru", "bn", "fr", "hi", "fa")
    }

    // JSON caches (fallback only for ar/en)
    private val awradCache = mutableMapOf<String, List<Awrad>>()
    private val munajatCache = mutableMapOf<String, List<Munajat>>()
    private val hisnCache = mutableMapOf<String, List<HisnCategory>>()
    private val staticContentCache = mutableMapOf<String, Map<String, com.example.awrad.WirdContentItem>>()
    private fun getStaticContent(lang: String): Map<String, com.example.awrad.WirdContentItem> {
        return staticContentCache.getOrPut(lang) { jsonDataLoader.loadStaticContent(lang) }
    }

    private fun getAwradListFromJson(lang: String): List<Awrad> {
        return awradCache.getOrPut(lang) { jsonDataLoader.loadAwrad(lang) }
    }

    private fun getMunajatListFromJson(lang: String): List<Munajat> {
        return munajatCache.getOrPut(lang) { jsonDataLoader.loadMunajat(lang) }
    }

    private fun getHisnListFromJson(lang: String): List<HisnCategory> {
        return hisnCache.getOrPut(lang) { jsonDataLoader.loadHisn(lang) }
    }

    // ═══════════════════════════════════════════
    // Static Content (Istiftah, Ibrahimi)
    // ═══════════════════════════════════════════

    override suspend fun getIstiftah(languageCode: String): String {
        // Try Room first
        val entity = translationDao.getTranslation("static_istiftah", languageCode)
        if (entity != null) return entity.mainText

        // Fallback to JSON for embedded languages
        if (languageCode in EMBEDDED_LANGUAGES) {
            val item = getStaticContent(languageCode)["istiftah"] ?: return ""
            if (languageCode != "ar" && item.translation.isNotBlank()) {
                return item.translation
            }
            return item.content
        }
        // For non-embedded languages, try Arabic as last resort
        return translationDao.getTranslation("static_istiftah", "ar")?.mainText
            ?: getStaticContent("ar")["istiftah"]?.content ?: ""
    }

    override suspend fun getIbrahimi(languageCode: String): String {
        val entity = translationDao.getTranslation("static_ibrahimi", languageCode)
        if (entity != null) return entity.mainText

        if (languageCode in EMBEDDED_LANGUAGES) {
            val item = getStaticContent(languageCode)["ibrahimi"] ?: return ""
            if (languageCode != "ar" && item.translation.isNotBlank()) {
                return item.translation
            }
            return item.content
        }
        return translationDao.getTranslation("static_ibrahimi", "ar")?.mainText
            ?: getStaticContent("ar")["ibrahimi"]?.content ?: ""
    }

    // ═══════════════════════════════════════════
    // Awrad (Dalail al-Khayrat)
    // ═══════════════════════════════════════════

    override suspend fun getDailyAwrad(dayOfWeek: Int, languageCode: String): Awrad {
        val index = if (dayOfWeek in 0..6) dayOfWeek else 0
        return getAwrad(index, languageCode)
    }

    override suspend fun getAllAwrad(languageCode: String): List<Awrad> {
        // Try Room first
        val roomEntities = translationDao.getByType("awrad", languageCode)
        if (roomEntities.isNotEmpty()) {
            return roomEntities.map { it.toAwrad() }
        }
        // Fallback to JSON
        if (languageCode in EMBEDDED_LANGUAGES) {
            return getAwradListFromJson(languageCode)
        }
        return getAwradListFromJson("ar") // Last resort
    }

    override suspend fun getAwradByResId(resId: Int, languageCode: String): Awrad? {
        val list = getAwradListFromJson(languageCode)
        val item = list.find { it.dayResId == resId } ?: return null
        val index = list.indexOf(item)
        return if (index != -1) getAwrad(index, languageCode) else item
    }

    override suspend fun getAwradByIndex(index: Int, languageCode: String): Awrad? {
        return getAwrad(index, languageCode)
    }

    suspend fun getAwrad(index: Int, languageCode: String): Awrad {
        val dayNames = listOf("saturday", "sunday", "monday", "tuesday", "wednesday", "thursday", "friday")
        val safeIndex = if (index in dayNames.indices) index else 0
        val id = "awrad_${dayNames[safeIndex]}"

        // Try Room first
        val entity = translationDao.getTranslation(id, languageCode)
        if (entity != null) {
            return entity.toAwrad()
        }

        // Fallback to JSON
        if (languageCode in EMBEDDED_LANGUAGES) {
            val list = getAwradListFromJson(languageCode)
            return list.getOrElse(safeIndex) { list.firstOrNull() ?: Awrad(0, "") }
        }

        // Non-embedded language not in Room → try Arabic
        val arEntity = translationDao.getTranslation(id, "ar")
        if (arEntity != null) return arEntity.toAwrad()
        
        val arList = getAwradListFromJson("ar")
        return arList.getOrElse(safeIndex) { arList.firstOrNull() ?: Awrad(0, "") }
    }

    // ═══════════════════════════════════════════
    // Munajat
    // ═══════════════════════════════════════════

    override suspend fun getRotatingMunajat(dayOfYear: Int, languageCode: String): Munajat {
        val totalMunajat = 15
        val index = (dayOfYear - 1) % totalMunajat
        return getMunajat(index, languageCode)
    }

    suspend fun getMunajat(index: Int, languageCode: String): Munajat {
        val id = "munajat_${index + 1}"

        // Try Room first
        val entity = translationDao.getTranslation(id, languageCode)
        if (entity != null) {
            return entity.toMunajat()
        }

        // Fallback to JSON
        if (languageCode in EMBEDDED_LANGUAGES) {
            val list = getMunajatListFromJson(languageCode)
            val safeIndex = if (index in list.indices) index else 0
            return list.getOrElse(safeIndex) { Munajat(0, "") }
        }

        // Non-embedded → try Arabic
        val arEntity = translationDao.getTranslation(id, "ar")
        if (arEntity != null) return arEntity.toMunajat()

        val arList = getMunajatListFromJson("ar")
        val safeIndex = if (index in arList.indices) index else 0
        return arList.getOrElse(safeIndex) { Munajat(0, "") }
    }

    suspend fun getAllMunajats(languageCode: String): List<Munajat> {
        // Try Room first
        val roomEntities = translationDao.getByType("munajat", languageCode)
        if (roomEntities.isNotEmpty()) {
            return roomEntities.map { it.toMunajat() }
        }

        if (languageCode in EMBEDDED_LANGUAGES) {
            return getMunajatListFromJson(languageCode)
        }
        return getMunajatListFromJson("ar")
    }

    // ═══════════════════════════════════════════
    // Hisn Al-Muslim
    // ═══════════════════════════════════════════

    suspend fun getHisnCategories(languageCode: String): List<HisnCategory> {
        // Try Room first
        val roomEntities = translationDao.getByType("hisn_category", languageCode)
        if (roomEntities.isNotEmpty()) {
            return roomEntities.mapIndexed { idx, entity ->
                val catId = entity.id.removePrefix("hisn_category_")
                HisnCategory(
                    id = catId,
                    titleResId = 0,
                    iconResId = 0,
                    items = emptyList(), // Items loaded separately
                    title = entity.title ?: entity.mainText
                )
            }
        }

        // Fallback to JSON for embedded languages
        if (languageCode in EMBEDDED_LANGUAGES) {
            return getHisnListFromJson(languageCode)
        }

        return getHisnListFromJson("ar")
    }

    suspend fun getHisnItems(categoryId: String, languageCode: String): List<DhikrItem> {
        // Try Room first
        val roomEntities = translationDao.getByCategoryId(categoryId, languageCode)
        // Ensure items exist AND have content (prevents showing empty items from partial syncs)
        if (roomEntities.isNotEmpty() && roomEntities.any { it.mainText.isNotBlank() }) {
            return roomEntities.mapIndexed { index, entity ->
                DhikrItem(
                    id = entity.id,
                    categoryId = categoryId,
                    content = entity.mainText,
                    translation = "",
                    count = entity.count,
                    orderIndex = entity.order,
                    fadl = entity.secondaryText ?: "",
                    audioFile = ""
                )
            }
        }

        // Fallback to JSON
        if (languageCode in EMBEDDED_LANGUAGES) {
            val category = getHisnListFromJson(languageCode).find { it.id == categoryId }
            return category?.items ?: emptyList()
        }

        val arCategory = getHisnListFromJson("ar").find { it.id == categoryId }
        return arCategory?.items ?: emptyList()
    }

    // ═══════════════════════════════════════════
    // Entity Mappers
    // ═══════════════════════════════════════════

    private fun TranslationEntity.toAwrad(): Awrad {
        val isAr = languageCode == "ar"
        return Awrad(
            dayResId = 0,
            content = if (isAr) mainText else secondaryText ?: "",
            translation = if (!isAr) mainText else "",
            dayTitle = title,
            type = "dua"
        )
    }

    private fun TranslationEntity.toMunajat(): Munajat {
        val isAr = languageCode == "ar"
        return Munajat(
            titleResId = 0,
            content = if (isAr) mainText else secondaryText ?: "",
            translation = if (!isAr) mainText else "",
            title = title,
            type = "dua"
        )
    }
}
