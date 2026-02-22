package com.example.awrad.data.sync

import android.content.Context
import android.util.Log
import com.example.awrad.data.room.TranslationDao
import com.example.awrad.data.source.FirebaseContentSource
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class LanguageSyncManager @Inject constructor(
    @ApplicationContext private val context: Context,
    private val firebaseContentSource: FirebaseContentSource,
    private val translationDao: TranslationDao
) {
    companion object {
        private const val TAG = "LanguageSync"
    }

    /**
     * Check if a language is already downloaded and cached in Room.
     */
    suspend fun isLanguageCached(languageCode: String): Boolean {
        return translationDao.hasLanguage(languageCode) > 0
    }

    /**
     * Sync a language from Firebase to Room.
     * For ar/en: these are embedded in JSON, so we can skip Firebase and seed from JSON.
     * For other languages: download from Firebase.
     */
    suspend fun syncLanguage(languageCode: String, forceUpdate: Boolean = false) {
        withContext(Dispatchers.IO) {
            try {
                // Check if already cached
                if (!forceUpdate && isLanguageCached(languageCode)) {
                    Log.d(TAG, "Language $languageCode already cached. Skipping download.")
                    return@withContext
                }

                Log.d(TAG, "Downloading language: $languageCode (Force: $forceUpdate)")
                val translations = firebaseContentSource.fetchTranslations(languageCode)

                if (translations.isNotEmpty()) {
                    if (forceUpdate) {
                        translationDao.deleteTranslationsForLanguage(languageCode)
                    }
                    translationDao.insertTranslations(translations)
                    Log.d(TAG, "Downloaded and saved ${translations.size} translations for $languageCode")
                } else {
                    Log.d(TAG, "No translations found for $languageCode on Firebase")
                }
            } catch (e: Exception) {
                Log.e(TAG, "Error syncing language $languageCode", e)
            }
        }
    }

    /**
     * Seed Arabic or English from local JSON files into Room.
     * This ensures Room has all content even for embedded languages.
     */
    suspend fun seedFromJson(languageCode: String, jsonDataLoader: com.example.awrad.data.utils.JsonDataLoader, forceUpdate: Boolean = false) {
        withContext(Dispatchers.IO) {
            try {
                if (!forceUpdate && isLanguageCached(languageCode)) {
                    Log.d(TAG, "Language $languageCode already seeded. Skipping.")
                    return@withContext
                }

                if (forceUpdate) {
                    translationDao.deleteTranslationsForLanguage(languageCode)
                }

                Log.d(TAG, "Seeding $languageCode from local JSON...")
                val entities = mutableListOf<com.example.awrad.data.room.TranslationEntity>()

                // Awrad
                val awradList = jsonDataLoader.loadAwrad(languageCode)
                val dayNames = listOf("saturday", "sunday", "monday", "tuesday", "wednesday", "thursday", "friday")
                awradList.forEachIndexed { index, awrad ->
                    val textToSeed = if (languageCode == "ar") awrad.content else {
                        if (awrad.translation.isNotEmpty()) awrad.translation else awrad.content
                    }
                    val arabicFallback = if (languageCode != "ar") awrad.content else ""
                    entities.add(com.example.awrad.data.room.TranslationEntity(
                        id = "awrad_${dayNames.getOrElse(index) { "day_$index" }}",
                        languageCode = languageCode,
                        type = "awrad",
                        title = awrad.dayTitle,
                        mainText = textToSeed,
                        secondaryText = arabicFallback,
                        order = index
                    ))
                }

                // Munajat
                val munajatList = jsonDataLoader.loadMunajat(languageCode)
                munajatList.forEachIndexed { index, munajat ->
                    val textToSeed = if (languageCode == "ar") munajat.content else {
                        if (munajat.translation.isNotEmpty()) munajat.translation else munajat.content
                    }
                    val arabicFallback = if (languageCode != "ar") munajat.content else ""
                    entities.add(com.example.awrad.data.room.TranslationEntity(
                        id = "munajat_${index + 1}",
                        languageCode = languageCode,
                        type = "munajat",
                        title = munajat.title,
                        mainText = textToSeed,
                        secondaryText = arabicFallback,
                        order = index
                    ))
                }

                // Hisn
                val hisnCategories = jsonDataLoader.loadHisn(languageCode)
                hisnCategories.forEachIndexed { catIndex, category ->
                    entities.add(com.example.awrad.data.room.TranslationEntity(
                        id = "hisn_category_${category.id}",
                        languageCode = languageCode,
                        type = "hisn_category",
                        title = category.title,
                        mainText = category.title ?: "",
                        order = catIndex
                    ))
                    category.items.forEachIndexed { itemIndex, item ->
                        entities.add(com.example.awrad.data.room.TranslationEntity(
                            id = "hisn_${category.id}_${itemIndex + 1}",
                            languageCode = languageCode,
                            type = "hisn",
                            categoryId = category.id,
                            mainText = item.content,
                            secondaryText = item.fadl,
                            order = itemIndex,
                            count = item.count
                        ))
                    }
                }

                // Static content
                val staticContent = jsonDataLoader.loadStaticContent(languageCode)
                for ((id, item) in staticContent) {
                    val textToSeed = if (languageCode == "ar") item.content else {
                        if (item.translation.isNotEmpty()) item.translation else item.content
                    }
                    entities.add(com.example.awrad.data.room.TranslationEntity(
                        id = "static_$id",
                        languageCode = languageCode,
                        type = "static",
                        mainText = textToSeed
                    ))
                }

                translationDao.insertTranslations(entities)
                Log.d(TAG, "Seeded ${entities.size} items for $languageCode from JSON")
            } catch (e: Exception) {
                Log.e(TAG, "Error seeding $languageCode from JSON", e)
            }
        }
    }
}
