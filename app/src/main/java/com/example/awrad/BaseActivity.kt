package com.example.awrad

import android.content.Context
import androidx.appcompat.app.AppCompatActivity
import androidx.activity.enableEdgeToEdge

open class BaseActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: android.os.Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge(
            statusBarStyle = androidx.activity.SystemBarStyle.light(
                android.graphics.Color.TRANSPARENT,
                android.graphics.Color.TRANSPARENT
            )
        )
    }

    override fun attachBaseContext(newBase: Context) {
        super.attachBaseContext(LocaleManager.setLocale(newBase))
    }

    protected fun applyWindowInsets(view: android.view.View) {
        androidx.core.view.ViewCompat.setOnApplyWindowInsetsListener(view) { v, insets ->
            val systemBars = insets.getInsets(androidx.core.view.WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }
    }

    protected fun applyHeaderInsets(view: android.view.View) {
        androidx.core.view.ViewCompat.setOnApplyWindowInsetsListener(view) { v, insets ->
            val systemBars = insets.getInsets(androidx.core.view.WindowInsetsCompat.Type.systemBars())
            // Apply top padding only, preserving existing padding
            v.setPadding(v.paddingLeft, systemBars.top, v.paddingRight, v.paddingBottom)
            insets
        }
    }
}
