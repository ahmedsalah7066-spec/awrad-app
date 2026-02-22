package com.example.awrad.domain.repository

interface SettingsRepository {
    fun areNotificationsEnabled(): Boolean
    fun setNotificationsEnabled(enabled: Boolean)
    fun getNotificationInterval(): Int
    fun setNotificationInterval(minutes: Int)
}
