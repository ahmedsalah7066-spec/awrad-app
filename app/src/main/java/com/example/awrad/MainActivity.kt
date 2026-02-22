package com.example.awrad

import android.content.Context
import android.content.res.Configuration
import android.os.Bundle
import android.widget.Button
import android.widget.ImageButton
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class MainActivity : BaseActivity() {

    @javax.inject.Inject
    lateinit var languageSyncManager: com.example.awrad.data.sync.LanguageSyncManager

    @javax.inject.Inject
    lateinit var jsonDataLoader: com.example.awrad.data.utils.JsonDataLoader

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        applyWindowInsets(findViewById(android.R.id.content))

        // Auto-detect language & sync content
        lifecycleScope.launch {
            val lang = LocaleManager.getLanguage(this@MainActivity)

            // 1. Seed embedded languages from local JSON into Room
            languageSyncManager.seedFromJson("ar", jsonDataLoader)
            languageSyncManager.seedFromJson("en", jsonDataLoader)
            // Force seed id, uz, ur, tr to clean up older database formatting and ensure updated translations
            languageSyncManager.seedFromJson("ur", jsonDataLoader, forceUpdate = true)
            languageSyncManager.seedFromJson("id", jsonDataLoader, forceUpdate = true)
            languageSyncManager.seedFromJson("uz", jsonDataLoader, forceUpdate = true)
            languageSyncManager.seedFromJson("fr", jsonDataLoader, forceUpdate = true)
            languageSyncManager.seedFromJson("bn", jsonDataLoader, forceUpdate = true)
            languageSyncManager.seedFromJson("tr", jsonDataLoader, forceUpdate = true)
            languageSyncManager.seedFromJson("ru", jsonDataLoader, forceUpdate = true)
            languageSyncManager.seedFromJson("ml", jsonDataLoader, forceUpdate = true)
            languageSyncManager.seedFromJson("hi", jsonDataLoader, forceUpdate = true)
            languageSyncManager.seedFromJson("fa", jsonDataLoader, forceUpdate = true)

            // 2. If language is NOT embedded, download from Firebase
            val embeddedLangs = setOf("ar", "en", "ur", "tr", "ml", "uz", "id", "fr", "bn", "ru", "hi", "fa")
            if (!embeddedLangs.contains(lang)) {
                if (!languageSyncManager.isLanguageCached(lang)) {
                    Toast.makeText(this@MainActivity, "Downloading $lang content...", Toast.LENGTH_SHORT).show()
                    languageSyncManager.syncLanguage(lang)
                }
            }
        }

        // Set current date (Gregorian + Hijri)
        val dateTextView = findViewById<TextView>(R.id.tvFullDate)
        
        // Use current locale for date formatting
        val currentLocale = LocaleManager.getLocale(resources)
        val today = Date()
        
        // Gregorian
        val sdfGregorian = SimpleDateFormat("EEEE - d MMMM yyyy", currentLocale)
        val gregorianDate = sdfGregorian.format(today)

        // Hijri
        val hijriDateStr = try {
            if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
                val hijriDate = java.time.chrono.HijrahDate.now()
                val formatter = java.time.format.DateTimeFormatter.ofPattern("d MMMM yyyy", currentLocale)
                formatter.format(hijriDate)
            } else {
                ""
            }
        } catch (e: Exception) {
            ""
        }

        dateTextView.text = "$gregorianDate\n$hijriDateStr"

        // Handle Start Reading button
        val startButton = findViewById<Button>(R.id.btnStartReading)
        startButton.setOnClickListener {
            val intent = android.content.Intent(this, DailyWirdActivity::class.java)
            startActivity(intent)
        }

        // Language Button
        findViewById<android.view.View>(R.id.btnLanguage).setOnClickListener {
            showLanguageDialog()
        }
        
        // Navigation Handlers
        findViewById<android.view.View>(R.id.cardMunajat).setOnClickListener {
            startActivity(android.content.Intent(this, MunajatListActivity::class.java))
        }
        
        findViewById<android.view.View>(R.id.cardDalail).setOnClickListener {
            startActivity(android.content.Intent(this, AwradListActivity::class.java))
        }
        
        findViewById<android.view.View>(R.id.tvTasbih).setOnClickListener {
            startActivity(android.content.Intent(this, HisnListActivity::class.java))
        }
        
        findViewById<android.view.View>(R.id.tvSettings).setOnClickListener {
            startActivity(android.content.Intent(this, SettingsActivity::class.java))
        }
    }

    private fun showLanguageDialog() {
        val languages = arrayOf("System Default", "English", "العربية", "Türkçe", "اردو", "മലയാളം", "O'zbekcha (Кирилл)", "Bahasa Indonesia", "Français", "বাংলা", "Русский", "हिन्दी", "فارسی")
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
        val intent = android.content.Intent(this, MainActivity::class.java)
        intent.addFlags(android.content.Intent.FLAG_ACTIVITY_CLEAR_TASK or android.content.Intent.FLAG_ACTIVITY_NEW_TASK)
        startActivity(intent)
        finishAffinity()
    }
}
