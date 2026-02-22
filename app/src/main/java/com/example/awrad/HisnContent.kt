package com.example.awrad

data class DhikrItem(
    val id: String, // Added ID
    val categoryId: String, // Added Category ID
    val content: String, // Renamed from arabic
    val translation: String = "",
    val count: Int = 1,
    val orderIndex: Int = 0,
    val fadl: String = "", // Changed from Map to String
    val audioFile: String = "" // Added audio support
)

data class HisnCategory(
    val id: String,
    val titleResId: Int, // Resource ID
    val iconResId: Int, // Drawable Resource ID
    val items: List<DhikrItem>,
    val title: String? = null // Dynamic title for translation
)

object HisnContent {
    val ALL_CATEGORIES = listOf<HisnCategory>()
    
    fun getCategoryById(id: String): HisnCategory? = null
}
