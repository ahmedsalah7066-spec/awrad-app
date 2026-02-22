package com.example.awrad.domain.repository

import com.example.awrad.Awrad
import com.example.awrad.Munajat

/**
 * Repository interface for accessing Islamic content
 * Simple and clean - no database complexity
 */
interface WirdRepository {
    suspend fun getIstiftah(languageCode: String): String
    suspend fun getIbrahimi(languageCode: String): String
    suspend fun getDailyAwrad(dayOfWeek: Int, languageCode: String): Awrad
    suspend fun getAllAwrad(languageCode: String): List<Awrad>
    suspend fun getRotatingMunajat(dayOfYear: Int, languageCode: String): Munajat
    suspend fun getAwradByIndex(index: Int, languageCode: String): Awrad?
    suspend fun getAwradByResId(resId: Int, languageCode: String): Awrad?
}
