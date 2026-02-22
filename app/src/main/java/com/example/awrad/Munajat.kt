package com.example.awrad

data class Munajat(
    val titleResId: Int,
    val content: String,
    val translation: String = "",
    val title: String? = null,  // Direct title from database
    val type: String = "dua"
)

object MunajatData {
    val list = listOf<Munajat>()
}
