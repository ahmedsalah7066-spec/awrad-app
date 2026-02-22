package com.example.awrad

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.example.awrad.data.repository.SimpleContentRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import javax.inject.Inject

import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.launch
import java.util.Locale

/**
 * ViewModel for Hisn Al-Muslim content
 * Now supports async loading from database
 */
@HiltViewModel
class HisnViewModel @Inject constructor(
    private val repository: SimpleContentRepository,
    private val application: android.app.Application
) : ViewModel() {

    private val _categories = MutableLiveData<List<HisnCategory>>()
    val categories: LiveData<List<HisnCategory>> = _categories

    init {
        loadCategories()
    }

    private fun loadCategories() {
        viewModelScope.launch {
            val lang = LocaleManager.getLanguage(application)
            _categories.value = repository.getHisnCategories(lang)
        }
    }

    suspend fun getHisnItems(categoryId: String): List<DhikrItem> {
        val lang = LocaleManager.getLanguage(application)
        return repository.getHisnItems(categoryId, lang)
    }

    fun refresh() {
        loadCategories()
    }

    fun getCategory(categoryId: String): HisnCategory? {
        return _categories.value?.find { it.id == categoryId }
    }
}
