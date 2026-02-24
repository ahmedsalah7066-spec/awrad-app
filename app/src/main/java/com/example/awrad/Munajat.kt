package com.example.awrad

data class Munajat(
    val titleResId: Int,
    val content: String,
    val translation: String = "",
    val title: String? = null,  // Direct title from database
    val type: String = "dua",
    val id: String? = null      // Document ID (e.g. munajat_taibin)
)

object MunajatData {
    val list = listOf<Munajat>()
}
