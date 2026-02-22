package com.example.awrad

import android.content.Context
import android.content.SharedPreferences
import android.content.res.Configuration
import android.os.Build
import android.os.LocaleList
import java.util.Locale

object LocaleManager {

    private const val PREFS_NAME = "Settings"
    private const val KEY_LANGUAGE = "app_language"

    fun setLocale(context: Context): Context {
        return updateResources(context, getLanguage(context))
    }

    fun setNewLocale(context: Context, language: String): Context {
        persistLanguage(context, language)
        return updateResources(context, language)
    }

    fun getLanguage(context: Context): String {
        val prefs: SharedPreferences = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
        return prefs.getString(KEY_LANGUAGE, "ar") ?: "ar" // Default to Arabic
    }

    private fun persistLanguage(context: Context, language: String) {
        val prefs: SharedPreferences = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
        prefs.edit().putString(KEY_LANGUAGE, language).apply()
    }

    private fun updateResources(context: Context, language: String): Context {
        val locale = Locale(language)
        Locale.setDefault(locale)

        val res = context.resources
        val config = Configuration(res.configuration)
        
        config.setLocale(locale)
        config.setLayoutDirection(locale)

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
            val localeList = LocaleList(locale)
            LocaleList.setDefault(localeList)
            config.setLocales(localeList)
        }
        
        // CRITICAL: Force update the resources of the CURRENT context.
        // createConfigurationContext() only creates a NEW wrapper — it does NOT 
        // update the original context's resources. Without this line,
        // application.getString() in ViewModels returns the old locale's strings.
        @Suppress("DEPRECATION")
        res.updateConfiguration(config, res.displayMetrics)

        return context.createConfigurationContext(config)
    }
    
    fun getLocale(res: android.content.res.Resources): Locale {
        val config = res.configuration
        return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
            config.locales.get(0)
        } else {
            config.locale
        }
    }
}
