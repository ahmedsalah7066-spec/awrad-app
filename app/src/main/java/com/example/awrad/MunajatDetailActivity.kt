package com.example.awrad

import android.os.Bundle
import android.util.TypedValue
import android.widget.Button
import android.widget.ImageView
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

import dagger.hilt.android.AndroidEntryPoint
import javax.inject.Inject
import android.content.Context
import androidx.lifecycle.lifecycleScope
import com.example.awrad.data.repository.SimpleContentRepository
import kotlinx.coroutines.launch
import java.util.Locale

@AndroidEntryPoint
class MunajatDetailActivity : BaseActivity() {

    @Inject
    lateinit var repository: SimpleContentRepository

    private var currentTextSize = 18f
    private lateinit var prefs: android.content.SharedPreferences
    private lateinit var titleView: TextView
    private lateinit var contentView: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_munajat_detail)

        val index = intent.getIntExtra("munajat_index", 0)
        
        prefs = getSharedPreferences("font_prefs", Context.MODE_PRIVATE)
        currentTextSize = prefs.getFloat("munajat_font_size", 18f)

        // Header Setup
        val headerView = findViewById<android.view.View>(R.id.header)
        applyHeaderInsets(headerView)
        
        titleView = findViewById(R.id.tvHeaderTitle) // Updated ID from included layout
        val backButton = findViewById<ImageView>(R.id.btnBack)
        val shareButton = findViewById<ImageView>(R.id.btnHeaderShare)
        
        contentView = findViewById(R.id.tvDetailContent)

        val increaseButton = findViewById<TextView>(R.id.btnIncreaseFont)
        val decreaseButton = findViewById<TextView>(R.id.btnDecreaseFont)

        // Apply window insets to handle overlaps
        applyWindowInsets(findViewById(android.R.id.content))

        // Back Button
        backButton.setOnClickListener {
            finish()
        }

        contentView.setTextSize(TypedValue.COMPLEX_UNIT_SP, currentTextSize)

        // Fetch Data
        lifecycleScope.launch {
            val lang = LocaleManager.getLanguage(this@MunajatDetailActivity)
            val munajat = repository.getMunajat(index, lang)
            
            val title = if (munajat.titleResId != 0) getString(munajat.titleResId) else munajat.title ?: ""
            titleView.text = title
            
            val displayText = when {
                (lang == "en" || lang == "ur" || lang == "tr") && munajat.translation.isNotEmpty() -> {
                    munajat.translation
                }
                lang == "ar" -> munajat.content
                else -> {
                    if (munajat.content.isNotEmpty() && munajat.translation.isNotEmpty()) {
                        "${munajat.content}\n\n${munajat.translation}"
                    } else if (munajat.content.isNotEmpty()) {
                        munajat.content
                    } else {
                        munajat.translation
                    }
                }
            }
            
            contentView.text = displayText
            
            contentView.post {
                val prefs = getSharedPreferences("munajat_prefs", Context.MODE_PRIVATE)
                val savedScrollY = prefs.getInt("scroll_munajat_$index", 0)
                if (savedScrollY > 0) {
                    val scrollView = findViewById<android.widget.ScrollView>(R.id.scrollView)
                    scrollView?.scrollTo(0, savedScrollY)
                }
            }
            
            // Share Button
            shareButton.visibility = android.view.View.VISIBLE
            shareButton.setOnClickListener {
                val shareIntent = android.content.Intent(android.content.Intent.ACTION_SEND)
                shareIntent.type = "text/plain"
                shareIntent.putExtra(android.content.Intent.EXTRA_SUBJECT, title)
                shareIntent.putExtra(android.content.Intent.EXTRA_TEXT, contentView.text.toString())
                startActivity(android.content.Intent.createChooser(shareIntent, "Share via"))
            }
        }

        increaseButton.setOnClickListener {
            if (currentTextSize < 32f) {
                currentTextSize += 2f
                contentView.setTextSize(TypedValue.COMPLEX_UNIT_SP, currentTextSize)
                prefs.edit().putFloat("munajat_font_size", currentTextSize).apply()
            }
        }

        decreaseButton.setOnClickListener {
            if (currentTextSize > 12f) {
                currentTextSize -= 2f
                contentView.setTextSize(TypedValue.COMPLEX_UNIT_SP, currentTextSize)
                prefs.edit().putFloat("munajat_font_size", currentTextSize).apply()
            }
        }
    }

    override fun onPause() {
        super.onPause()
        val scrollView = findViewById<android.widget.ScrollView>(R.id.scrollView)
        val index = intent.getIntExtra("munajat_index", 0)
        if (scrollView != null) {
            val prefs = getSharedPreferences("munajat_prefs", Context.MODE_PRIVATE)
            prefs.edit().putInt("scroll_munajat_$index", scrollView.scrollY).apply()
        }
    }
}
