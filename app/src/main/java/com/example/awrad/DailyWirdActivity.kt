package com.example.awrad

import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.util.TypedValue
import android.view.View
import android.widget.ImageView
import android.widget.TextView
import androidx.activity.viewModels
import dagger.hilt.android.AndroidEntryPoint
import java.util.Calendar

@AndroidEntryPoint
class DailyWirdActivity : BaseActivity() {

    private val viewModel: WirdViewModel by viewModels()
    private lateinit var contentView: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_daily_wird)
        applyWindowInsets(findViewById(android.R.id.content))

        contentView = findViewById(R.id.tvDetailContent)
        
        // Font Size Controls
        findViewById<View>(R.id.btnIncreaseFont).setOnClickListener {
            viewModel.increaseFontSize()
        }

        findViewById<View>(R.id.btnDecreaseFont).setOnClickListener {
            viewModel.decreaseFontSize()
        }
        
        // Share Button
        findViewById<View>(R.id.btnShare).setOnClickListener {
            shareContent(viewModel.uiState.value?.plainTextContent ?: "")
        }
        
        // Observe UI State
        viewModel.uiState.observe(this) { state ->
            renderState(state)
        }
        
        // Refresh data with current resources (to handle locale changes)
        viewModel.refreshData(resources)
    }
    
    private fun renderState(state: WirdUiState) {
        android.util.Log.d("DailyWirdActivity", "renderState: htmlContent length=${state.htmlContent.length}, titleResId=${state.dayTitleResId}")
        if (state.htmlContent.isEmpty()) {
            // Loading...
        }
        
        // Update Content
        contentView.text = androidx.core.text.HtmlCompat.fromHtml(state.htmlContent, androidx.core.text.HtmlCompat.FROM_HTML_MODE_LEGACY)
        contentView.setTextSize(TypedValue.COMPLEX_UNIT_SP, state.fontSize)
        
        contentView.post {
            val prefs = getSharedPreferences("daily_wird_prefs", Context.MODE_PRIVATE)
            val today = java.text.SimpleDateFormat("yyyy_MM_dd", java.util.Locale.getDefault()).format(java.util.Date())
            val savedScrollY = prefs.getInt("scroll_daily_$today", 0)
            if (savedScrollY > 0) {
                val scrollView = findViewById<android.widget.ScrollView>(R.id.scrollView)
                scrollView?.scrollTo(0, savedScrollY)
            }
        }
        
        // Update Title if needed
        if (state.dayTitleResId != 0) {
            val titleView = findViewById<TextView>(R.id.tvDetailTitle)
            titleView.text = getString(state.dayTitleResId)
        }
    }

    private fun shareContent(content: String) {
        if (content.isEmpty()) return
        
        val intent = Intent(Intent.ACTION_SEND)
        intent.type = "text/plain"
        intent.putExtra(Intent.EXTRA_SUBJECT, "ورد اليوم / Today's Wird")
        intent.putExtra(Intent.EXTRA_TEXT, content)
        startActivity(Intent.createChooser(intent, "Share via"))
        android.widget.Toast.makeText(this, "تم نسخ الورد بالكامل", android.widget.Toast.LENGTH_SHORT).show()
    }

    override fun onPause() {
        super.onPause()
        val scrollView = findViewById<android.widget.ScrollView>(R.id.scrollView)
        if (scrollView != null) {
            val prefs = getSharedPreferences("daily_wird_prefs", Context.MODE_PRIVATE)
            val today = java.text.SimpleDateFormat("yyyy_MM_dd", java.util.Locale.getDefault()).format(java.util.Date())
            prefs.edit().putInt("scroll_daily_$today", scrollView.scrollY).apply()
        }
    }
}
