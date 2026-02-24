package com.example.awrad.data.utils

import android.content.Context
import com.example.awrad.Awrad
import com.example.awrad.DhikrItem
import com.example.awrad.HisnCategory
import com.example.awrad.Munajat
import com.example.awrad.R
import dagger.hilt.android.qualifiers.ApplicationContext
import org.json.JSONArray
import org.json.JSONObject
import java.io.IOException
import java.nio.charset.Charset
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class JsonDataLoader @Inject constructor(
    @ApplicationContext private val context: Context
) {

    fun loadAwrad(languageCode: String): List<Awrad> {
        val fileName = getLocalizedFileName("dalail.json", languageCode)
        val jsonString = loadJSONFromAsset(fileName) ?: return emptyList()
        val list = mutableListOf<Awrad>()
        
        try {
            val jsonArray = JSONArray(jsonString)
            for (i in 0 until jsonArray.length()) {
                val obj = jsonArray.getJSONObject(i)
                val id = obj.getString("id")
                
                // Try to match strict ID map if possible, but fallback to 0 if not found
                // We rely on the order in the file mostly for index-based access
                // But for title/Day mapping we might need resId. 
                // However, since we now load dynamic titles from JSON, resId is less critical for Title,
                // but might be needed for Icon/Color mapping if used elsewhere.
                // For now, we keep the existing logic:
                val resId = getResId("dalail_$id", "string")

                val title = obj.optString("title", "")
                val content = obj.getString("content")
                // In localized files, 'content' is the target language text. 'translation' is generic/empty.
                val type = obj.optString("type", "dua")
                
                val translation = obj.optString("translation", "")
            
                list.add(Awrad(
                    dayResId = resId,
                    content = content,
                    translation = translation,
                    dayTitle = title,
                    type = type
                ))
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
        return list
    }

    fun loadMunajat(languageCode: String): List<Munajat> {
        val fileName = getLocalizedFileName("munajat.json", languageCode)
        val jsonString = loadJSONFromAsset(fileName) ?: return emptyList()
        val list = mutableListOf<Munajat>()
        
        try {
            val jsonArray = JSONArray(jsonString)
            for (i in 0 until jsonArray.length()) {
                val obj = jsonArray.getJSONObject(i)
                
                val title = obj.optString("title", "")
                val content = obj.getString("content")
                val type = obj.optString("type", "dua")
                val id = obj.optString("id", "")
                val translation = obj.optString("translation", "")

                list.add(Munajat(
                    titleResId = 0,
                    content = content,
                    translation = translation,
                    title = title,
                    type = type,
                    id = id.ifBlank { null }
                ))
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
        return list
    }

    fun loadHisn(languageCode: String): List<HisnCategory> {
        val fileName = getLocalizedFileName("hisn.json", languageCode)
        val jsonString = loadJSONFromAsset(fileName) ?: return emptyList()
        val list = mutableListOf<HisnCategory>()
        
        try {
            val jsonArray = JSONArray(jsonString)
            for (i in 0 until jsonArray.length()) {
                val obj = jsonArray.getJSONObject(i)
                val id = obj.getString("id")
                val title = obj.optString("title", "")
                // Support both icon and icon_res field names
                val iconName = obj.optString("icon", obj.optString("icon_res", ""))
                val iconRes = getResId(iconName, "drawable")
                
                val itemsArray = obj.getJSONArray("items")
                val dhikrItems = mutableListOf<DhikrItem>()
                
                for (j in 0 until itemsArray.length()) {
                    val itemObj = itemsArray.getJSONObject(j)
                    val itemId = itemObj.getString("id")
                    // Support both content and arabic field names
                    val content = itemObj.optString("content", itemObj.optString("arabic", ""))
                    val count = itemObj.optInt("count", 1)
                    // Support both fadl string and fadl object
                    val fadlValue = itemObj.opt("fadl")
                    val fadl = when (fadlValue) {
                        is String -> fadlValue
                        is JSONObject -> fadlValue.optString("ar", fadlValue.optString("en", ""))
                        else -> ""
                    }
                    
                    dhikrItems.add(DhikrItem(
                        id = itemId,
                        categoryId = id,
                        content = content,
                        translation = itemObj.optString("translation", ""), 
                        count = count,
                        orderIndex = j,
                        fadl = fadl,
                        audioFile = ""
                    ))
                }
                
                list.add(HisnCategory(
                    id = id,
                    titleResId = 0, 
                    iconResId = iconRes,
                    items = dhikrItems,
                    title = title
                ))
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
        return list
    }

    fun loadStaticContent(languageCode: String = "ar"): Map<String, com.example.awrad.WirdContentItem> {
        // Try language-specific static.json first, then fall back to data/static.json
        val localizedFileName = "$languageCode/static.json"
        val jsonString = loadJSONFromAsset(localizedFileName) ?: loadJSONFromAsset("data/static.json") ?: return emptyMap()
        val map = mutableMapOf<String, com.example.awrad.WirdContentItem>()
        
        try {
            val jsonArray = JSONArray(jsonString)
            for (i in 0 until jsonArray.length()) {
                val obj = jsonArray.getJSONObject(i)
                val id = obj.getString("id")
                val content = obj.getString("content")
                val translation = obj.optString("translation", "")
                
                map[id] = com.example.awrad.WirdContentItem(content, translation)
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
        return map
    }

    private fun getLocalizedFileName(baseName: String, languageCode: String): String {
        // Try the requested language path first
        val localizedPath = "$languageCode/$baseName"
        return try {
            context.assets.open(localizedPath).close()
            localizedPath
        } catch (e: Exception) {
            // Fallback to Arabic
            "ar/$baseName"
        }
    }
    fun loadTurkishFullContent(): Map<String, String> {
        val jsonString = loadJSONFromAsset("data/turkish_full_content.json") ?: return emptyMap()
        val map = mutableMapOf<String, String>()
        try {
            val jsonObject = JSONObject(jsonString)
            val keys = jsonObject.keys()
            while (keys.hasNext()) {
                val key = keys.next()
                map[key] = jsonObject.getString(key)
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
        return map
    }

    private fun loadJSONFromAsset(fileName: String): String? {
        return try {
            val inputStream = context.assets.open(fileName)
            val size = inputStream.available()
            val buffer = ByteArray(size)
            inputStream.read(buffer)
            inputStream.close()
            String(buffer, Charset.forName("UTF-8"))
        } catch (ex: IOException) {
            ex.printStackTrace()
            null
        }
    }
    
    // Helper to find resource ID by name
    private fun getResId(resName: String, defType: String): Int {
        return try {
            context.resources.getIdentifier(resName, defType, context.packageName)
        } catch (e: Exception) {
            0
        }
    }
}
