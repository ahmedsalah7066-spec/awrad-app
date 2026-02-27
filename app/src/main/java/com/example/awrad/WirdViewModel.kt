package com.example.awrad

import android.app.Application
import android.util.Log
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.viewModelScope
import com.example.awrad.domain.repository.WirdRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import java.util.Calendar
import javax.inject.Inject
import kotlinx.coroutines.launch

@HiltViewModel
class WirdViewModel @Inject constructor(
    private val wirdRepository: WirdRepository,
    private val application: Application
) : BaseViewModel() {

    private val fontPrefs = application.getSharedPreferences("font_prefs", android.content.Context.MODE_PRIVATE)
    private val _uiState = MutableLiveData(WirdUiState(fontSize = fontPrefs.getFloat("wird_font_size", 18f)))
    val uiState: LiveData<WirdUiState> = _uiState

    init {
        viewModelScope.launch {
            try {
                Log.d("WirdViewModel", "Loading daily content...")
                loadDailyContent()
                Log.d("WirdViewModel", "Content loaded successfully")
            } catch (e: Exception) {
                Log.e("WirdViewModel", "Error loading content", e)
            }
        }
    }

    fun refreshData(resources: android.content.res.Resources? = null) {
        viewModelScope.launch {
            loadDailyContent(resources)
        }
    }

    fun loadAwradByResId(resId: Int) {
        viewModelScope.launch {
            val languageCode = LocaleManager.getLanguage(application)
            val awrad = wirdRepository.getAwradByResId(resId, languageCode)
            
            updateUiWithAwrad(awrad)
        }
    }

    fun loadAwradByIndex(index: Int) {
        viewModelScope.launch {
            val languageCode = LocaleManager.getLanguage(application)
            val awrad = wirdRepository.getAwradByIndex(index, languageCode)
            
            updateUiWithAwrad(awrad)
        }
    }

    private fun updateUiWithAwrad(awrad: com.example.awrad.Awrad?) {
        if (awrad != null) {
             val current = _uiState.value ?: WirdUiState()
             
             val displayText = if (awrad.translation.isNotEmpty()) {
                 "${awrad.content}\n\n---\n\n${awrad.translation}"
             } else {
                 awrad.content
             }

             _uiState.value = current.copy(
                 plainTextContent = displayText,
                 // dayTitleResId is not used for display anymore in DetailActivity (passed via Intent)
                 // but we keep it compatible
                 dayTitleResId = awrad.dayResId
             )
        }
    }

    private suspend fun loadDailyContent(resources: android.content.res.Resources? = null) {
        Log.d("WirdViewModel", "loadDailyContent: Starting...")
        val calendar = Calendar.getInstance()
        val dayOfWeek = getDayOfWeekIndex(calendar)
        val dayOfYear = calendar.get(Calendar.DAY_OF_YEAR)

        val languageCode = LocaleManager.getLanguage(application)
        Log.d("WirdViewModel", "Calendar values: dayOfWeek=$dayOfWeek, dayOfYear=$dayOfYear, lang=$languageCode")

        val todaysAwrad = wirdRepository.getDailyAwrad(dayOfWeek, languageCode)
        val todaysMunajat = wirdRepository.getRotatingMunajat(dayOfYear, languageCode)
        val istiftah = wirdRepository.getIstiftah(languageCode)
        val ibrahimi = wirdRepository.getIbrahimi(languageCode)

        Log.d("WirdViewModel", "Retrieved data:")
        Log.d("WirdViewModel", "  - Istiftah length: ${istiftah.length}")
        Log.d("WirdViewModel", "  - Awrad title: '${todaysAwrad.dayTitle}', content length: ${todaysAwrad.content.length}")
        Log.d("WirdViewModel", "  - Ibrahimi length: ${ibrahimi.length}")
        Log.d("WirdViewModel", "  - Munajat title: '${todaysMunajat.title}', content length: ${todaysMunajat.content.length}")

        // Build HTML Content
        val htmlContent = buildString {
            
            val awradTitle = if (todaysAwrad.dayResId != 0) {
                    resources?.getString(todaysAwrad.dayResId) ?: application.getString(todaysAwrad.dayResId)
                } else {
                    todaysAwrad.dayTitle ?: (resources?.getString(R.string.wird_today_title) ?: application.getString(R.string.wird_today_title))
                }
                
            val istiftahTitle = resources?.getString(R.string.istiftah_title) ?: application.getString(R.string.istiftah_title)
            val ibrahimiTitle = resources?.getString(R.string.ibrahimi_title) ?: application.getString(R.string.ibrahimi_title)
            val munajatDefaultTitle = resources?.getString(R.string.munajat_title) ?: application.getString(R.string.munajat_title)

            append("<font color='#1E5631'><b><u>$istiftahTitle</u></b></font><br><br>")
            append(istiftah.replace("\n", "<br>"))
            
            if (todaysAwrad.translation.isNotEmpty()) {
                append("<br><br><font color='#808080'>-------------------</font><br><br>")
            }

            append("<br><br><font color='#1E5631'>═══════════════</font><br><br>")
            append("<font color='#1E5631'><b><u>$awradTitle</u></b></font><br><br>")
            // For non-Arabic languages with translation, show ONLY the translation
            // For Arabic, show content
            if (languageCode != "ar" && todaysAwrad.translation.isNotEmpty()) {
                append(todaysAwrad.translation.replace("\n", "<br>"))
            } else if (todaysAwrad.content.isNotEmpty()) {
                append(todaysAwrad.content.replace("\n", "<br>"))
            }

            append("<br><br><font color='#1E5631'>═══════════════</font><br><br>")
            append("<font color='#1E5631'><b><u>$ibrahimiTitle</u></b></font><br><br>")
            append(ibrahimi.replace("\n", "<br>"))
            append("<br><br><font color='#1E5631'>═══════════════</font><br><br>")
            
            val munajatTitle = if (todaysMunajat.titleResId != 0) {
                     resources?.getString(todaysMunajat.titleResId) ?: application.getString(todaysMunajat.titleResId)
                } else {
                     todaysMunajat.title ?: munajatDefaultTitle
                }

            append("<font color='#1E5631'><b><u>$munajatTitle</u></b></font><br><br>")
            // For non-Arabic languages with translation, show ONLY the translation
            // For Arabic, show content
            if (languageCode != "ar" && todaysMunajat.translation.isNotEmpty()) {
                append(todaysMunajat.translation.replace("\n", "<br>"))
            } else if (todaysMunajat.content.isNotEmpty()) {
                append(todaysMunajat.content.replace("\n", "<br>"))
            }
        }

        // Build Plain Text Content
        val plainText = buildString {
            val istiftahTitle = resources?.getString(R.string.istiftah_title) ?: application.getString(R.string.istiftah_title)
            val ibrahimiTitle = resources?.getString(R.string.ibrahimi_title) ?: application.getString(R.string.ibrahimi_title)
            
            append("━━━ $istiftahTitle ━━━\n\n")
            append(istiftah)
            append("\n\n")
            append("━━━━━━━━━━━━━━━━━━━━━\n\n")
            
            val awradTitle = todaysAwrad.dayTitle 
                ?: if (todaysAwrad.dayResId != 0) {
                    resources?.getString(todaysAwrad.dayResId) ?: application.getString(todaysAwrad.dayResId)
                } else {
                    resources?.getString(R.string.wird_today_title) ?: application.getString(R.string.wird_today_title)
                }
                
            append("━━━ $awradTitle ━━━\n\n")
            // For non-Arabic languages with translation, show ONLY the translation
            if (languageCode != "ar" && todaysAwrad.translation.isNotEmpty()) {
                append(todaysAwrad.translation)
            } else {
                append(todaysAwrad.content)
            }

            append("\n\n")
            append("━━━━━━━━━━━━━━━━━━━━━\n\n")
            append("━━━ $ibrahimiTitle ━━━\n\n")
            append(ibrahimi)
            append("\n\n")
            append("━━━━━━━━━━━━━━━━━━━━━\n\n")
            
            val munajatTitle = todaysMunajat.title 
                ?: if (todaysMunajat.titleResId != 0) {
                    resources?.getString(todaysMunajat.titleResId) ?: application.getString(todaysMunajat.titleResId)
                } else {
                    resources?.getString(R.string.munajat_title) ?: application.getString(R.string.munajat_title)
                }
                
            append("━━━ $munajatTitle ━━━\n\n")
            // For non-Arabic languages with translation, show ONLY the translation
            if (languageCode != "ar" && todaysMunajat.translation.isNotEmpty()) {
                append(todaysMunajat.translation)
            } else {
                append(todaysMunajat.content)
            }
        }

        val current = _uiState.value ?: WirdUiState()
        _uiState.value = current.copy(
            htmlContent = htmlContent,
            plainTextContent = plainText,
            dayTitleResId = todaysAwrad.dayResId
        )
    }

    fun increaseFontSize() {
        val current = _uiState.value ?: return
        var newSize = current.fontSize + 2f
        if (newSize > 40f) newSize = 40f
        _uiState.value = current.copy(fontSize = newSize)
        fontPrefs.edit().putFloat("wird_font_size", newSize).apply()
    }

    fun decreaseFontSize() {
        val current = _uiState.value ?: return
        var newSize = current.fontSize - 2f
        if (newSize < 14f) newSize = 14f
        _uiState.value = current.copy(fontSize = newSize)
        fontPrefs.edit().putFloat("wird_font_size", newSize).apply()
    }

    private fun getDayOfWeekIndex(calendar: Calendar): Int {
        // Map Calendar.DAY_OF_WEEK (1..7) to List Index (0..6)
        // Awrad list starts with Saturday (Index 0)
        return when (calendar.get(Calendar.DAY_OF_WEEK)) {
            Calendar.SATURDAY -> 0
            Calendar.SUNDAY -> 1
            Calendar.MONDAY -> 2
            Calendar.TUESDAY -> 3
            Calendar.WEDNESDAY -> 4
            Calendar.THURSDAY -> 5
            Calendar.FRIDAY -> 6
            else -> 0 // Fallback
        }
    }
}
