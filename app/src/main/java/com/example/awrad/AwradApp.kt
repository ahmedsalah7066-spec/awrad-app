package com.example.awrad

import android.app.Application
import android.util.Log
import dagger.hilt.android.HiltAndroidApp

@HiltAndroidApp
class AwradApp : Application() {
    
    override fun attachBaseContext(base: android.content.Context) {
        super.attachBaseContext(LocaleManager.setLocale(base))
    }

    override fun onCreate() {
        super.onCreate()
        Log.d(TAG, "Awrad App initialized - Simple mode activated!")
    }
    
    companion object {
        private const val TAG = "AwradApp"
    }
}
