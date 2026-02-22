package com.example.awrad.data.source

import android.util.Log
import com.example.awrad.data.room.TranslationEntity
import com.google.firebase.firestore.FirebaseFirestore
import kotlinx.coroutines.tasks.await
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class FirebaseContentSource @Inject constructor(
    private val firestore: FirebaseFirestore
) {
    companion object {
        private const val TAG = "FirebaseContentSource"
        private const val COLLECTION = "content"
    }

    /**
     * Fetches all translations for a specific language code from the new schema.
     *
     * Firestore Structure:
     * content/{universalId} -> { type, order, categoryId?, count?,
     *                            ar: { title?, content, fadl? },
     *                            en: { title?, content, fadl? },
     *                            tr: { ... }, ... }
     */
    suspend fun fetchTranslations(languageCode: String): List<TranslationEntity> {
        return try {
            Log.d(TAG, "Fetching all content for language: $languageCode")

            val snapshot = firestore.collection(COLLECTION)
                .get()
                .await()

            val entities = mutableListOf<TranslationEntity>()

            for (doc in snapshot.documents) {
                val docId = doc.id
                val type = doc.getString("type") ?: continue
                val order = doc.getLong("order")?.toInt() ?: 0
                val categoryId = doc.getString("categoryId")
                val count = doc.getLong("count")?.toInt() ?: 1

                // Get the language-specific sub-map
                @Suppress("UNCHECKED_CAST")
                val langData = doc.get(languageCode) as? Map<String, Any> ?: continue

                val content = langData["content"] as? String ?: ""
                val title = langData["title"] as? String
                val fadl = langData["fadl"] as? String

                entities.add(
                    TranslationEntity(
                        id = docId,
                        languageCode = languageCode,
                        type = type,
                        title = title,
                        mainText = content,
                        secondaryText = fadl,
                        categoryId = categoryId,
                        order = order,
                        count = count
                    )
                )
            }

            Log.d(TAG, "Fetched ${entities.size} items for $languageCode")
            entities
        } catch (e: Exception) {
            Log.e(TAG, "Error fetching translations for $languageCode", e)
            emptyList()
        }
    }
}
