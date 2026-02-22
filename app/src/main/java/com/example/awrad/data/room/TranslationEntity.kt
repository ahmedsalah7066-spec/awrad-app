package com.example.awrad.data.room

import androidx.room.Entity

@Entity(tableName = "translations", primaryKeys = ["id", "languageCode"])
data class TranslationEntity(
    val id: String,           // Universal ID, e.g., "awrad_saturday", "munajat_1", "hisn_morning_1"
    val languageCode: String, // e.g., "ar", "en", "tr", "fr", "ur"
    val type: String = "",    // "awrad", "munajat", "hisn", "hisn_category", "static"
    val title: String? = null,
    val mainText: String,     // The primary content
    val secondaryText: String? = null, // Fadl, explanation, etc.
    val categoryId: String? = null,    // For hisn items: "morning", "evening", etc.
    val order: Int = 0,       // Sort order within type/category
    val count: Int = 1        // Repetition count (for hisn dhikr items)
)
