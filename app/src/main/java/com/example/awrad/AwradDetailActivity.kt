package com.example.awrad

import android.os.Bundle
import android.util.TypedValue
import android.widget.Button
import android.widget.ImageView
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

import dagger.hilt.android.AndroidEntryPoint
import javax.inject.Inject
import androidx.activity.viewModels // Import this!
import com.example.awrad.data.repository.SimpleContentRepository
import java.util.Locale

@AndroidEntryPoint
class AwradDetailActivity : BaseActivity() {

    private val viewModel: AwradDetailViewModel by viewModels()

    private var currentTextSize = 18f
    private lateinit var explanationView: TextView
    private lateinit var titleView: TextView
    private lateinit var contentView: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_awrad_detail)

        val dayIndex = intent.getIntExtra("day_index", -1)
        val dayTitle = intent.getStringExtra("day_title") ?: ""

        // Header Setup
        val headerView = findViewById<android.view.View>(R.id.header)
        applyHeaderInsets(headerView)

        titleView = findViewById(R.id.tvHeaderTitle)
        val backButton = findViewById<ImageView>(R.id.btnBack)
        val shareButton = findViewById<ImageView>(R.id.btnHeaderShare)
        
        contentView = findViewById(R.id.tvDetailContent)
        explanationView = findViewById(R.id.tvExplanation) // Might be unused but keeping ref

        val increaseButton = findViewById<TextView>(R.id.btnIncreaseFont)
        val decreaseButton = findViewById<TextView>(R.id.btnDecreaseFont)

        // Apply window insets
        applyWindowInsets(findViewById(android.R.id.content))

        titleView.text = dayTitle
        
        // Back Button
        backButton.setOnClickListener {
            finish()
        }
        
        contentView.setTextSize(TypedValue.COMPLEX_UNIT_SP, currentTextSize)
        explanationView.visibility = android.view.View.GONE

        // Observe ViewModel
        viewModel.awradContent.observe(this) { content ->
            contentView.text = content
        }

        // Trigger Data Load
        if (dayIndex != -1) {
            viewModel.loadAwradByIndex(dayIndex)
        } else {
             // Fallback
             contentView.text = "Error loading content"
        }

        // Share Button (Visible)
        shareButton.visibility = android.view.View.VISIBLE
        shareButton.setOnClickListener {
            val shareIntent = android.content.Intent(android.content.Intent.ACTION_SEND)
            shareIntent.type = "text/plain"
            shareIntent.putExtra(android.content.Intent.EXTRA_SUBJECT, titleView.text.toString())
            shareIntent.putExtra(android.content.Intent.EXTRA_TEXT, contentView.text.toString())
            startActivity(android.content.Intent.createChooser(shareIntent, "Share via"))
        }

        increaseButton.setOnClickListener {
            if (currentTextSize < 32f) {
                currentTextSize += 2f
                contentView.setTextSize(TypedValue.COMPLEX_UNIT_SP, currentTextSize)
            }
        }

        decreaseButton.setOnClickListener {
            if (currentTextSize > 12f) {
                currentTextSize -= 2f
                contentView.setTextSize(TypedValue.COMPLEX_UNIT_SP, currentTextSize)
            }
        }
    }
}
