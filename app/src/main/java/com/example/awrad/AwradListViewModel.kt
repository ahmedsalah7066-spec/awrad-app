package com.example.awrad

import android.app.Application
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.awrad.domain.repository.WirdRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.launch
import java.util.Locale
import javax.inject.Inject

@HiltViewModel
class AwradListViewModel @Inject constructor(
    private val wirdRepository: WirdRepository,
    private val application: Application
) : ViewModel() {

    private val _uiState = MutableLiveData<List<Awrad>>()
    val uiState: LiveData<List<Awrad>> = _uiState

    init {
        loadData() // Initial load
    }

    fun loadData() {
        viewModelScope.launch {
            val lang = LocaleManager.getLanguage(application)
            _uiState.value = wirdRepository.getAllAwrad(lang)
        }
    }
}
