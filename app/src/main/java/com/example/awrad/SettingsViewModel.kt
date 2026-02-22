package com.example.awrad

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import com.example.awrad.domain.repository.SettingsRepository
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.launch
import dagger.hilt.android.lifecycle.HiltViewModel
import javax.inject.Inject

@HiltViewModel
class SettingsViewModel @Inject constructor(
    private val repository: SettingsRepository,
    private val dataUploader: com.example.awrad.data.DataUploader
) : BaseViewModel() {

    private val _notificationsEnabled = MutableLiveData<Boolean>()
    val notificationsEnabled: LiveData<Boolean> = _notificationsEnabled

    private val _notificationInterval = MutableLiveData<Int>()
    val notificationInterval: LiveData<Int> = _notificationInterval

    init {
        loadSettings()
    }

    private fun loadSettings() {
        _notificationsEnabled.value = repository.areNotificationsEnabled()
        _notificationInterval.value = repository.getNotificationInterval()
    }

    fun setNotificationsEnabled(enabled: Boolean) {
        repository.setNotificationsEnabled(enabled)
        _notificationsEnabled.value = enabled
    }

    fun setNotificationInterval(minutes: Int) {
        repository.setNotificationInterval(minutes)
        _notificationInterval.value = minutes
    }


}

sealed class Resource<out T> {
    object Loading : Resource<Nothing>()
    data class Success<out T>(val data: T) : Resource<T>()
    data class Error(val message: String) : Resource<Nothing>()
}
