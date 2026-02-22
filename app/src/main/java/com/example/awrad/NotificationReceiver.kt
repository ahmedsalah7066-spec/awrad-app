package com.example.awrad

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.os.Build
import androidx.core.app.NotificationCompat
import java.util.Calendar

class NotificationReceiver : BroadcastReceiver() {

    override fun onReceive(context: Context, intent: Intent) {
        // Show the notification
        showNotification(context)
        
        // Schedule the next one (chaining)
        NotificationScheduler.scheduleNotifications(context)
    }

    private fun showNotification(context: Context) {
        // Apply the user's selected locale so getString() returns localised text
        val localizedContext = LocaleManager.setLocale(context)

        val notificationManager = localizedContext.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        val channelId = "dhikr_channel"

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                channelId,
                localizedContext.getString(R.string.notification_title),
                NotificationManager.IMPORTANCE_HIGH
            ).apply {
                description = localizedContext.getString(R.string.notification_desc)
                enableLights(true)
                enableVibration(true)
            }
            notificationManager.createNotificationChannel(channel)
        }

        val tapIntent = Intent(localizedContext, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
        }
        val pendingIntent = PendingIntent.getActivity(
            localizedContext, 0, tapIntent, PendingIntent.FLAG_IMMUTABLE
        )

        // Randomly pick one of the three dhikr messages
        val messages = listOf(
            localizedContext.getString(R.string.notif_msg_salawat),
            localizedContext.getString(R.string.notif_msg_dhikr),
            localizedContext.getString(R.string.notif_msg_istighfar)
        )
        val randomMessage = messages.random()

        val notification = NotificationCompat.Builder(localizedContext, channelId)
            .setSmallIcon(R.drawable.ic_notification)
            .setContentTitle(localizedContext.getString(R.string.notif_title))
            .setContentText(randomMessage)
            .setStyle(NotificationCompat.BigTextStyle().bigText(randomMessage))
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setDefaults(NotificationCompat.DEFAULT_ALL)
            .setContentIntent(pendingIntent)
            .setAutoCancel(true)
            .build()

        notificationManager.notify(System.currentTimeMillis().toInt(), notification)
    }
}
