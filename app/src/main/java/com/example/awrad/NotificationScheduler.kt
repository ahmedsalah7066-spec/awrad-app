package com.example.awrad

import android.app.AlarmManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import java.util.Calendar

object NotificationScheduler {

    private const val CHANNEL_ID = "dhikr_channel"
    private const val CHANNEL_NAME = "Dhikr Reminders"
    private const val PREFS_NAME = "Settings"

    fun createNotificationChannel(context: Context) {
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
            val channel = android.app.NotificationChannel(
                CHANNEL_ID,
                CHANNEL_NAME,
                android.app.NotificationManager.IMPORTANCE_HIGH
            ).apply {
                description = "Reminders for Dhikr and Istighfar"
                enableLights(true)
                enableVibration(true)
            }
            val notificationManager = context.getSystemService(android.app.NotificationManager::class.java)
            notificationManager.createNotificationChannel(channel)
        }
    }

    fun scheduleNotifications(context: Context) {
        createNotificationChannel(context)
        cancelNotifications(context)

        val prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
        val isEnabled = prefs.getBoolean("notifications_enabled", true)
        
        if (!isEnabled) return

        val intervalMinutes = prefs.getInt("notification_interval", 30) // Default 30 mins
        val intervalMillis = intervalMinutes * 60 * 1000L
        
        // Ensure minimum interval of 5 minutes to avoid system throttling issues if user sets it too low manually
        val safeInterval = if (intervalMillis < 5 * 60 * 1000L) 5 * 60 * 1000L else intervalMillis

        val alarmManager = context.getSystemService(Context.ALARM_SERVICE) as AlarmManager
        val intent = Intent(context, NotificationReceiver::class.java)
        val pendingIntent = PendingIntent.getBroadcast(
            context,
            0,
            intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        // Fix: Use Calendar to calculate trigger time safely
        val calendar = Calendar.getInstance()
        calendar.timeInMillis = System.currentTimeMillis() + safeInterval

        // Guard against infinite loop if time is in the past (though safeInterval ensures it shouldn't be)
        if (calendar.timeInMillis <= System.currentTimeMillis()) {
            calendar.add(Calendar.DAY_OF_YEAR, 1)
        }

        try {
            if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.S) {
                if (alarmManager.canScheduleExactAlarms()) {
                    alarmManager.setExactAndAllowWhileIdle(
                        AlarmManager.RTC_WAKEUP,
                        calendar.timeInMillis,
                        pendingIntent
                    )
                } else {
                    alarmManager.set(
                        AlarmManager.RTC_WAKEUP,
                        calendar.timeInMillis,
                        pendingIntent
                    )
                }
            } else if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.M) {
                alarmManager.setExactAndAllowWhileIdle(
                    AlarmManager.RTC_WAKEUP,
                    calendar.timeInMillis,
                    pendingIntent
                )
            } else {
                alarmManager.setExact(
                    AlarmManager.RTC_WAKEUP,
                    calendar.timeInMillis,
                    pendingIntent
                )
            }
        } catch (e: SecurityException) {
            e.printStackTrace()
        }
    }

    fun scheduleNextNotification(context: Context) {
        // Called by Receiver to schedule the next one (chaining)
        scheduleNotifications(context)
    }

    fun cancelNotifications(context: Context) {
        val alarmManager = context.getSystemService(Context.ALARM_SERVICE) as AlarmManager
        val intent = Intent(context, NotificationReceiver::class.java)
        val pendingIntent = PendingIntent.getBroadcast(
            context,
            0,
            intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )
        alarmManager.cancel(pendingIntent)
    }
}
