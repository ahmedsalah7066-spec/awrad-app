package com.example.awrad.data.repository

import android.content.Context
import android.content.SharedPreferences
import com.example.awrad.domain.repository.SettingsRepository
import dagger.hilt.android.qualifiers.ApplicationContext
import javax.inject.Inject

class SettingsRepositoryImpl @Inject constructor(
    @ApplicationContext private val context: Context
) : SettingsRepository {

    private val prefs: SharedPreferences = context.getSharedPreferences("Settings", Context.MODE_PRIVATE)

    override fun areNotificationsEnabled(): Boolean {
        return prefs.getBoolean("notifications_enabled", true)
    }

    override fun setNotificationsEnabled(enabled: Boolean) {
        prefs.edit().putBoolean("notifications_enabled", enabled).apply()
    }

    override fun getNotificationInterval(): Int {
        return prefs.getInt("notification_interval", 30)
    }

    override fun setNotificationInterval(minutes: Int) {
        prefs.edit().putInt("notification_interval", minutes).apply()
    }
}
