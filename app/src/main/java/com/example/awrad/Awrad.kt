package com.example.awrad

data class Awrad(
    val dayResId: Int,
    val content: String,
    val translation: String = "",
    val dayTitle: String? = null,  // Direct title from database
    val type: String = "dua" // "dua" or "quran" (default "dua")
)

object AwradData {
    val list = emptyList<Awrad>()
}
