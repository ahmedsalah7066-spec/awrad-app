package com.example.awrad

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.viewModelScope
import com.example.awrad.domain.repository.WirdRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class AwradDetailViewModel @Inject constructor(
    private val wirdRepository: WirdRepository,
    application: Application
) : AndroidViewModel(application) {

    private val _awradContent = MutableLiveData<String>()
    val awradContent: LiveData<String> = _awradContent

    fun loadAwradByIndex(index: Int) {
        viewModelScope.launch {
            val languageCode = LocaleManager.getLanguage(getApplication())
            val awrad = wirdRepository.getAwradByIndex(index, languageCode)

            if (awrad != null) {
                // Formatting logic
                val displayText = when {
                    // For English and Urdu, show translation if available
                    (languageCode == "en" || languageCode == "ur") && awrad.translation.isNotEmpty() -> {
                        awrad.translation
                    }
                    // For Turkish, show translation if available
                    languageCode == "tr" && awrad.translation.isNotEmpty() -> {
                        awrad.translation
                    }
                    // For Arabic, show content
                    languageCode == "ar" -> {
                        awrad.content
                    }
                    // Default: show content
                    else -> awrad.content
                }
                
                _awradContent.value = displayText
            }
        }
    }
}
