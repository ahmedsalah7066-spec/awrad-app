package com.example.awrad

import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.widget.ImageView
import android.widget.TextView
import androidx.activity.viewModels
import androidx.lifecycle.lifecycleScope
import kotlinx.coroutines.launch
import androidx.appcompat.app.AppCompatDelegate
import androidx.core.os.LocaleListCompat
import com.google.android.material.card.MaterialCardView
import com.google.android.material.switchmaterial.SwitchMaterial
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class SettingsActivity : BaseActivity() {

    private val viewModel: SettingsViewModel by viewModels()
    private lateinit var switchNotifications: SwitchMaterial
    private lateinit var tvInterval: TextView // Kept for reference, though synthesized in valid code

    @javax.inject.Inject
    lateinit var dataUploader: com.example.awrad.data.DataUploader

    @javax.inject.Inject
    lateinit var languageSyncManager: com.example.awrad.data.sync.LanguageSyncManager

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_settings)

        // Check and request POST_NOTIFICATIONS permission on Android 13+
        checkAndRequestPermissions()

        // --- Notification Switch ---
        switchNotifications = findViewById(R.id.switchNotifications)
        val prefs = getSharedPreferences("Settings", Context.MODE_PRIVATE)
        switchNotifications.isChecked = prefs.getBoolean("notifications_enabled", true)

        switchNotifications.setOnCheckedChangeListener { _, isChecked ->
            prefs.edit().putBoolean("notifications_enabled", isChecked).apply()
            if (isChecked) {
                NotificationScheduler.scheduleNotifications(this)
            } else {
                NotificationScheduler.cancelNotifications(this)
            }
        }

        // --- Notification Interval Button ---
        val btnNotificationSettings = findViewById<android.widget.TextView>(R.id.btnNotificationSettings)
        val savedInterval = prefs.getInt("notification_interval", 30)
        updateIntervalText(savedInterval)

        btnNotificationSettings.setOnClickListener {
            showIntervalDialog()
        }

        // --- Header Back Arrow ---
        val btnBack = findViewById<android.widget.ImageView>(R.id.btnBack)
        btnBack?.setOnClickListener { finish() }

        // Language Card
        val cardLanguage = findViewById<MaterialCardView>(R.id.cardLanguage)
        cardLanguage.setOnClickListener {
            showLanguageDialog()
        }

        // Update Content Logic
        val cardUpdateContent = findViewById<MaterialCardView>(R.id.cardUpdateContent)
        val progressUpdate = findViewById<android.widget.ProgressBar>(R.id.progressUpdate)
        val imgArrowUpdate = findViewById<ImageView>(R.id.imgArrowUpdate)

        cardUpdateContent.setOnClickListener {
            lifecycleScope.launch {
                try {
                    android.widget.Toast.makeText(this@SettingsActivity, getString(R.string.updating), android.widget.Toast.LENGTH_SHORT).show()
                    progressUpdate.visibility = android.view.View.VISIBLE
                    imgArrowUpdate.visibility = android.view.View.GONE
                    cardUpdateContent.isEnabled = false
                    
                    // 1. Upload Data to Cloud (Seeder)
                    dataUploader.uploadAllData()
                    
                    // 2. Force Sync current language from Cloud to Local Room
                    val currentLang = LocaleManager.getLanguage(this@SettingsActivity)
                    languageSyncManager.syncLanguage(currentLang, forceUpdate = true)
                    
                    android.widget.Toast.makeText(this@SettingsActivity, getString(R.string.update_success), android.widget.Toast.LENGTH_LONG).show()
                } catch (e: Exception) {
                    android.widget.Toast.makeText(this@SettingsActivity, getString(R.string.update_error), android.widget.Toast.LENGTH_LONG).show()
                    e.printStackTrace()
                } finally {
                    progressUpdate.visibility = android.view.View.GONE
                    imgArrowUpdate.visibility = android.view.View.VISIBLE
                    cardUpdateContent.isEnabled = true
                }
            }
        }
    }

    private fun updateIntervalText(minutes: Int) {
        val btnNotificationSettings = findViewById<TextView>(R.id.btnNotificationSettings)
        val hours = minutes / 60
        val mins = minutes % 60
        
        val timeString = if (hours > 0) {
            if (mins > 0) "$hours ساعات $mins دقيقة" else "$hours ساعات"
        } else {
            "$mins دقيقة"
        }
        
        btnNotificationSettings.text = "تكرار التذكير: كل $timeString"
    }

    private fun showIntervalDialog() {
        val intervals = ArrayList<Int>()
        val intervalStrings = ArrayList<String>()
        
        for (i in 5..180 step 5) {
            intervals.add(i)
            val h = i / 60
            val m = i % 60
             if (h > 0) {
                 if (m > 0) intervalStrings.add("$h ساعة و $m دقيقة") else intervalStrings.add("$h ساعة")
            } else {
                intervalStrings.add("$m دقيقة")
            }
        }

        val builder = androidx.appcompat.app.AlertDialog.Builder(this)
        builder.setTitle("اختر وقت التذكير")
        
        builder.setItems(intervalStrings.toTypedArray()) { _, which ->
            val selectedMinutes = intervals[which]
            viewModel.setNotificationInterval(selectedMinutes)
            
            // Reschedule if enabled
            if (switchNotifications.isChecked) {
                NotificationScheduler.scheduleNotifications(this)
            }
        }
        builder.show()
    }

    private fun showLanguageDialog() {
        val languages = arrayOf("System Default", "English", "العربية", "Türkçe", "اردو", "മലയാളം", "O\'zbekcha (Кирилл)", "Bahasa Indonesia", "Français", "বাংলা", "Русский", "हिन्दी", "فارسی")
        val builder = androidx.appcompat.app.AlertDialog.Builder(this)
        builder.setTitle(getString(R.string.feature_multilingual))
        
        val adapter = android.widget.ArrayAdapter(this, R.layout.dialog_item_language, languages)
        builder.setAdapter(adapter) { _, which ->
            val langCode = when (which) {
                1 -> "en"
                2 -> "ar"
                3 -> "tr"
                4 -> "ur"
                5 -> "ml"
                6 -> "uz"
                7 -> "id"
                8 -> "fr"
                9 -> "bn"
                10 -> "ru"
                11 -> "hi"
                12 -> "fa"
                else -> "" // Default/System
            }

            // 1. Persist new language preference
            LocaleManager.setNewLocale(this, langCode)
            
            // 2. Restart App to apply changes cleanly
            restartApp()
        }
        builder.show()
    }
    
    private fun restartApp() {
        val intent = Intent(this, MainActivity::class.java)
        intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TASK or Intent.FLAG_ACTIVITY_NEW_TASK)
        startActivity(intent)
        finishAffinity() // Close all activities
    }

    private fun getCurrentLanguageLabel(): String {
        val currentLang = LocaleManager.getLanguage(this)
        return when (currentLang) {
            "ar" -> "العربية"
            "en" -> "English"
            "tr" -> "Türkçe"
            "ur" -> "اردو"
            "ml" -> "മലയാളം"
            "uz" -> "O\'zbekcha (Кирилл)"
            "id", "in" -> "Bahasa Indonesia"
            "fr" -> "Français"
            "bn" -> "বাংলা"
            "ru" -> "Русский"
            "hi" -> "हिन्दी"
            "fa" -> "فارسی"
            else -> "System Default"
        }
    }
    private fun checkAndRequestPermissions() {
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.TIRAMISU) {
            if (androidx.core.content.ContextCompat.checkSelfPermission(
                    this,
                    android.Manifest.permission.POST_NOTIFICATIONS
                ) != android.content.pm.PackageManager.PERMISSION_GRANTED
            ) {
                androidx.core.app.ActivityCompat.requestPermissions(
                    this,
                    arrayOf(android.Manifest.permission.POST_NOTIFICATIONS),
                    101
                )
            }
        }
        
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.S) {
            val alarmManager = getSystemService(android.app.AlarmManager::class.java)
            if (!alarmManager.canScheduleExactAlarms()) {
                // optional
            }
        }
    }
}
