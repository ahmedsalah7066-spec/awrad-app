package com.example.awrad.data.room

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query

@Dao
interface TranslationDao {

    // ── Single Item ──
    @Query("SELECT * FROM translations WHERE id = :id AND languageCode = :languageCode")
    suspend fun getTranslation(id: String, languageCode: String): TranslationEntity?

    // ── By Type ──
    @Query("SELECT * FROM translations WHERE type = :type AND languageCode = :languageCode ORDER BY `order` ASC")
    suspend fun getByType(type: String, languageCode: String): List<TranslationEntity>

    // ── By Category (for Hisn items) ──
    @Query("SELECT * FROM translations WHERE type = 'hisn' AND categoryId = :categoryId AND languageCode = :languageCode ORDER BY `order` ASC")
    suspend fun getByCategoryId(categoryId: String, languageCode: String): List<TranslationEntity>

    // ── All for a language ──
    @Query("SELECT * FROM translations WHERE languageCode = :languageCode")
    suspend fun getAllTranslationsForLanguage(languageCode: String): List<TranslationEntity>

    // ── Check if language exists ──
    @Query("SELECT COUNT(*) FROM translations WHERE languageCode = :languageCode LIMIT 1")
    suspend fun hasLanguage(languageCode: String): Int

    // ── Insert ──
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertTranslation(translation: TranslationEntity)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertTranslations(translations: List<TranslationEntity>)

    // ── Delete ──
    @Query("DELETE FROM translations WHERE languageCode = :languageCode")
    suspend fun deleteTranslationsForLanguage(languageCode: String)

    @Query("DELETE FROM translations")
    suspend fun deleteAll()
}
