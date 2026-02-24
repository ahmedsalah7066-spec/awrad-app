package com.example.awrad

import android.os.Bundle
import android.widget.ImageView
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class AboutActivity : BaseActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_about)

        applyWindowInsets(findViewById(android.R.id.content))

        findViewById<ImageView>(R.id.btnBack).setOnClickListener {
            finish()
        }
    }
}
